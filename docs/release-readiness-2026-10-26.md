# 0.18.0 release gates, October 26

0.18.0 remains a candidate. Source review and repository checks do not complete
client acceptance. This is the current planning ledger; the
[October 20 record](release-readiness-2026-10-20.md) retains earlier checkpoints.
No merge, installation, billing change, model run, tag, or release is authorized
by this ledger.

## Current inventory and evidence

The candidate has 88 skills in 11 packs: 88 in Codex and Claude projections,
and 71 implicit skills in Antigravity. Its 17 explicit-only exclusions remain.
The daily profile selects 12 skills; the finish-work profile selects 14.
Neither profile has receiving-client qualification. The catalog retains 87 skills
with no behavioral evidence and one with partial historical evidence. Package
availability, installation, successful loading, correct behavior, and measured
benefit are separate claims.

This follow-up starts at `115b65085efa472584e9ae1be23b0f2737e68c9c` and preserves
its source anchor `ddf40499835e8dc0b39079cd8deb7dba0594f85a` and all earlier
source/acceptance anchors. The new manifest must bind the clean source commit.
It retains 139 artifacts; the two source catalogs and prompt-review provenance
require rebinding, while canonical skills and generated archives are unchanged.

| Gate | Current evidence and limit | Required next step |
| --- | --- | --- |
| Online source freshness | The [new closeout](audits/openai-swift-source-closeout-2026-10-26.json) records 64 matching sources, none changed, none unavailable, after [two individual decisions](audits/openai-swift-source-review-2026-10-26.json). Earlier 33-source and Antigravity failures remain historical. | Passed at this checkpoint. Recheck before a later release decision; new drift remains blocking. |
| Repository consistency | The prior checkpoint passed 285 unit tests. This follow-up adds four authority/source-binding tests. Follow-up checks and the refreshed manifest must pass on the submitted revision. | Verify the final source/manifest pair and exact pushed-head CI; local tests do not prove hosted execution. |
| Generated artifacts | Canonical skills and generated output are unchanged in this source-review increment. Existing byte checks cover projections and all 88 archives. | Retain byte correspondence and complete manifest inventory; version labels alone are insufficient. |
| Originality and licensing disposition | The maintainer [accepted the exact scoped decision](audits/originality-acceptance-0.18.0.json) for `36a4e56c7fcde0411d2b3c7052c9f2b889d05aa7`, including the gate replacement. The undefined corpus and further independent-review holds are closed for that payload. | Preserve the accepted packet and [post-acceptance delta](audits/post-acceptance-delta-2026-10-20.json). Later changes are technical delta reviews, not new acceptance or universal legal clearance. |
| Claude Code acceptance | The [pilot](audits/cli-pilot-observations-2026-10-20.json) and [retest](audits/claude-retest-observations-2026-10-21.json) recorded routing and evidence failures, including continuity and GCP contract errors. Both allowances are consumed. | The [five-case, two-follow-up diagnostic proposal](audits/claude-routing-contract-retest-plan-2026-10-21.md) remains prepared, not run. It needs a separate execution decision and fresh billing/isolation checks. Repairs alone do not establish success. |
| Codex CLI acceptance | [Dated native checks](audits/client-controls-2026-10-21.md) established isolated discovery but not a verified no-paid-fallback route. | Establish the actual billing boundary before a model run. No proxy or API fallback is authorized. |
| Antigravity CLI acceptance | The same dated checks found ambient skill/instruction loading despite the disposable workspace. Published loading and slash-command documentation do not demonstrate effective isolation. | Find and verify supported isolation without altering ordinary installations; retain exclusions and leave the lane unrun meanwhile. |
| App, account-library, and second-machine acceptance | No new app-mode or second-machine qualification is recorded. CLI observations cannot fill these cells. | Inspect and test each claimed surface separately under its own authority. Narrowing claims does not waive required gates. |
| External validators | Standalone skills-ref and Codex CLI plugin validation were unavailable in the retained environment evidence. Native format results are not behavior results. | Record availability honestly; a reviewed isolated validator installation remains separate work. |
| Release decision | The candidate draft remains unmerged and unpromoted. Required trigger and manual evidence is incomplete. | Follow the [release gate](testing.md#release-gate), retain failed/unavailable cells, then seek a separate release decision. |

## Source closeout

The [current closeout](audits/openai-swift-source-closeout-2026-10-26.json) records
64 matches, no changes, and none unavailable. The [two-source decision ledger](audits/openai-swift-source-review-2026-10-26.json)
records the exact before/after bindings and their limits. All other 62 pins and
the global review clock remain unchanged.

OpenAI's HTML differs from the retained body only in site asset URLs. Its official
page advertises [complete Markdown](https://developers.openai.com/api/docs/guides/prompt-engineering.md),
which was reviewed against the article and returned three identical responses.
The complete Markdown bytes are hashed; no content is stripped. The provenance
URL and one exact primary-document allowance now name that representation.
Regression tests reject neighboring URLs. The skill's human-facing HTML link and
non-executing prompt-review contract remain unchanged.

The [Swift Evolution document](https://www.swift.org/swift-evolution/) also returned
three identical responses. Its old exact body was unavailable; this is an explicit
current-content review, not a claim that the drift was cosmetic. The page explains
proposal discovery and review, while JavaScript loads the proposal list. Its HTML
fingerprint does not bind every linked proposal, feature status, or compiler result.
Retain exact toolchain and per-module setting checks for technical claims. No new
runtime or installed-client qualification is inferred.

The [previous Antigravity closeout](audits/antigravity-source-closeout-2026-10-26.json)
remains the historical 62-match/two-hold checkpoint. The source repairs below are
retained context, not a claim that their earlier counts are current.

The [Antigravity review](audits/antigravity-source-resolution-2026-10-26.json)
checks complete official Markdown for [headless CLI](https://antigravity.google/docs/cli/headless.md),
[skills](https://antigravity.google/docs/skills.md),
[plugins](https://antigravity.google/docs/plugins.md), and
[SDK overview](https://antigravity.google/docs/sdk/overview.md). Ordered document
headings match the corresponding HTML; manual review covers the instructions,
not just headings. No canonical instruction repair is needed. Published controls
still do not prove installed loading, isolation, or a no-paid-fallback route.

The tab-selected plugin Markdown alternated between two app navigation labels.
The selector-free official URL retains all three client sections and returned six
identical complete documents. The rejected candidate and its failed online scan
remain recorded. The SDK sometimes returns declared gzip despite an identity
request. Correct HTTP decoding produces the same complete document; the repaired
checker hashes those decoded bytes and rejects corrupt or unsupported coding.
Regression tests first reproduced the defect. This adds no text normalization,
source allowlist exemption, or global review-date reset.

The [earlier closeout](audits/source-check-closeout-2026-10-26.json) remains the
historical 60-match/four-hold checkpoint. The new bindings and checks do not rewrite
it or promise that any source stays unchanged. Future mismatches remain blocking.

The prior review gave three header-only changes a stronger binding: ADK's index and safety page,
and Git's worktree manual, each returned six identical full bodies despite
changed ETag or Last-Modified values. Those individual decisions use the existing
full-content SHA-256 method. At that earlier checkpoint, OpenAI's prompting-page
response changed only Astro asset URLs, with three identical responses supporting
its then-reviewed full-body pin. That historical comparison does not classify the
OpenAI HTML drift reviewed in this follow-up. No byte is removed when computing these pins.

A changed marker is not proof that an instruction is wrong. Conversely, three
matching markers do not prove stable page bytes or semantic equivalence. The
old exact bodies were unavailable for the initial 33 comparisons, so the review
checks current requirements against canonical guidance instead of claiming that
all drift was cosmetic. Later comparisons use bodies retrieved in this session.
No new normalization or global review-date reset was introduced.

## What can proceed without paid evaluations

1. Retain source-review decisions and repeat freshness before a later release
   decision. Complete deterministic checks and exact-head CI.
   Preserve unavailable hosted execution as unavailable; changing billing is not
   a repair within this scope.
2. Inspect native account controls, loading paths, and duplicate-source inventories
   read-only. Keep private inventories outside public artifacts. A documentation
   claim cannot substitute for an observed billing or isolation control.
3. Review the prepared Claude diagnostic inputs, expected outputs, and fresh
   prerequisite checklist. Do not run it under either consumed allowance.
4. Prepare an explicit supported-surface claim and acceptance matrix. Failed,
   untested, and unavailable cells remain visible. Do not call a reduced scope
   an automatic waiver.

The post-0.18 review-learning pilot is deferred until after release. It is not
another gate or part of this candidate. Separate machine-tool hosted-CI issues
also do not become evidence that the public catalog checks failed or passed.
