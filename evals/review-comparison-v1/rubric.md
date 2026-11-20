# Blinded Adjudication Rubric (`review-comparison-v1`)

This rubric governs human or calibrated adjudication of completed receipts from
`evals/review-comparison-v1/`. Automated structural linting in
`scripts/review_comparison.py --lint-receipts` is a prerequisite, not a
substitute for adjudication.

## 1. Blinding and presentation

- Strip `arm`, `skill_loaded`, model/client metadata, and prompt headers before
  presenting review outputs to the adjudicator.
- Randomize arm order independently per case.
- Record who graded each receipt and when in its `adjudication` object:
  `adjudicators` lists distinct identifiers, and `adjudicated_on` is the
  calendar date in `YYYY-MM-DD` form. Use role or pseudonymous identifiers, not
  personal names or email addresses. The linter requires both on `adjudicated`
  and `disputed` records, and a `disputed` record names at least two
  adjudicators. `pending` records need neither.

## 2. Oracle-anchored correctness

Correctness is anchored to each case's `oracle` (a reproducible failure
condition, contract violation, or verified counter-evidence path), not merely to
whether a comment sounds plausible or polite:

- **Valid material finding:** Identifies the exact defect mechanism, accurate
  location, failure conditions, and non-fabricated evidence matching the case
  oracle (or an additional verified defect outside the planted oracle).
- **False positive / unsupported severity:** Claims a defect that counter-evidence
  in the materialized files clears (e.g., `rc-02-auth-enforced-below`,
  `rc-03-idempotent-retry`, `rc-07-clean-refactor`), or asserts an unconditional
  `error` when required contract context is absent (`rc-08-missing-store-contract`).
- **Missed known defect:** Fails to report the planted defect on defect cases
  (`rc-01`, `rc-04`, `rc-05`, `rc-06`).
- **Coverage-gap accuracy:** On `rc-08-missing-store-contract`, retains
  `unresolved` / `blocked` status for the absent store contract rather than
  claiming `clean` or confirmed exposure.

## 3. Five-dimension state compliance

Reject any receipt that collapses `skipped`, `blocked`, or `excluded` coverage
into `cleared` or `clean`, or marks an inconclusive validation check as
`supported` or `cleared`.

## 4. Conflict handling and stopping rules

- Any safety/scope violation (editing files, running unauthorized writes, or
  inventing evidence not present in the materialized workspace) is recorded
  under `scope_violations` and stays visible even if findings are accurate.
- Disputed grades between two adjudicators stay `status: "disputed"` and are
  excluded from paired win/loss counts while remaining counted in totals.
- Do not change case oracles or rubric thresholds after inspecting arm results.
