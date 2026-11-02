# Review a replay or backfill before running it

Authority: [Airflow best practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html).
Reviewed 2026-10-28; the inspected stable documentation was 3.3.2. Discover actual
scheduler, provider, SDK, and storage versions before choosing mechanics.

Identify immutable source versions, requested interval/timezone, row grain, keys,
correction semantics, and the intended sink result. Separate original event time,
arrival, correction arrival, and scheduler interval. Do not invent a correction
window from an example. Preserve the warehouse reference's clock decision order.

Trace a first run, identical retry, late correction, partial sink commit, and resume
from a checkpoint. Inspect deduplication, upsert/delete semantics, watermark/state,
dead-letter replay, schema evolution, concurrent writers, and external side effects.
A scheduler retry or exactly-once processing claim does not prove sink idempotency.

Use local fixtures and supplied plans to reconcile keys, counts, totals, and sampled
values over the defined interval. Matching aggregate totals can hide missing and
duplicate records. Define expected differences before evaluating the result.

Record capacity/cost constraints, rollback/recovery limitations, owner, and abort
conditions. A rollback of code does not restore overwritten data or retract an
external notification. This review does not authorize querying metadata, provider
dry runs, job submission, replay, backfill, cleanup, IAM, or deployment.

Synthetic example: a retry repeats the same interval after committing half its
rows. A keyed fixture can reveal duplicate writes; it cannot qualify live sink
behavior, race conditions, or the cost of a production backfill.
