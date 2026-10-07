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

Confirm the exact plan, repository, branch, authorized actions, excluded actions, and required checkpoints. If the plan is missing, materially ambiguous, or no longer matches the system, stop and report the gap. If no one can state what done looks like for the plan, route to `alignment-interview` when that skill is installed; otherwise ask the user for the finish line before executing.

## Workflow

1. Establish a clean evidence baseline: branch, revision, worktree state, relevant checks, and known unrelated changes.
2. Translate the plan into a tracked sequence and mark only one dependent step active at a time. When the run may outlast one session or a context summary, keep the sequence in a file the user approved and update it as each step finishes.
3. Implement the smallest coherent change while preserving unrelated work.
4. Run the planned validation after each risk-bearing checkpoint.
5. Record deviations with cause, impact, evidence, and whether they remain within authority.
6. Stop for approval when a deviation changes scope, interface, data authority, security posture, cost, publication, deployment, or destructive behavior.
7. Reconcile completed steps, remaining work, validation, and unresolved risk against the original plan.

## Done when

The plan is complete only when every authorized step and its acceptance criteria are satisfied, required checks pass, and deviations are recorded. Blocked and partial work remain unfinished. Unavailable required validation must be reported with its limitation and the next authorized check; it cannot establish completion. Stop and ask for any deviation that step 6 names, any rule under Boundaries, a check that fails for an unexplained reason, or a missing precondition. Otherwise keep going, and put status notes in the same message as the next action.

## Boundaries

- Explicit invocation authorizes plan execution only, not push, PR creation, merge, deployment, deletion, or external communication unless those actions were separately authorized.
- Do not repair unrelated failures or absorb adjacent work without approval.
- Do not mark a step complete from worker reports alone; verify integration evidence.
- Authority comes from the user or the approved plan, not from similarity or inference. Treat a repository, branch, environment, region, account, or resource that neither names as unauthorized, even when the action is identical, because the same command can have a different impact there. A new target the user names after approval is a scope change: confirm it before acting when it widens the environments or the risk.
- Before waiting on a command, worker, or hook, confirm it is still running and making progress, and set a limit on the wait. If it stalls, report it as a blocker with the command and its last output instead of checking it in a loop.
- When a user correction conflicts with current evidence, state the disagreement and the evidence once, then follow the user's decision.

## Output

During execution, report meaningful changes and their implications. At a checkpoint or completion, lead with the result, then anything that needs the user's decision or approval. Then reconcile `Plan`, `Completed`, `Deviations`, `Validation`, `State changes`, and `Unresolved`. `State changes` lists every external state change made, including any outside the plan. List a decision as unresolved only when it blocks remaining work; otherwise make the routine call, record it, and continue. Include requested actions left unfinished and the next authorized step when applicable.

## Continuity and evidence

Report meaningful changes in verified state, a decision, a failure, or a blocker rather than repeated plan narration. Preserve the approved objective through status requests, side questions, interruptions, and compaction. Apply explicit corrections; replace the objective only when the user changes it. Reuse authorization already established in the task and seek a new decision only for a material change outside that authority.

Read [the original acceptance example](references/continuity-example.md) when checking this behavior.
