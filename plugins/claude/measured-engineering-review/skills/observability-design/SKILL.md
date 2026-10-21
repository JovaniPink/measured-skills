---
name: observability-design
description: "Designs logs, metrics, traces, and alerts when asked how to detect or explain failures; connects telemetry to user impact and operator actions rather than log volume."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-engineering-review"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Observability Design

Use [OpenTelemetry signal concepts](https://opentelemetry.io/docs/concepts/signals/) for telemetry vocabulary. The journey, alert, privacy, and operator checks below are this catalog's design contract; the reference does not certify a complete operational design.

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

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return Journeys and objectives, Signal design, Correlation, Dashboards, Alerts, Privacy and cost controls, and Validation plan.

## Example

Synthetic example; not an observed client result.

Input: An alert reports CPU usage but says nothing about failed checkouts.

Output: Add a user-impact signal tied to checkout failures and an operator action. CPU remains diagnostic context, not proof of customer impact.
