---
name: publish-change-safely
description: "Commits, pushes, or opens a PR only when explicitly requested; verifies identity, destination, diff, and checks while keeping merge, deployment, and release separately authorized."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-skills"
  invocation: "explicit"
  provenance: "clean-room"
  risk_class: "external-write"
disable-model-invocation: true
---

# Publish Change Safely

Perform only the publication actions the user authorized while keeping neighboring scopes clear. `request-code-review` builds the reviewer-facing packet: scope, checks, risks, and review focus. This workflow moves the change to the remote: commit, push, and the pull request record. When one request covers both, publish here first, then hand the packet to `request-code-review`. Repository identity, transport identity, review state, merge, deployment, and live behavior are separate facts.

## Workflow

1. Restate the authorized action and stopping point: commit, push, PR, or another named boundary.
2. Inspect working-tree status, current branch, remotes, upstream, and recent history.
3. Verify the account or credential used by the publishing channel. Do not assume Git transport and hosting API identities match.
4. Review the exact staged and unstaged scope. Preserve unrelated user changes. Never stage everything without first resolving new, deleted, secret-like, generated, or binary files.
5. Run the relevant repository gates or report why they remain incomplete.
6. Create a focused commit using the repository's real convention. Do not invent attribution or coauthor trailers.
7. Re-read the remote before pushing when concurrent changes are plausible. Never force-push, rewrite shared history, change visibility, or alter branch protection without explicit authorization.
8. Push only the intended branch and verify the resulting remote revision.
9. If authorized, open or update a PR with evidence-bounded claims. Do not merge unless the user separately authorized merge.
10. Reconcile the authorized boundary against the observed remote state and report the result using the output contract.

## Stop conditions

Stop before mutation when identity, target repository, branch, staged scope, secret exposure, history divergence, or requested authority is unclear. A rejected push is not permission to rebase, merge, or force. A remote, repository, or branch with a similar name is a different target until its URL or identifier matches the authorized one.

## Done when

The work is done when the authorized boundary is reached and, if that boundary includes a push, the remote readback matches the intended revision.

## Output

Lead with the verified result at the authorized publication boundary. Preserve
exact identity, revision, remote readback, PR/check state, failed checks, every
remote state change made, requested actions left unfinished, and consequential
lifecycle limits. Include a user decision only when one is needed; omit unrelated
actions that were never requested.

Read [the original acceptance example](references/continuity-example.md) when checking this behavior.

## Example

Synthetic example; not an observed client result.

Input: The authorized push succeeded, but creating the requested PR failed.

Output: The revision is pushed; the PR remains unfinished. Report the actual error and next authorized retry without claiming review or merge.
