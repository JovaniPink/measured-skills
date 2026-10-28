# Merged work and remaining release gates

Snapshot: October 28, 2026. Repository baseline:
`b4200af067fe696d5e9e41bc3413cf4938d18c64`.

The implementation and two-Mac tooling are merged. Neither 0.18 nor 0.19 is a
published release. GitHub's release list was empty at this observation; its tag
list contained `v0.16.0`, with no 0.18 or 0.19 tag. This does not erase older
package distributions or claim they were qualified on every client.

## Which source means what

| Record | Exact identity | Meaning |
| --- | --- | --- |
| [0.18 preparation, PR #72](https://github.com/JovaniPink/measured-skills/pull/72) | Candidate head `cd9ff2417a5b6ca468642fad2da179dbebd99cbd`; merge `5235afe681a8814d667d5e070f6deac997f7ebf7` | Preserved 88-skill, 11-pack candidate; merged, not promoted |
| [Motion proposal, PR #77](https://github.com/JovaniPink/measured-skills/pull/77) | Merge `f3f9739bf2af69b51246d32009f0e6da3eaaa1d4` | Preserved proposal and pilot evidence, not portable-skill acceptance |
| [0.19 redesign, PR #78](https://github.com/JovaniPink/measured-skills/pull/78) | Head `aa1d85981ecec017c53db27b209fb850317dae66`; merge `b4200af067fe696d5e9e41bc3413cf4938d18c64` | Merged 90-skill, four-pack preview |
| Two-Mac tooling | Dotfiles #35 and #37 merged October 28 | Staging and receipt support, not an installed update or M5 qualification |

The 0.18 manifest names source `f209dcf26047edc35c7d5c3489198826ddd136a0`.
The 0.19 manifest names source `87b9741ba3dc8133974bd0ba38b74338fad9ead5`.
The discovery export names input source `d9d9055a87bbe47b72122c2370404e8c2779c1a2`.
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
| Source and metadata | October 28 inventory: 90 skills, four packs, 73 implicit and 17 explicit-only; all remain candidates | Source audit complete within [its stated scope](audits/post-merge-review-2026-10-28.md). No new skill or rename is justified by this pass |
| Automated repository evidence | [Merged-main validate job](https://github.com/JovaniPink/measured-skills/actions/runs/40753511774/job/123046173473) succeeded for `b4200af` | Existing remote evidence was read, not rerun. It does not validate later documentation changes or receiving-client behavior |
| Online authorities | October 26 0.18 closeout: 64 matching sources | Dated evidence only. A new online check and individual drift decisions remain required for a later release; no freshness run or repinning occurred in this audit |
| Originality | Exact scoped acceptance at `36a4e56`, plus subsequent technical delta records | Preserve that acceptance and record this documentation delta. Do not reopen the closed undefined hold or imply new maintainer acceptance |
| Human chooser usability | [Ten-card protocol](acceptance-0.19.md) prepared; no participant results recorded | Let the user select routes and prompts without coaching. Record time, errors, help, intended output and scope; do not score code inspection as human success |
| 0.18 Claude diagnostic | Four cases and two continuity follow-ups passed at the recorded October 27 source | Keep that diagnostic closed. Distinct installation lifecycle, invocation-control, changed-goal and remaining profile acceptance are not complete |
| 0.19 receiving-client behavior | No retained receiving-client acceptance | Prepare the separate bounded real-work trial only after actual account, isolation, permission and no-paid-fallback checks. No new model calls in this pass |
| Codex and Antigravity controls | October 26 records leave Codex paid fallback and Antigravity isolation unresolved | Re-inspect actual controls before any later model trial. Do not substitute another account, proxy, billing route or permission bypass |
| Apps and second Mac | No new qualification recorded | Verify each receiving surface independently; do not transfer credentials, caches or acceptance results |
| Public discovery | Studio chooser and personal guidance remain in their website draft sequence | Complete existing website approval and deployment gates separately. Local guide use does not require website publication |
| Release | No 0.18/0.19 tag or GitHub Release at the snapshot | Select an exact version and qualified revision, satisfy its applicable gates, and obtain the separate release decision. Merge alone is insufficient |

## Use what is available now

Read [the start guide](start.md), open the local chooser, and choose the intended
scope. Its source is available without installing anything. Check the actual
installed entry before sending a native command; use the documented ordinary
request fallback when it is missing. Do not infer that 0.18 observations qualify
the renamed 0.19 package.

Human results and model results stay separate. If the chooser is confusing,
record the concrete confusion and simplify that path before expanding the
catalog. No productivity, revenue, routing-accuracy or cross-client parity claim
follows from this audit.

This ledger grants no installation, billing, trial, merge, deployment or release
authority. The preserved [0.18 ledger](release-readiness-2026-10-26.md) holds its
dated evidence; the [0.19 acceptance record](client-candidate-v0.19.0.md) holds the
preview boundary. Update this summary when actual evidence changes.
