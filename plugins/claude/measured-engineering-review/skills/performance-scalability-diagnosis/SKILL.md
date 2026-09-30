---
name: performance-scalability-diagnosis
description: Diagnose latency, throughput, resource, contention, and scalability problems using measured evidence and competing hypotheses. Use when a system is slow, unstable under load, or approaching a capacity boundary; do not silently optimize code.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.17.1"
  plugin: "measured-engineering-review"
  invocation: "implicit"
  provenance: "clean-room"
  risk_class: "read-only"
---

# Performance and Scalability Diagnosis

Use current primary guidance as a review baseline, then report only what the available evidence supports. Primary authority: [official reference](https://sre.google/sre-book/monitoring-distributed-systems/).

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

Return Symptom, Baseline, Hypotheses, Measurements, Causal diagnosis, Capacity estimate, and Next experiment.

