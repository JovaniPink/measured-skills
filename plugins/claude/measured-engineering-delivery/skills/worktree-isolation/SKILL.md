---
name: worktree-isolation
description: Assess whether dirty or concurrent repository work needs Git worktree isolation and design a safe isolation approach. Use when work may overlap existing changes; require explicit authority before creating, moving, locking, repairing, or removing a worktree.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-engineering-delivery"
  invocation: "implicit"
  provenance: "clean-room"
  risk_class: "bounded-execution"
---

# Worktree Isolation

Protect concurrent and unrelated repository work by assessing isolation before mutation.

Read [linked worktree model](references/linked-worktree-model.md) when the decision depends on shared repository state, submodules, pruning, locking, or repair.

## Workflow

1. Inspect the current branch, revision, status, existing worktrees, and target files without changing them.
2. Identify ownership overlap, uncommitted work, branch conflicts, shared generated output, and commands that can affect all worktrees.
3. Decide whether the work can proceed in place, needs a linked worktree, or must wait for coordination.
4. Propose the exact branch, base revision, worktree path, ownership boundaries, validation, and cleanup conditions.
5. Require explicit authority before creating, moving, locking, repairing, pruning, or removing a worktree.
6. Recheck the shared repository state before cleanup. Preserve worktrees with uncommitted or unintegrated work.

## Done when

The assessment is done when the isolation decision and proposed layout are stated with the authority each step needs. Stop and ask before any worktree change that is not already authorized.

## Boundaries

- Linked worktrees share repository-level state, including refs and some configuration; they are not independent clones.
- Do not assign the same branch to multiple worktrees.
- Treat submodule-heavy repositories cautiously because linked-worktree support can be incomplete.
- Never remove a worktree or branch merely because another change is complete.

## Output

Report `Current state`, `Collision risks`, `Isolation decision`, `Proposed layout`, `Required authority`, `Validation`, and `Cleanup conditions`.
