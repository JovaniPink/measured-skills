# Evaluation Contract Reference

Use this reference only when the main workflow needs a complete evaluation design. The structure is informed by the [NIST AI Resource Center](https://airc.nist.gov/) test, evaluation, verification, and validation resources, but the workflow and contract are independently authored for this catalog.

## Contract Fields

| Field | Required content |
| --- | --- |
| Decision | The decision the results will support and its owner. |
| System | Exact agent, model, prompt, tools, context policy, configuration, revision, and environment. |
| Population | Intended task population, exclusions, sampling method, and important subgroups. |
| Cases | Representative, boundary, adversarial, abstention, recovery, and known-failure cases. |
| Baseline | Current, simpler, human, or no-system comparison and why it is fair. |
| Oracle | Source of expected behavior, its authority, uncertainty, and adjudication path. |
| Grader | Deterministic check, rubric, reviewer protocol, calibration, and conflict resolution. |
| Errors | Named error classes, severity, and whether multiple labels may apply. |
| Measures | Numerator, denominator, unit, aggregation, uncertainty, cost, and latency. |
| Thresholds | Predeclared pass, review, stop, and regression thresholds. |
| Human review | Selection, blinding, training, agreement check, escalation, and privacy boundary. |
| Limitations | Coverage gaps, contamination risks, dependencies, and unsupported conclusions. |
| Authority | Permitted local work and separately authorized external provider, data, or budget actions. |

## Grader Selection

Use the least subjective credible grader. Exact equality is appropriate only when representation is stable. Semantic or rubric grading needs explicit criteria, examples, calibration, and disagreement handling. A model grader does not become independent evidence merely because it uses a different prompt.

## Threshold Discipline

Set thresholds before candidate results are inspected. Report counts and denominators beside rates. Keep safety-critical errors visible even when aggregate performance passes. Treat a small or unrepresentative sample as a limitation, not proof of broad reliability.
