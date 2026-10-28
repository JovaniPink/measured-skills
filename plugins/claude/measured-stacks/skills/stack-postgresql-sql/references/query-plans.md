# Diagnose a supplied query plan

Authority: [PostgreSQL 18 EXPLAIN](https://www.postgresql.org/docs/18/sql-explain.html),
reviewed 2026-10-28. Discover the actual engine/version before applying this advice.

Record query text and parameters, schema/index definitions, data distribution,
statistics freshness, workload/concurrency, and whether the plan is estimated or
executed. Missing inputs remain unknown. Planner costs are relative estimates,
not milliseconds or money. Estimated rows and actual rows answer different questions.

Trace row-count expansion, repeated loops, filtering, sort/hash spill, scan choices,
and relevant buffer observations. Check predicates and cardinality before proposing
an index or join rewrite. A sequential scan can be appropriate. A plan alone cannot
establish lock contention; use supplied lock/wait evidence for that hypothesis.

EXPLAIN ANALYZE executes the statement. A rollback can leave sequence increments,
external effects, resource use, or locks during execution; wrapping it in a
transaction is not blanket safety. Even an estimated plan requires database access
and resources. Read-only diagnosis uses supplied plans by default and does not
permit a live query, index change, cancellation, or provider spending.

Return the observed bottleneck, competing explanations, smallest discriminating
check, and correctness risks. Compare proposed changes on the same workload when
a separately authorized environment is available.

Synthetic example: an inner join shows many loops and a row estimate far below
observed rows. That supports investigating statistics and predicate selectivity;
it does not by itself prove a missing index or authorize an index build.
