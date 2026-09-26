# Measured Skills candidate

Catalog version: 0.17.0

Updated: 2026-09-23

This candidate retains 79 skills and splits engineering into build, review, and delivery, for nine packs. Publisher metadata is Measured Studios. The source repository has not transferred. See the [migration guide](measured-migration.md).

## Evidence boundaries

Native adapters and package checks do not prove client discovery, behavioral benefit, or sustained-session adherence. Prior [0.16.0 evidence](client-candidate-v0.16.0.md) retains its original identity and limits. Explicit-only and turn-depth holds remain in effect on unverified surfaces.

On 2026-09-21, a fresh Codex CLI 0.154.0 read-only session using the existing gpt-5.6-sol model at medium effort listed all seven focused native project skills. User configuration was excluded for that check. Unrelated global Clerk skills remained visible and were misclassified by the response as legacy skills, so the response is not a complete inventory oracle. This checks the standalone projection, not installation of the renamed plugin. No implementation task, controlled comparison, or default promotion followed from it.

On 2026-09-23, all nine packs passed the native install, upgrade, downgrade, and reinstall lifecycle, with installed files matching the generated source by hash, on Claude Code 2.1.280, Codex CLI 0.154.0, and Antigravity CLI 1.2.8. Uninstall passed at the inventory level on all three CLIs: each client's plugin list stopped listing the removed packs. That is not the full removal check, which requires the pack to be absent in a fresh task. Claude Code also kept every removed pack's cached files. Each CLI ran in a throwaway configuration upgraded from 0.16.0 by following the migration guide. The lifecycle steps ran no model prompt. Separate Claude Code 2.1.281 fresh-task checks then loaded all nine packs, loaded two skills by direct selection, left the explicit-only `publish-change-safely` inactive for one natural prompt, and found an uninstalled pack absent, so fresh-task removal is verified on Claude Code only. Each case ran once. Codex and Antigravity fresh-task loading, selection, explicit-only controls, and removal remain unverified. See the [lifecycle record](manual-smoke-tests.md#0170-isolated-install-lifecycle-2026-09-23).

A fresh Claude Code 2.1.220 check using the staged build plugin and two project skills stopped before inference with HTTP 401: its OAuth token was expired. No discovery or behavioral pass is inferred. Marketplace and build-plugin native structural validation passed separately.

## PR 44 disposition

The [independent review](https://github.com/JovaniPink/measured-skills/pull/44) proposes remediation; its documentation-only patch does not implement fixes.

| Finding | Disposition | Evidence |
| --- | --- | --- |
| Explicit-only mapping | Preserved | Native adapters and mapping tests remain authoritative for structure, not observed behavior. |
| Description-only size | Addressed | Discovery estimates include names, repository-relative paths, separators, and descriptions. Absolute install path and client serialization overhead remain unknown. |
| Private pre-commit hook | Deferred | Policy-only repository forbids hooks; its existing validator is not a comprehensive secret scanner. |
| Motion routing length | Addressed | Canonical description shortened; full safety meaning remains in the workflow. Fresh activation requires rechecking. |
| Engineering pack size | Addressed | Three packs; focused activation is tested separately from packaging. |
| Offline security claim | Addressed | SECURITY.md distinguishes offline packaging from opt-in network checks and host tool permissions. |
| Behavioral evidence gap | Addressed for recoverable records | Ledger entries index 24 existing historical records across four skills, preserving dates, client versions, and source case IDs. Current skill and comparison records stay unobserved. |

No release tag, marketplace update, deployment, or global-default promotion follows from preparing this candidate.
