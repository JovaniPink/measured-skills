# Validation Evidence

See the [current 0.18.0 candidate checks](client-candidate-v0.18.0.md). Older observations below retain their original package versions.

Start with the [September 8 Claude account repair](claude-account-repair-2026-09-08.md) for the historical 0.11 account and CLI checks. The [client support checklist](client-support.md) tracks checks still open. Earlier sections retain their named versions, dates, and failures. They do not prove that a current install works.

Current test suite: 133 regression tests.

## 0.18.0 candidate baseline

Observed on 2026-10-04 at commit `70182b2`, the `main` head before this change, on Python 3.11.15 with PyYAML 6.0.3, mypy 1.20.2, and ruff 0.15.12 at the versions in `requirements-ci-linux.txt`: the public-boundary scan, workflow-syntax check, strict typing, lint, generated-distribution drift check, full deterministic validation, and all 133 unit tests passed. CI runs Python 3.12, so this was not a CI run. The run used a clean checkout. It records no installed-client behavior and no model run.

## Equal client setup candidate

The setup candidate had 73 regression tests.

The new offline Antigravity preview builder preserves source files and references, excludes all explicit-only skills, and refuses existing output paths. Codex and Claude distribution bytes are unchanged. Current setup guidance gives the three clients equal priority. Each app and CLI still needs its own loading and use evidence.

Observed on 2026-09-08: full deterministic validation passed; all 73 tests passed; generated-file checks, strict typing, lint, public-boundary, and workflow checks passed. Claude Code 2.1.220 accepted the marketplace and all seven native plugin manifests with `--strict`. The refreshed manifest binds source commit `b160500`. These are package and repository checks, not live behavior tests. Historical results below keep their original dates and counts.

## v0.11 continuity candidate

The candidate contains 77 skills, with 13 targeted workflow changes and original synthetic examples. Native distributions are generated from canonical source. Behavioral acceptance remains unobserved; historical client and pilot records do not establish behavior for this candidate. See [the candidate audit](continuity-candidate.md).

Observed local checks on 2026-09-08: complete deterministic validation passed, all 69 unit tests passed, native distribution and marketplace drift checks passed, strict typing and lint passed, and both workflow syntax checks passed. The 0.11.0 release manifest binds source commit `02e29f9` and exact current artifact hashes. These checks establish local candidate consistency only; no installed-client experiment or publication was performed.

This file records observed outcomes for catalog release candidates. Validators do not rewrite it automatically.

## v0.10 behavioral-evidence candidate

- Catalog/plugin version: `0.10.0`
- Date: 2026-09-04
- Canonical skills: 77 across seven optional plugins
- Generated artifacts: 77 Codex projections, 77 Claude projections, and 77 deterministic Claude.ai archives
- Evidence model: workflow maturity, behavioral evidence, client compatibility, and runtime eligibility remain orthogonal
- Profile decision: the seven-skill Delivery TypeScript profile remains experimental and non-default; its prior neutral synthetic record was invalidated and no valid behavioral result currently exists
- Google extension: Antigravity CLI is the primary future Google behavioral-portability lane and remains blocked behind a useful Codex pilot treatment; historical Gemini CLI 0.56.0 evidence is not reused as Antigravity or enterprise compatibility evidence
- Acceptance: BLOCKED. Repository and package validation may pass, but the corrected preregistered 12-case behavioral pilot, blinded human review, second-environment reproduction, Work/Desktop observations, Claude portability, and Google portability remain incomplete.

## v0.10 automated checks

- `python3 scripts/build_distributions.py --check`: PASS - all seven Codex and Claude plugin trees and both marketplace records match canonical sources
- `python3 scripts/package_claude_ai.py`: PASS - 77 deterministic, individually nested Claude.ai ZIPs generated with SHA-256 checksums
- `python3 scripts/check_workflows.py`: PASS - both GitHub Actions workflows parse with locked PyYAML 6.0.3
- `python3 scripts/check_public_boundary.py`: PASS - public canonical, documentation, generated, and packaged surfaces contain no private lab or product evidence
- `python3 scripts/check_originality.py`: PASS - canonical, generated, and packaged skill content passed originality checks
- `python3 scripts/check_repository_independence.py`: PASS - repository references remain within reviewed policy
- `python3 scripts/validate.py`: PASS - schemas, links, invocation mappings, provenance, packages, current release manifest, generated drift, fixtures, and policy records
- `python3 -m unittest discover -s tests -v`: PASS - 69 regression tests
- `git diff --check`: PASS

## v0.10 evidence boundary

