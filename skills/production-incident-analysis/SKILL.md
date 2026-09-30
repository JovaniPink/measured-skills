---
name: production-incident-analysis
description: Analyze a production incident using timestamped evidence, system behavior, contributing conditions, response actions, and recovery. Use after an incident to establish what happened, why controls failed, and what learning or remediation is justified.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.17.1"
  plugin: "measured-operations"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Production Incident Analysis

Use generic terminology and preserve the status of every material statement: observed fact, proposal, ratified decision, rejected decision, unresolved question, measured result, estimate, or causal claim.

## Workflow

1. Define incident scope, impact, affected users, environment, detection, start, mitigation, recovery, and evidence custody.
2. Build a timestamped timeline from logs, metrics, traces, alerts, changes, communications, and operator actions.
3. Distinguish triggering event, contributing conditions, propagation, detection gaps, response friction, and recovery controls.
4. Test causal claims against competing explanations and identify uncertainty or missing telemetry.
5. Assess user, data, security, compliance, financial, and operational impact with supported units.
6. Identify corrective actions across prevention, detection, containment, recovery, process, and learning.
7. Assign owners, priorities, validation, due conditions, and effectiveness review.

## Boundaries

- Do not blame individuals or infer intent from incomplete operational evidence.
- Do not disclose secrets, personal data, or protected incident details.
- Do not claim root cause, full recovery, or action completion without exact evidence.

## Output

Return Impact, Timeline, Detection, Causal analysis, Contributing conditions, Response, Recovery evidence, Actions, and Unresolved questions.

