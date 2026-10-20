---
name: task-handoff
description: "Prepares a continuation record when explicitly asked to hand off or resume work elsewhere; records exact state, unfinished work, evidence, and existing authority without transferring new permissions."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-reasoning"
  invocation: "explicit"
  provenance: "clean-room"
  risk_class: "bounded-execution"
disable-model-invocation: true
---

# Task Handoff

Create a compact, verifiable continuation record without transferring hidden reasoning or unrelated private context.

## Workflow

1. Name the objective, repository or system boundary, intended recipient, and exact continuation point.
2. Verify current branch, revision, worktree state, remote or PR state, validation, and external surface state when each claim is relevant and accessible.
3. Separate completed work, partially completed work, proposed work, blocked work, and work not started.
4. Record decisions with their status and evidence. Preserve unresolved questions and named decision owners.
5. List changed files or artifacts, commands already run, observed results, known failures, and safe next checks.
6. State authorized actions, actions requiring new approval, sensitive context that is deliberately omitted, and stopping conditions.
7. Provide the smallest ordered next-step list that lets the recipient verify before acting.

## Boundaries

- Do not describe local work as pushed, a PR as merged, a preview as deployed, or a deployment as live without current evidence.
- Do not include chain-of-thought, raw transcripts, credentials, personal data, or unrelated repository details.
- A handoff transfers context, not authority.
- Write a file or send the handoff externally only when that destination and action are authorized.

## Output

Lead with the continuation point and next verification or authorized action.
Retain the objective, exact revision and working state, changed artifacts,
completed and in-progress work, decisions, validation, blockers, evidence
references and freshness, existing authorization, and stop conditions. Use one
compact record unless a fuller handoff is requested or needed. Reverify stale
evidence before dependent action; do not repeat work already proved current.

Read [the original acceptance example](references/continuity-example.md) when checking this behavior.

## Example

Synthetic example; not an observed client result.

Input: A patch passed tests at revision A, but the receiving checkout is B.

Output: Preserve the patch and receipt at A. Compare B before relying on those tests; carry forward the unfinished work and existing authorization.
