---
name: review-data-migration
description: "Reviews migration readiness when asked if a schema change, backfill, or cutover is safe; checks compatibility, reconciliation, and rollback without executing the migration."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.19.0"
  plugin: "measured-quality"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Data Migration Readiness

Use [Google SRE monitoring guidance](https://sre.google/sre-book/monitoring-distributed-systems/) for monitoring concepts. The migration, reconciliation, and rollback checks below are this catalog's review contract; that chapter does not establish their completeness or approve a migration.

## Workflow

1. Identify authoritative data, owners, writers, readers, projections, retention, and legal or policy constraints.
2. Define source and target schemas, transformations, keys, defaults, null behavior, ordering, and conflict rules.
3. Review compatibility across expand, backfill, dual-read or dual-write, cutover, contraction, and cleanup phases.
4. Specify volume, duration, throttling, retry, idempotency, checkpoint, and resumability assumptions.
5. Define reconciliation totals, invariants, sampling, error quarantine, and exact acceptance thresholds.
6. Design rollback or roll-forward behavior for code, schema, state, and partially migrated records.
7. Name decision owners, go or no-go gates, monitoring, and post-cutover evidence.

## Boundaries

- Do not declare a source or target authoritative without ratified evidence.
- Do not run migrations, enable writers, or change production state without separate authorization.
- A successful dry run does not prove production duration, contention, or rollback safety.

## Output

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return Authority map, Migration phases, Compatibility, Reconciliation, Failure handling, Rollback, and Decision gates.

## Example

Synthetic example; not an observed client result.

Input: A migration drops a column still read by the current application.

Output: Not ready: the deployed reader still depends on the column. Establish a compatible transition and recovery evidence before removal.
