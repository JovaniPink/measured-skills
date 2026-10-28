---
name: finish-branch
description: "Assesses next steps for a finished branch when explicitly asked to wrap up development; presents PR, retention, or cleanup options without assuming merge or deletion authority."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.19.0"
  plugin: "measured-workflows"
  invocation: "explicit"
  provenance: "original"
  risk_class: "external-write"
disable-model-invocation: true
---

# Finish Development Branch

Make the branch state and available integration choices explicit before any irreversible action.

## Workflow

1. Verify repository identity, remote, branch, base, exact head, worktree status, commits, and diff.
2. Reconcile the requested scope, implemented behavior, tests, review state, and unresolved risks.
3. Check whether the remote branch or pull request already exists and whether its head matches local state.
4. Present distinct options: retain locally, push, open or update a PR, request review, merge through an authorized method, or clean up after verified integration.
5. State the consequences and prerequisites of each option.
6. Perform only the option the user explicitly selects or has already authorized.
7. Read back remote and merge state after any authorized external action.
8. Remove worktrees or branches only after verifying integration, ownership, and absence of uncommitted work.

## Done when

The workflow is done when the branch state and options are reported, any selected action has been performed and read back, and cleanup happened only where it was authorized and verified. Stop and ask before any option the user has not selected or already authorized.

## Boundaries

- Explicit invocation does not automatically authorize push, PR creation, merge, deletion, or deployment.
- Do not confuse a mergeable branch with an approved or merged branch.
- Never discard unrelated or uncommitted work during cleanup.

## Output

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Report `Branch state`, `Scope reconciliation`, `Validation`, `Remote and review state`, `Options`, `Selected authority`, and `Final readback`.

## Example

Synthetic example; not an observed client result.

Input: The patch is tested locally; no push or cleanup was requested.

Output: The branch is ready for a delivery decision. Report its revision and checks; retain it until the user chooses the next authorized state.
