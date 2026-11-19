# Follow a change through review

Start with your role in the change: prepare it, review it, or address its feedback.
Copy one request below, replace the bracketed details, and paste it into your
assistant. These requests need no skill installation. Each asks for an inspection
and a prepared result; it does not edit code or send a message.

Use the [chooser](../dist/discovery/guide.md) for these tasks and their scopes.
Choose only the guidance needed for the question. The skills linked here are
optional support, not a sequence every change must follow.

Use [code review as part of the delivery system](review-systems-thinking.md) for
review capacity, shared understanding, and outcome measures. For changes to
prompts, rubrics, tools, or retries, use [the feedback-loop audit](prompt-feedback-loops.md)
to examine runtime recovery and learning across versions separately.

## Prepare a change for review

Choose **Prepare a change for review** when you are the author. Give the reviewer
the intended outcome, the exact change, and the evidence already available. A
useful packet makes the highest-risk questions easy to inspect. It does not call
an unrun check a pass or an author's self-review an independent review.

```text
Prepare a review packet for [repository and PR, or a local change].
The intended outcome and constraints are [brief description or issue].
Identify the base and head revisions. If I requested a local change, identify
the relevant staged, unstaged, and untracked contents separately; exclude
unrelated work. Explain the approach, user-visible effects, system dependencies,
and excluded work. Inspect existing check evidence and say which revision it
supports. List untested risks and focused questions for the reviewer.
Prepare the packet only: do not edit, run checks, send it, or request reviewers.
```

Optional guidance: [request-review](../skills/request-review/SKILL.md). Its packet
can include a working-tree snapshot when that is the requested scope. A named PR
packet concerns that PR's committed comparison, unless local work was also requested.

## Review a change

Choose **Review a change** when the result you need is findings about a diff.
Start from the intended behavior, then inspect enough context to establish each
failure condition. A changed line, an unrun test, or an unfamiliar implementation
is a lead to inspect; each alone is insufficient evidence of a defect.

```text
Review [repository and PR, exact base-to-head comparison, or pasted diff].
The intended behavior and constraints are [description or linked requirement].
Pin the supplied comparison. Review only that PR or diff; do not add local
working-tree changes unless I requested them. Inspect relevant callers, data
contracts, authorization, retry paths, and existing tests as needed.
For each actionable finding, give its location, impact, failure conditions,
and evidence. Keep unresolved assumptions conditional in the headline and verdict.
Separate observed test results from proposed assertions and static predictions.
State the inspected boundary and remaining gaps. Do not edit, run checks,
launch reviewers, post comments, approve, or merge.
```

