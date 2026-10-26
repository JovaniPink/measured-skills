---
name: multi-agent-orchestration
description: "Coordinates delegated work when explicitly asked for independent workers or a bounded reviewer; defines ownership, evidence, and budgets without duplicating edits or delegating irreversible decisions."
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

# Multi-Agent Orchestration

Use workers only when the host and user permit delegation. Parallel tasks must
be genuinely independent. An explicitly requested sequential reviewer is also a
supported coordination pattern; it does not authorize parallel editing.

Read [client mapping](references/client-mapping.md) only when selecting a client-specific coordination mechanism. Read [candidate comparison](references/candidate-comparison.md) only when several independent implementations can be tested against one rubric. Read [coverage fanout](references/coverage-fanout.md) only when independent review lenses can inspect the same pinned artifact without overlapping writes.

## Workflow

1. Confirm delegation authority, supported host behavior, budget or cost constraints, and the integration owner. State the planned worker count and expected cost or time before launching, and get agreement when they exceed what the user implied.
2. Decompose the work into bounded tasks with clear inputs, outputs, owned files or read-only scope, stopping conditions, and required evidence. Match each worker's capability and cost to its task, and brief each worker completely the first time.
3. Identify dependencies. Keep tightly sequential work with one owner.
4. Prevent overlapping write ownership and state which worker may modify each shared artifact.
5. Launch only useful independent tasks and retain meaningful local integration work.
6. Require workers to report evidence, limitations, changed files, validation, and unresolved risks.
7. Before waiting on a worker, command, or hook, confirm it is still running and making progress, and set a limit on the wait. If it stalls, report it as a blocker with its last output instead of checking it in a loop.
8. Reconcile results against the shared objective. Independently inspect diffs and rerun integration gates.
9. Stop when tasks conflict, authority changes, costs exceed the agreed bound, or external decisions are required.

## One optional reviewer

For a bounded review of one change, the owner keeps implementation responsibility.
Before launching, verify the actual host, effective custom-agent permissions,
model configuration, data exposure, and absence of paid fallback. Use one read-only
reviewer at a time; prohibit nested delegation, edits, external replies,
publication, and merge. Do not install an agent or change settings to enable it.

Pass the outcome, acceptance conditions, exact base/head, relevant working-tree
snapshot, findings ledger, and available rounds. Include affected callers and
contracts rather than only changed lines. The default is three review rounds
across self-review and delegated attempts per maintenance invocation. Failed or
unusable delegated attempts consume a round. Preserve the count across new heads,
comments, and resumed sessions; extensions require explicit authority.

If the optional reviewer is unavailable, report the limitation and continue
permitted owner work. If independent review is required, leave it blocked. Never
silently fall back to another account, proxy, API, or billing route. Worker success
is evidence to assess, not human approval or permission for another action.

## Forbidden delegation

- Do not delegate without user or host authorization.
- Do not assign multiple workers to edit the same owned files.
- Do not delegate irreversible publication, deletion, deployment, or merge decisions.
- Do not treat worker completion as verified integration.
- Do not parallelize work whose outputs depend tightly on earlier unfinished steps.

## Output

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Lead with the integrated result and anything that needs the user's decision. Then return `Delegation authority`, `Task map`, `Ownership`, `Evidence contract`, `Cost boundary`, `Worker results`, `Integration verification`, and `Unresolved decisions`. List a decision as unresolved only when it blocks remaining work; otherwise make the routine call, record it, and continue.

## Example

Synthetic example; not an observed client result.

Input: Two agents are authorized to review independent API and storage changes.

Output: Give each agent a distinct artifact and evidence contract, then reconcile findings against one revision. Keep shared edits with one owner.
