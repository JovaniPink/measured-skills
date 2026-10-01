---
name: postgresql-sql-engineering-profile
description: Apply focused PostgreSQL and SQL engineering judgment after repository gate discovery. Use for schemas, queries, transactions, migrations, indexing, compatibility, and database test concerns; never mutate shared data merely to validate.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-stack-profiles"
  invocation: "implicit"
  provenance: "clean-room"
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

Return Discovery, Hazards, Commands selected, Results, Compatibility, Missing evidence, and Next safe gate.

