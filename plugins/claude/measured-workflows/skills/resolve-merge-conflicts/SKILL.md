---
name: resolve-merge-conflicts
description: "Resolves a named Git conflict when explicitly asked to reconcile a merge, rebase, or cherry-pick; preserves both intents and keeps continuation, commit, and push authority separate."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.19.0"
  plugin: "measured-workflows"
  invocation: "explicit"
  provenance: "original"
  risk_class: "bounded-execution"
disable-model-invocation: true
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

## Done when

Reconciliation is done when no conflict markers remain in the authorized files, focused checks pass, and the next Git action is named. Stop and ask when repository evidence cannot establish the intended behavior or the next step would advance Git state without authorization.

## Boundaries

- Keep abort visible until the user authorizes an irreversible or state-advancing step.
- Do not choose one side mechanically when both changed semantics.
- Do not infer product, data, security, or migration intent from conflict markers alone.
- Do not use destructive reset or cleanup to make the conflict disappear.

## Output

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Lead with the result and any decision that needs the user. List a decision as unresolved only when it blocks the reconciliation. Then return `Git state`, `Conflict map`, `Side A intent`, `Side B intent`, `Resolution`, `Validation`, `Remaining conflicts`, `Abort option`, and `Next authorized action`.

## Example

Synthetic example; not an observed client result.

Input: One branch adds validation; the other renames the validated field.

Output: Preserve the rename and apply validation to the new field. Check both intended behaviors before staging or continuing under the task's authorization.
