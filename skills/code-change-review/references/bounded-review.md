# Bounded review

Use this protocol when the user requests repeated review of one identified
change. It does not turn a findings-only review into authority to edit, delegate,
post replies, push, or merge. The implementing owner handles authorized repairs
between review passes. Self-review is the default and is not independent review.

## Pin the packet

Record the outcome, acceptance conditions, repository and PR when supplied, exact
base and head revisions, intended diff scope, and existing authorization. Include
relevant staged, unstaged, and untracked work. A committed diff does not include
those changes. Identify relevant uncommitted file contents by path and SHA-256;
record deletions and relevant file modes separately. Do not collect unrelated
files, credentials, or private logs. A pasted diff supports only its stated scope.

Keep the snapshot stable during each pass. If files or the remote head change,
identify what the reviewer actually saw and reconcile before using the result.
Read affected callers, contracts, tests, configuration, and generated boundaries.
An unchanged line can carry the consequence of a changed assumption.

## Spend the review budget deliberately

- The default is three review rounds per maintenance invocation, including
  self-review and delegated attempts. A failed or unusable delegated attempt
  consumes one round; preflight discovery without launching does not.
- Round one covers the full identified change. Later rounds cover the delta,
  open findings, and surrounding behavior affected by the repair.
- The owner records each accepted repair and its checks. Reviewers return
  findings only; they do not modify the code they are reviewing.
- Stop a review cycle when no actionable findings remain. This does not clear
  required tests, other approvals, or later findings from new evidence.
- Evaluate documentation, naming, and configuration findings by their effects.
  Decline unsupported or out-of-scope suggestions with evidence, not by category.
- A new revision, new comment, interruption, or resumed session does not reset
  the allowance. Carry used and remaining rounds in the continuation record.
- Extend only with explicit additional authority. Risk alone does not permit
  extra rounds. On exhaustion, retain open findings and unreviewed repairs;
  do not claim that a final repair passed review without another available round.

## Optional independent review

Only launch a separate reviewer when delegation is explicitly authorized and the
actual host, effective permissions, model configuration, data exposure, and absence
of paid fallback are verified. Use one read-only reviewer at a time. No nested
reviewers, edits, external replies, publication, or merge are permitted. Do not
substitute a proxy, API, model, or account if the approved route is unavailable.

Continue authorized owner work when this optional lane is unavailable and say so.
If the task requires independent review, its absence remains a blocker. A separate
model is not independent human approval and does not remove correlated blind spots.

## Preserve findings and limits

Keep stable finding IDs, location and reviewed snapshot, the claim and conditions,
severity and finding state, disposition, evidence, repair revision, and verification.
Use the existing severity/state vocabulary. Track disposition separately as
accept, reject, defer, clarify, or already addressed. A rejected finding can reopen
when new evidence changes its premise; preserve the earlier decision and reason.

Report reviewed revision or snapshot, self/independent review mode, actual reviewer
identity when known, rounds used/remaining, unresolved findings, and coverage
limits. Never invent a model identity. A model verdict is not human approval.
