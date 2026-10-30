# Merged work and remaining release gates

Snapshot: October 29, 2026. Merged repository baseline:
`7cc619503c04cac2f178118830e7b0f82901587c`.

The implementation and two-Mac tooling are merged. Neither 0.18 nor 0.19 is a
published release. GitHub's release list was empty at this observation. The October 28 tag
inspection contained `v0.16.0`, with no 0.18 or 0.19 tag; tags were not rechecked
in this pass. This does not erase older
package distributions or claim they were qualified on every client.

## Which source means what

| Record | Exact identity | Meaning |
| --- | --- | --- |
| [0.18 preparation, PR #72](https://github.com/JovaniPink/measured-skills/pull/72) | Candidate head `cd9ff2417a5b6ca468642fad2da179dbebd99cbd`; merge `5235afe681a8814d667d5e070f6deac997f7ebf7` | Preserved 88-skill, 11-pack candidate; merged, not promoted |
| [Motion proposal, PR #77](https://github.com/JovaniPink/measured-skills/pull/77) | Merge `f3f9739bf2af69b51246d32009f0e6da3eaaa1d4` | Preserved proposal and pilot evidence, not portable-skill acceptance |
| [0.19 redesign, PR #78](https://github.com/JovaniPink/measured-skills/pull/78) | Head `aa1d85981ecec017c53db27b209fb850317dae66`; merge `b4200af067fe696d5e9e41bc3413cf4938d18c64` | Merged 90-skill, four-pack preview |
| [Chooser usability and boundary repairs, PR #79](https://github.com/JovaniPink/measured-skills/pull/79) | Reviewed head `f8e03f99ab6ec39f3c1b80572217519867c51258`; merge `4a35cdef387f9b90c6b1e32dc03d4f96ba34b06f` | Merged with both parents preserved; no release or installation |
| [Source freshness, PR #80](https://github.com/JovaniPink/measured-skills/pull/80) | Reviewed head `978437939c47340f1c5af1f0b11d700db9520de0`; merge `4d8205c4f569a4dd4096d9daea413b2219ced4e9` | Merged source decisions and retained receipts; no release or client acceptance |
| [Task-sentence search and acceptance preparation, PR #81](https://github.com/JovaniPink/measured-skills/pull/81) | Reviewed head `8e9cb09e6a40cb2b8f2d4f45ae001fe12c1cebf4`; merge `7cc619503c04cac2f178118830e7b0f82901587c` | Merged chooser repair; later disposable trial edits are not part of this PR |
| Two-Mac tooling | Dotfiles #35 and #37 merged October 28 | Staging and receipt support, not an installed update or M5 qualification |

The 0.18 manifest names source `f209dcf26047edc35c7d5c3489198826ddd136a0`.
Read the current 0.19 artifact source from `source_commit` in
[its manifest](../releases/0.19.0/manifest.json); the reviewed source-pin follow-up rebinds it from its clean source
commit in a separate manifest-only commit. Read the discovery input source from `source_revision` in
[its catalog](../dist/discovery/catalog.json).
These identities have different jobs. Do not replace them with a merge SHA just
to make the labels match. A website can also retain a separately pinned export;
merging a repository does not update that website or an installed client cache.

For 0.18 work, use its preserved source in a separate checkout. Current `main`
has 0.19 metadata, generators and renamed skills. Do not run current generators
and label their output 0.18. Follow the [release process](release-process.md)
and [migration guidance](migration-0.19.md), preserving ancestry.

## Remaining gates and concrete next work

| Gate | Retained evidence | Next action and boundary |
| --- | --- | --- |
| Source and metadata | Merged inventory: 90 skills, four packs, 73 implicit and 17 explicit-only; all remain candidates | [Follow-up source tracing](audits/post-merge-review-2026-10-28.md#follow-up-source-trace-and-repairs) repairs action-entry search and adds copyable ordinary requests. No new skill or rename is justified by this pass |
| Automated repository evidence | October 29 source-review checks and all 318 regression tests passed locally; [exact PR-head validation](https://github.com/JovaniPink/measured-skills/actions/runs/40953581963) passed for `9784379`. Fresh merge review also passed deterministic validation and three focused source regressions | See [validation evidence](validation-evidence.md). Local and hosted checks do not establish receiving-client behavior. Later chooser work has its own source and validation record |
| Online authorities | October 29 0.19 closeout: 69 matching sources, zero changed or unavailable | [Individual review](audits/source-review-2026-10-29.json) covers the initial 29 changes and three later NIST/OWASP changes; [final receipt](audits/source-check-final-2026-10-29.json). Source URLs, marker kinds, global review age and validator behavior are unchanged. Preserve the [initial failure](audits/upstream-freshness-2026-10-29.json) and [intermediate failure](audits/source-check-intermediate-2026-10-29.json). No canonical instruction defect was established by this source review; current-content review does not prove historical equivalence where old bodies are missing. Recheck before release |
| Originality | Exact scoped acceptance at `36a4e56`, plus subsequent technical delta records | Preserve that acceptance and record this documentation delta. Do not reopen the closed undefined hold or imply new maintainer acceptance |
| Human chooser usability | [Ten-card protocol](acceptance-0.19.md) prepared; no participant results recorded | The October 29 reply repeated the task without a route, scope or time; it remains unscored. Sentence lookup is a separate engineering finding. Record actual human selections without coaching |
| 0.18 Claude diagnostic | Four cases and two continuity follow-ups passed at the recorded October 27 source | Keep that diagnostic closed. Distinct installation lifecycle, invocation-control, changed-goal and remaining profile acceptance are not complete |
| 0.19 receiving-client behavior | Two Claude Haiku tasks and one continuation observed at the October 29 source, with evidence-discovery and reporting findings; no full acceptance | Original results retained in the [follow-up record](audits/haiku-evidence-followup-2026-10-29.md). Revised contracts and one-session/one-continuation retest are preparation only; fresh controls and new execution authorization remain required |
| Codex and Antigravity controls | October 26 records leave Codex paid fallback and Antigravity isolation unresolved | Re-inspect actual controls before any later model trial. Do not substitute another account, proxy, billing route or permission bypass |
| Apps and second Mac | No new qualification recorded | Verify each receiving surface independently; do not transfer credentials, caches or acceptance results |
| Public discovery | Studio #141 and personal #164 are open drafts as of October 29 | Complete existing website approval and deployment gates separately. Local guide use does not require website publication |
| Release | No GitHub Release at this observation; prior tag inspection dated October 28 | Select an exact version and qualified revision, satisfy its applicable gates, and obtain the separate release decision. Merge alone is insufficient |

## Merge checkpoint and next sequence

PR #80 merged October 29 at 23:13:55 UTC with parents `4a35cde` and
`9784379`. Exact-head validation passed; all review threads were inspected and
none remained. Effective branch rules were empty and classic protection reported
"Branch not protected". No required approval was bypassed. The merge used an
exact-head guard and the merge-commit method without changing repository settings.


PR #79 merged October 29 at 20:20:37 UTC after exact-head validation passed.
GitHub reported no effective branch rules, no classic branch protection, and no
unresolved review threads. There was no required human approval to bypass. The
merge used the reviewed head as a guard, no admin override, and no settings
change. Its two parents are `b4200af` and `f8e03f9`. At that merge, artifact
source `34be842a94aa2411a4a4844274e98df196ff4d61` and discovery source
`5bdf10844d34fc738766a5a56be59542deba8bfd` were verified ancestors. The later
source-pin follow-up retains those anchors and records its new source in the
current manifest.

1. Keep the reviewed source decisions and their limits with the candidate. All 69
   sources matched on the final October 29 pass. Recheck near release and review
   any new drift individually; this snapshot is not a permanent freshness pass.
2. Complete the prepared human chooser exercise. The user's reported uncertainty
   is a reason to improve clarity, not a completed task result or acceptance score.
3. Review the retained Claude findings and proposed one-session/one-continuation
   retest. Its execution requires new authorization and fresh account, isolation,
   permission and billing-route checks. The original Claude allowance is consumed;
   other client lanes and the closed 0.18 diagnostic remain separate.
4. Complete the website publication sequence under its own approvals. This does
   not prevent using the local guide now.
5. Decide the release version and exact qualified revision only when its required
   gates have evidence. A fresh source check is a release checkpoint, not a
   permanent guarantee about mutable upstream pages.

The source follow-up changes reviewed fingerprints and their evidence inventory.
All 90 package archives matched across two builds; canonical instructions and
client projections are unchanged. The manifest is rebound to the new source
commit without rewriting history. No new client result is claimed.

## Use what is available now

Read [the start guide](start.md), open the local chooser, and choose the intended
scope. Its source is available without installing anything. Ordinary requests
are the default; select the native-command option only after checking the actual
installed entry. Do not infer that 0.18 observations qualify
the renamed 0.19 package.

Human results and model results stay separate. If the chooser is confusing,
record the concrete confusion and simplify that path before expanding the
catalog. No productivity, revenue, routing-accuracy or cross-client parity claim
follows from this audit.

This ledger grants no installation, billing, trial, merge, deployment or release
authority. The preserved [0.18 ledger](release-readiness-2026-10-26.md) holds its
dated evidence; the [0.19 acceptance record](client-candidate-v0.19.0.md) holds the
preview boundary. Update this summary when actual evidence changes.
