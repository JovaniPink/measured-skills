---
name: merge-conflict-reconciliation
description: "Reconcile an active Git merge, rebase, or cherry-pick conflict by inspecting exact repository state, preserving both sides' intent, validating the result, and keeping abort available. Invoke explicitly for an identified conflicted worktree; staging, continuing, committing, and pushing require separate authority."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.17.1"
  plugin: "measured-engineering-delivery"
  invocation: "explicit"
  provenance: "clean-room"
  risk_class: "bounded-execution"
---

# Merge Conflict Reconciliation

Resolve semantic conflict without manufacturing intent or silently advancing Git state.

## Preconditions

Confirm the exact worktree, current operation, revisions, uncommitted changes, conflict set, authorized file edits, and permitted Git actions. Record the operation-specific abort command as an available option before editing.

## Workflow

1. Inspect read-only Git state and identify whether the worktree is in merge, rebase, cherry-pick, revert, or another operation.
2. Pin the base and both sides where available. Read each conflict in surrounding code and trace related callers, tests, schemas, and history.
3. State each side's observed behavior and the unresolved semantic decision. Ask for direction when repository evidence cannot establish intended behavior.
4. Edit only authorized conflicted files and necessary consistency updates. Remove conflict markers without discarding unrelated changes.
5. Run focused tests and repository gates that can detect a wrong reconciliation.
6. Reinspect the diff and Git state. Report resolved files, unresolved files, validation, and the exact next Git action.
7. Stage, continue, commit, push, or open a pull request only when that specific action is authorized.

## Boundaries

- Keep abort visible until the user authorizes an irreversible or state-advancing step.
- Do not choose one side mechanically when both changed semantics.
- Do not infer product, data, security, or migration intent from conflict markers alone.
- Do not use destructive reset or cleanup to make the conflict disappear.

## Output

Return `Git state`, `Conflict map`, `Side A intent`, `Side B intent`, `Resolution`, `Validation`, `Remaining conflicts`, `Abort option`, and `Next authorized action`.
