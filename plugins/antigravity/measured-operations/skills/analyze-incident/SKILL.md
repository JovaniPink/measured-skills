---
name: analyze-incident
description: "Analyzes an incident when asked what happened, why recovery took time, or how to prevent recurrence; builds an evidence-backed timeline without assigning unsupported blame."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.19.0"
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

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return Impact, Timeline, Detection, Causal analysis, Contributing conditions, Response, Recovery evidence, Actions, and Unresolved questions.

## Example

Synthetic example; not an observed client result.

Input: Errors began at 10:05; rollback ended them at 10:12, but the cause is unknown.

Output: The timeline supports recovery after rollback. It does not yet establish root cause; compare the changed behavior and failure evidence.
