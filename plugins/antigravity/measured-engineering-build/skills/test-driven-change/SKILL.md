---
name: test-driven-change
description: "Implements a bounded behavior change when explicitly asked to use test-driven development; establishes a meaningful failing test, makes it pass, and refactors within authorized scope."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-engineering-build"
  invocation: "implicit"
  provenance: "original"
  risk_class: "bounded-execution"
---

# Test-Driven Change

Use executable evidence to prove that a change addresses the intended behavior.

## Workflow

1. State the behavior, observable boundary, and smallest failing example.
2. Confirm that the failure is meaningful and caused by the target gap rather than a broken fixture or environment.
3. Add or identify a test that fails for the expected reason. Record the red evidence.
4. Implement the smallest behaviorally complete change through the intended architectural seam, not a special case that only satisfies the test.
5. Run the focused test and relevant regression gates. Record the green evidence.
6. Refactor only while the tests remain green, then rerun the appropriate gate set.
7. Report any behavior not covered by executable tests and the required manual or platform observation.

## Done when

The change is done when the target test failed for the expected reason and now passes, or, on the exception path, the replacement evidence passes and the follow-up test obligation is recorded. In both cases the relevant regression gates must pass. Stop and ask only when the intended behavior is ambiguous, no replacement evidence can be defined, or the fix needs changes outside the requested scope.

## Exception path

If test-first is unsuitable, state why before changing code. Valid reasons can include inaccessible hardware, nondeterministic external systems, a missing safe harness, or a purely investigative spike. Define the replacement evidence and a follow-up test obligation where practical.

## Boundaries

- A test that never failed does not prove it detects the target defect.
- Do not weaken assertions, delete coverage, regenerate broad snapshots, or alter production data merely to obtain green output.
- Passing focused tests do not prove deployment or live behavior.
- A passing narrow test is feedback, not proof that the user capability is complete. Verify the slice's boundary and failure behavior separately.
- Run focused checks during implementation and broader required gates at the review checkpoint. Repeat a passing check when relevant code, environment, or assumptions change, not merely because work changes hands.

## Output

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Report `Behavior`, `Red evidence`, `Implementation`, `Green evidence`, `Refactor`, `Regression coverage`, and `Unverified behavior`.

## Example

Synthetic example; not an observed client result.

Input: Change a parser so empty input returns an empty list.

Output: First reproduce the missing behavior with a failing test, implement the smallest fix, and rerun relevant existing cases before refactoring.

## Test framework authority

The reviewed [official unittest documentation source](https://raw.githubusercontent.com/python/cpython/3.15/Doc/library/unittest.rst) is a 3.15-branch snapshot. Discover the repository's actual framework and interpreter first; this reference does not authorize substituting unittest, upgrading tools, or assuming later-version APIs exist locally.
