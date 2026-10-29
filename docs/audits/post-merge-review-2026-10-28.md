# Post-merge Skills review

Reviewed source: `b4200af067fe696d5e9e41bc3413cf4938d18c64` (merged main).
Initial method: owner self-review, source and control-flow tracing, read-only metadata
inventory, and GitHub state readback. No independent reviewer, model trial,
installation, test rerun, generator, dependency audit, or client-control change.
This is not comprehensive validation of every skill's engineering guidance.

## Findings and dispositions

1. **Warning, new: current release status still described merged work as unmerged.**
   `docs/release-readiness-2026-10-26.md` called #72 unmerged after its October 28
   merge. The 0.18 candidate header and 0.19 preview did not explain which checkout
   now owned current generation. Corrected the status, added exact candidate,
   manifest and merge identities, and linked one cross-version release ledger.
   The feature and finish-work guides also labeled the October 20 record as
   current readiness; they now link to the cross-version status. Preserved older
   source/client receipts and the original acceptance packet.
   The shared client guide still presented 88/88/71 as its current counts. It
   now states 90/90/73 for the 0.19 preview and links preserved 0.18 separately.
   Daily guidance now distinguishes the closed 0.18 diagnostic from earlier
   failures and unobserved 0.19 behavior.
2. **Note, new: missing-entry fallback needed a user-side step.**
   Current prompts start with 0.19 native entries and include ordinary-wording
   fallback instructions. An older installation may not recognize that entry;
   fallback prose is not a mechanism for resolving a missing native command.
   Updated the start and client guides to check the installed entry and remove
   an unavailable prefix before sending the ordinary request. No universal claim
   about unknown-command handling in every client version is made.
3. **Note, updated: generic copied prompts must retain current constraints.**
   Local-repair prompts normally request checks. Added a concrete source-review-only
   substitution for a user who has prohibited test reruns. This clarifies use of
   the existing prompts; it does not weaken normal repository gates or change
   canonical workflow permissions.

## End-to-end source trace

| Boundary | Inspected owner | Result and limit |
| --- | --- | --- |
| Task selection | `catalog/workflows.json`, `scripts/discovery-ui.js` | Fifteen routes; search uses route phrases and canonical/historical names. This describes the search code, not human selection success |
| Action and client | `scripts/discovery.py:action_guidance`, UI mode rendering | Assessment uses `plan-change`; repair uses `execute-plan`; maintenance uses `publish-change`. Each action renders the selected client's guidance. The earlier route-only availability defect is already repaired |
| Core selection | `catalog/profiles.json` | Nine-skill core excludes execution and publication. Existing daily and finish-work selections have mapped IDs. Older experimental profiles are not all implicit staging selections |
| Prompt authority | Registry client variants and finish-work guide | Assessment prohibits edits; repair stops locally; maintenance permits scoped normal pushes and existing-finding replies, with three rounds and 30 cumulative waiting minutes. Antigravity uses ordinary requests for excluded orchestration. No prompt here establishes actual loading |
| Metadata and taxonomy | All 90 catalog rows and frontmatter identities | No discrepancy in ID, pack, invocation or risk class in the inventory. Four packs contain 32/27/20/11 skills. All 90 maturity values remain candidate; observed use, repeatable acceptance and benefit are separately defined |
| Native controls | Generated skill inventory and generation control flow | Codex and Claude each contain 90 entries; 17 Codex false implicit-invocation controls and 17 Claude user-only controls are present. Antigravity has 73 entries and none of the 17 explicit IDs. Presence is not receiving-client enforcement |
| Migration | `catalog/migrations/0.18-to-0.19.json`, `scripts/discovery.py:migration_errors` | Maps 88 preserved skills plus two additions; rejects duplicate mappings, lost inventory, changed authority and installed aliases. Historical migration body comparisons remain anchored to the naming checkpoint, with later canonical deltas separate |
| Selected exports | `scripts/export_selected.py`, `scripts/build_antigravity.py`, `scripts/project_skills.py` | Current exporters provide replacement messages for old IDs and retain explicit-only restrictions. Selected staging checks destination and references before copying. Old receipts must be checked against their recorded source, not today's names |
| Generated boundaries | `scripts/build_distributions.py`, `scripts/discovery.py` | Codex adapts the prompt namespace; Claude excludes Codex agent metadata and adds explicit control; Antigravity receives only implicit skills. Discovery binds exact input hashes. Generators and validators were read, not executed |
| Completion evidence | `docs/taxonomy.md`, acceptance and release records | Earlier maturity contradiction is already repaired. Human chooser and 0.19 client behavior remain unobserved; merge and old CI do not close those gates |

