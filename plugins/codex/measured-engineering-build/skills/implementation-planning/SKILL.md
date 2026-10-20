---
name: implementation-planning
description: "Plans a change when asked for implementation steps, acceptance criteria, or a handoff-ready design; resolves interfaces and dependencies before execution without treating the plan as authorization."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-engineering-build"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Implementation Planning

Create an executable plan that another engineer can follow without reopening material design decisions.

Read [specification synthesis](references/specification-synthesis.md) when multiple evidence sources must become one behavioral contract. Read [work packages](references/work-packages.md) when the plan needs independently reviewable units. Read [decision map](references/decision-map.md) when unresolved choices or multiple sessions control sequencing.

Read [document lifecycle](references/document-lifecycle.md) when a specification or README drives implementation, or a plan must survive a handoff.

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
- Walk the slices in order and confirm that each slice's prerequisites exist by that point. Move any slice that depends on later work.
- Name uncertainty directly; do not hide it inside vague steps.
- Keep one short outcome-and-architecture brief: capability, observable completion, module owner, state transitions, invariants, smallest end-to-end slice, and failure checkpoints. Match its depth to the change.
- For unfamiliar designs, explain the state model, failure modes, and a rejected alternative so the user can challenge the design before implementation.
- Do not perform implementation, publication, deployment, or merge unless separately authorized.

## Output

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return `Objective`, `Current evidence`, `Interfaces`, `Implementation steps`, `Test strategy`, `Rollout and rollback`, `Checkpoints`, `Risks`, and `Stopping conditions`.

## Example

Synthetic example; not an observed client result.

Input: Plan a parser change that must accept empty input and retain existing errors.

Output: Define acceptance for empty input and existing error behavior, change the parser boundary, and verify both paths with focused tests before declaring completion.
