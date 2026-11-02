# Linked worktree model

Consult the current [Git worktree documentation](https://git-scm.com/docs/git-worktree) before relying on version-sensitive behavior.

## Decision facts

- A linked worktree has its own working files, index, and checked-out `HEAD`.
- Linked worktrees share repository-level references and common Git data.
- A branch generally cannot be checked out in more than one linked worktree at once.
- Worktree metadata can require locking, pruning, or repair when directories move or disappear.
- Git documents incomplete support for multiple checkout operations with submodules. Prefer a separate clone or explicit experiment when submodules make correctness uncertain.

## Safe evidence set

Before proposing isolation, capture the repository root, current branch and revision, porcelain status, registered worktrees, target branch availability, and whether submodules or shared generated outputs are involved. Recheck before removal.