The prompt review covered all route scopes and their native/ordinary invocation
construction, with detailed attention to finish-work, publication, prompt review,
reconciliation, refactoring, upgrades, query plans and replay. Query inspection
does not authorize EXPLAIN ANALYZE, provider reads or backfills. Reviewing a prompt
does not execute the quoted task. Self-review is not independent review.

No additional actionable code defect survived the initial bounded source inspection.
That is not a guarantee about runtime behavior, browser usability, every export
failure path, or all engineering advice in the catalog. Existing regression test
sources were read for coverage; none was executed. No new prose-mirroring tests
were added. Canonical skills, catalog selections, generators, exports, archives,
source pins and manifests were outside that initial documentation change.

## Follow-up source trace and repairs

The existing draft at `ee71f2f5253d9007e6f63bf6f894fcc804e7964f` received a
successful automatic hosted validation. That result was read, not rerun.
Further review of the selector's actual data path found a warning missed by
the initial inventory review: search considered primary and optional skills,
but not action-specific entries. `execute-plan`, or its historical name
`plan-execution`, could fail to return Finish existing work, Upgrade a dependency,
and Refactor, even though each route has an execution action. Search now uses
a generated union of primary, optional and action entries; the same alias
matching feeds that index. This changes route lookup, not skill selection policy.

The missing-entry clarification now also reaches the actual copy control. The
chooser defaults to an ordinary request, with a separate native-command option
for verified installed Codex or Claude entries. Antigravity and web-account
requests remain ordinary. Text-only and no-JavaScript guides include the same
fallback. Only a leading recognized native selector is removed; quoted commands,
scope and permissions are preserved. Client changes clear stale copy-success
messages. These are prepared behavior changes, not observed browser or human
acceptance results.

Focused regression definitions cover action-entry lookup through a historical
name and preservation of task authority while removing a leading native token.
They were not executed locally under the user's no-test-rerun instruction.
No validator was weakened or changed. Generation carries the new data and controls
into the offline guide, bundled index, projections and affected archive. The
input checkpoint is `82115567df98d85fbc70a2e26b82c8adb5b48fa1`. The 0.19
manifest is rebound in its separate commit; the
preserved 0.18 manifest remains untouched. No model call, installation or release
is part of this repair.

## Human acceptance and follow-through

The original [ten-card exercise](../acceptance-0.19.md) remains prepared, not run.
A request to finish the package does not supply participant selections. Do not
invent times, wrong selections, copied prompts or successful rediscovery. Preserve
all outcomes when the participant actually responds; use the original thresholds,
not a smaller replacement exercise. Later real-work trials retain their separate
authorization and billing/isolation prerequisites.

See [release status](../release-status.md) for actual completed boundaries and
next actions. The [post-acceptance delta](post-acceptance-delta-2026-10-20.json)
records this owned documentation revision without extending originality acceptance.

## Second follow-up: bookmarks and asynchronous copy results

A fresh source review at `5b787a4` found two further user-path defects. The
offline enhancement replaced plain-HTML task anchors with `choice-` anchors and
hid the original targets. A bookmark such as `#finish-work` could therefore land
on hidden content. The enhancement now moves the original IDs into the visible
route, retains earlier `choice-` links, and restores a known task on initial load
or hash navigation. Only known route IDs affect navigation; private search text
is not written to the URL or storage.

Clipboard completion was also asynchronous without an identity guard. A request
could complete after changing the displayed client, stack, search or request
style, overwriting the cleared status with a success for the previous prompt.
The offline UI now scopes completion to its rendered view and latest copy attempt.
The website uses an invalidated copy-attempt identity for the same boundary.
Stale failures cannot move focus back to an obsolete prompt either. Copying still
does not execute a task or establish skill loading.

The source review traced current caller and event paths. Browser regression
cases are prepared in the website draft; no local test suite or model evaluation
was run. Generation updates only the derived discovery artifacts and their exact
source binding. Human rediscovery and receiving-client acceptance remain pending.
