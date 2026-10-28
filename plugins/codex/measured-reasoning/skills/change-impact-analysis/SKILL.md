---
name: change-impact-analysis
description: "Traces a change's blast radius when asked what might break, which callers depend on it, or what else needs updating; separates traced dependencies from hypotheses."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-reasoning"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Change Impact Analysis

Trace what a change can affect beyond its immediate diff.

## Workflow

1. Pin the exact change, base revision, intended outcome, and deployment or migration shape.
2. Identify changed interfaces, behavior, data, configuration, permissions, dependencies, and timing assumptions.
3. Trace direct callers and consumers, then indirect effects through shared types, events, schemas, caches, jobs, clients, reports, and operational controls.
4. Check compatibility across independent upgrade order, partial rollout, rollback, retry, replay, and mixed-version states.
5. Classify impacts as `Confirmed`, `Possible`, or `Cleared`, and attach the evidence that supports each classification.
6. Prove the highest-risk facts with focused tests, static queries, or safe read-only inspection when available.
7. Report untraced surfaces and the owner or evidence needed to clear them.

## Boundaries

- A textual match is a lead, not proof of a runtime dependency.
- Do not claim no impact outside the reviewed scope.
- Use API compatibility or authority review when those specialized contracts dominate the question.
- Do not deploy, migrate, merge, or notify stakeholders without separate authority.

## Output

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return `Change`, `Confirmed impacts`, `Possible impacts`, `Cleared surfaces`, `Evidence`, `Required tests`, `Rollout and rollback concerns`, and `Coverage gaps`.

## Example

Synthetic example; not an observed client result.

Input: The supplied call graph shows that removing `event.total` affects `web/summary.ts` and `jobs/settle.py`. Other consumers have not been inspected.

Output: Both traced consumers are confirmed impacts: each reads `event.total`. Other consumers remain possible impacts and a coverage gap; no uninspected surface is cleared. Evidence is the supplied call graph, not a runtime test. Required checks are old/new event decoding and both consumer paths. Keep the field through a compatible upgrade order, and retain an old-contract rollback path until consumer migration is verified.
