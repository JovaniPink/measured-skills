# Merged work and remaining release gates

## Current state on November 5

The November 5 safety fixes merged in [PR #97](https://github.com/JovaniPink/measured-skills/pull/97)
at `1ba9787815733643e440c38ad6d6270b983edd60`, and [validation on that commit](https://github.com/JovaniPink/measured-skills/actions/runs/42107090587)
passed. The 0.19.0 preview has 90 skills in four packs, with 73 implicit and 17 explicit-only.
The cleanup record and follow-up source review in
[PR #98](https://github.com/JovaniPink/measured-skills/pull/98) passed hosted
validation at `d871b70ef40784df4c04bf26ab8f95d49ca0ae4a`.

The merged work tunes the nine core descriptions and the assess prompt from a
[one-model Haiku exploration and retest](audits/haiku-exploration-2026-11-05.md). That record
is exploratory. It does not close any acceptance gate below.

[The release decision](audits/release-decision-0.19.0.md), accepted by the maintainer on
November 5, sets what a stable tag would claim, which gates block it, and what the
frozen candidate is. It does not authorize a tag or a Release.

The [November 5 skill security review](audits/skill-security-review-2026-11-05.md) found no
errors and five warnings. The maintainer chose to fix them before tagging, which replaced
the earlier freeze. See
[the amendment](audits/release-decision-0.19.0.md#amendment-on-november-5-2026-safety-fixes).

| Record | Revision |
| --- | --- |
| Chooser input in [the export](../dist/discovery/catalog.json) | Read `source_revision` there |
| Artifact source in [the manifest](../releases/0.19.0/manifest.json) | Read `source_commit` there |

| Gate | State on November 5 | Who can close it |
| --- | --- | --- |
| Repository checks | [Hosted validation passed](https://github.com/JovaniPink/measured-skills/actions/runs/42135750310) on the PR #98 head `d871b70e`. The eventual tag commit needs its own result | Hosted CI on the exact head |
| Description wording | Closed. The maintainer accepted the third-person wording on November 5. It scored 8 of 32 in the full catalog in each of two runs, against 12 of 32 for the imperative. The gain did not hold under a forced 8,000 character listing. This accepts the wording only, not client behavior or the originality record | Closed by the maintainer |
| Exploration account check | Open. The November 5 runs did not inspect usage-credit controls, and $3.85 and $2.64 are list-price estimates. A later usage readback showed extra usage off, but the maintainer has not confirmed it in Settings | The maintainer, by reading the account's usage |
| Online sources | Open. The [earlier November 5 check](audits/source-check-final-2026-11-05.json) matched 69 of 69 after [review](audits/source-review-2026-11-05.json). A later check at `1ba97878` matched 58 of 69. [All eleven changes were reviewed](audits/source-review-followup-2026-11-05.json). Ten stable replacements were repinned. OpenTelemetry remains on hold because successive captures changed its body and ETag despite matching extracted text. The [follow-up check](audits/source-check-followup-2026-11-05.json) passed 67 of 69 sources, with a new OWASP page change also held for review | Review drift, then recheck on the exact commit proposed for the tag |
| Human chooser usefulness | Open. Ten-card exercise unscored. [Results go here](acceptance-0.19.md#ten-card-results) | A real participant |
| 0.18 upgrade | [Rehearsed and applied](audits/upgrade-0.18-to-0.19.md) on three CLIs on one Mac. All 12 enabled CLI pack trees match the safety-fix manifest. One Claude account lists 73 current account skills and 69 enabled legacy entries. Other account installs still need readback | Not a tag gate |
| Install lifecycle | Passed on the frozen candidate, then [rerun](audits/lifecycle-0.19.0.md) on the safety fix candidate. [All four packs](audits/lifecycle-0.19.0.md) passed install, upgrade, downgrade, uninstall, and reinstall on Claude Code, Codex, and Antigravity CLIs, in throwaway configurations. This covers packaging only. No fresh task ran | Closed for these three CLIs |
| Claude Code acceptance | Open. The packet is bound to `3df7e438` and its receipt records 51 passing static checks. The prepared packet has no run or authorization. Native permission enforcement, loading both packs together, and task behavior still need observation | A separately decided task |
| Codex and Antigravity | Open. No new evidence. Unclaimed for 0.19.0 | The maintainer, after their controls are verified |
| Gemini IDE packet | Open. Prepared and unrun. The exact host and model are unverified. Unclaimed for 0.19.0 | The maintainer, by separate authorization |
| Apps and second Mac | Unclaimed for 0.19.0. [OpenAI documents a skills upload path](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) for eligible ChatGPT workspaces. Account availability and install results need their own readback | The maintainer, on each intended surface |
| Dotfiles companion | Not a tag gate. PR 39 is still a draft at `bdc3c901df08b442ed39d9c18e60abaf424526b0`, and no release rule depends on it | The maintainer |
| Skill security review | Closed for this candidate. Five warnings fixed in skill text, no errors. Static review only | Not applicable |
| Candidate freeze | The safety fixes ended the freeze at `63156e05`. The replacement freeze took effect when PR #97 merged. The artifact freeze is `3df7e438`; the reviewed repin moves manifest source to `109942aa43ccae0aac505f8413789aae41fdb097`. PR #98 includes a reviewed repin of the two allowed catalog files. Plugin, ZIP, and discovery hashes retain the safety-fix freeze. See the [freeze rules](audits/release-decision-0.19.0.md#freeze) | The maintainer |
| Native eval suite | Exploratory, not a gate. One `routing-specialist` pass ran on the imperative wording. The other four arms are unrun, and each needs the maintainer's yes | Not applicable |
| Public launch framing | Decided on November 5. Lead with copied requests and present skills as an optional preview. The website was updated through Studio PR 143. The launch posts are drafted and not posted | Closed by the maintainer |
| Public chooser | Open. This is a website gate, not a tag gate. Studio PR 143 merged on November 5 at `44fe7e6f121765b1290b8ef895c71525b8ebab5a`, and the live site pins `1ba9787815733643e440c38ad6d6270b983edd60`. Comprehension with a real participant is unscored | The maintainer, through website approval |
| Release | Open. No tag or published Release | The maintainer's separate decision |

Do not describe this work as a stable release or a benchmark result. Supported
public wording: the copied requests are usable today without installing anything,
and skills are an optional preview with published limits.

## Historical November 4 checkpoint after PR 86

Reviewed main at `ddd8c05890dd4d9fae18bbd98001faf1bef136dd` after the November 4,
2026 merge of [PR #86](https://github.com/JovaniPink/measured-skills/pull/86).
[Validation on merged main](https://github.com/JovaniPink/measured-skills/actions/runs/41936984685)
passed all 343 regression tests. The 0.19.0 preview has 90 skills in four packs,
with 73 implicit and 17 explicit-only skills.

| Record | Revision |
| --- | --- |
| Reviewed main | `ddd8c05890dd4d9fae18bbd98001faf1bef136dd` |
| Chooser input in [the export](../dist/discovery/catalog.json) | `c494143eb210ee1692fbff7f30813e36a7db9e5a` |
| Artifact source in [the manifest](../releases/0.19.0/manifest.json) | `bfeab70ebfbfd2c147fd6d98f21b5164bc3fda16` |
| Manifest binding commit | `691d498211427aadd0dbfe82e9255476f9e8729a` |

PR #86 added a read-only scope review that explains the requested comparison
before assessing whether changes fit the approved work. The two-Mac runbook
companion (#41) merged with separate pins for the generated chooser and the
review contract. The companion comparison study is prepared. Execution requires
its separate authorization. See the [scope review record](audits/review-scope-2026-11-04.md).

| Gate | Evidence and next action |
| --- | --- |
| Human chooser usefulness | The ten-card exercise is unscored. Start with the [five-minute participant sheet](acceptance-0.19-participant.md) on the pinned chooser. Record actual choices, time, help, and prior exposure under the [existing protocol](acceptance-0.19.md). |
| Claude Code | The November 2 task stopped when a required reference was blocked. Rebuild and hash the candidate packet, verify reference access and current controls, and record the separate execution decision. See the [stopped attempt and corrected preparation](audits/client-preflight-2026-11-02.md). |
| Other clients and machines | Codex paid-fallback control and Antigravity isolation still need evidence. Verify the applicable lifecycle and behavioral checks for each intended client, app, and machine. See [client acceptance](client-candidate-v0.19.0.md). |
| Online sources | The [November 2 closeout](audits/source-check-closeout-2026-11-02.json) matched 69 of 69 sources. Repeat the online check on the frozen release candidate and review any drift individually. |
| Public chooser | The website pins its own export. Compare its deployed revision with the qualified artifact before updating the public entry point. |
| Release | GitHub lists `v0.16.0` as the only tag and has no published Releases at this checkpoint. Complete the [staged release process](release-process.md) and obtain the separate release decision for the exact qualified revision. |

## Historical November 2 checkpoint after the priority merge train

Audited main: `a7eee41817625efbd8527db17ed562edddd9f441`.
PR #83 is merged at `bcf157aa8d2f0c2b0874f5e6c643bfdf9fa995c9`;
maintenance #76 and #74 are merged with their reviewed heads preserved.
[Current-main validation](https://github.com/JovaniPink/measured-skills/actions/runs/41532669339)
passes, including 323 regression tests. This is repository evidence, not a
release or receiving-client acceptance. The catalog remains 90 skills in four
packs: 73 implicit and 17 explicit-only.

The [current qualification audit](audits/release-qualification-2026-11-02.md)
records exact source identities, source holds and the next preparation. The
historical sections below retain their original observations. Their old draft,
account and publication states are not current-state instructions.

| Boundary | Current result and next action |
| --- | --- |
| Source freshness | The November 2 read-only check found 42 matching and 27 changed. All 27 were then reviewed individually in the [source-review ledger](audits/source-review-2026-11-02.json): 25 were repinned after unchanged marker methods read identically on every observation, and the two ai.google.dev pages were rebound to their official Markdown representation because the HTML address now redirects to a script shell with a varying fallback fingerprint. No canonical instruction defect was found. The [final online receipt](audits/source-check-final-2026-11-02.json) shows 69 of 69 matching. A [fresh owner review](audits/source-review-followup-2026-11-02.md) confirms all 27 decisions, narrows unsupported wording, and repairs manifest delivery without rewriting history. A later delivery check found two new hosting-only changes. Both were reviewed and repinned in the [addendum](audits/source-review-addendum-2026-11-02.json); see its [closeout receipt](audits/source-check-closeout-2026-11-02.json) for the latest result. The checker, age policy and review date are unchanged; the original [raw receipt](audits/upstream-freshness-release-2026-11-02.json) and [hold queue](audits/release-qualification-2026-11-02.json) are retained. This is a dated checkpoint, not a permanent pass: repeat it on the frozen candidate. |
| Human usefulness | The original ten-card exercise is still unscored. Use the [participant sheet](acceptance-0.19-participant.md), with a separate coached practice and two-card next block. Keep prior exposure and help visible; do not turn repeated or coached choices into new uncoached results. Targets remain unchanged. |
| Claude revised-source behavior | The November 2 task stopped on blocked reference access; no edit or continuation occurred. The corrected preparation's 52 recorded files are unchanged. Its 31 staged skill/reference/license files matched the generated files before the [chooser usability change](audits/chooser-usability-2026-11-02.md); that change regenerates one staged reference, so the staged plugin must be rebuilt, re-hashed and rechecked before any task. Native CLI is now 2.1.316; only version/help/authentication class were rechecked. A new task still needs explicit authorization, fresh same-account billing controls and effective isolation/read-access verification. |
| Other clients | Codex CLI 0.161.0 and Antigravity CLI 1.4.7 were observed through native metadata only. Codex no-paid-fallback and Antigravity effective isolation remain unverified. The separate Gemini IDE preparation is not a CLI result or an execution allowance. |
| Installation and supported claims | No current-source install/upgrade/downgrade/uninstall/reinstall or full behavioral acceptance was added. Each claimed CLI, app, web surface and second Mac needs its own applicable evidence. This audit narrows no support requirement and grants no waiver. |
| Chooser usability | The chooser requests now ask only for fields a person can fill, name their standing limits once, and carry structured action facts. The [change record](audits/chooser-usability-2026-11-02.md) lists what changed, what did not, and the effect on the prepared Claude packet. It is a design repair, not a usability result: the ten-card exercise is still unscored. |
| Public discovery | Studio #140/#141/#142, personal #162/#164/#165, and profile #13 are merged and published. November 2 readbacks verify Studio `a78390af`, personal `6d60fdef` and profile `f1f1c709`. The chooser and articles are available; publication does not score human usefulness or qualify a client. |
| Dotfiles companion | #35/#37 remain merged. #39 is still a separate draft at `bdc3c901df08b442ed39d9c18e60abaf424526b0`, with a failed hosted status. It was not rerun here. Neither a companion PR nor its local checks establish installed-machine behavior. |
| Formal release | Fresh GitHub readback: no releases; the returned tag list contains only v0.16.0. The 0.18 and 0.19 source records remain distinct. No release, tag or installation is authorized by this audit. |

Generated artifacts are unchanged since artifact source
`474c0bd5bd9084a5dcb938ef98d82181c64469a2`; discovery input is
`cfc952d0735e6e87d5403e2434b776dd65916b74`. Both are ancestors of audited main.
Do not replace either with a merge SHA. The source-review manifest first bound
`173fe8aace86580654d6eb6b286ce13d9c050165`, with only the pins and reviews
hashes changed. Its commit also edited documentation. The follow-up restores the
required clean-source, manifest-only delivery sequence with ordinary commits.
Read the current binding from [the manifest](../releases/0.19.0/manifest.json);
the prior commits remain ancestors. The follow-up changes only two later pins
and the manifest source binding; generated package and discovery hashes remain unchanged.
The retained narrow task deliberately uses older frozen evidence; it does not
silently make that evidence current.

Next: record actual human choices, and obtain the
separate decision for a corrected bounded client task only after its controls
pass. Freeze the final candidate, repeat the online source check on it, and complete
the applicable release checks. Preserve the Gemini 3.8 Flash packet. A newer latest-model page does not prove its model unavailable on the selected IDE; verify that exact host and model before any separately authorized run, without automatic substitution. No paid run, billing change or release occurred.

## Historical November 2 checkpoint before PR 83 merged

Remote main is `3bbc88ce08bb5d686338f9185a742b752a31507f`: [PR 82](https://github.com/JovaniPink/measured-skills/pull/82)
merged October 30 with both parents preserved. Its reviewed head
`1e8bf7923189986c445a283bd06aa727d7c55a8d` passed all 320 tests in hosted CI;
[merged-main validation](https://github.com/JovaniPink/measured-skills/actions/runs/41066698814)
also passed. These results do not qualify receiving-client behavior.

November 2 work adds two pending operational routes over existing skills and
clarifies [current checkout selection](start.md#check-which-source-you-opened).
Its source, validation and review status belong to [draft PR 83](https://github.com/JovaniPink/measured-skills/pull/83), not PR 82. Reviewed head `d85c7b59` passed all 320 local tests and [exact-head CI](https://github.com/JovaniPink/measured-skills/actions/runs/41472637584); the later preflight documentation has its own checks.
The merged catalog still has 90 skills in four packs, with 17 explicit-only skills.

| Remaining boundary | Current evidence and next action |
| --- | --- |
| Human usefulness | Ten-card exercise remains unscored; record actual route choice, expected output, scope, time and requests for help. Do not infer user success from search tests. |
| Claude revised-source behavior | [November 2](audits/client-preflight-2026-11-02.md): matching account controls observed off; one authorized Haiku task stopped on blocked reference access, no edits or continuation. Corrected preparation passes static checks but needs a new execution decision, fresh controls and runtime verification. Original results remain unchanged. |
| Gemini 3.8 Flash behavioral evaluation | Bounded trial protocol recorded in [preparation](audits/gemini-flash-trial-preparation-2026-11-02.md); execution remains unrun and requires separate authorization and quota checks. |
| Other clients and machines | Codex no-paid-fallback and Antigravity isolation remain unresolved in retained evidence. Other surfaces and the second Mac need their own observations. |
| Sources | [November 2 online check](audits/upstream-freshness-2026-11-02.json): 43 matching, 26 changed, none unavailable. Individually review all changes before justified pin updates. No pin or freshness policy changed; the October 29 pass remains a dated snapshot. |
| Dotfiles companion | PR 39 remains an open draft at `bdc3c901df08b442ed39d9c18e60abaf424526b0`. Its retained hosted job did not start because of a payment/spending-limit issue; local checks do not clear that gate. |
| Formal release | November 2 readback found no GitHub releases; the returned tags contain only v0.16.0. No 0.18 or 0.19 release or installation follows from merged source. |

The accepted originality packet, source pins, original trial outputs, and retest
remain intact. The new technical delta is not another maintainer acceptance.
The dated records below preserve earlier evidence and their original limitations.

## Historical October 29 checkpoint

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

## Historical October 29 remaining gates and next work

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

## Historical October 29 merge checkpoint and next sequence

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
