# Pipeline execution boundaries

Primary authorities reviewed 2026-10-20:
[Cloud Storage metadata](https://docs.cloud.google.com/storage/docs/metadata),
[Dataflow exactly-once processing](https://docs.cloud.google.com/dataflow/docs/concepts/exactly-once),
[Spark SQL performance](https://spark.apache.org/docs/latest/sql-performance-tuning.html),
[managed Spark image versions](https://docs.cloud.google.com/managed-spark/docs/concepts/versioning/image-version-lists), and
[Airflow best practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html).
These current pages do not establish the versions installed in a project.

## Storage and streaming

- Distinguish an object name from its generation and metadata revision. Preserve the identity needed to reproduce a read; do not treat a mutable staging path as immutable source evidence.
- Locate schema interpretation and source retention decisions separately from compute jobs. Deleting staging data may remove evidence or break replay.
- Inspect the selected Dataflow streaming mode and Apache Beam SDK version, event identity, watermark/window policy, late-data thresholds, emission triggers, and sink guarantees. Exactly-once pipeline processing does not make arbitrary external side effects execute once.
- Test duplicate delivery, late records, worker retry, partial sink failure, and replay through isolated fixtures before proposing a live recovery action.

## Spark and orchestration

- Discover the Dataproc or managed Spark image and its component versions. Inspect physical plans, partition sizes, shuffle, skew, and spill before tuning executor resources or join strategy.
- Discover the actual Composer environment, Airflow version, providers, and DAG configuration. Do not apply current upstream defaults to an older managed environment.
- Review tasks as repeatable operations over a defined data interval. Avoid dependence on an unrecorded current time or mutable input selection when rerunning a task.
- Trace retries, concurrency, catchup, and backfill scope through the sink. A scheduler retry can duplicate external effects even when the task code is unchanged.
- Treat credentials, job submission, scheduler changes, backfills, and cleanup as separately authorized actions. Report recovery proposals with expected results and a stopping condition.