No valid public behavioral observation currently supports the Delivery TypeScript profile. The prior neutral synthetic record was invalidated because the experiment harness did not yet preserve a reachable fixture revision, isolate treatment installation from mutation grading, independently protect the test contract, or enforce a single comparison envelope. It must not establish a default profile, prove any client behavior, or establish ADK runtime eligibility. No private product case, prompt, raw trace, repository name, architecture detail, or failure pattern is published.

## v0.9 agent-platform candidate

- Source artifact commit: `24998cdfd16ce0b87ad0883c9919c24d058f89ce`
- Catalog/plugin version: `0.9.0`
- Date: 2026-08-25
- Canonical skills: 76 across seven optional plugins; 6 agent-platform skills and 13 explicit-only skills
- Generated artifacts: 76 Codex projections, 76 Claude projections, and 76 deterministic Claude.ai archives
- Evaluation contract: every skill has three positive cases, three near-miss cases, one safety or conflict case, an output-quality rubric, a baseline comparison, provenance, taxonomy, and maturity evidence
- Upstream review: twelve changed primary sources have human-readable review records; mutable A2A latest guidance was replaced with the reviewed versioned 1.0.0 specification, and GitHub review guidance uses its stable official Markdown representation
- Manual matrix: 16 exact-version rows; 6 pass, 2 fail, 8 blocked, 0 not supported, and 0 not run
- Acceptance: BLOCKED. The partial exact-version v0.9 observations include passes, failures, and authority or authentication blockers, but they do not cover every required behavior on every claimed surface.

## v0.9 agent-platform automated checks

- `python3 scripts/build_distributions.py --check`: PASS - all seven Codex and Claude plugin trees and both marketplace records match canonical sources
- `python3 scripts/package_claude_ai.py`: PASS - 76 deterministic, individually nested Claude.ai ZIPs generated with SHA-256 checksums
- `python3 scripts/check_workflows.py`: PASS - both GitHub Actions workflows parse with locked PyYAML 6.0.3; regressions reject the historical unquoted `--only-binary=:all:` command, empty or nonmapping roots, and missing or mismatched parser versions
- `python3 scripts/check_public_boundary.py`: PASS - canonical, documentation, generated, and packaged surfaces passed the public/private boundary scan
- `python3 scripts/check_originality.py`: PASS - canonical, generated, and packaged skill content passed generic originality checks
- `python3 scripts/check_repository_independence.py`: PASS - external repository references remain limited to primary authorities and the reviewed Google Agents CLI provenance exception
- `python3 scripts/validate.py`: PASS - schemas, taxonomy, recipes, links, invocation mappings, provenance, packages, release manifest, generated drift, fixtures, and policy records
- `python3 -m unittest discover -s tests -v`: PASS - 56 regression tests
- `python3 scripts/check_upstream_freshness.py --online`: PASS - every reviewed primary-authority marker matched current observed content
- `git diff --check`: PASS
- Codex bundled skill validator: PASS - all six new canonical agent-platform skills
- Codex bundled plugin validator: PASS - generated `jovanipink-agent-platforms` plugin
- `claude plugin validate plugins/claude/jovanipink-agent-platforms --strict`: PASS

## v0.9 client evidence boundary

The current v0.9 matrix records exact-version installation, discovery, and focused-reference observations where they were performed. It also records failures and authentication, application-control, account, network, and cost blockers without inferring parity. Update, removal, Desktop invocation, API invocation, managed-agent behavior, and authenticated Gemini discovery remain incomplete. Runtime Google ADK behavior belongs to the separate runtime adapter repository. Automated validation proves structural consistency, deterministic packaging, editorial boundaries, and exact upstream markers; it does not prove unobserved receiving-client behavior.

## v0.8 tested source

- Source commit: `0340f99347674ffd631b3c3be766eaa5b1667ef0`
- Catalog/plugin version: `0.8.0`
- Date: 2026-08-24
- Canonical skills: 70 across six optional plugins; 3 AI-systems skills and 13 explicit-only skills
- Generated artifacts: 70 Codex projections, 70 Claude projections, and 70 deterministic Claude.ai archives
- Manual matrix: 42 terminal rows across six surfaces; 0 pass, 42 blocked, 0 fail, 0 not supported, 0 not run
- Acceptance: BLOCKED until receiving-client installation, discovery, implicit activation, focused-reference loading, refusal, update, and removal are separately authorized and observed

## v0.8 automated repository checks

