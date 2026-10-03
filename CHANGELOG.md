# Changelog

All notable changes use this file. The project follows semantic versioning after its first release.

## [Unreleased]

### 0.18.0 candidate: run endings and target authority

- Limit execution authority to the exact targets named, list every external state change, and confirm identity by identifier rather than by a similar name.
- Add `Done when` sections with explicit stop-and-ask conditions to execution skills, and decision-ready completion to problem framing and design rationale work.
- Bound waits on workers, commands, and hooks; agree on worker count and expected cost before fan-out; keep long-run task lists in an approved file.
- Lead execution reports with the result and what needs the user, and list a decision as unresolved only when it blocks remaining work.
- Ask research to name the sources checked for unconfirmed claims, code review to mark merge-blocking findings at every severity, plans to check prerequisites across slices, candidate comparisons to remove authorship labels, and interface designs to justify each component.
- Require qualification records to name the model that served every turn and to rerun any run with a model-switch notice.
- These are authored instruction changes. No model run has measured their effect.

### 0.17.0 candidate

- Rename the offering to Measured Skills by Measured Studios; retain source ownership and historical attribution.
- Split engineering into build, review, and delivery while preserving all 79 skills and invocation controls.
- Add selected-skill native exports, identifier migration records, and discovery estimates including names and relative paths.
- Refine planning, module design, and TDD around architecture and behaviorally complete vertical slices.
- Index historical motion observations without asserting current behavior or comparative benefit.
- Reconcile PR 44 findings; defer the policy-only repository's prohibited pre-commit hook.
- Keep client acceptance, comparative runs, the normal-work pilot, and default promotion unverified.
- Mark Antigravity explicit-only controls and marketplace install as unverified; limit generated Antigravity `plugin.json` files to documented fields; install packs from local folders.
- Narrow the private overlay guard to client skill folders without an `.agent-skills/` source, and apply it under `--check`.

## [0.16.0] - 2026-09-11

### Added

- Structured client observations for 0.13, 0.14, and 0.15, restored from the candidate documents that recorded them. Machine-checked recording had stopped after 0.9.
- `session_depth` and `turn_index` on observation records, so every observation states how far into a session it was taken.
- `surfaces_covered` on each observation matrix, replacing a hardcoded six-surface expectation that rejected any partial matrix.
- A written turn-depth study design, and HOLD-TURN-DEPTH, which bars describing any skill as governing a working session until that study runs.
- Two review domains in `skill-security-review`: agent-facing configuration shipped inside a reviewed package, and client-shipped behavior overrides such as output styles that apply without asking.

### Changed

- `observed_at` accepts a date without a clock time, but only on historical evidence, and is now checked as a real calendar date with a true end anchor.
- `docs/client-observations.json` is renamed `docs/client-observations-v0.1.json`. Its old name read as the current store while holding the oldest records.

### Security

- The ships-nothing list now names output styles. A plugin may ship one that applies as soon as it is enabled, replacing the user's own setting with no prompt. This catalog ships none; each pack contains a `skills` folder and nothing else.


## [0.15.0] - 2026-09-10

### Added

- `finding-consolidation` merges findings from several completed reviews into one ranked list with a single owner for each root cause.
- A shared severity scale and finding state, adopted in seven review skills, with an adoption table that records which skills use them.

### Changed

- Seven review skills grade findings on one scale instead of naming a severity no document defined.
- Skills that review a system or a package report severity alone, because no pinned change exists to compare a finding against.

### Security

- `public-private-boundary-review` keeps its own dispositions; converting them would replace a required reader action with a severity.
- Consolidation reads reported findings and asserts no verdict, re-runs no review, and claims no coverage that a source review did not establish.
- The consolidator ships beside the skills whose output it consumes, so its input format is authored rather than observed.

## [0.14.0] - 2026-09-10

### Changed

- Motion review is selected when a request would make fixture or sample data appear live, gate readable content behind an animation callback, or present modeled results as observed outcomes.

### Security

- The 0.13.0 command-line run showed two safety cases failing because the skill was never selected, so its refusals never applied. Widening the trigger is the fix under test; it is not evidence that selection changed.
- The Codex and Claude Code engineering packs stay held until the ten original cases are observed again with selection recorded.

## [0.13.0] - 2026-09-10

### Added

