---
name: test-quality-review
description: "Reviews test quality when asked whether tests catch real regressions or merely mirror implementation; checks assertions, isolation, failure behavior, and coverage without equating count with confidence."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-engineering-review"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Test Quality Review

Use current primary guidance as a review baseline, then report only what the available evidence supports. Primary authority: [official reference](https://docs.python.org/3/library/unittest.html).

## Workflow

1. Identify the behaviors and risks the tests are expected to protect.
2. Trace representative tests from setup through action, oracle, cleanup, and failure output.
3. Check that assertions can fail for the target defect and are not coupled only to implementation details.
4. Review boundary, negative, concurrency, retry, migration, permission, and recovery coverage where relevant.
5. Inspect isolation, determinism, clocks, randomness, network, shared state, fixtures, and parallel safety.
6. Find skipped, quarantined, flaky, snapshot-heavy, redundant, slow, or low-signal coverage.
7. Recommend focused mutations or controlled defect injection to test sensitivity when authorized.

## Boundaries

- Do not equate test count, line coverage, or a green suite with meaningful behavioral protection.
- Do not weaken assertions or accept broad snapshots merely to reduce failures.
- Do not execute destructive fixtures or shared-environment tests without explicit authorization.

## Output

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return Protected behavior, Oracle quality, Missing risks, Flakiness and isolation, Maintenance cost, and Recommended evidence. Grade each finding `none`, `note`, `warning`, or `error`, and order the list with the most severe first. When a pinned change is under review, mark each finding `new`, `unchanged`, `updated`, or `absent` against the state before the change; otherwise report severity alone.

## Example

Synthetic example; not an observed client result.

Input: A test asserts only that a mock method was called, not what the user receives.

Output: The test may pass with incorrect output. Add an observable result or error assertion and demonstrate that a real regression fails it.