- `python3 scripts/build_distributions.py --check`: PASS - all six Codex and Claude plugin trees and both marketplace records match canonical sources
- `python3 scripts/package_claude_ai.py`: PASS - 70 deterministic, individually nested Claude.ai ZIPs generated with SHA-256 checksums
- `python3 scripts/check_public_boundary.py`: PASS - canonical, documentation, generated, and packaged surfaces passed the public/private boundary scan
- `python3 scripts/check_originality.py`: PASS - canonical, generated, and packaged skill content passed generic originality checks
- `python3 scripts/check_repository_independence.py`: PASS - no external skill repository, marketplace, source mapping, or implementation attribution is present
- `python3 scripts/validate.py`: PASS - schemas, links, invocation mappings, provenance, packages, release manifest, generated drift, fixtures, and policy records
- `python3 -m unittest discover -s tests -v`: PASS - 39 regression tests
- `python3 scripts/check_upstream_freshness.py --online`: PASS - every reviewed primary-authority marker matched current observed content after narrow per-request instrumentation normalization
- `git diff --check`: PASS
- Built-in skill validator: PASS - all three new canonical skills
- Built-in Codex plugin validator: PASS - generated `jovanipink-ai-systems` plugin; the installed Codex CLI exposes no separate `plugin validate` command
- `claude plugin validate --strict`: PASS - all six generated Claude plugins

## v0.8 client evidence boundary

See `client-observations-v0.8.json`. Installation, discovery, implicit activation, focused-reference loading, refusal, update, and removal are separate rows for each surface. Every row is terminal `blocked` because no receiving-client mutation or invocation was authorized. Generated compatibility and strict manifest validation are not treated as installation, activation, resource loading, lifecycle behavior, or cross-client parity.

See `client-observations-v0.9.json` and `client-observations-v0.9.md` for the first candidate observations. Codex CLI focused-reference loading passed. Claude Code discovery passed but invocation was blocked by expired authentication. ChatGPT web and Claude.ai did not contain the new v0.9 skill. Historical Gemini CLI 0.56.0 workspace linking passed, but authenticated discovery was blocked; it does not establish Antigravity or enterprise Gemini CLI behavior. API and managed-agent surfaces remain authority-gated.

## v0.7 tested source

- Source commit: `782ef2b9992710bb0c2770be82bd969c4d3949f0`
- Catalog/plugin version: `0.7.0`
- Date: 2026-08-23
- Canonical skills: 67 across five optional plugins; 24 engineering skills, 11 stack profiles, and 13 explicit-only skills
- Manual matrix: 6 terminal suite rows; 0 pass, 6 blocked, 0 fail, 0 not supported, 0 not run
- Acceptance: BLOCKED until fresh installed-client discovery, activation, reference-loading, and refusal observations are separately authorized and recorded

## v0.7 automated repository checks

- `python3 scripts/build_distributions.py`: PASS - 67 Codex and 67 Claude skill projections generated
- `python3 scripts/package_claude_ai.py`: PASS - 67 deterministic, individually nested Claude.ai ZIPs generated with SHA-256 checksums
- `python3 scripts/check_public_boundary.py`: PASS - canonical, documentation, generated, and packaged surfaces passed the public/private boundary scan
- `python3 scripts/check_originality.py`: PASS - canonical, generated, and packaged skill content passed generic originality checks
- `python3 scripts/check_repository_independence.py`: PASS - only Jovani-owned repository links and pinned CI Action provenance remain as repository-link exceptions
- `python3 scripts/validate.py`: PASS - schemas, links, invocation mappings, provenance, packages, release-candidate manifest, generated drift, fixtures, and policy records
- `python3 -m unittest discover -s tests -v`: PASS - 36 regression tests
- `python3 scripts/check_upstream_freshness.py --online`: PASS - all pinned primary-authority markers matched current observed content
- `git diff --check`: PASS
- Codex bundled skill validator: PASS - `acceptance-evidence-ledger` and all five new professional stack profiles
- `claude plugin validate plugins/claude/jovanipink-engineering --strict`: PASS
- `claude plugin validate plugins/claude/jovanipink-stack-profiles --strict`: PASS
- `skills-ref`: UNAVAILABLE - the command was not installed in the validation environment, so no passing claim is made

## v0.7 client evidence boundary

See `client-observations-v0.7.json`. Every supported surface has a terminal `blocked` suite record tied to the exact source commit and representative ZIP checksum. No client installation, upload, discovery, activation, reference loading, or lifecycle action was performed, and no parity is inferred from generated artifacts.

## v0.6 tested source

- Source commit: `759b3bf9bfca9967144b02d18f0678e3b509e2b3`
- Catalog/plugin version: `0.6.0`
- Date: 2026-08-21
- Canonical skills: 61 across five optional plugins
- Manual matrix: 6 terminal suite rows; 0 pass, 6 blocked, 0 fail, 0 not supported, 0 not run
- Acceptance: BLOCKED until fresh client installation and invocation observations are recorded

## v0.6 automated repository checks

