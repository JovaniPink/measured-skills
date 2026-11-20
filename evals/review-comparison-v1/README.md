# 3-Arm Code Review Comparison Kit (`review-comparison-v1`)

**Status:** `prepared_not_run` (`execution_authorized: false`). This kit defines a
small, fair, paired comparison to test which layer of Measured Skills actually
contributes value on code review before investing in runtime automation.

## Research question

On identical repository snapshots, model configuration, tool permissions, and
resource limits, does adding structured request framing (`structured_request`)
or selected Measured skills (`structured_plus_skills`) improve valid findings,
reduce false positives and unsupported severity claims, or reduce human
verification effort compared with an ordinary review request
(`ordinary_baseline`), at acceptable time and token cost?

## Three matched arms

| Arm ID | Condition | What it isolates |
| --- | --- | --- |
| `ordinary_baseline` | Short review prompt commonly used today (`"Review this diff for bugs, regressions, and risks. Do not edit files."`) with no skills installed | Practical baseline |
| `structured_request` | Measured's current copied `Review a change` ordinary request with no skills installed | Contribution of request structure alone |
| `structured_plus_skills` | Same structured task with selected Measured skills installed (`review-code-change`, plus an optional stack skill only when relevant to the case) | Incremental contribution of the skill layer |

Record both the assigned arm and whether the skill actually loaded in each run.
Failed activation is a workflow outcome and remains visible in the summary.

## Eight compact cases

| Case ID | Category | Primary judgment tested |
| --- | --- | --- |
| `rc-01-missing-tenant-scope` | Real defect | Detecting cross-tenant lookup exposure when store is unscoped |
| `rc-02-auth-enforced-below` | Cleared false alarm | Checking lower repository layer and clearing handler refactor |
| `rc-03-idempotent-retry` | Cleared false alarm | Clearing duplicate-write lead via stable key, unique constraint, and conflict handler while keeping rollout caveat |
| `rc-04-tautological-test` | Test-quality defect | Catching a passing test that mocks out the validator under test |
| `rc-05-mixed-version-rollout` | Rollout defect | Catching N-1 / N schema skew across producer and consumer |
| `rc-06-caller-outside-diff` | Cross-boundary defect | Reading callers outside changed lines when a helper return shape changes |
| `rc-07-clean-refactor` | Clean control | Avoiding false alarms and reviewer workload on a behavior-preserving change |
| `rc-08-missing-store-contract` | Insufficient evidence | Keeping exposure conditional and reporting an explicit coverage gap when store code is absent |

## Six preserved measures

Do not collapse tradeoffs into a single composite score. Report all six
dimensions separately across the three arms:

1. Valid, material findings retained after blinded adjudication against case oracles.
2. False positives and unsupported severity claims.
3. Missed known defects.
4. Human effort required to verify or reject findings.
5. Completion time, turns, token usage, and reported cost.
6. Blocked outcomes, uncertainty/coverage-gap reporting, and scope violations.

## Offline commands (zero model calls)

```sh
python3 scripts/review_comparison.py --check
python3 scripts/review_comparison.py --materialize rc-01-missing-tenant-scope /tmp/rc-01-view
python3 scripts/review_comparison.py --lint-receipts PRIVATE_RECEIPTS.json
python3 scripts/review_comparison.py --summarize PRIVATE_RECEIPTS.json
```

`--lint-receipts` checks **structural completeness only** (hashes, arm
identities, 5-dimension state invariants, and evidence links). It does not
verify finding truth or review quality. Raw model receipts stay outside the
repository per `evals/AGENTS.md`.

## Authorization and Phase 5 gate

There is intentionally no `--run` option or model subprocess in this kit.
Running live arms requires explicit owner authorization naming the client,
model, repetitions, and budget ceiling. Any thin local review-state adapter
remains deferred until observed comparison results show recurring failures to
preserve revisions, finding IDs, coverage gaps, or stopping bounds.
