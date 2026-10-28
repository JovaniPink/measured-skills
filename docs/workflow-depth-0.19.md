# Make the next piece of work easier to finish

This 2026-10-28 increment makes existing capabilities easier to apply. Start in
[the chooser](start.md), not a second catalog. The preview still has **90 skills,
four packs and 17 explicit-only workflows**. Antigravity receives the 73 implicit
skills; that difference is deliberate, not a packaging defect.

## Choose the task and finish line

The seven main choices remain. Search reveals the specialist routes below; all
prompts, client variants and offline views come from `catalog/workflows.json`.

| Request | Route and useful result | Boundary |
| --- | --- | --- |
| Where does this behavior live? | Understand a codebase: one source-linked context map | No recursive README or AGENTS.md generation |
| Is this design ready? | Understand a design: reconstructed behavior, alternatives and missing decisions | Self-review by default; no implied delegation |
| Do these docs describe the code? | Compare documents with implementation: claim-to-evidence discrepancies | Code may be wrong; do not silently weaken requirements |
| Upgrade this dependency | Upgrade a dependency or framework: exact versions, callers, slices and recovery | Assess first or explicitly authorize local repair/install; no publication |
| Untangle this module | Refactor without changing behavior: characterization and before/after comparisons | Separate known defects and intended behavior changes |
| Why is this query slow? | Diagnose a query or execution plan: observed bottleneck and competing causes | Supplied evidence; no database/provider access |
| Is this replay safe? | Review a replay or backfill: identity, corrections, retry and sink conditions | No job submission or live backfill |
| Why does this Swift screen retain memory or hitch? | Diagnose a failure with the Swift stack: lifetime and trace interpretation | No invented Instruments, MetricKit or device result |

Use the scope selector for upgrade and refactoring. Assessment does not install or
edit. Upgrade repair permits reviewed project-local dependency installation under
the repository script policy because otherwise it could not validate the change.
Neither repair prompt permits global tools, unreviewed scripts, commits or pushes.
A later draft-PR route remains a separate request with its existing budgets.

A characterization test records existing behavior. It can expose a bug but cannot
decide whether preserving that bug is desirable. Similarly, a mismatch between a
runbook and code needs an authority decision: changing either artifact merely to
remove the mismatch can conceal the actual defect.

## Decisions on the proposed gaps

| Suggestion | Decision for this increment |
| --- | --- |
| Context compiler or automatic sentinel generation | One bounded context map in explain-codebase; no claimed token savings |
| Mandatory naive reader or contrarian swarm | Design reconstruction and alternatives in plan-change; independent review optional and authorized |
| AST-based drift scanner | Selected-document reconciliation in verify-claims; agent reasoning is not deterministic AST analysis |
| Dependency upgrades and refactoring | New practical routes and self-contained references; no new skill |
| Data pack | Query and replay routes over existing SQL/GCP contracts; future pack remains proposal-only |
| Swift memory and performance | Focused official-source guidance and synthetic fixtures; no cross-device umbrella claim |
| CI-workflow and web-journey skills | Former 0.19 commitments explicitly deferred to unassigned follow-ups, preserving track IDs and entry criteria |
| Companion sync, privacy, live incident response, unit cost | Retain candidate scope; require a representative task and distinct contract before admission |
| Release records, rollout, telemetry and prompt/schema regression | Existing capabilities remain available; no new execution or provider authority |

The historical roadmap records remain historical. Unreleased pack destinations use
the four-pack vocabulary; the agent-platform track spans Quality and the ADK stack.
No old client observation is transferred to a new name as acceptance.

## Source review and limits

All retrievals below were read-only. New pins use two byte-identical observations
on 2026-10-28; the exact hashes are in `catalog/upstream-pins.json`. No existing pin
was replaced and no normalization or freshness rule was relaxed.

| Source | Inspected identity and supported use | Limits |
| --- | --- | --- |
| [Refactoring definition](https://martinfowler.com/bliki/DefinitionOfRefactoring.html) | Author's definition, dated 2004; distinction between structure and observable behavior | Does not specify our characterization protocol or prove equivalence |
| [Next.js migration](https://nextjs.org/docs/app/guides/upgrading/version-16) | Version-16 guide; exact version discovery, runtime/API/bundler changes | Floating installer examples are not an approved command; no project upgrade executed |
| [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/18/sql-explain.html) | Version 18; estimated cost and actual execution are different | Other engines and versions require their own evidence |
| [Apple memory guide](https://developer.apple.com/documentation/xcode/gathering-information-about-memory-use.md) | Official Markdown body; graphs, allocation stacks, generations, simulator caveat | Text renderer rejected Markdown; direct public retrieval succeeded. No app trace executed |
| [Apple SwiftUI performance](https://developer.apple.com/documentation/xcode/understanding-and-improving-swiftui-performance.md) | Official Markdown body; expensive versus frequent updates and profiling | Does not establish a universal device frame budget |
| [Airflow best practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html) | Planning review of stable 3.3.2; repeatable tasks and fixed intervals | Existing pin retained; installed Composer/Airflow version still requires discovery |
| [BigQuery computation](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute) | Existing reviewed warehouse authority; plan stages and scan scope | No authenticated metadata query or performance observation |

Earlier EGM research remains in [the discovery audit](audits/discovery-0.19.md),
including inspected revision 05f8984. Its document/source comparison is not an AST
scanner. No EGM implementation, persona, branding, or orchestration was imported.
The proposed 30% context saving and universal 10-16x token multiplier remain
unsupported and are not product claims. New prose is original synthesis; existing
owned-adaptation lineage and the accepted originality packet remain intact.

## Discovery budgets are measurements, not acceptance

At the preserved identity checkpoint, Workflows descriptions total 5,807 characters,
while synthetic listings estimate 8,563 for Codex and 8,595 for Claude. The catalog's
`within-budget` description metric is not an installed-client context-fit result.
Use focused profiles. This increment changes reference depth, not descriptions,
profile membership, invocation policy, staging defaults, or wrapper identities.

## Verification and next observation

The [24 prepared scenarios](../evals/workflow-depth/README.md) cover eight areas
with useful, confusable, and authority/evidence cases. They are fixtures, not model
runs. The original ten-card human exercise stays unchanged and pending. After the
drafts are pushed, use five additional uncoached cards: assess an upgrade without
installing; refactor a serializer without changing errors; diagnose a supplied SQL
plan; review a partial replay; investigate Swift memory growth from supplied data.
Record route, time, help needed, copied scope and expected evidence. Zero cards may
expand authority. These extra cards do not replace failed original cards or alter
the original acceptance targets. Simplify confusing navigation before adding skills.

The immutable naming checkpoint is 62af7d15431c9b3e653523888cd574b7319d7171.
Historical rename preservation is checked at that revision. Current canonical edits
are separately bound by [the technical delta](audits/workflow-depth-2026-10-28.json),
with missing, extra, stale or unreviewed file hashes rejected. The existing
post-acceptance ledger still covers the complete current payload; neither ledger
extends prior maintainer acceptance. Generated chooser references are verified by
regeneration, not treated as hand-authored changes.

Available repository, export, browser and machine checks must be reported with
exact revisions and limitations in the draft PRs. Human usability, installed-client
activation, device acceptance, productivity and release readiness remain unproven.
