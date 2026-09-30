---
name: implementation-planning
description: Produce a decision-complete implementation plan grounded in repository and platform evidence. Use when a change needs concrete interfaces, ordered steps, tests, rollout controls, checkpoints, and stopping conditions before work begins.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.17.1"
  plugin: "measured-engineering-build"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Implementation Planning

Create an executable plan that another engineer can follow without reopening material design decisions.

Read [specification synthesis](references/specification-synthesis.md) when multiple evidence sources must become one behavioral contract. Read [work packages](references/work-packages.md) when the plan needs independently reviewable units. Read [decision map](references/decision-map.md) when unresolved choices or multiple sessions control sequencing.

## Workflow

1. Confirm the approved problem, desired outcome, scope, non-goals, and decision owner.
2. Inspect the current repository and relevant external authority before naming files, interfaces, or commands.
3. Describe the target behavior and every public interface, data contract, state transition, or compatibility promise that changes.
4. Name the existing module to extend and its ownership boundary. Break work into behaviorally complete vertical slices with exact locations and dependencies, not test or PR tranches.
5. Define tests by risk: unit, integration, contract, migration, end-to-end, property, and manual observation as applicable.
6. Specify rollout, monitoring, compatibility, rollback, and data-recovery behavior.
7. Add checkpoints where evidence must be reviewed before proceeding.
8. State stopping conditions for missing authority, unexpected scope, failing safety gates, or invalidated assumptions.

## Quality rules

- Resolve discoverable facts from the repository instead of delegating discovery to the implementer.
- Distinguish proposed changes from ratified decisions.
- Name uncertainty directly; do not hide it inside vague steps.
- Keep one short outcome-and-architecture brief: capability, observable completion, module owner, state transitions, invariants, smallest end-to-end slice, and failure checkpoints. Match its depth to the change.
- For unfamiliar designs, explain the state model, failure modes, and a rejected alternative so the user can challenge the design before implementation.
- Do not perform implementation, publication, deployment, or merge unless separately authorized.

## Output

Return `Objective`, `Current evidence`, `Interfaces`, `Implementation steps`, `Test strategy`, `Rollout and rollback`, `Checkpoints`, `Risks`, and `Stopping conditions`.
