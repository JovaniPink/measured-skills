# 0.18.0 release readiness, October 20

Status: candidate; release blocked. No tag, release, public-directory submission, or installed-client promotion is authorized by this record.

Merged baseline `7aff034` passed 233 unit tests and deterministic gates. All 87 archives matched generated Claude source bytes. Its manifest bound 137 artifacts to ancestor `81c6701`, preserving both feature and main histories. These are baseline receipts, not results for later edits.

## Follow-up repairs

The new archive regression mutates bytes and recomputes the archive checksum; content must still match the generated source. Missing, extra, and duplicate archive members are rejected. The current manifest must contain each required artifact path and kind exactly once. Historical manifests keep their own schemas and evidence.

The [initial source review](audits/source-review-2026-10-20.md) retains its historical nine holds. The [PR follow-up decisions](audits/pr72-source-hold-repairs-2026-10-20.json) address all nine: four renderer-shell bindings were replaced with substantive official documentation data, one obsolete duplicate URL was retired in favor of the existing official guide, and four current-content sources had three agreeing planned samples. Newly observed OpenAI subagent drift was also reviewed and repinned. There are now 62 active sources.

The [follow-up closeout](audits/pr72-source-closeout-2026-10-20.json) matched 61 of 62 sources. It found new ASVS drift, whose three planned body samples subsequently disagreed. Its pin remains unchanged, so the online gate still fails for that one source. No global review clock, normalization rule, or fail-closed policy was relaxed. The initial nine holds are addressed; the new hold is not concealed by that progress.

The [originality disposition](audits/originality-disposition-2026-10-20.md) now traces all 87 histories and locates the owned MIT source license for four historical adaptations. Their later clean-room relabel changed no procedural body. Current provenance qualifies those labels; no independent process or comprehensive originality qualification was found. The release hold remains until a scoped review and maintainer disposition are accepted.

## Limited-evidence target

Package availability, installed files, enabled state, actual loading, case outcomes, and benefit are separate claims. A small daily-profile smoke check can support only its exact cases and client conditions. It cannot qualify all 87 skills, all 12 selected skills, every app mode, long sessions, or comparative benefit. Full catalog and frozen behavioral studies remain unchanged and unrun by this work.

Subscription sign-in does not by itself attest a no-paid-fallback billing route. Effective pilot isolation and billing prerequisites remain unverified for this source. No model request is permitted while those preconditions are unresolved. Account-specific inventories and authentication observations remain private.

The initial authorized ceiling is six synthetic cases and two continuity follow-ups per CLI, with human grading. The [pilot contract](../evals/daily-engineering/cli-smoke-2026-10-20.json) freezes those inputs. No paid native eval, API collection, automated judge, overage, or permission bypass is allowed. A blocked lane consumes no further requests. Global installations must not be removed to manufacture isolation.

Cloud libraries, managed work-account policies, and app-mode loading require separate inspection. Do not copy a terminal result into ChatGPT Work/web, Codex desktop, Claude Chat/Code/Cowork, or Antigravity desktop/IDE records. Acceptance on a second machine remains pending until performed there.

## Exit checklist

- Required deterministic and official-format checks pass at the submitted head.
- Generated output and repeated archive checksums agree; the manifest source remains in submitted ancestry.
- Remaining source and originality holds have explicit accepted dispositions before release.
- Every claimed skill/client case has fresh loading and outcome evidence under ordinary permissions.
- Private account inventories and raw traces stay outside public artifacts.
- Release claims identify exact supported scope and untested conditions.

No release follows automatically from completing repository repairs or the pilot. A separate maintainer release decision remains required.
