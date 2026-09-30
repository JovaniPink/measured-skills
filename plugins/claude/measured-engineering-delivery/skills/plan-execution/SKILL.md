---
name: plan-execution
description: Execute a named, approved implementation plan with checkpoints, validation, deviation tracking, and strict stopping boundaries. Invoke explicitly when the user authorizes implementation against an identified plan.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-engineering-delivery"
  invocation: "explicit"
  provenance: "original"
  risk_class: "bounded-execution"
disable-model-invocation: true
---

# Plan Execution

Implement an approved plan without silently changing its scope or authority.

## Preconditions

Confirm the exact plan, repository, branch, authorized actions, excluded actions, and required checkpoints. If the plan is missing, materially ambiguous, or no longer matches the system, stop and report the gap.

## Workflow

1. Establish a clean evidence baseline: branch, revision, worktree state, relevant checks, and known unrelated changes.
2. Translate the plan into a tracked sequence and mark only one dependent step active at a time.
3. Implement the smallest coherent change while preserving unrelated work.
4. Run the planned validation after each risk-bearing checkpoint.
5. Record deviations with cause, impact, evidence, and whether they remain within authority.
6. Stop for approval when a deviation changes scope, interface, data authority, security posture, cost, publication, deployment, or destructive behavior.
7. Reconcile completed steps, remaining work, validation, and unresolved risk against the original plan.

## Boundaries

- Explicit invocation authorizes plan execution only, not push, PR creation, merge, deployment, deletion, or external communication unless those actions were separately authorized.
- Do not repair unrelated failures or absorb adjacent work without approval.
- Do not mark a step complete from worker reports alone; verify integration evidence.

## Output

During execution, report meaningful changes and their implications. At a checkpoint or completion, reconcile `Plan`, `Completed`, `Deviations`, `Validation`, and `Unresolved`. Include requested actions left unfinished and the next authorized step when applicable.

## Continuity and evidence

Report meaningful changes in verified state, a decision, a failure, or a blocker rather than repeated plan narration. Preserve the approved objective through status requests, side questions, interruptions, and compaction. Apply explicit corrections; replace the objective only when the user changes it. Reuse authorization already established in the task and seek a new decision only for a material change outside that authority.

Read [the original acceptance example](references/continuity-example.md) when checking this behavior.
