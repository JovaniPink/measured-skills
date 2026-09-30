---
name: observability-design
description: Review or design observability for services and applications using logs, metrics, traces, alerts, and user-impact signals. Use when operators need to detect, explain, and respond to failures without confusing telemetry volume with operational understanding.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.17.1"
  plugin: "measured-engineering-review"
  invocation: "implicit"
  provenance: "clean-room"
  risk_class: "read-only"
---

# Observability Design

Use current primary guidance as a review baseline, then report only what the available evidence supports. Primary authority: [official reference](https://opentelemetry.io/docs/concepts/signals/).

## Workflow

1. Identify critical user journeys, service objectives, dependencies, failure modes, and decision owners.
2. Define logs, metrics, and traces that answer distinct operational questions and share useful correlation context.
3. Specify event names, dimensions, units, cardinality bounds, sampling, retention, privacy, and redaction.
4. Design dashboards around user impact, traffic, errors, latency, saturation, and dependency health as applicable.
5. Define alerts with symptoms, thresholds or burn behavior, ownership, runbook links, and expected action.
6. Cover deploy markers, configuration changes, queues, retries, background work, and partial failure.
7. Test whether an operator can distinguish detection, localization, diagnosis, and recovery from the proposed signals.

## Boundaries

- Do not log secrets, tokens, personal data, or unbounded high-cardinality identifiers.
- Do not claim telemetry exists or alerts work without repository, provider, and observed firing evidence.
- A dashboard is not an alerting or incident-response system.

## Output

Return Journeys and objectives, Signal design, Correlation, Dashboards, Alerts, Privacy and cost controls, and Validation plan.

