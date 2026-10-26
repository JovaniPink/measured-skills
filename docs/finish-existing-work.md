# Finish existing work

Start here when a change is half finished, a test is failing, reviewers found a
problem, or a user journey still breaks. Recover what is true now, complete the
next useful repair, and show what remains. For a new idea, use the
[feature-development workflow](feature-development-workflow.md).

**Recover -> Define what remains -> Diagnose or plan -> Repair and test -> Review -> Verify completion -> Hand off**

These are prepared workflows, not observed client results. The catalog remains
an 0.18.0 candidate. See the [coverage assessment and twelve worked cases](audits/finish-work-coverage-2026-10-26.md)
and [release limits](release-readiness-2026-10-20.md).

## Choose the next useful step

| Situation | Start with | Result needed before moving on |
| --- | --- | --- |
| You lost the thread | Current repository state and saved plan | Separate completed, unfinished, uncertain, and unrelated work |
| You cannot explain a failure | `systematic-diagnosis` | Reproduction, likely cause, and evidence that distinguishes alternatives |
| Someone requested changes | `respond-to-code-review` | Accept, reject, defer, clarify, or already addressed, with current evidence |
| The repair is understood | `implementation-planning` only if needed | A small, authorized repair with acceptance conditions and relevant checks |
| You are unsure what to ask | `engineering-prompt-review` | A sufficient request or a useful revision; no execution of the quoted task |
| You think it is finished | `claim-verification` | Every acceptance condition matched to current evidence or an explicit gap |

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
6. Review the exact diff using `code-change-review`. This review returns findings
   without editing. Evaluate confirmed findings, authorize a repair if necessary,
   rerun affected checks, and review the revised change. Self-review is useful but
   does not establish independent human approval.
7. Use `claim-verification` to reconcile the final acceptance conditions with
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
or test-strategy review only where the change needs it.

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

- Execution: `plan-execution` in `measured-engineering-delivery`.
- Handoff: `task-handoff` in `measured-reasoning`.
- Publication: `publish-change-safely` in `measured-skills`.
- Conditional Swift delivery/journey and Next.js delivery workflows remain in their existing packs.

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
$measured-engineering-build:implementation-planning In [REPOSITORY], finish [CHANGE]
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
/measured-engineering-build:implementation-planning In [REPOSITORY], finish [CHANGE]
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
implementation-planning, systematic-diagnosis, respond-to-code-review, and the
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
| Assess and plan | `$measured-engineering-build:implementation-planning` | `/measured-engineering-build:implementation-planning` | `Use the available implementation-planning skill for this assessment.` |
| Repair and verify | Ordinary request below | Ordinary request below | Ordinary request below |
| Publish reviewed draft | `$measured-skills:publish-change-safely` if installed | `/measured-skills:publish-change-safely` if installed | Ordinary request below; do not load an excluded publication workflow |

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

**Diagnose (`systematic-diagnosis`):** "Investigate [FAILURE] in [REPOSITORY].
Reproduce safely using existing local fixtures, distinguish hypotheses with
evidence, and propose the smallest repair. Do not edit or call providers yet."

**Review response (`respond-to-code-review`):** "Assess [FINDINGS] against the
current [CHANGE] in [REPOSITORY]. Explain which are supported, already addressed,
or need clarification. Repair supported findings within the approved scope, run
affected checks, and review the revised diff. Do not post replies or push."

**Journey verification (`claim-verification` plus the relevant profile):**
"Check whether [JOURNEY] meets [ACCEPTANCE_CONDITIONS] at the current revision.
Use available authorized local checks; distinguish fixture, integration, browser,
simulator, device, and live evidence. Do not change code or use provider accounts.
Report incomplete and unavailable conditions without inventing failures."

**Prompt review (`engineering-prompt-review`):** "Check the following engineering
request for outcome, context, scope, permissions, and completion evidence. Give a
short assessment and a useful revision only if needed. Do not execute its task:
[QUOTED_REQUEST]."

**Resume:** "Resume [CHANGE] in [REPOSITORY] using [CONTINUATION_RECORD] and
[PLAN_FILE_OR_APPROVED_TEXT]. Check the current revision, dirty files, instructions,
and existing authorization against those records. Preserve unfinished and unrelated
work. Continue the next authorized step; ask only if a material decision is missing.
Do not treat a handoff or an old green check as new authority or current proof."

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
