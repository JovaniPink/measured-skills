# 0.19.0 preview acceptance

Catalog version: 0.19.0

PR #78 merged on October 28 at `b4200af067fe696d5e9e41bc3413cf4938d18c64`.
This is merged preview source, not a release or installation. See
[merged state and remaining gates](release-status.md) for the preserved 0.18
identity, two-Mac tooling, and outstanding acceptance work.

Package generation and local checks are separate from installation, successful loading,
useful behavior, and deployment. The renamed catalog has no receiving-client acceptance.
Preserved 0.18 observations remain historical; they do not qualify 0.19.

Human selection and later separately authorized real-work trials are described in
[the acceptance protocol](acceptance-0.19.md). The implementation itself ran no model trial or installation. A later bounded
Claude observation has findings; see [the October 29 receipt](audits/haiku-evidence-followup-2026-10-29.md).
It does not qualify the revised skills or other clients. The later
[November 2 setup-blocked task](audits/client-preflight-2026-11-02.md) and
[current-main qualification audit](audits/release-qualification-2026-11-02.md)
retain the failed reference access, corrected unrun preparation and remaining gates.
Neither is a full acceptance pass.
The [November 5 Haiku exploration](audits/haiku-exploration-2026-11-05.md) changed discovery wording
and one prompt. It is one model on one synthetic task, not client acceptance.

## November 5 state

The candidate is frozen at manifest source `63156e05a9c7c5f25ed50920cc49b8c49bd00cfe`, with
chooser source `8f5f32e62e05bcde8c4be0815d3c01211ab84a47`. The maintainer accepted the
[release decision](audits/release-decision-0.19.0.md) on November 5.

| Client or app | Packaging | Behavior | 0.19.0 claim |
| --- | --- | --- | --- |
| Claude Code CLI | [Passed](audits/lifecycle-0.19.0.md) | Not yet run | Behavior claimed only if the bounded task passes |
| Codex CLI | [Passed](audits/lifecycle-0.19.0.md) | Blocked, no zero-credit control | Packaging only |
| Antigravity CLI | [Passed](audits/lifecycle-0.19.0.md) | Blocked, isolation unproven | Packaging only |
| Antigravity IDE, desktop and web apps, second Mac | Not checked | Not checked | Unclaimed |

Unclaimed means not tested, not failed. Packaging covers install, upgrade, downgrade, uninstall,
and reinstall in throwaway configurations. It does not show that a skill loads in a fresh task.

## Earlier records

The 0.18 candidate remains an independent preserved workstream. See its
[release ledger](release-readiness-2026-10-26.md). A preview is not a release approval.