- A named substitute for missing comprehension evidence in motion review: a test-local observation against the existing build, or a separately consented study with a named owner.
- Routing disambiguation between `publish-change-safely` and `request-code-review`, with a safety case for a combined push-and-review request.
- Engineering-pack hold notices in the readme, quickstart, and selection guides, plus a `functional-motion-review` row in the readme engineering table.
- Backfilled changelog entries for the 0.9.0, 0.11.0, and 0.12.0 releases.

### Changed

- Motion review states where the supported finding must appear and returns named output sections, so a reply cannot open with file paths.
- The pack discovery guardrail is documented as a repository rule of Codex origin rather than a portable client limit.
- Maturity, release, and selection guidance no longer anchor to superseded version numbers.

### Security

- The Codex and Claude Code engineering packs remain held. Changed skill text does not lift a hold without observed client behavior.
- The 14 explicit-only workflows remain held for Claude account uploads until a receiving mode has a verified control that prevents automatic selection.
- The Antigravity motion preview stays disabled; its invented-evidence failure is not addressed by this release.

## [0.12.0] - 2026-09-09

### Added

- `functional-motion-review` for evidence-led motion assessment, with a focused reference that separates WCAG levels from catalog preferences.
- A reviewed source inventory covering 46 tracked authorities, including the relocated Swift documentation.
- Evidence-link checks that reject nested code, raw HTML, and historical-only links to the current client record.

### Changed

- The catalog grew to 78 skills across seven plugins.

### Security

- The Codex and Claude Code engineering packs were held after original motion cases failed on both command lines.
- The Antigravity two-skill preview was disabled after its answer invented duration and automation evidence.

## [0.11.0] - 2026-09-08

### Added

- Per-client setup guides for Codex, Claude, and Antigravity, with a combined client-support record.
- A focused continuity reference for the 13 skills that must separate an interim progress update from a checkpoint report.

### Changed

- Progress updates and checkpoint reports are distinguished so an interim note is not read as an acceptance record.

### Security

- Installed client packages are checked file by file. A matching version number alone does not establish installed content.

## [0.10.0] - 2026-09-04

### Added

- Orthogonal workflow-maturity, behavioral-evidence, client-compatibility, and runtime-eligibility records.
- Skill-level activation profiles with surface-specific discovery measurements.
- Scoped Codex and Claude repository instruction projections.
- A deliberately generalized public finding from one synthetic baseline-versus-focused Codex comparison.
- Deterministic local PyYAML validation for GitHub Actions workflow syntax, including regression tests for the v0.9 unquoted `--only-binary=:all:` failure, invalid document roots, and parser dependency drift.

### Changed

- Plugins remain distribution units while profiles become activation and discovery units.
- The seven-skill Delivery TypeScript profile remains experimental and non-default after a neutral public synthetic case.

### Security

- Raw traces, private prompts, product case IDs, exact private failures, and product architecture remain outside the public catalog.
- Client behavior and ADK runtime compatibility are recorded in separate evidence lanes.
- PyYAML and its type information are exact-versioned, SHA-256 locked for the Linux CI runner, and reconciled with reviewed dependency provenance.

## [0.9.0] - 2026-08-30

### Added

- Optional `jovanipink-agent-platforms` plugin with agent context, tool boundary, protocol, security, retrieval, and Google ADK workflows.
- `research-to-publication-lifecycle` for connecting sources, forecasts, outcomes, evaluations, and public-safe findings.
- A strict evidence taxonomy with capability, lifecycle, target, risk, invocation, and maturity facets.
- Deterministic local validation for GitHub Actions workflow syntax.
- Strict typing across scripts and tests, with locked provenance for reviewed CI tools.

### Changed

- Catalog skill counts were reconciled against the canonical source and the generated client trees.

### Security

- v0.9 acceptance remained blocked. Local package installation does not establish web, desktop, API, or managed-agent behavior.
- Exact-version observations record passes, failures, and authority or authentication blockers separately instead of implying parity.

## [0.8.0] - 2026-08-23

### Added

- Optional `jovanipink-ai-systems` plugin with original agent-evaluation, context-reliability, and source-to-output conformance workflows.
- Focused NIST TEVV and W3C PROV references used as correctness authorities without importing third-party skill implementations.
- Trigger, conflict, safety, output-quality, provenance, upstream-pin, package, and client-observation records for all three workflows.

### Security

- Evaluation design launches no paid or external run without separate provider, data, budget, and network authority.
- Context review embeds no private facts and keeps authority, time, permissions, supersession, and revocation distinct.
- Conformance execution is limited to repository-defined checks and authorized disposable fixtures or test stores; customer data, credentials, provider calls, production writes, migrations, and deployments remain excluded.

