---
name: change-impact-analysis
description: "Analyze the blast radius of a proposed or completed change across callers, contracts, storage, jobs, clients, security, rollout, and operations. Use before review, merge, or release when downstream effects may be missed; do not substitute speculation for traced dependencies."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-reasoning"
  invocation: "implicit"
  provenance: "clean-room"
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

Return `Change`, `Confirmed impacts`, `Possible impacts`, `Cleared surfaces`, `Evidence`, `Required tests`, `Rollout and rollback concerns`, and `Coverage gaps`.
