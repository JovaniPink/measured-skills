# Data workflow pack proposal

Status: proposal only. The 0.18.0 candidate adds one generic GCP stack profile
inside the existing stack pack. It adds no data workflow pack.

A future pack could separate three reusable capabilities:

| Capability | Contract | Evidence needed before authoring |
| --- | --- | --- |
| Transformation review | Review grain, keys, incremental behavior, schema evolution, and reconciliation | Independent cases that exceed existing SQL and GCP review coverage |
| Pipeline diagnosis | Localize batch or stream failures across source, processing, and sink | Reproducible failures and distinct routing from general diagnosis |
| Orchestration reliability | Review retries, intervals, concurrency, and backfills | Representative scheduler cases and a clear boundary from operations review |

Keep generic review semantics public and local identities, data contracts, and
approval owners in their owning private context. Do not turn this proposal into
a product-specific workflow, new tool permission, or executable payload.

Before creating a pack, demonstrate a distinct capability, define near misses,
review primary authorities, and test whether the smaller profile already serves
the need. Installation, live data access, behavioral trials, and release remain
separate decisions. No version or delivery date is assigned here.
