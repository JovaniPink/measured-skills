# Contributing

Write skills in `skills/`. The `plugins/` folders are generated, so do not edit them by hand.

Before you start, read [the authoring guide](docs/authoring.md), [the security model](docs/security-model.md), and [the provenance policy](docs/provenance.md).

Then, for one skill at a time:

1. Add or update a single focused skill.
2. Record where its content came from in `provenance/catalog.json`.
3. Add test cases to `evals/cases.json`: three that should start the skill, three near misses that should not, and one safety case.
4. Regenerate the client packages and the Claude.ai archives with `python3 scripts/build_distributions.py` and `python3 scripts/package_claude_ai.py`. Git ignores `dist/`, so a new archive needs `git add -f`.
5. Run the checks listed in [the testing guide](docs/testing.md).
6. Keep observed results separate from assumptions in `docs/manual-smoke-tests.md`.

## Keep the release manifest current

The file `releases/<version>/manifest.json` records hashes of the generated packs, the Claude.ai archives, and some catalog files. After you change a skill, `python3 scripts/validate.py` reports `current checksum drift` until the manifest is refreshed. Refresh it in a second commit:

1. Commit the source change together with the regenerated `plugins/` and `dist/` folders.
2. On a clean checkout where HEAD is that commit, run `python3 scripts/build_release_manifest.py --source-commit <full 40-character commit hash>`.
3. Commit only `releases/<version>/manifest.json`.
4. Push both commits together. CI on the first commit alone fails by design.

Expected result: `python3 scripts/validate.py` ends with `All deterministic catalog validations passed.`

Merge the pull request with a merge commit. The check needs the source commit to stay in history, and a squash or rebase merge removes it.

## What a contribution must not contain

- secrets or credentials
- private system names or identifiers
- proprietary text
- absolute paths from your own machine
- claims about results we have not measured
- hooks, MCP servers, broad tool grants, or skill-level programs

The [glossary](docs/glossary.md) defines the terms used here. The [editorial style guide](docs/editorial-style.md) covers the writing rules.
