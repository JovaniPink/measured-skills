---
name: review-code-change
description: "Reviews PR diffs for bugs, regressions, and access-control changes on requests such as review this PR diff, check this patch, or find a regression. Applies to pasted changes and repository diffs; returns findings without editing, approving, or merging."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.19.0"
  plugin: "measured-quality"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Code Change Review

Review a pinned change and return evidence-bounded findings.

Read [bounded review](references/bounded-review.md) when repeated review or a
maintenance loop is requested. The reference defines snapshot identity, round
limits, and the optional reviewer boundary; this skill remains findings-only.

## Routing and evidence

Use this workflow when the requested result is findings about changed code,
including a self-contained pasted diff without a checkout. An access-control
change is still a code review; a broader security assessment is a different task.
Use verify-claims when the question is whether a receipt proves completion.
An implementation request does not become read-only review merely because code
is supplied.

Separate the observed change, the contract needed for a failure, and the evidence
that establishes that contract. If store behavior or equivalent authorization is
unknown, the defect remains conditional in its heading, conclusion, severity
explanation, and suggested direction. A qualifier buried in the body does not
support an unconditional headline or verdict.

Track test existence, execution, and outcome separately:

| Evidence | Supported statement | Still unknown |
| --- | --- | --- |
| No test has run | No execution result is available | Whether a test exists and how it would behave |
| No test was supplied | Coverage was not provided in this review | Existence or execution elsewhere |
| A proposed test assertion | Desired behavior required by a stated contract | What the current implementation returns and whether the assertion passes |
| A static prediction | Predicted response and assertion outcome under named implementation assumptions | Whether those assumptions hold and what an actual run observes |
| A recorded test result | Observed outcome for its identified revision and setup | Behavior outside that test's scope; an incomplete run does not establish a pass |

Do not use "expected result" to mean both the desired assertion and the predicted
response. For a proposed test, identify what it should assert, what the current
code would do under named assumptions, and whether that would satisfy the
assertion. If implementation semantics are missing, keep the prediction
conditional or unknown. A desired denial does not predict denial from a broken
authorization path. A predicted assertion failure is still not an executed result.

## Workflow

1. Pin the repository, base revision, head revision, diff scope, intended behavior, and relevant authority when supplied. A pasted diff or snippet is enough for a scoped static review; label unavailable repository context instead of inventing it or requiring access unrelated to the request.
2. Include relevant staged, unstaged, and untracked files when the scope is a working tree; a committed diff omits them. Bind relevant uncommitted contents with path, representation (index, working-tree, or untracked), and SHA-256; retain both versions when staged and working-tree bytes differ, plus deletions and file modes. Do not collect unrelated or sensitive files. Reconcile concurrent changes before calling the review current.
3. Read the changed code in context, including callers, consumers, contracts, tests, configuration, and generated boundaries.
4. Test each suspected issue against actual control flow, data flow, upgrade order, failure handling, and repository conventions.
5. Rank only actionable findings by user impact and likelihood. Attach exact locations and a concrete failure scenario.
6. Inspect available coverage and compatibility. Separate the desired assertion from the implementation's predicted response and the predicted pass/fail outcome. None is an observed result before execution. Do not claim it fails against a patch while required store, authorization, or test semantics remain unknown. Label a complete static proof separately; it still does not establish test execution.
7. Separate findings from questions, optional improvements, and unsupported concerns.
8. Report validation performed, unavailable evidence, and the remaining review boundary.

## Boundaries

- A changed line is not automatically defective, and an unchanged line can still be affected.
- Do not implement fixes unless the user separately asks for changes.
- Do not treat a review comment as a decision, a passing check as merge authority, or a mergeable state as approval.
- Do not claim the change is safe outside the inspected scope.
- Keep a demonstrated defect, a conditional risk, and missing evidence distinct. Do not turn an unrun test into a separate missing-test defect without inspecting the relevant coverage.
- Use verify-claims for whether an old receipt still proves completion at a new revision; use this workflow when the requested result is code findings.

## Status updates and resumed reviews

Carry forward the original goal, pinned scope, evidence actually reviewed,
findings with their conditions, validation performed, unresolved checks, and next
authorized step. Change those states only when new evidence supports the change.
An earlier assistant answer is not new evidence: correct its unsupported claim
rather than repeating it as fact.

If only "no test has run" was supplied, both a pause update and a resumed review
must retain unknown test existence and an unobserved outcome. Do not change that
to "not written", "missing coverage", or "will fail". If equivalent tenant
scoping remains unknown, retain that condition through the final verdict; an
equivalent control could establish that the suspected exposure does not occur.
Preserve the desired assertion, prediction assumptions, and observed-result status
separately. If an earlier answer called desired behavior a prediction, correct that
wording explicitly; continuity does not require carrying forward its mistake.

## Output

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Lead with findings ordered by severity, most severe first. For each finding provide `Severity`, `State`, `Location`, `Failure`, `Evidence`, `Impact`, and `Suggested direction`. Grade `Severity` as `none`, `note`, `warning`, or `error`. Set `State` to `new`, `unchanged`, `updated`, or `absent` against the pinned base revision. `error` means the finding would block the reviewed action; keep reporting findings of every severity. Then report `Questions`, `Validation`, and `Review boundary`. If no actionable finding survives verification, say so and name remaining risks or untested surfaces.

## Example

Synthetic example; not an observed client result.

Input: In the supplied A-to-B diff at `api/objects.py:42`, an object lookup loses its tenant predicate and filters only by ID. No access test has run.

Output: error, new, `api/objects.py:42`: the explicit tenant filter is removed. If the lookup has no implicit tenant scope, a caller who knows another tenant's ID could receive that object. Evidence: the supplied diff; the store implementation is unavailable. Restore or demonstrate an equivalent authorization check before acceptance. Validation: static review only; test execution is unobserved and test existence is unknown. Review boundary: the supplied handler diff. Next inspect the store contract and existing cross-tenant coverage; do not report missing tests as a confirmed defect.

Proposed test: A tenant-B actor requests a tenant-A object. The desired assertion
is denial without object disclosure, using the endpoint's documented response
contract. If the store is unscoped, the object exists, and no equivalent control
applies, the predicted response is the other tenant's object, so that denial
assertion would fail. If an equivalent control applies, it may pass. The supplied
diff alone leaves those conditions unverified; no test result was observed.

Follow-up input: Pause, then resume the same review with no new evidence.

Output: The goal and supplied handler scope are unchanged. Exposure remains
conditional on the uninspected store and authorization contract. Test existence
is unknown and no test result is available. Denial is the proposed assertion,
not the predicted response from an assumed unscoped store. Under the missing-control
assumptions above, disclosure would violate that assertion; actual behavior is
unverified. Next inspect the equivalent control and coverage within the
authorized review scope. No files were changed and no check was run.
