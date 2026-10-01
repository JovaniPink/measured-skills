---
name: test-strategy
description: Design risk-proportionate test coverage across unit, integration, contract, end-to-end, property, migration, and manual layers. Use when a feature, architecture change, or defect needs a justified coverage plan rather than only running existing checks.
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

Return a matrix with `Risk`, `Behavior`, `Test layer`, `Fixture`, `Oracle`, `Environment`, and `Failure signal`, followed by omissions and manual evidence needs.
