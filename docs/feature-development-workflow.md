# Build a feature with Measured Skills

Take one feature from an idea to a reviewed change and a draft pull request.
Start with the next useful step; you do not need to run the entire catalog.

**Frame -> Plan -> Implement -> Validate -> Review -> Verify completion -> Open a draft PR**

Tests belong inside implementation, too. The validation stage is the broader
checkpoint before review. If review finds a defect, repair it, repeat the
checks affected by the repair, and review the changed code again.

Use the [Codex prompts](#codex-prompts), [Claude Code prompts](#claude-code-prompts),
or [Antigravity prompts](#antigravity-prompts). Each section has a step-by-step
path and a three-request fast path. These are authored prompts, not a claim that
a client has passed this workflow. The catalog remains a 0.18.0 candidate; see
[current release readiness](release-readiness-2026-10-20.md).

## Before you start

1. Open the intended repository and identify the feature, its users, and the
   outcome they need. Read its instructions before choosing files or commands.
2. Check the branch, current commit, and uncommitted changes. Preserve work that
   belongs to someone else or another task. Use the project's isolation policy.
3. Choose a finish line: a plan, tested local changes, or a draft pull request.
   A pull request (PR) proposes a change; it does not mean someone approved it.
4. Check the available skills and their source. The twelve-skill daily profile
   covers much of this guide, but it does not contain the full lifecycle.
5. Replace the placeholders in the prompt you will paste. Paste prompts into
   the assistant's chat input, not a shell. Use one stage at a time.

| Placeholder | What to provide |
| --- | --- |
| `[REPOSITORY]` | The exact checkout or repository you authorize the assistant to work in |
| `[FEATURE]` | The user need, desired behavior, and important constraints |
| `[PLAN_FILE]` | An existing plan, or a new file chosen using the project's document conventions |
| `[BRANCH]` | The intended feature branch; use the repository's branch policy |
| `[BASE_REVISION]` | The branch or commit to compare against; have the assistant resolve and record its exact commit |
| `[DESTINATION]` | The authorized remote repository and PR base branch |

Do not invent a plan directory for every project. Reuse an issue or specification
when it already holds the contract. If a saved plan no longer matches the code,
reconcile the difference before implementing it. For a small, clear change,
combine framing and planning using the fast path.

### A running example

The following task is fictional; it is not a tested feature or client result.

> People need to see only unfinished tasks. Add an All / Open / Done filter to
> the task list. Keep All as the default. Changing the filter must not change a
> task's status. Leave sorting and saved preferences unchanged.

Acceptance criteria are observable conditions that show the feature works.
For this example: All shows every task; Open and Done show only matching tasks;
no matches show a useful empty state; filtering never edits a task. If the
interface is graphical, check keyboard use, labels, and focus behavior as well
as automated tests. Confirm the existing status model before selecting code.

A regression is previously working behavior that breaks after a change. Test
that existing sorting and task editing still work. CI means continuous
integration: automated checks run by the repository host on pushed changes.
Local checks and CI provide evidence for their exact revision; neither proves
that the feature is deployed or works in production.

## What each stage delivers

| Stage and primary skill | Start with | Finish with |
| --- | --- | --- |
| 1. Frame: `problem-framing` | A need and current evidence | A clear problem, users, constraints, non-goals, and success criteria; skip if already settled |
| 2. Plan: `implementation-planning` | The agreed outcome and repository | A plan grounded in actual code, complete implementation slices, tests, and recovery steps |
| 3. Implement: `plan-execution` where available | A named plan and authorization to edit | Complete slices, focused checks, updated progress, and explicit unfinished work |
| 4. Validate: `cross-stack-quality-gates` | The changed components | Required check results, including failures and unavailable checks |
| 5. Review: `code-change-review` | The exact diff and intended behavior | Findings with evidence, impact, and unresolved conditions; no edits in this stage |
| 6. Verify completion: `claim-verification` | Acceptance criteria and current receipts | What is complete, what is unverified, and which required work remains |
| 7. Open a draft PR: `publish-change-safely` where available | Reviewed changes and explicit publication authority | Verified commit, remote branch, draft PR, and CI status for the pushed commit |

A slice is a small, self-contained behavior change, including its tests and
relevant documentation. Prefer slices that can be understood and reviewed on
their own. Do not separate a change from the tests needed to assess it.

Verification of completion uses evidence; it is not a second name for running
tests. Keep an unrun test distinct from a missing test and from a failing test.
Keep a conditional finding conditional in the title and conclusion, too.

### Bring in a specialist when the change needs one

| Situation | Supporting skill |
| --- | --- |
| Existing callers, workflows, or data may change | `change-impact-analysis` |
| A module boundary or public interface needs design | `module-interface-design` |
| Coverage spans several layers or important failure modes | `test-strategy` |
| You explicitly want a failing-test-first approach | `test-driven-change` |
| Permissions, sensitive data, or attack paths change | `application-security-review` |
| Existing API consumers could break | `api-contract-compatibility-review` |
| A failure needs a cause before a fix | `systematic-diagnosis` |
| Language or platform details matter | The matching engineering profile, such as Python, TypeScript, Swift, or GCP |

Test-driven development is a choice: first show a meaningful failing test, then
implement the behavior and keep it passing while improving the code. Do not
force this approach onto a prose edit or pretend an unavailable test ran.
Choose checks based on the change's risks and the repository's requirements.

## Select skills without guessing

For the seven-stage path, the relevant packs are `measured-engineering-build`
(framing and planning), `measured-engineering-delivery` (plan execution),
`measured-engineering-review` (code review), and `measured-skills` (checks,
claim verification, and safe publication). Optional specialists live in these
packs or `measured-reasoning` and `measured-stack-profiles`.

The daily profile includes five of the seven primary skills. It excludes
`plan-execution` and `publish-change-safely`. A pack is an installation unit;
a profile is a selected set. Merely having the profile does not make the missing
skills available. See [Choose Your Skills](choose-your-skills.md) and the
[client guides](client-support.md); this guide does not install anything.

Before relying on a named skill, check the client's actual selector and loading
trace. Distinguish three things: the skill was selected, its instructions loaded,
and the answer met the task's requirements. An answer that sounds right proves
none of the preceding loading steps. If a skill is missing or a duplicate name
has an unclear source, report that fact. Do not install another copy or claim a
successful invocation. The user can select the correct entry or explicitly
choose ordinary assistance without that skill.

These examples target the named installed packs. A staged pilot wrapper or a
project-local skill may have a different name in the selector. Use the actual
entry from the intended reviewed source. Do not change installations to match
an example.

## Codex prompts

Type `$` or open the skill picker and select the matching installed entry. The
namespaced examples below follow this repository's packs. Explicit selection
and automatic matching are different; duplicate names can expose more than one
entry. Confirm the source rather than assuming Codex combined them. See
[OpenAI's skill documentation](https://learn.chatgpt.com/docs/build-skills) and
[our Codex setup guide](clients/codex.md).

If Codex is in Plan mode, the implementation prompt does not switch modes by
itself. Move to an execution-capable mode when you decide to authorize editing.

### 1. Frame the feature

```text
$measured-engineering-build:problem-framing In [REPOSITORY], frame this feature: [FEATURE].
Inspect repository instructions and relevant code first. Separate facts from assumptions.
Identify users, constraints, success criteria, non-goals, and the next useful step. Preserve
unrelated work. Return a concise proposal with evidence; do not edit or publish.
```

### 2. Plan the change

```text
$measured-engineering-build:implementation-planning In [REPOSITORY], plan [FEATURE]. Inspect the
current branch, relevant changes, code, tests, and project document conventions. Save the plan
in [PLAN_FILE]; only that document may change. Name observable acceptance criteria, affected
interfaces, self-contained slices, checks, rollout and rollback needs, and material unknowns.
Use relevant specialists if available. Preserve unrelated work. Do not implement or publish. If
the current mode prevents saving, return the plan in chat and state that it is unsaved.
```

### 3. Implement the approved plan

```text
$measured-engineering-delivery:plan-execution Implement [PLAN_FILE] in [REPOSITORY] on [BRANCH].
First check that the plan matches the current code and repository instructions. Complete each
authorized slice, run its focused checks, and update the plan with evidence and unfinished work.
Preserve unrelated changes. Resolve routine details within scope; ask before material scope,
permission, or cost changes. Report failures and unavailable checks. Stop with local changes
ready for review; do not commit, push, deploy, or release.
```

### 4. Run the required checks

```text
$measured-skills:cross-stack-quality-gates Check the feature changes in [REPOSITORY] against
[BASE_REVISION]. Inspect repository instructions and CI to find the required commands; do not
invent substitutes. Run the relevant checks without rewriting tracked files. Preserve unrelated
work and ordinary permissions. Report PASS, FAIL, or INCOMPLETE with commands, results,
revision, and unavailable checks. Do not repair failures or publish in this step.
```

### 5. Review the exact change

```text
$measured-engineering-review:code-change-review Review the feature change in [REPOSITORY]
against [BASE_REVISION], including relevant uncommitted changes, using [PLAN_FILE] as intent.
Record the exact comparison and inspect repository instructions. Check behavior, design,
regressions, security, compatibility, tests, and documentation as relevant. Return concise
findings with location, severity, evidence, and conditions that remain unknown. State the review
limits. Make no edits and do not approve, merge, or publish.
```

### 6. Verify completion

```text
$measured-skills:claim-verification In [REPOSITORY], compare [PLAN_FILE] acceptance criteria
with current code, review findings, and check receipts. Inspect current revision and changes
before reusing evidence. State which criteria are met, incomplete, or unverified and the next
required check. Keep test existence, execution, and result separate. Do not treat local success
as deployment or live acceptance. Return a concise evidence summary; do not edit, run new
checks, or publish.
```

### 7. Open a draft pull request

```text
$measured-skills:publish-change-safely In [REPOSITORY], commit and push only the reviewed
feature changes on [BRANCH] to [DESTINATION], and open or update its draft PR. Inspect
instructions, identity, exact diff, required checks, and remote state first. Preserve unrelated
work; no force-push. If required evidence is missing or failing, report the gap before
publication. Describe behavior, checks, risks, and unverified work. Verify the remote commit and
inspect CI for that exact head; report pending or failed checks accurately. Keep the PR draft.
Do not merge, deploy, tag, or release.
```

### Three-request fast path

Use this when the feature is already bounded. Each block is a separate request.
The implementation request authorizes local repairs of confirmed review findings;
publication remains the third request. It does not grant new scope or permissions.

**1. Define and plan**

```text
$measured-engineering-build:implementation-planning In [REPOSITORY], inspect instructions,
relevant code, and current changes, then plan [FEATURE]. Use problem-framing if the need is
unclear and relevant impact, test, or stack skills if available. Save a concise plan in
[PLAN_FILE] using project conventions, with acceptance criteria, non-goals, interfaces, complete
slices, checks, and rollback needs. Separate evidence from assumptions and preserve unrelated
work. Only the plan may change; do not implement or publish. If the current mode prevents
saving, return the plan in chat and state that it is unsaved.
```

**2. Implement, check, and review**

```text
$measured-engineering-delivery:plan-execution Implement [PLAN_FILE] in [REPOSITORY] on [BRANCH]
after checking it against current code and instructions. Complete each slice with focused tests
and documentation; preserve unrelated work. Then use cross-stack-quality-gates,
code-change-review against [BASE_REVISION], and claim-verification where available. Keep the
review findings-only, then repair confirmed findings within the approved scope, rerun affected
checks, and review the changed code again. Record actual skill loading, results, missing checks,
deviations, and unfinished criteria. Ask before material scope, permission, or cost changes.
Finish with reviewed local changes; do not commit, push, deploy, or release.
```

**3. Publish the reviewed change**

```text
$measured-skills:publish-change-safely In [REPOSITORY], commit and push only the reviewed
feature changes on [BRANCH] to [DESTINATION], and open or update its draft PR. Inspect
instructions, identity, exact diff, required checks, and remote state first. Preserve unrelated
work; no force-push. If required evidence is missing or failing, report the gap before
publication. Describe behavior, checks, risks, and unverified work. Verify the remote commit and
inspect CI for that exact head; report pending or failed checks accurately. Keep the PR draft.
Do not merge, deploy, tag, or release.
```

## Claude Code prompts

Paste one leading `/pack:skill` command at a time into Claude Code. Check the
installed command and its source first. These examples use plugin names, not
account-upload aliases. Supporting skill names in the text are requests, not
proof they loaded. The fast path deliberately uses one leading command rather
than depending on command stacking: terminal and headless handling differ.
See [Claude's skill documentation](https://code.claude.com/docs/en/skills) and
[our Claude guide](clients/claude.md).

Switch out of a read-only planning mode when you authorize implementation.
A prompt cannot override the client's permission mode or managed policy.

### 1. Frame the feature

```text
/measured-engineering-build:problem-framing In [REPOSITORY], frame this feature: [FEATURE].
Inspect repository instructions and relevant code first. Separate facts from assumptions.
Identify users, constraints, success criteria, non-goals, and the next useful step. Preserve
unrelated work. Return a concise proposal with evidence; do not edit or publish.
```

### 2. Plan the change

```text
/measured-engineering-build:implementation-planning In [REPOSITORY], plan [FEATURE]. Inspect the
current branch, relevant changes, code, tests, and project document conventions. Save the plan
in [PLAN_FILE]; only that document may change. Name observable acceptance criteria, affected
interfaces, self-contained slices, checks, rollout and rollback needs, and material unknowns.
Use relevant specialists if available. Preserve unrelated work. Do not implement or publish. If
the current mode prevents saving, return the plan in chat and state that it is unsaved.
```

### 3. Implement the approved plan

```text
/measured-engineering-delivery:plan-execution Implement [PLAN_FILE] in [REPOSITORY] on [BRANCH].
First check that the plan matches the current code and repository instructions. Complete each
authorized slice, run its focused checks, and update the plan with evidence and unfinished work.
Preserve unrelated changes. Resolve routine details within scope; ask before material scope,
permission, or cost changes. Report failures and unavailable checks. Stop with local changes
ready for review; do not commit, push, deploy, or release.
```

### 4. Run the required checks

```text
/measured-skills:cross-stack-quality-gates Check the feature changes in [REPOSITORY] against
[BASE_REVISION]. Inspect repository instructions and CI to find the required commands; do not
invent substitutes. Run the relevant checks without rewriting tracked files. Preserve unrelated
work and ordinary permissions. Report PASS, FAIL, or INCOMPLETE with commands, results,
revision, and unavailable checks. Do not repair failures or publish in this step.
```

### 5. Review the exact change

```text
/measured-engineering-review:code-change-review Review the feature change in [REPOSITORY]
against [BASE_REVISION], including relevant uncommitted changes, using [PLAN_FILE] as intent.
Record the exact comparison and inspect repository instructions. Check behavior, design,
regressions, security, compatibility, tests, and documentation as relevant. Return concise
findings with location, severity, evidence, and conditions that remain unknown. State the review
limits. Make no edits and do not approve, merge, or publish.
```

### 6. Verify completion

```text
/measured-skills:claim-verification In [REPOSITORY], compare [PLAN_FILE] acceptance criteria
with current code, review findings, and check receipts. Inspect current revision and changes
before reusing evidence. State which criteria are met, incomplete, or unverified and the next
required check. Keep test existence, execution, and result separate. Do not treat local success
as deployment or live acceptance. Return a concise evidence summary; do not edit, run new
checks, or publish.
```

### 7. Open a draft pull request

```text
/measured-skills:publish-change-safely In [REPOSITORY], commit and push only the reviewed
feature changes on [BRANCH] to [DESTINATION], and open or update its draft PR. Inspect
instructions, identity, exact diff, required checks, and remote state first. Preserve unrelated
work; no force-push. If required evidence is missing or failing, report the gap before
publication. Describe behavior, checks, risks, and unverified work. Verify the remote commit and
inspect CI for that exact head; report pending or failed checks accurately. Keep the PR draft.
Do not merge, deploy, tag, or release.
```

### Three-request fast path

Use this when the feature is already bounded. Each block is a separate request.
The implementation request authorizes local repairs of confirmed review findings;
publication remains the third request. It does not grant new scope or permissions.

**1. Define and plan**

```text
/measured-engineering-build:implementation-planning In [REPOSITORY], inspect instructions,
relevant code, and current changes, then plan [FEATURE]. Use problem-framing if the need is
unclear and relevant impact, test, or stack skills if available. Save a concise plan in
[PLAN_FILE] using project conventions, with acceptance criteria, non-goals, interfaces, complete
slices, checks, and rollback needs. Separate evidence from assumptions and preserve unrelated
work. Only the plan may change; do not implement or publish. If the current mode prevents
saving, return the plan in chat and state that it is unsaved.
```

**2. Implement, check, and review**

```text
/measured-engineering-delivery:plan-execution Implement [PLAN_FILE] in [REPOSITORY] on [BRANCH]
after checking it against current code and instructions. Complete each slice with focused tests
and documentation; preserve unrelated work. Then use cross-stack-quality-gates,
code-change-review against [BASE_REVISION], and claim-verification where available. Keep the
review findings-only, then repair confirmed findings within the approved scope, rerun affected
checks, and review the changed code again. Record actual skill loading, results, missing checks,
deviations, and unfinished criteria. Ask before material scope, permission, or cost changes.
Finish with reviewed local changes; do not commit, push, deploy, or release.
```

**3. Publish the reviewed change**

```text
/measured-skills:publish-change-safely In [REPOSITORY], commit and push only the reviewed
feature changes on [BRANCH] to [DESTINATION], and open or update its draft PR. Inspect
instructions, identity, exact diff, required checks, and remote state first. Preserve unrelated
work; no force-push. If required evidence is missing or failing, report the gap before
publication. Describe behavior, checks, risks, and unverified work. Verify the remote commit and
inspect CI for that exact head; report pending or failed checks accurately. Keep the PR draft.
Do not merge, deploy, tag, or release.
```

## Antigravity prompts

These prompts use ordinary language and name only eligible skills. If you want
a native command, select the entry your installed client actually shows.
[Google documents skill slash commands](https://www.antigravity.google/docs/skills?tab=ide),
but that does not establish a single plugin namespace spelling across versions
or prove these packs work on your installation. See [our Antigravity guide](clients/antigravity.md).

All 17 explicit-only workflows remain excluded from this distribution, including
`plan-execution` and `publish-change-safely`. Steps 3 and 7 below are ordinary
user requests, not invocations or copies of those held skills. Do not install or
manually load an excluded skill to follow this guide. Use the client's normal
permissions and switch out of read-only planning when editing is authorized.

### 1. Frame the feature

```text
Use the installed problem-framing skill for this task; report if it is unavailable. In
[REPOSITORY], frame this feature: [FEATURE]. Inspect repository instructions and relevant code
first. Separate facts from assumptions. Identify users, constraints, success criteria,
non-goals, and the next useful step. Preserve unrelated work. Return a concise proposal with
evidence; do not edit or publish.
```

### 2. Plan the change

```text
Use the installed implementation-planning skill for this task; report if it is unavailable. In
[REPOSITORY], plan [FEATURE]. Inspect the current branch, relevant changes, code, tests, and
project document conventions. Save the plan in [PLAN_FILE]; only that document may change. Name
observable acceptance criteria, affected interfaces, self-contained slices, checks, rollout and
rollback needs, and material unknowns. Use relevant specialists if available. Preserve unrelated
work. Do not implement or publish. If the current mode prevents saving, return the plan in chat
and state that it is unsaved.
```

### 3. Implement the approved plan

```text
In [REPOSITORY] on [BRANCH], implement the feature described in [PLAN_FILE]. I authorize local
source, test, and documentation edits for that feature. Inspect project instructions and confirm
the plan still matches the code. Preserve unrelated work. Test the changed behavior and report
results, limitations, and unfinished criteria. Ask before expanding scope or permissions. Finish
with local changes ready for review; do not commit, push, deploy, or release.
```

### 4. Run the required checks

```text
Use the installed cross-stack-quality-gates skill for this task; report if it is unavailable.
Check the feature changes in [REPOSITORY] against [BASE_REVISION]. Inspect repository
instructions and CI to find the required commands; do not invent substitutes. Run the relevant
checks without rewriting tracked files. Preserve unrelated work and ordinary permissions. Report
PASS, FAIL, or INCOMPLETE with commands, results, revision, and unavailable checks. Do not
repair failures or publish in this step.
```

### 5. Review the exact change

```text
Use the installed code-change-review skill for this task; report if it is unavailable. Review
the feature change in [REPOSITORY] against [BASE_REVISION], including relevant uncommitted
changes, using [PLAN_FILE] as intent. Record the exact comparison and inspect repository
instructions. Check behavior, design, regressions, security, compatibility, tests, and
documentation as relevant. Return concise findings with location, severity, evidence, and
conditions that remain unknown. State the review limits. Make no edits and do not approve,
merge, or publish.
```

### 6. Verify completion

```text
Use the installed claim-verification skill for this task; report if it is unavailable. In
[REPOSITORY], compare [PLAN_FILE] acceptance criteria with current code, review findings, and
check receipts. Inspect current revision and changes before reusing evidence. State which
criteria are met, incomplete, or unverified and the next required check. Keep test existence,
execution, and result separate. Do not treat local success as deployment or live acceptance.
Return a concise evidence summary; do not edit, run new checks, or publish.
```

### 7. Open a draft pull request

```text
In [REPOSITORY], I authorize committing and pushing the reviewed feature on [BRANCH] to
[DESTINATION] and opening or updating its draft PR. Inspect project instructions, Git status,
identity, diff, checks, and remote state first. Preserve unrelated work and use a normal push.
Report missing or failing required checks before publishing. Include behavior, checks, risks,
and limits in the PR. Verify the remote commit and CI for that head, reporting pending or failed
results. Keep it draft; do not merge, deploy, tag, or release.
```

### Three-request fast path

Use this when the feature is already bounded. Each block is a separate request.
The implementation request authorizes local repairs of confirmed review findings;
publication remains the third request. It does not grant new scope or permissions.

**1. Define and plan**

```text
Use the installed implementation-planning skill; report if unavailable. In [REPOSITORY], inspect
instructions, relevant code, and current changes, then plan [FEATURE]. Use problem-framing if
the need is unclear and relevant impact, test, or stack skills if available. Save a concise plan
in [PLAN_FILE] using project conventions, with acceptance criteria, non-goals, interfaces,
complete slices, checks, and rollback needs. Separate evidence from assumptions and preserve
unrelated work. Only the plan may change; do not implement or publish. If the current mode
prevents saving, return the plan in chat and state that it is unsaved.
```

**2. Implement, check, and review**

```text
In [REPOSITORY] on [BRANCH], implement [PLAN_FILE]. I authorize local feature, test, and
documentation changes. Inspect instructions and current code first; preserve unrelated work. Run
focused tests during implementation. Use the available cross-stack-quality-gates,
code-change-review against [BASE_REVISION], and claim-verification skills to check the result.
Review without editing first, then fix confirmed findings within scope and repeat affected
checks and review. Report actual loading, evidence, unavailable checks, and unfinished work. Ask
before expanding scope, permissions, or cost. Stop before commit, push, deployment, or release.
```

**3. Publish the reviewed change**

```text
In [REPOSITORY], I authorize committing and pushing the reviewed feature on [BRANCH] to
[DESTINATION] and opening or updating its draft PR. Inspect instructions, identity, current
changes, required checks, and remote state; preserve unrelated work. Report missing or failing
required checks before publishing. Use a normal push and verify the remote commit. Include
behavior, evidence, risks, and limits in the PR. Inspect CI for that exact head and report its
actual state. Keep it draft; do not merge, deploy, tag, or release.
```

## Repair findings without losing the review boundary

After the findings-only review, use this separate request if repairs are within
the intended scope. Rejected findings need evidence, too; do not change code
merely because a reviewer suggested it.

```text
In [REPOSITORY], assess the review findings for [PLAN_FILE] against current code and evidence.
Fix confirmed findings within the approved feature scope, preserving unrelated changes. Explain
any finding that does not hold. Repeat affected checks and review the revised diff against
[BASE_REVISION]. Keep unknowns and unavailable checks visible. Update the plan and report what
remains. Ask before expanding scope, permissions, or cost. Do not commit, push, deploy, or
release.
```

## Resume or hand off the feature

Use the saved plan and current repository as the starting point. An old test
receipt describes the revision it checked; it does not prove later changes pass.

```text
Resume [PLAN_FILE] in [REPOSITORY] on [BRANCH]. Read repository instructions, the plan, current
revision, and relevant committed and uncommitted changes. Reconcile completed criteria, actual
check receipts, review findings, and unfinished work. Correct unsupported earlier claims; do not
turn an unrun test into a missing or failing test. Preserve unrelated work and the existing
authorization. State the next authorized action and continue it if its prerequisites hold. Ask
only for material decisions outside that authority. Do not infer permission to publish, merge,
deploy, or release from the plan's status.
```

A fresh review context can reduce reliance on the implementation conversation,
but it is not automatically an independent review. Provide the exact diff, plan,
and relevant evidence. Do not send private context to another account or service
without authorization.

## What ready for a draft PR means

The feature's acceptance criteria have current evidence, required checks have
results, and review findings have a disposition. Any gap remains visible. The
PR description explains the user-visible change, how it was checked, and what
is not yet verified. If CI is pending or fails, report that state rather than
claiming completion of the publication checks.

A draft PR is a review artifact. It does not mean human approval, merge,
deployment, or production acceptance. GitHub keeps draft and ready-for-review
states separate; see its [pull request reference](https://docs.github.com/en/pull-requests/reference/pull-requests).

## Sources and evidence limits

Official documentation checked October 26, 2026:

- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills): selection, discovery, and duplicate names.
- [Anthropic: Skills](https://code.claude.com/docs/en/skills): plugin commands and invocation behavior.
- [Anthropic: Development practices](https://code.claude.com/docs/en/best-practices): explore, plan, implement, and give work concrete checks.
- [Google: Antigravity skills](https://www.antigravity.google/docs/skills?tab=ide): skill discovery and commands by client.
- [Google Engineering Practices: Small changes](https://google.github.io/eng-practices/review/developer/small-cls.html): self-contained, reviewable changes with related tests.
- [Google Engineering Practices: Code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html): design, behavior, tests, and documentation.
- [GitHub: Pull requests](https://docs.github.com/en/pull-requests/reference/pull-requests): draft state, review context, and checks.

This guide applies those practices to our catalog. It does not import an
upstream workflow implementation or establish measured benefit. Published
client capabilities and our own observed acceptance are different evidence.
The prior Claude failures and the [unrun diagnostic proposal](audits/claude-routing-contract-retest-plan-2026-10-21.md)
remain unchanged. These prompts do not authorize a pilot, paid evaluation,
billing change, or installation. Account and machine checks belong in the
operator's runbook; never infer one machine's acceptance from another's.
