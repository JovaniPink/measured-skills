---
name: finish-development-branch
description: Reconcile a development branch and present evidence-based options for pull request, merge, retention, or cleanup. Invoke explicitly when implementation is complete enough to decide the branch's next state without assuming push, merge, deletion, or abandonment authority.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.17.1"
  plugin: "measured-engineering-delivery"
  invocation: "explicit"
  provenance: "original"
  risk_class: "external-write"
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

## Boundaries

- Explicit invocation does not automatically authorize push, PR creation, merge, deletion, or deployment.
- Do not confuse a mergeable branch with an approved or merged branch.
- Never discard unrelated or uncommitted work during cleanup.

## Output

Report `Branch state`, `Scope reconciliation`, `Validation`, `Remote and review state`, `Options`, `Selected authority`, and `Final readback`.