## [0.7.0] - 2026-08-23

### Added

- Original explicit-only `acceptance-evidence-ledger` workflow with current-evidence, freshness, blocker, and visible-abandonment states.
- Five original professional stack profiles for Adobe AEM, C# and .NET, Java and Spring, PHP and Drupal, and Salesforce, Apex, and Lightning Web Components.
- Generic repository-independence validation for canonical sources, documentation, generated plugins, and packaged skills.
- Blocked client-observation records that keep generated compatibility separate from installed behavior.

### Changed

- Skill provenance now uses Jovani-owned work and only primary authorities needed for format, interoperability, or correctness.
- Item-level external capability audits and restricted inventory summaries were retired from maintained trees without rewriting Git history.

### Security

- Ledger content is always untrusted data and never gains command or tool authority.
- File persistence requires explicit authority for an exact conflict-free path.
- New stack profiles use only official platform documentation as correctness authority and preserve provider, credential, migration, package, deployment, activation, and destructive-change gates.
- Hooks, dependencies, command runners, bundled agents, background processes, network grants, and hidden abandonment remain excluded.

## [0.6.0] - 2026-08-21

### Added

- Read-only change review and module interface design in `jovanipink-engineering`.
- Explicit-only prototype, merge conflict, guided configuration, handoff, and retrospective workflows with bounded authority.
- Focused specification, work-package, decision-map, candidate-comparison, and coverage-fanout references.

### Security

- Conflict reconciliation keeps abort available and gates stage, continue, commit, push, and pull request actions separately.
- Prototypes do not imply production credentials, sensitive data, commit, merge, deploy, migration, or publication.
- Retrospectives and handoffs exclude hidden reasoning, raw transcripts, secrets, unrelated history, and automatic policy mutation.

## [0.5.0] - 2026-08-21

### Added

- Eight independently authored reasoning, explanation, writing, impact, trace, and portable skill-authoring workflows in the optional `jovanipink-reasoning` plugin.
- Primary-authority provenance for format, interoperability, and correctness boundaries.
- Deterministic originality scanning for canonical, generated, and packaged skill content.

### Security

- No external text, structure, implementation, scripts, agents, hooks, templates, dependencies, model rosters, or examples were copied.
- Transcript mining, broad tool sweeps, self-modifying skills, and unconditional delegation remain excluded.
- Decision traces exclude hidden reasoning, raw transcripts, secrets, private data, and unrelated activity.

## [0.4.0] - 2026-08-21

### Added

- Eleven generic operating workflows in the independently installable `jovanipink-operations` plugin.
- Catalog-wide SemVer release manifests, checksums, compatibility records, deprecation and revocation registries, and rollback guidance.
- Weekly read-only primary-authority pin and security re-review freshness validation.
- A fictional private-overlay example and standard-library synchronizer.

### Security

- Revoked skills are omitted from generation, packaging, and marketplace advertisement without claiming installed-copy deletion.
- All CI actions are immutable revision pins with public provenance records.
- Public provenance contains only unauthenticated primary authorities; private facts remain private.

## [0.3.0] - 2026-08-21

### Added

- Nine read-only engineering-quality reviews for application security, supply chain, observability, performance, migrations, compatibility, test quality, accessibility, and operational readiness.
- Six optional stack profiles for Go, Python, Swift and SwiftUI, TypeScript and JavaScript, PostgreSQL and SQL, and Terraform.
- Stack-specific judgment failures in every representative fixture and an observed terminal macOS Swift result.

### Security

- Application security remains separate from agent skill security.
- Reviews prohibit unsupported compliance, SLSA-level, conformance, deployment, apply, and production-readiness claims.

## [0.2.0] - 2026-08-21

### Added

- Ten engineering lifecycle skills in the independently installable `jovanipink-engineering` plugin.
- Metadata-driven routing and generation for multiple Codex and Claude plugins.
- Output-quality rubrics and terminal baseline-comparison records for new skills.

### Security

- Explicit-only controls for plan execution, review requests, branch completion, and multi-agent orchestration.
- No hooks, MCP servers, bundled agents, skill executables, or broad tool grants.

## [0.1.0] - 2026-08-21

### Added

- Ten-skill portable v0.1 foundation.
- Generated Codex and Claude distributions.
- Trigger, provenance, security, packaging, and drift validation.
- Self-hosted marketplace manifests and individual Claude.ai packages.
