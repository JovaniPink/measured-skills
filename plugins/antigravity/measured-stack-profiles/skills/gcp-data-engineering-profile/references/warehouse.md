# Warehouse and transformations

Primary authorities reviewed 2026-10-20:
[BigQuery computation](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute),
[dbt incremental models](https://docs.getdbt.com/docs/build/incremental-models), and
[Dataform tables](https://docs.cloud.google.com/dataform/docs/create-tables).
Use the project's installed versions for version-sensitive recommendations.

## BigQuery

- Inspect selected columns, partition predicates, join cardinality, and intermediate data volume. A query plan can identify the stage that expands data; it does not establish why without the relevant inputs.
- Evaluate partitioning and clustering against actual filters and distribution. Do not prescribe a universal key or claim fewer scanned bytes without comparable evidence.
- Separate query shape from slot contention and reservation configuration. State which observations support a capacity diagnosis before recommending capacity changes.
- Querying job metadata is provider access too. Prefer supplied redacted plans during local review; request only the missing evidence needed for an authorized diagnosis.
- A supplied plan without a partition filter supports a finding about that plan. Check the full query and partition definition before claiming every execution scans the whole table; missing bytes and cache observations remain unknown.
- Pruning is an optimization constrained by correctness. A bounded partition predicate is a candidate only when the source and target scans still cover the accepted correction and replay contract; do not require a narrower scan merely to make the plan prune.

## Incremental contracts

- Define row grain and the uniqueness property before choosing a merge key. A configured unique key is not proof that source and target values are unique.
- Test initial build, repeated batch, late updates, null keys, duplicate keys, and schema changes. Record the intended result for each case before selecting a materialization.
- In dbt, distinguish the incremental filter from the adapter's update strategy and full-refresh behavior. Inspect macros and hooks before assuming compilation or testing is local.
- In Dataform, inspect the incremental condition, unique-key configuration, dependencies, assertions, and full-refresh behavior. A passing assertion covers its defined predicate, not the entire business meaning.
- Reconciliation needs source identity, expected totals or keys, and a defined comparison window. Matching one aggregate can hide lost or duplicated rows.
- Distinguish event time, original ingestion time, correction arrival time, and the run's date/timezone. An arrival-date filter may include a late correction today. A skipped-run risk is conditional on schedules, replay, and backfill policy; do not assert permanent loss when those are unknown.
- Do not infer `MERGE` from `unique_key` alone. Inspect the adapter, strategy, and compiled operation. Duplicate source matches can fail an updating BigQuery merge; other strategies and insert-only cases have different behavior.
- Keep a finding, a hypothesis, and an untested repair separate. Do not supply executable-looking SQL or a required window, key, or deduplication rule before resolving grain, tie-breaking, timestamp meaning, event-age bounds, and recovery contracts. Name the missing decisions instead.

## Correction-window decision order

1. Record what the supplied filter and plan actually show. Keep "correction coverage unverified" distinct from a demonstrated exclusion or loss; use the same qualification in headings and the verdict.
2. Define the clocks separately: event occurrence, original ingestion, correction authoring, correction delivery, and scheduled/retried run. "Two days late" needs a reference clock; it does not automatically mean every corrected event is at most two days old.
3. Establish the oldest event that may be corrected and the missed-run/replay requirement. A delivery-delay limit alone cannot justify a finite event-time lookback or an arbitrary margin. If eligible corrections have no event-age bound, a finite lookback needs a separately accepted path for older corrections; otherwise it can discard valid input.
4. Inspect grain, update strategy, and source/target match semantics before choosing keys or tie-breakers. A target-side pruning predicate can also affect which existing rows match, so a performance change needs a correctness check for older records.
5. Only then compare candidate predicates and their scan behavior using supplied evidence or separately authorized checks. Without those contracts, return a readiness limit and the next contract question, not a mandatory repair.
