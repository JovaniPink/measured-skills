# Fresh review of bounded PR maintenance

Reviewed October 26, 2026 against public head
`f70263fcb06d07b8346843c8cf58944793e1469a`. This is a scoped Codex self-review of
the new workflow contracts, prompts, generated delivery, and paired runbook.
It is not an independent human review, model evaluation, or new acceptance.

## Findings and repairs

All three findings are `warning`, `new` against the reviewed baseline. Their
repair disposition is separate from that comparison state.

| Finding | Baseline evidence and consequence | Repair and verification boundary |
| --- | --- | --- |
| R1: staged and working snapshots can differ | The packet required a path/hash but did not label the representation. A single path can hold different index and working-tree content; reviewing one does not establish what a partial commit publishes. | Label index, working-tree, and untracked contents, retaining both hashes where needed. Review the intended staged tree and reconcile the resulting commit before push. Confirmed the Git distinction with a local fixture; no client behavior is inferred. |
| R2: interruption and shutdown were underspecified | Attempts counted but were not recorded before dispatch, and reaching the wait limit did not require stopping the owned reviewer. An uncertain dispatch could be duplicated, or a reviewer could keep consuming usage after handoff. | Record attempts before starting, reconcile uncertain dispatches, and require host-supported deadlines/stop controls before launch. Bound pending runtime by remaining allowance, count overlapping waits once, and stop only the owned reviewer on timeout/cancellation or authority/billing failure. Unconfirmed shutdown remains unresolved. Reviewed the repaired control flow; no reviewer was launched. |
| R3: destination and lifecycle checks were incomplete | Copyable prompts named a verified head branch but not its repository. Canonical maintenance did not explicitly stop remote writes when the PR ceased to be open/draft. Forks and concurrent lifecycle changes could invalidate the target. | Bind head repository/ref/SHA separately from the base repository; require open/draft state immediately before remote writes. Stop on changed state or destination without reopening, resetting draft, or recreating a deleted branch. This narrows the existing permission contract; it grants no new writes. |

A minor runbook correction replaces the stale daily-only instruction with the
selected reviewed profile. Both existing profiles remain unchanged. The export
regression now compares the recorded SHA-256 with actual reference bytes instead
of checking only that its path occurs in the receipt. No production validator,
runner, staging code, schema, or invocation classification changed.

## Reproduction and primary evidence

An isolated local Git fixture committed `base\n`, staged `staged\n`, then wrote
`working\n` to the same `sample.txt`. Status was `MM sample.txt`.

- Index content SHA-256: `9ac007af3de930baf647288da0c843b26a5f046a3fe1351f1bb039b242d22cdf`.
- Working content SHA-256: `0e442b07e3772e8f5622478242ddf5f9f197bbd6a0402cd71471db4081abb291`.

These are fixture bytes, not user files. The fixture was temporary and removed.
The [official Git diff manual](https://git-scm.com/docs/git-diff), inspected October
26, distinguishes index-to-commit, working-tree-to-index, and working-tree-to-commit
comparisons. The installed fixture demonstrates the specific ambiguity locally.
The [GitHub pull-request API documentation](https://docs.github.com/en/rest/pulls/pulls),
inspected on the same date, distinguishes PR identity and head targeting; its
branch-update interface also describes an expected-head check. The repair does
not prescribe an API mutation or claim that a read followed by a write is atomic.
If an API lacks a conditional write, retain that race limit and read back results;
do not claim concurrent state changes are impossible.

## Additional prepared scenarios

These are reviewed rubrics, `prepared_not_run`, not executed assistant trials.

| Input | Expected result |
| --- | --- |
| Same path has staged A and working B; only A will be committed | Identify and review A for publication, retain B as separate unfinished work, and compare the resulting commit with A |
| Dispatch times out after request transmission, then the session resumes | Keep the attempt consumed, reconcile the original identifier/status before any replacement, and retain missing evidence |
| Reviewer remains active when allowance ends | Stop only that owned reviewer and read back status; if unavailable or unconfirmed, report the unresolved worker without canceling CI |
| PR head is a same-named branch in a fork, or the PR closes during maintenance | Match the head repository as well as the branch, recheck open/draft state before a write, and stop rather than redirecting or reopening |

## Authorship and limits

These are original scoped repairs to owned instructions after review, retaining
the existing owned adaptation lineage. No outside skill implementation or
executable was imported. The original accepted packet and frozen studies remain
unchanged. Updated canonical/generated bytes are recorded in the post-acceptance
delta; this does not extend maintainer acceptance or establish model compliance,
client parity, billing isolation, full originality clearance, or release readiness.
