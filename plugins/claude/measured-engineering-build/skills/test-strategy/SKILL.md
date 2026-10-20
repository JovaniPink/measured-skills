---
name: test-strategy
description: "Plans tests when asked what to test, which checks matter, or how to cover a risky change; selects proportionate unit, integration, contract, and journey evidence."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-engineering-build"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Test Strategy

Choose the smallest set of tests that provides credible evidence for the actual risks.

## Workflow

1. Inventory changed behaviors, interfaces, data states, permissions, failure modes, and user journeys.
2. Rank risks by impact, likelihood, detectability, and reversibility.
3. Map each material risk to the lowest useful test layer:
   - unit for local rules and transformations
   - property for broad invariants and generated input spaces
   - integration for component boundaries and real adapters
   - contract for producer-consumer compatibility
   - migration for forward, reconciliation, and rollback behavior
   - end-to-end for critical cross-system journeys
   - manual observation for visual, hardware, provider, or operational behavior not credibly automated
4. Define fixtures, oracles, isolation, determinism, and cleanup.
5. Include negative paths, boundary values, concurrency, retries, degraded dependencies, and recovery where relevant.
6. Identify redundant, brittle, slow, or low-signal tests and explain any deliberate omission.

## Boundaries

- Do not equate line coverage with behavior coverage.
- Do not prescribe every test type for every change.
- Do not claim a layer passed unless it was executed in the relevant environment.

## Output

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return a matrix with `Risk`, `Behavior`, `Test layer`, `Fixture`, `Oracle`, `Environment`, and `Failure signal`, followed by omissions and manual evidence needs.

## Example

Synthetic example; not an observed client result.

Input: A change adds retries at an external API boundary. The operation can create an object, and callers can cancel it.

Output: Use controlled responses to check retry behavior before seeking provider evidence.

| Risk | Behavior | Test layer | Fixture | Oracle | Environment | Failure signal |
| --- | --- | --- | --- | --- | --- | --- |
| Lost recovery | Retry succeeds or exhausts | Unit | Failure then success; repeated failure | Expected result or terminal error, bounded attempts | Local fake transport | Wrong result or excess attempts |
| Duplicate effect | Same operation repeats | Contract | Replayed operation key | One logical creation | Isolated provider test environment | Multiple created objects |
| Ignored cancellation | Caller cancels during delay | Unit | Controlled clock and cancellation | No later attempt | Local fake transport | Attempt after cancellation |

Provider idempotency remains unverified until a separately authorized integration check. No check has run, and live production behavior is outside this test plan.
