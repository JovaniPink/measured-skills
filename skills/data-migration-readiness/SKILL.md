---
name: data-migration-readiness
description: Review a proposed data or schema migration for authority, compatibility, sequencing, reconciliation, rollback, and operational evidence. Use before a migration or cutover; do not execute or ratify the migration.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.17.1"
  plugin: "measured-engineering-review"
  invocation: "implicit"
  provenance: "clean-room"
  risk_class: "read-only"
---

# Data Migration Readiness

Use current primary guidance as a review baseline, then report only what the available evidence supports. Primary authority: [official reference](https://sre.google/sre-book/monitoring-distributed-systems/).

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

Return Authority map, Migration phases, Compatibility, Reconciliation, Failure handling, Rollback, and Decision gates.

