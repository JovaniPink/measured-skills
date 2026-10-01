---
name: operational-readiness-review
description: Review whether a service or application is operationally ready for release and sustained ownership. Use for read-only assessment of objectives, dependencies, monitoring, alerts, capacity, failure handling, incidents, runbooks, recovery, and support boundaries.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-engineering-review"
  invocation: "implicit"
  provenance: "clean-room"
  risk_class: "read-only"
---

# Operational Readiness Review

Use current primary guidance as a review baseline, then report only what the available evidence supports. Primary authority: [official reference](https://sre.google/sre-book/monitoring-distributed-systems/).

## Workflow

1. Define critical journeys, service objectives, owners, support hours, dependencies, and failure budgets.
2. Review deployment, configuration, capacity, rate limits, queues, retries, timeouts, backpressure, and graceful degradation.
3. Assess logs, metrics, traces, dashboards, symptom-based alerts, escalation, and runbook actionability.
4. Review backup, restore, disaster recovery, regional or dependency failure, and data reconciliation evidence.
5. Inspect incident roles, communication paths, severity rules, status updates, and learning processes.
6. Verify rollback, feature control, canary, deploy markers, and post-release observation plans.
7. Classify each readiness item as proven, partial, blocked, or not applicable with evidence.

## Boundaries

- Do not infer live readiness from a local build or passing repository checks.
- Do not claim backup recovery without an observed restore test.
- Do not deploy, page responders, change provider settings, or declare go without separate authority.

## Output

Return Objectives and ownership, Failure readiness, Observability, Recovery, Incident response, Blockers, and Go or no-go decision needs.

