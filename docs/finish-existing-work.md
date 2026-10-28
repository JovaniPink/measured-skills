# Finish existing work

**0.19 preview:** [Find your next workflow](start.md). Start with finishing existing work; commands and package identities differ from 0.18. No new client acceptance is implied.


Start here when a change is half finished, a test is failing, reviewers found a
problem, or a user journey still breaks. Recover what is true now, complete the
next useful repair, and show what remains. For a new idea, use the
[feature-development workflow](feature-development-workflow.md).

**Recover -> Define what remains -> Diagnose or plan -> Repair and test -> Review -> Verify completion -> Hand off**

These are prepared workflows, not observed client results. The catalog remains
a 0.19.0 preview. See the [coverage assessment and twelve worked cases](audits/finish-work-coverage-2026-10-26.md)
and [current release limits](release-status.md).

The prompts use 0.19 names. Check [the installed-entry guidance](start.md#use-the-guide-with-the-skills-you-actually-have)
before sending a native command, and preserve current constraints when adapting
a request. Missing skills do not authorize installation or new external actions.

## Choose the next useful step

| Situation | Start with | Result needed before moving on |
| --- | --- | --- |
| You lost the thread | Current repository state and saved plan | Separate completed, unfinished, uncertain, and unrelated work |
| You cannot explain a failure | `diagnose-failure` | Reproduction, likely cause, and evidence that distinguishes alternatives |
| Someone requested changes | `address-review` | Accept, reject, defer, clarify, or already addressed, with current evidence |
| The repair is understood | `plan-change` only if needed | A small, authorized repair with acceptance conditions and relevant checks |
| You are unsure what to ask | `review-engineering-prompt` | A sufficient request or a useful revision; no execution of the quoted task |
| You think it is finished | `verify-claims` | Every acceptance condition matched to current evidence or an explicit gap |

Acceptance conditions are observable facts that show the work meets the need.
A regression is previously working behavior that breaks. CI means the automated
checks run by the repository host. None of these terms means human approval.

## Recover and finish

1. Read repository instructions. Confirm the checkout, branch, current commit,
   comparison revision, relevant draft PR, dirty files, and saved plan. Preserve
   unrelated work and existing authorization. A previous summary helps locate
   evidence; it does not prove current completion or grant permissions.
2. List only the remaining acceptance conditions. Compare the plan with actual
   code and findings. Preserve omitted requirements; do not call them complete
   because another check passed. Reframe only if the intended behavior is unclear.
3. Choose diagnosis, review response, or implementation. Do not restart planning
   for an already clear repair. For larger work, choose a self-contained slice
   with meaningful behavior, tests, and documentation.
4. Repair within the authorized scope. For a reproducible defect, first add a
   failing regression test when feasible. Run affected checks during the work.
   Do not impose test-first ceremony on every prose or configuration edit.
5. Follow the relevant stack route below. Discover commands from the repository
   and installed versions. Record failed, unavailable, and unrun checks as such.
6. Review the exact diff using `review-code-change`. This review returns findings
   without editing. Evaluate confirmed findings, authorize a repair if necessary,
   rerun affected checks, and review the revised change. Self-review is useful but
   does not establish independent human approval.
7. Use `verify-claims` to reconcile the final acceptance conditions with
   current evidence. Record remaining blockers. Commit, push, or update a draft
   only within the user's authorization. Merge, deployment, and release are
   separate actions. If interrupted, leave a continuation record.

A blocked requirement is unfinished. If part of the work can continue safely,
complete that part and preserve the blocker. Ask about a material scope or product
decision; do not manufacture another approval checkpoint for already authorized work.

## Four routes through the same process

### Backend and API

Use the Python or TypeScript/JavaScript profile after discovering the actual
framework and versions. Trace callers through validation, authorization, service
logic, and persistence. Check status/error contracts, retries, concurrent requests,
and rollback compatibility. Add interface, API compatibility, security, migration,
or plan-tests review only where the change needs it.

A fictional retrying task API is complete when the intended effect occurs once
under the supported retry contract, errors remain useful to callers, and tests
cover the affected boundaries. A successful response alone does not prove the
write occurred. An interrupted response does not prove it failed. Use isolated
fixtures for external dependencies; live access needs its own authority.

### Full-stack user journey

Trace the user's action from the UI through the API and storage, then back to the
visible result. Check loading, error, empty, unauthorized, stale, and recovery
states where relevant. Use existing Next.js/cache-auth, accessibility, and test
skills if that stack is present. Do not assume every TypeScript app is Next.js.

For a fictional task status filter, verify both the saved status and what the user
sees after refresh, navigation, or retry. Component tests, an HTTP success, and a
browser journey answer different questions. Name which layers were observed and
which were substituted by fixtures.

### SQL and GCP pipelines

Use the PostgreSQL or GCP profile appropriate to the discovered system. Establish
grain, keys, source authority, event time, correction arrival, update strategy,
and replay semantics before choosing a query window or deduplication rule.
Trace schema changes, partial writes, retries, and reconciliation to the sink.

For a fictional status-event pipeline, a correction arriving today can concern an
old event. Do not invent an event-age limit to improve pruning. Local fixtures
can check a proposed transformation; they do not prove production completeness,
cost, capacity, or recovery. Queries, cloud dry runs, jobs, IAM changes, backfills,
and deployment require their own authorization. Use version-matched dbt,
Dataform, Beam/Dataflow, Spark/Dataproc, or Airflow/Composer guidance only as needed.
The [data-pack proposal](data-workflow-pack-proposal.md) remains a proposal.

### Swift application

Use the Swift/SwiftUI profile and existing concurrency/persistence reviews. Trace
state ownership, stable identity, task lifetime, cancellation, and persistence
across navigation and app lifecycle. Check accessibility and supported platform
conditions. Discover the project's Xcode, SDK, package, simulator, and device lanes.

For a fictional task list, a canceled request must not overwrite the currently
selected task. A persisted task must keep the identity the navigation depends on.
Unit tests do not establish a completed simulator or device journey. If a device
is unavailable, preserve that gap instead of calling the whole feature accepted.

## Available skills and client selection

The `finish-existing-work-experimental` profile contains nine core skills and five
stack profiles. It is an optional staged selection, not an installation command.
The existing daily twelve remain unchanged. See [profile definitions](../catalog/profiles.json).
Neither profile includes the entire lifecycle or every conditional specialist.

- Execution: `execute-plan` in `measured-workflows`.
- Handoff: `handoff-work` in `measured-workflows`.
- Publication: `publish-change` in `measured-workflows`.
- Conditional Swift delivery/journey and Next.js delivery workflows are in `measured-stacks`.

Check installed names and sources before selecting them. Codex examples below use
normal pack selectors; choose the matching installed entry. Claude uses one
leading command. Local staging wrappers can have different namespaces. Supporting
skills requested in prose need their own loading evidence. If missing, report that
fact and use ordinary authorized assistance without claiming the skill ran. Do not
install another pack or remove duplicates simply to satisfy a prompt.

Antigravity's 17 explicit-only exclusions remain. Its implementation and publication
requests below are ordinary user instructions; they do not invoke or reproduce an
excluded skill. Use actual commands shown by the installed client for eligible
skills rather than inventing a portable slash spelling.

## Full finish-work prompts

Replace `[REPOSITORY]`, `[CHANGE]`, `[PLAN_FILE_OR_APPROVED_TEXT]`, and
`[BASE_REVISION]`. A missing plan can be recovered from supplied approved text or
current requirements; do not invent a previous decision. Paste into chat, not a shell.
These requests authorize scoped repair and local checks, stopping before publication.

### Codex

```text
$measured-workflows:plan-change In [REPOSITORY], finish [CHANGE]
using [PLAN_FILE_OR_APPROVED_TEXT]. Read instructions, inspect the branch and dirty
files, and resolve [BASE_REVISION]. Reconcile completed, unfinished, uncertain,
and unrelated work with current evidence. Preserve existing authorization and
unrelated changes. Diagnose unexplained failures and assess review feedback before
editing. Plan only what remains, then implement the understood repairs and run
relevant local checks. Use the applicable stack profile when available. Review the
exact diff in a findings-only pass, repair confirmed findings within scope, rerun
affected checks, and verify every acceptance condition. Keep unavailable checks
and blockers explicit. Leave concise evidence and continuation notes; do not
commit, push, deploy, merge, or release.
```

The leading skill supplies planning. The user's remaining text authorizes ordinary
implementation; planning itself does not authorize editing. If the client is in
read-only planning mode, first switch modes through its supported controls.

### Claude Code

```text
/measured-workflows:plan-change In [REPOSITORY], finish [CHANGE]
using [PLAN_FILE_OR_APPROVED_TEXT]. Read instructions and inspect the current branch,
dirty files, and [BASE_REVISION]. Reconcile the plan with current evidence and
preserve unrelated work and existing authorization. Diagnose unexplained failures,
assess review findings, and plan only the remaining repairs. Then implement those
repairs and run the relevant local checks using the applicable stack guidance.
Review the exact diff without edits during that pass; repair confirmed findings
within scope, rerun affected checks, and verify the acceptance conditions. Return
concise evidence, unresolved blockers, and continuation notes. Do not commit, push,
deploy, merge, or release. Report missing skills instead of claiming they loaded.
```

### Antigravity

```text
In [REPOSITORY], finish [CHANGE] from [PLAN_FILE_OR_APPROVED_TEXT] against
[BASE_REVISION]. Inspect repository instructions and current branch, files, and
plan first. Preserve unrelated work and existing authorization. Use available
plan-change, diagnose-failure, address-review, and the
relevant engineering profile as needed. Plan only what remains; I authorize the
scoped repairs and local checks. Review the resulting diff in a findings-only pass,
repair confirmed findings within scope, rerun affected checks, and verify each
acceptance condition. Keep missing evidence and unavailable checks explicit.
Leave continuation notes. Do not load excluded explicit-only workflows, change
installations, commit, push, deploy, merge, or release.
```

## Three-request fast path

Use one request at a time. Select the matching installed entry; replace the first
line using this table. The shared text below each line is the request body.

| Request | Codex first line | Claude Code first line | Antigravity first line |
| --- | --- | --- | --- |
| Assess and plan | `$measured-workflows:plan-change` | `/measured-workflows:plan-change` | `Use the available plan-change skill for this assessment.` |
| Repair and verify | Ordinary request below | Ordinary request below | Ordinary request below |
| Publish reviewed draft | `$measured-workflows:publish-change` if installed | `/measured-workflows:publish-change` if installed | Ordinary request below; do not load an excluded publication workflow |

**1. Assess and plan**

```text
In [REPOSITORY], inspect [CHANGE] and [PLAN_FILE_OR_APPROVED_TEXT] against
[BASE_REVISION]. Preserve unrelated work. Reconcile current evidence, remaining
acceptance conditions, review findings, and blockers. Plan the smallest complete
repairs with relevant checks. Save the plan using project conventions, or return
its exact text if writing is unavailable. Do not implement or publish yet.
```

**2. Repair and verify**

```text
Implement the identified repairs in [PLAN_FILE_OR_APPROVED_TEXT] in [REPOSITORY].
I authorize scoped edits and relevant local checks. Preserve unrelated work and
existing constraints. Use diagnosis and review-response guidance where needed.
Review the exact diff without editing during review; repair confirmed findings,
rerun affected checks, then verify all acceptance conditions. Report current
revision and uncommitted state, evidence, and unfinished work. Do not commit,
push, deploy, merge, or release. Do not claim an unavailable skill was loaded.
```

**3. Publish the reviewed draft**

```text
In [REPOSITORY], verify the reviewed changes and their evidence still match the
current tree. I authorize committing those changes, pushing normally to
[DESTINATION: exact remote repository and PR base branch], and creating or updating
[PR_TARGET: exact draft URL or new draft PR]. Preserve unrelated work and source
history. Stop if the destination or target is ambiguous. Inspect CI for the exact
pushed head and report failures or unavailable checks. Keep the PR draft. Do not
merge, deploy, tag, publish a package, or release.
```

## Short requests for specific problems

Use the named skill from the client's actual installed selector when available.

**Diagnose (`diagnose-failure`):** "Investigate [FAILURE] in [REPOSITORY].
Reproduce safely using existing local fixtures, distinguish hypotheses with
evidence, and propose the smallest repair. Do not edit or call providers yet."

**Review response (`address-review`):** "Assess [FINDINGS] against the
current [CHANGE] in [REPOSITORY]. Explain which are supported, already addressed,
or need clarification. Repair supported findings within the approved scope, run
affected checks, and review the revised diff. Do not post replies or push."

**Journey verification (`verify-claims` plus the relevant profile):**
"Check whether [JOURNEY] meets [ACCEPTANCE_CONDITIONS] at the current revision.
Use available authorized local checks; distinguish fixture, integration, browser,
simulator, device, and live evidence. Do not change code or use provider accounts.
Report incomplete and unavailable conditions without inventing failures."

**Prompt review (`review-engineering-prompt`):** "Check the following engineering
request for outcome, context, scope, permissions, and completion evidence. Give a
short assessment and a useful revision only if needed. Do not execute its task:
[QUOTED_REQUEST]."

**Resume:** "Resume [CHANGE] in [REPOSITORY] using [CONTINUATION_RECORD] and
[PLAN_FILE_OR_APPROVED_TEXT]. Check the current revision, dirty files, instructions,
and existing authorization against those records. Preserve unfinished and unrelated
work. Continue the next authorized step; ask only if a material decision is missing.
Do not treat a handoff or an old green check as new authority or current proof."

## Finish and maintain a draft PR

Use this route when you want the assistant to keep working after the first push.
It is active-session maintenance, not a background service. The default is three
review rounds and 30 cumulative minutes waiting for CI and reviews. These are
chosen limits, not measured optimal values or a total implementation deadline.

1. Recover the repository, receiving account, PR URL, branch, exact base/head,
   dirty files, plan, acceptance conditions, and existing authority. Preserve
   unrelated work. A committed diff misses staged, unstaged, and untracked changes;
   bind relevant uncommitted contents by path and SHA-256, including deletion/mode
   records where applicable. Label index (staged), working-tree, and untracked
   representations; one path can need two hashes. Review the intended staged tree
   and reconcile the resulting commit before push. Do not collect unrelated files
   or private logs. Bind the PR's head repository as well as its branch; for a fork,
   this differs from the base repository. Require open/draft state before writes,
   stopping on closure, merge, state change, or a changed destination.
2. Identify the remaining gates: behavior, local checks, hosted checks, current
   findings, required approvals, and required conversations. Read all relevant
   pages. Missing pages or inaccessible rules mean incomplete knowledge.
3. Repair within scope, run affected checks, and review without editing during the
   review pass. Start with the full identified change; subsequent rounds cover the
   delta, open findings, and affected callers/contracts. The owner handles repairs.
   Keep a finding ledger with evidence and dispositions; new evidence can reopen
   a previously rejected claim. Do not dismiss documentation defects as mere nits.
4. Commit only scoped reviewed work, push normally, verify remote readback, and
   update the existing draft. Discover history rules first. This catalog preserves
   release source anchors through merge-based integration; rebase, squash, reset,
   and force-push are not acceptable shortcuts. Never overwrite concurrent work.
5. Inspect CI for the pushed revision and assess new feedback. Recheck the remote
   head before replies and handoff. A changed head or relevant base requires
   evidence reconciliation. Repair valid in-scope findings, rerun affected checks,
   and review within the remaining allowance. Stop a review cycle early when no
   actionable findings remain; this does not clear other gates.
6. Reply only when the task explicitly permits technical replies on this PR.
   Check prior replies, respond to the existing finding with evidence, and read
   back the write. An uncertain send requires readback before retry. Do not resolve
   threads, dismiss reviews, request reviewers, approve, or enable auto-merge.
7. Stop at the authorized boundary or a real blocker/budget limit. Preserve a
   continuation record rather than silently abandoning remaining requirements.

Use supported bounded waits or backoff polling within the active session. Count
all waiting for CI/reviews toward 30 minutes; do not reset it after a push or
resume. Count all self-review and delegated attempts toward three rounds; failed
or unusable delegated attempts count. Record a round as started before self-review
or dispatch, then its outcome; retain a dispatch identifier where available.
An uncertain dispatch stays consumed and must be reconciled before replacement.
A final repair with no round left is still
unreviewed. An explicit extension is needed for more allowance. Stop the affected
lane on uncertain billing, missing authority, unexpected exposure, or unsafe
execution; complete independent permitted work. Do not retry billing-blocked jobs,
change billing, or create an automation to keep waiting.

For each check record its name, provider, result, link, and tested revision. A host
may report a PR-head, test-merge, or merge-queue check; verify its relationship to
the current head/base. Skipped or neutral status may satisfy a hosting rule while
no intended test ran. Report that distinction. Required human approvals and
unresolved conversations remain visible; green checks and mergeability are not
approval. A draft can be prepared for human review while merge requirements remain
pending. Name that boundary instead of claiming universal readiness.

Use proportionate verification. A unit test proves its covered behavior, not a
complete user journey. A prose-only change need not launch an app. Missing runtime
evidence does not authorize production access, provider jobs, uploads, or spending.

| Outcome | Report |
| --- | --- |
| Ready for the authorized handoff | Exact completed boundary and revision, its satisfied gates, and separate remaining approval/merge requirements |
| Blocked | Unmet requirement, evidence, and next permitted action |
| Budget exhausted | Used/remaining rounds and wait time, open findings, pending checks, and unreviewed repairs |
| Canceled | User redirection and safely preserved unfinished work |

### Maintenance prompts

These requests explicitly authorize scoped repairs, ordinary publication, and
technical replies to existing findings on one PR. They do not authorize thread
resolution or contacting reviewers. Replace every placeholder, including
[PLAN_FILE_OR_APPROVED_TEXT], [BASE_REVISION], and [PR_URL]. Stop if the named PR is
not the intended draft; do not change another PR's state. Exit a read-only planning
mode using supported controls before implementation.

Select the actual installed entry in Codex. Claude examples use one leading
command for portability: current documentation describes interactive stacking,
while headless/SDK handling differs. This is not installed-version acceptance.
Missing skills permit ordinary authorized help, not a claim that the skill loaded.
Antigravity requests do not load or reproduce excluded explicit-only workflows.

**Codex**

```text
$measured-workflows:publish-change
In [REPOSITORY], finish and maintain the existing draft [PR_URL] for
[PLAN_FILE_OR_APPROVED_TEXT] against [BASE_REVISION]. Inspect instructions, current
base/head, dirty files, identity, history rules, and existing authorization first.
Preserve unrelated work. I authorize scoped repairs, relevant local checks,
committing reviewed changes, normal pushes to this PR's verified head repository
and branch, updating its description, and technical replies to existing findings on this PR.
Keep review findings-only; the owner repairs accepted findings and reruns affected
checks. Use self-review by default, at most three review rounds total, and at most
30 cumulative minutes waiting for CI/reviews. Preserve used budgets across pushes
and resumes. Record rounds before starting them; retain uncertain attempts.
Inspect all relevant check/comment pages and exact tested revisions.
Verify the PR is still open and draft before each remote write; stop if its state
or destination changed. Match the push remote to its head repository, including
forks. Distinguish staged and working-tree bytes, review the intended staged tree,
and reconcile the resulting commit before push. Recheck remote head before writes
and handoff; reconcile concurrent changes rather than overwriting them.
Check prior replies and read back writes. Missing required local evidence blocks
publication unless I have separately authorized a draft documenting that gap.
Report actual skill loading, evidence, unfinished requirements, and budgets.
Keep the PR draft. Do not delegate unless separately authorized, resolve threads,
request reviewers, dismiss reviews, approve, change billing or installations,
rewrite history, merge, deploy, tag, publish a package, or release. Stop affected
unsafe or billing-blocked lanes; continue independent permitted work. Do not
create background monitoring. Save a continuation record at a blocker or limit.
```

**Claude Code**

```text
/measured-workflows:publish-change
In [REPOSITORY], finish and maintain the existing draft [PR_URL] for
[PLAN_FILE_OR_APPROVED_TEXT] against [BASE_REVISION]. Inspect instructions, current
base/head, dirty files, identity, history rules, and existing authorization first.
Preserve unrelated work. I authorize scoped repairs, relevant local checks,
committing reviewed changes, normal pushes to this PR's verified head repository
and branch, updating its description, and technical replies to existing findings on this PR.
Keep review findings-only; the owner repairs accepted findings and reruns affected
checks. Use self-review by default, at most three review rounds total, and at most
30 cumulative minutes waiting for CI/reviews. Preserve used budgets across pushes
and resumes. Record rounds before starting them; retain uncertain attempts.
Inspect all relevant check/comment pages and exact tested revisions.
Verify the PR is still open and draft before each remote write; stop if its state
or destination changed. Match the push remote to its head repository, including
forks. Distinguish staged and working-tree bytes, review the intended staged tree,
and reconcile the resulting commit before push. Recheck remote head before writes
and handoff; reconcile concurrent changes rather than overwriting them.
Check prior replies and read back writes. Missing required local evidence blocks
publication unless I have separately authorized a draft documenting that gap.
Report actual skill loading, evidence, unfinished requirements, and budgets.
Keep the PR draft. Do not delegate unless separately authorized, resolve threads,
request reviewers, dismiss reviews, approve, change billing or installations,
rewrite history, merge, deploy, tag, publish a package, or release. Stop affected
unsafe or billing-blocked lanes; continue independent permitted work. Do not
create background monitoring. Save a continuation record at a blocker or limit.
```

**Antigravity**

```text
Use ordinary authorized assistance and eligible installed skills only.
Do not load excluded explicit-only execution or publication workflows.
In [REPOSITORY], finish and maintain the existing draft [PR_URL] for
[PLAN_FILE_OR_APPROVED_TEXT] against [BASE_REVISION]. Inspect instructions, current
base/head, dirty files, identity, history rules, and existing authorization first.
Preserve unrelated work. I authorize scoped repairs, relevant local checks,
committing reviewed changes, normal pushes to this PR's verified head repository
and branch, updating its description, and technical replies to existing findings on this PR.
Keep review findings-only; the owner repairs accepted findings and reruns affected
checks. Use self-review by default, at most three review rounds total, and at most
30 cumulative minutes waiting for CI/reviews. Preserve used budgets across pushes
and resumes. Record rounds before starting them; retain uncertain attempts.
Inspect all relevant check/comment pages and exact tested revisions.
Verify the PR is still open and draft before each remote write; stop if its state
or destination changed. Match the push remote to its head repository, including
forks. Distinguish staged and working-tree bytes, review the intended staged tree,
and reconcile the resulting commit before push. Recheck remote head before writes
and handoff; reconcile concurrent changes rather than overwriting them.
Check prior replies and read back writes. Missing required local evidence blocks
publication unless I have separately authorized a draft documenting that gap.
Report actual skill loading, evidence, unfinished requirements, and budgets.
Keep the PR draft. Do not delegate unless separately authorized, resolve threads,
request reviewers, dismiss reviews, approve, change billing or installations,
rewrite history, merge, deploy, tag, publish a package, or release. Stop affected
unsafe or billing-blocked lanes; continue independent permitted work. Do not
create background monitoring. Save a continuation record at a blocker or limit.
```

### Optional independent-review add-on

Self-review remains the default. This separate request authorizes one reviewer
only if the actual route satisfies the stated prerequisites. It does not install
agents, grant tools, or authorize paid calls. The daily/finish profiles omit
explicit orchestration; its absence must not be bypassed. For Antigravity, use
ordinary host-supported delegation only when available and permitted, without
loading an excluded workflow. If no compliant route exists, retain the gap.

```text
For [PR_URL] in [REPOSITORY], I authorize one read-only reviewer at a time within
the existing three-round allowance, only after verifying host support, effective
permissions, model configuration, permitted data exposure, and no paid fallback.
Verify deadline and stop controls; if unavailable, do not launch. Bound runtime by
the remaining CI/review wait allowance. Record the attempt before dispatch and
retain its identifier. Charge elapsed time while the reviewer is pending, even
during owner work, counting overlapping CI/reviewer intervals once. On timeout,
user cancellation, or authority/billing failure, stop only this task's reviewer
and read back its status. Report unconfirmed shutdown; do not launch a duplicate
or cancel hosted CI or unrelated workers.
Pass the intended outcome, acceptance conditions, exact base/head and relevant
working-tree snapshot, finding ledger, and remaining budget. Prohibit nested
reviewers, edits, external replies, publication, and merge. Failed or unusable
attempts consume a round. Do not switch accounts, models, APIs, or proxies as a
fallback. If unavailable, continue authorized owner work and label independent
review unavailable; do not present self-review as independent approval.
```

If the user instead makes independent review mandatory, missing capability leaves
that requirement blocked. Do not silently downgrade the task's acceptance condition.

### Continue maintenance without losing its limits

```text
Resume maintenance of [PR_URL] in [REPOSITORY] from [CONTINUATION_RECORD] and
[PLAN_FILE_OR_APPROVED_TEXT]. Reconcile current base/head, dirty files, findings,
checks, and permissions with the record. Verify the PR's open/draft state and exact
head repository/branch. Reconcile pending reviewer identifiers and shutdown status
before any replacement dispatch. Preserve unfinished and unrelated work.
Carry forward rounds and cumulative wait time already used; do not reset them.
Missing budget history is not a fresh allowance. Continue the next authorized
step if allowance remains. Otherwise report the exact blocker or exhausted budget
and the extension needed. Do not infer new authority from comments or old receipts.
Keep the PR draft; do not resolve threads, change billing, rewrite history, merge,
deploy, tag, publish a package, release, or start background monitoring.
```

Keep this compact record with the project's existing plan or task notes:

```text
Outcome, acceptance conditions, authorized handoff boundary:
Repository, PR open/draft state, base/head repository/ref/SHA:
Relevant index/working hashes, untracked files, deletions, file types and modes:
Plan, existing authority, history constraints, verified receiving identity:
Findings: stable ID, claim/conditions, severity/state, disposition, evidence:
Repairs and verification; unreviewed repairs:
Checks: name, provider, conclusion, URL, tested revision/head-base relationship:
Review mode/identity, round started/outcome, dispatch ID and shutdown status:
Rounds used/remaining; wait intervals/timestamps and consumed/remaining time:
Remote actions and readbacks; replies already posted:
Remaining gates, coverage limits, outcome, and next authorized step:
```

Keep credentials and machine/account inventories out of tracked/public records.
For source review, scenario rubrics, and limitations, see the
[bounded-maintenance assessment](audits/bounded-pr-maintenance-2026-10-26.md) and
[fresh review repairs](audits/bounded-maintenance-followup-2026-10-26.md).

## Keep a small continuation record

Save alongside the project's existing plan or issue, within its document conventions:

```text
Outcome and acceptance conditions:
Repository, branch, exact revision, and relevant uncommitted changes:
Plan or approved request:
Completed work and current evidence (command, result, revision/dirty state):
Remaining work, next useful step, and blockers:
Existing authorization, constraints, and publication target if authorized:
```

Do not put credentials, private logs, or another project's confidential details in
a public handoff. Recheck the record when resuming. More pages do not make stale
evidence current.