Optional guidance: [review-code-change](../skills/review-code-change/SKILL.md).
Choose **Explain this PR and check its scope** if you first need an inventory and
an assessment against the approved work. That mode is described in
[the getting-started guide](start.md#explain-a-pr-before-judging-its-scope).

## Address review feedback

Choose **Address review feedback** when you are the author or maintainer deciding
what to do with comments. Reviewers can miss context; authors can miss defects.
Check the technical premise before accepting or rejecting a comment. Preserve
the earlier reason if new evidence later changes that decision.

```text
Assess the review feedback for [repository and PR or supplied comments].
Identify the reviewed revision and the current revision. Read all relevant
comments and threads, noting incomplete access or pagination. For each claim,
inspect the current code, contract, and existing evidence. Classify it as accept,
reject, defer, clarify, or already addressed, with a reason.
Keep stable finding IDs, the reviewer's claim, its conditions, any repair revision,
and observed verification together. Propose the smallest repair and relevant
verification for accepted findings. Prepare concise replies and identify only
decisions that block the remaining work. Do not edit, run checks, send replies,
resolve threads, approve, or merge.
```

Optional guidance: [address-review](../skills/address-review/SKILL.md). For conflicting
reviews, [consolidate-findings](../skills/consolidate-findings/SKILL.md) can compare
their evidence without treating agreement as proof.

When you want to implement the accepted changes, choose **Finish existing work**
and the local repair or draft PR scope in [the finish-work guide](finish-existing-work.md).
Carry forward the dispositions instead of restarting the review. A local repair
does not prove that a remote PR contains it. Record the repair revision and the
relevant verification before treating a finding as addressed.

## Trace the system around the diff

A review should follow the failure path as far as the claim requires. An interface
can have several consumers; a retry can cross a transaction boundary; an upgrade
can leave old and new clients active together. Inspect those relationships before
judging the change from its file count or local tests alone.

| Question | Evidence to inspect | Optional guidance |
| --- | --- | --- |
| What behavior should change, and what must remain true? | Requirement, current contract, and chosen scope | [frame-problem](../skills/frame-problem/SKILL.md) |
| Who or what can be affected? | Callers, events, shared data, caches, jobs, and upgrade order | [assess-change-impact](../skills/assess-change-impact/SKILL.md) |
| Does the proposed change violate that contract? | Control flow, failure conditions, permissions, and compatible versions | [review-code-change](../skills/review-code-change/SKILL.md) |
| Could the checks detect the claimed regression? | Observable assertions, fixtures, isolation, and relevant failure cases | [review-tests](../skills/review-tests/SKILL.md) |
| Does the evidence cover the repaired change? | Exact revision, check setup, result, and remaining gaps | [verify-claims](../skills/verify-claims/SKILL.md) |
| What should the next change address? | Dated outcomes, baseline, population, and confounding factors | [learn-after-launch](../skills/learn-after-launch/SKILL.md) |

Choose **Assess system impact** when tracing these dependencies is the main task.
Separate confirmed effects, possible effects, and concerns cleared by inspection.
An untraced consumer remains a gap. It need not become a speculative defect or a
reason to expand a bounded review indefinitely.

## Worked example: a retry that might duplicate work

This example is synthetic. The files, contracts, and observations below illustrate
a review; they are not results from this repository or an executed client task.

Suppose a patch retries `create_export(request_id)` after a timeout. The function
inserts an export request into a database. A timeout can leave the caller unsure
whether the first insert committed.

**Initial concern:** "Retries may create duplicate export requests if the request
identity or store does not prevent duplicate inserts." The patch alone does not
establish those conditions. Calling it a confirmed duplicate-write defect would
skip the most important inspection.

In this fictional follow-up, the supplied source shows all of these controls:

- The retry reuses the same request ID and tenant ID.
- The schema requires a unique `(tenant_id, request_id)` pair.
- The conflict path returns the existing export request.
- This function has no additional side effect outside that insert.

With those controls, the duplicate-row concern is cleared for that source path
under the stated schema contract. Do not require a new deduplication layer merely
to satisfy the original comment. Whether the constraint is applied in a deployed
database and whether another consumer can repeat an external effect remain
separate questions. Inspect them if the requested rollout review includes them.

| Evidence state | What the example supports |
| --- | --- |
| Proposed assertion | After a committed insert whose response is lost, retrying the same request should return the original identity and leave one stored request. |
| Static prediction | With the stable identity, unique constraint, and conflict path above, the retry should satisfy that assertion. Without those controls, the prediction changes. |
| Executed result | None. No test was run in this example, and no claim is made about whether an existing test covers it. |
| Useful next check | Inspect existing coverage for the ambiguous timeout and concurrent retries. If execution is authorized and that behavior remains unverified, run or add a focused test. |

The resolution records the cleared concern and its evidence, then stops that line
of repair. If later evidence shows that an old schema lacks the constraint, reopen
the claim with that condition and retain the earlier disposition. This is how
review improves the shared model of the system rather than accumulating comments.

## Close the feedback loop after release

Review, repair, verification, approval, merge, deployment, and measured outcomes
are separate states. Carry the purpose and remaining risks forward so later
observations can test the assumptions behind the change.

For the fictional retry, possible measures include duplicate durable requests per
accepted request and recovery failures per retried request, within a named time
window and version population. Define the baseline, exclusions, and data limits
before judging improvement. A lower error count could reflect lower usage; a
green deployment alone does not establish that users recovered successfully.

Choose **Learn after a release** to compare actual observations with the intended
outcome. Use [measure-outcomes](../skills/measure-outcomes/SKILL.md) when the measure
itself needs definition. Let supported findings inform the next requirement,
focused check, or operational change. Keep uncertain attribution visible and
avoid adding work once the authorized result is complete.

These requests and examples describe a process. They do not establish measured
benefit or client parity for Measured Skills. The [preview evidence](client-candidate-v0.19.0.md)
records which sources and client setups have actually been observed.
