# Focused checks

Primary documentation: [official PostgreSQL and SQL Engineering Profile reference](https://www.postgresql.org/docs/current/). Verify version-sensitive behavior against the repository's pinned toolchain.

## Discovery

Inspect migration directories, schema definitions, SQL files, database test harnesses, version declarations, and repository scripts. Resolve nested modules, workspaces, generated sources, and CI commands before selecting gates.

## Judgment focus

Review null semantics, implicit casts, transaction boundaries, lock duration, deadlocks, write amplification, missing indexes, unstable ordering, timezone errors, and privilege escalation.

## Gate families

Consider repository migration checks, parsing or linting, disposable-database tests, query-plan inspection, reconciliation checks, and rollback exercises when configured and authorized. Run only commands supported by repository evidence and the current authorization boundary.

## Compatibility

Check PostgreSQL version, extension availability, online schema-change behavior, client drivers, replicas, generated columns, constraints, and data backfills. Record unavailable tools and environments explicitly; never manufacture a passing result.

