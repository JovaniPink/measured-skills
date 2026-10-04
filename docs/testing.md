# Testing and Validation

Run these from the repository root.

## Set up

Use Python 3.12, the version CI runs. Other versions may work, but CI does not check them. Install the tool versions pinned in `requirements-ci-linux.txt`.

On the platform CI runs on (Linux on x86-64 with Python 3.12), install from the hash-locked file:

```sh
python3 -m pip install --require-hashes --only-binary=:all: -r requirements-ci-linux.txt
```

On any other system, including other Linux CPU types, install the same versions without the hashes:

```sh
python3 -m pip install PyYAML==6.0.3 mypy==1.20.2 ruff==0.15.12 types-PyYAML==6.0.12.20260815
```

## After you change a skill

Regenerate the client packages and the Claude.ai archives:

```sh
python3 scripts/build_distributions.py
python3 scripts/package_claude_ai.py
```

## Run the checks

These run in the order CI runs them:

```sh
python3 scripts/check_workflows.py
python3 -m mypy --strict scripts tests
python3 -m ruff check scripts tests
python3 scripts/build_distributions.py --check
python3 scripts/package_claude_ai.py
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

Each command should exit with status 0. `scripts/validate.py` ends with `All deterministic catalog validations passed.` It already runs the public-boundary scan. To run only that scan, use `python3 scripts/check_public_boundary.py`. If a change affects generated files, also refresh the release manifest as described in [Contributing](../CONTRIBUTING.md).

The Linux CI requirements file pins the workflow parser, its type information, and every type and lint dependency by version and wheel hash. It is not a portable local environment. Use PyYAML 6.0.3 with `scripts/check_workflows.py` on other platforms. `scripts/validate.py` reconciles the Linux lock with reviewed provenance and checks canonical metadata, Codex policy mapping, Claude explicit-invocation mapping, trigger coverage, primary-authority provenance, originality, repository independence, local references, public/private boundary patterns, marketplace structure, ZIP layout, and generated-tree drift.

## Antigravity preview checks

The unit suite also checks the offline preview builder: selected source and reference files survive unchanged, explicit-only skills are rejected before output is written, unknown skills are rejected, repeated builds match, and old output cannot be overwritten. Build a review copy with `python3 scripts/build_antigravity.py --output dist/antigravity-review`. Use a new folder for each build. This does not install a plugin or prove client loading.

## External validators

When installed, also run the current official tools:

```sh
skills-ref validate skills/<skill-name>
claude plugin validate plugins/claude/measured-skills --strict
```

Run Codex's bundled skill validator for every canonical skill and the bundled plugin validator for the Codex plugin. Tool availability and observed output belong in `docs/validation-evidence.md`; never silently treat an unavailable validator as passing.

## Trigger evaluations

`evals/cases.json` is a deterministic coverage contract, not a claim that every client model behaves identically. Execute the cases on each supported surface and record observed activation or refusal separately in `docs/manual-smoke-tests.md`.

## Release gate

A release requires green automated checks, clean generated trees, all required trigger cases, and completed manual evidence for every surface claimed as supported. A pending manual surface blocks parity claims and public-directory submission, not local authoring.

## Current evidence links

The introductions to the manual checks and validation evidence must link to the current dated client record. The validator checks that record's catalog version. Use plain Markdown in those introductions. Links hidden in comments, code examples, or raw HTML do not count. Historical matrices stay in their own sections; do not relabel them as current observations. Update the record, its entry points, and the validator together when a new dated record becomes current.

The shared release-manifest schema accepts semantic versions for retained releases. Tests reject leading zeros, invalid prerelease values, and trailing newlines. A new candidate must not invalidate a historical manifest.
