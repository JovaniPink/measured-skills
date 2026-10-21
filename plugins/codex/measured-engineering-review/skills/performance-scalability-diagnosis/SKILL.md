---
name: performance-scalability-diagnosis
description: "Diagnoses a slow or overloaded system when asked why latency, throughput, or resource use changed; compares measurements and hypotheses without silently optimizing code."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-engineering-review"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Performance and Scalability Diagnosis

Use [Google SRE monitoring guidance](https://sre.google/sre-book/monitoring-distributed-systems/) for operational signals. The diagnosis and capacity workflow below is this catalog's review contract; neither the reference nor a signal alone proves a cause or scaling limit.

## Workflow

1. Define the affected journey, workload, percentile, units, environment, time window, and expected objective.
2. Capture a reproducible baseline and separate client, network, queue, service, datastore, and dependency time.
3. Form competing hypotheses for latency, saturation, allocation, locking, retries, fan-out, and load amplification.
4. Use profiles, traces, query plans, metrics, and controlled load evidence to discriminate among hypotheses.
5. Identify the first constrained resource and whether the limit is per request, per instance, or shared.
6. Estimate headroom and scaling behavior with explicit assumptions; distinguish measurement from extrapolation.
7. Recommend the smallest experiment or remediation capable of falsifying the diagnosis.

## Boundaries

- Do not optimize from averages alone when tail behavior matters.
- Do not run load tests against shared or production systems without explicit authorization and safeguards.
- Do not claim scalability from a single local benchmark or an unrepresentative fixture.

## Output

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return Symptom, Baseline, Hypotheses, Measurements, Causal diagnosis, Capacity estimate, and Next experiment.

## Example

Synthetic example; not an observed client result.

Input: Latency doubled, but no comparable load or tracing data is available.

Output: The regression is reported, not localized. Establish comparable workload and stage timings before choosing an optimization.
