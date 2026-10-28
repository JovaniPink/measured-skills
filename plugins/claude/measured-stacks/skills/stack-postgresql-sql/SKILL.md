---
name: stack-postgresql-sql
description: "Reviews PostgreSQL schemas, queries, indexes, transactions, and migrations when database changes need focused checks; does not mutate shared data merely to validate a proposal."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.19.0"
  plugin: "measured-stacks"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# PostgreSQL and SQL Engineering Profile

Use this profile only after repository discovery identifies the stack. Read [focused checks](references/checks.md) when stack-specific gates or hazards determine the result.

## Workflow

1. Discover migration directories, schema definitions, SQL files, database test harnesses, version declarations, and repository scripts.
2. Follow repository-defined commands and pinned tool versions before suggesting defaults.
3. Review idiomatic design and material hazards, especially null semantics, implicit casts, transaction boundaries, lock duration, deadlocks, write amplification, missing indexes, unstable ordering, timezone errors, and privilege escalation.
4. Select proportionate gates from repository migration checks, parsing or linting, disposable-database tests, query-plan inspection, reconciliation checks, and rollback exercises when configured and authorized.
5. Review compatibility across PostgreSQL version, extension availability, online schema-change behavior, client drivers, replicas, generated columns, constraints, and data backfills.
6. Report every missing tool, skipped command, unsupported platform, or unavailable environment as incomplete rather than passing.

## Boundaries

- Do not invent one universal command or replace repository policy with generic preferences.
- Do not install, upgrade, publish, deploy, apply, or mutate shared state merely to run a gate.
- Separate static review, executed checks, build evidence, provider state, and live behavior.

## Output

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return Discovery, Hazards, Commands selected, Results, Compatibility, Missing evidence, and Next safe gate.

## Example

Synthetic example; not an observed client result.

Input: A new index is proposed for a slow query without its plan or workload.

Output: Index benefit is unverified. Inspect the query plan and write workload before recommending the index; do not alter shared data to test the idea.