- `python3 scripts/validate.py`: PASS - schemas, links, boundary scan, originality scan, package checksums, trigger coverage, generated drift, fixtures, and catalog records
- `python3 -m unittest discover -s tests -v`: PASS - 24 regression tests
- non-mutating `python3 scripts/build_distributions.py --check`: PASS - all five Codex and Claude plugin trees and both marketplace records match canonical sources
- Codex bundled skill validator: PASS - all 61 canonical skills
- Codex bundled plugin validator: PASS - all five Codex plugins
- `claude plugin validate --strict`: PASS - all five generated Claude plugins
- Claude.ai packages: PASS - 61 deterministic, individually nested ZIPs with SHA-256 checksums
- online primary-authority freshness: PASS - changed official sources were re-reviewed and refreshed pins matched current primary-authority content
- `skills-ref`: UNAVAILABLE - the command was not installed in the validation environment, so no passing claim is made

## v0.6 client evidence boundary

See `client-observations-v0.6.json`. Every supported surface has a terminal `blocked` suite record tied to the exact tested source commit and representative ZIP checksum. Package and validator results are not treated as installation, discovery, activation, reference loading, upload acceptance, or client parity.

## v0.5 tested source

- Source commit: `0c53d68a552aa475746a85c228c1e063233f8ed4`
- Catalog/plugin version: `0.5.0`
- Date: 2026-08-21
- Canonical skills: 54 across five optional plugins
- Manual matrix: 6 terminal suite rows; 0 pass, 6 blocked, 0 fail, 0 not supported, 0 not run
- Acceptance: BLOCKED until fresh client installation and invocation observations are recorded

## v0.5 automated repository checks

- `python3 scripts/validate.py`: PASS - schemas, links, boundary scan, originality scan, package checksums, trigger coverage, generated drift, fixtures, and catalog records
- `python3 -m unittest discover -s tests -v`: PASS - 22 regression tests
- non-mutating `python3 scripts/build_distributions.py --check`: PASS - all five Codex and Claude plugin trees and both marketplace records match canonical sources
- Codex bundled skill validator: PASS - all 54 canonical skills
- Codex bundled plugin validator: PASS - all five Codex plugins
- `claude plugin validate --strict`: PASS - all five generated Claude plugins
- Claude.ai packages: PASS - 54 deterministic, individually nested ZIPs with SHA-256 checksums
- `skills-ref`: UNAVAILABLE - the command was not installed in the validation environment, so no passing claim is made

## v0.5 client evidence boundary

See `client-observations-v0.5.json`. Every supported surface has a terminal `blocked` suite record tied to the exact tested source commit and representative ZIP checksum. Package validation is not treated as installation, discovery, activation, reference loading, upload acceptance, or client parity.

## Tested source

- Source commit: `e2426dcb1f6d4a170c91c68a1eace4869de4fce0`
- Catalog/plugin version: `0.1.0`
- Date: 2026-08-20
- Manual matrix: 31 terminal rows; 17 pass, 14 blocked, 0 fail, 0 not supported, 0 not run
- Acceptance: BLOCKED until the row-level client blockers are cleared

## Automated repository checks

- `python3 scripts/validate.py`: PASS - catalog, adapters, trigger coverage, strict schemas, links, public boundary, packages, checksums, fixtures, and generated drift
- `python3 -m unittest discover -s tests -v`: PASS - 13 regression tests
- non-mutating `python3 scripts/build_distributions.py --check`: PASS - generated plugin trees and both marketplace records match canonical sources
- public-boundary scan: PASS - tracked/non-ignored publishable files plus generated ZIP contents; local sensitive terms come only from the gitignored denylist
- cross-stack fixture evaluation: PASS - six discovery contracts, including evidence-insufficient SQL and forbidden mutating commands
- Codex bundled skill validator: PASS - all 10 canonical skills
- Codex bundled plugin validator: PASS - generated Codex plugin
- `skills-ref`: PASS - all 10 canonical skills using official reference revision `69ef37e9424c0a7ea9dd2293b559e43ec8176379`
- `claude plugin validate . --strict`: PASS - marketplace and referenced plugin, Claude Code 2.1.220
- `claude plugin validate plugins/claude/jovanipink-skills --strict`: PASS - generated Claude plugin, Claude Code 2.1.220
- Claude.ai packages: PASS - 10 deterministic, individually nested ZIPs with SHA-256 checksums

## Client evidence boundary

See `manual-smoke-tests.md` and `client-observations-v0.1.json`. Codex CLI and the required manual Claude Code CLI behaviors passed. Codex Desktop, Claude Code Desktop, and Claude.ai invocation remain blocked, and Claude Code's built-in plugin-eval ablation remains blocked by client availability. No validation, CLI result, or package inspection is substituted for those observations.
