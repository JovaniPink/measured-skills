---
name: multi-agent-orchestration
description: Coordinate authorized parallel agents on independent bounded tasks with explicit ownership, evidence contracts, cost awareness, and final reconciliation. Invoke explicitly when parallel work can reduce latency without creating edit collisions or delegating irreversible decisions.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.17.1"
  plugin: "measured-engineering-delivery"
  invocation: "explicit"
  provenance: "clean-room"
  risk_class: "bounded-execution"
---

# Multi-Agent Orchestration

Use parallel workers only when their tasks are genuinely independent and the host and user permit delegation.

Read [client mapping](references/client-mapping.md) only when selecting a client-specific coordination mechanism. Read [candidate comparison](references/candidate-comparison.md) only when several independent implementations can be tested against one rubric. Read [coverage fanout](references/coverage-fanout.md) only when independent review lenses can inspect the same pinned artifact without overlapping writes.

## Workflow

1. Confirm delegation authority, supported host behavior, budget or cost constraints, and the integration owner.
2. Decompose the work into bounded tasks with clear inputs, outputs, owned files or read-only scope, stopping conditions, and required evidence.
3. Identify dependencies. Keep tightly sequential work with one owner.
4. Prevent overlapping write ownership and state which worker may modify each shared artifact.
5. Launch only useful independent tasks and retain meaningful local integration work.
6. Require workers to report evidence, limitations, changed files, validation, and unresolved risks.
7. Reconcile results against the shared objective. Independently inspect diffs and rerun integration gates.
8. Stop when tasks conflict, authority changes, costs exceed the agreed bound, or external decisions are required.

## Forbidden delegation

- Do not delegate without user or host authorization.
- Do not assign multiple workers to edit the same owned files.
- Do not delegate irreversible publication, deletion, deployment, or merge decisions.
- Do not treat worker completion as verified integration.
- Do not parallelize work whose outputs depend tightly on earlier unfinished steps.

## Output

Return `Delegation authority`, `Task map`, `Ownership`, `Evidence contract`, `Cost boundary`, `Worker results`, `Integration verification`, and `Unresolved decisions`.
