---
name: code-change-review
description: "Reviews a supplied PR diff, commit, or code snippet when asked to \"review this PR\", check changes, or find bugs and regressions; covers static review without a checkout and returns findings without editing code."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-engineering-review"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Code Change Review

Review a pinned change and return evidence-bounded findings.

## Workflow

1. Pin the repository, base revision, head revision, diff scope, intended behavior, and relevant authority when supplied. A pasted diff or snippet is enough for a scoped static review; label unavailable repository context instead of inventing it or requiring access unrelated to the request.
2. Read the changed code in context, including callers, consumers, contracts, tests, configuration, and generated boundaries.
3. Test each suspected issue against actual control flow, data flow, upgrade order, failure handling, and repository conventions.
4. Rank only actionable findings by user impact and likelihood. Attach exact locations and a concrete failure scenario.
5. Check whether inspected tests would fail for the defect and whether the proposed behavior is compatible with existing consumers. A test that has not run may still exist; absent test results do not prove absent coverage.
6. Separate findings from questions, optional improvements, and unsupported concerns.
7. Report validation performed, unavailable evidence, and the remaining review boundary.

## Boundaries

- A changed line is not automatically defective, and an unchanged line can still be affected.
- Do not implement fixes unless the user separately asks for changes.
- Do not treat a review comment as a decision, a passing check as merge authority, or a mergeable state as approval.
- Do not claim the change is safe outside the inspected scope.
- Keep a demonstrated defect, a conditional risk, and missing evidence distinct. Do not turn an unrun test into a separate missing-test defect without inspecting the relevant coverage.
- Use claim-verification for whether an old receipt still proves completion at a new revision; use this workflow when the requested result is code findings.

## Output

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Lead with findings ordered by severity, most severe first. For each finding provide `Severity`, `State`, `Location`, `Failure`, `Evidence`, `Impact`, and `Suggested direction`. Grade `Severity` as `none`, `note`, `warning`, or `error`. Set `State` to `new`, `unchanged`, `updated`, or `absent` against the pinned base revision. `error` means the finding would block the reviewed action; keep reporting findings of every severity. Then report `Questions`, `Validation`, and `Review boundary`. If no actionable finding survives verification, say so and name remaining risks or untested surfaces.

## Example

Synthetic example; not an observed client result.

Input: In the supplied A-to-B diff at `api/objects.py:42`, an object lookup loses its tenant predicate and filters only by ID. No access test has run.

Output: error, new, `api/objects.py:42`: the explicit tenant filter is removed. If the lookup has no implicit tenant scope, a caller who knows another tenant's ID could receive that object. Evidence: the supplied diff; the store implementation is unavailable. Restore or demonstrate an equivalent authorization check before acceptance. Validation: static review only; test execution is unobserved and test existence is unknown. Review boundary: the supplied handler diff. Next inspect the store contract and existing cross-tenant coverage; do not report missing tests as a confirmed defect.
