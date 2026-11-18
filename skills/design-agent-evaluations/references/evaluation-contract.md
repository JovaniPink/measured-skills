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

## Two distinct feedback loops

| Loop | Contract to define | Stop or handoff |
| --- | --- | --- |
| Runtime, within a task | Check objective constraints first. Return the rule, observed condition, and required condition. Bound attempts, elapsed time, usage, and side effects across nested workers. | Stop on exhausted bounds, repeated failure without new evidence, or lack of progress; preserve unresolved work for its owner. |
| Offline, across versions | Triage observed failures, select representative cases, review prompt or tool changes, and calibrate graders against human judgments. | Promote an authorized change only after its regression and calibration gates; retain the rejected candidate and reasons. |

Choose loop structure from the failure: use a deterministic check for a structural
contract, a scoped critique for judgment, or separated stages when responsibilities
cannot be evaluated together. Repeated rewriting alone may drift from the original
goal. Preserve that goal, relevant diagnostics, and valid evidence when summarizing
retry context; remove superseded material without hiding failures or audit history.
A separate critic can still share the generator's blind spots. Specify what context
is isolated and how disagreements are adjudicated, rather than assuming independence.
For a timed-out write, inspect the durable state or idempotency contract before
repeating it. A retry budget does not establish that repeating an effect is safe.

## Version and grader integrity

Record the prompt, rubric, case set, tools, context policy, model identifiers,
sampling settings, and runner revision with each result. Use provider-supported
version pins when available; record requested and served identifiers and any
unresolved alias or provider drift. Do not invent a snapshot identifier or assume
that a zero temperature makes repeated results identical.

Keep human calibration cases separate from cases used to tune the candidate or
grader. Cover historical failures and representative recent tasks, and report each
slice separately. Refresh the evidence under review when the population changes.
A passing old benchmark does not prove current alignment. Review a rubric change
against the governing requirement and held-out human judgments; then score both
baseline and candidate with the same accepted rubric. Version coupling records
dependencies; it does not require changing the judge whenever a prompt changes.

Use explicit criteria with evidence for each decision. Binary criteria fit clear
contracts; ordered or comparative judgments require their own calibration. For
pairwise grading, hide treatment labels and swap output order. Record order-sensitive
decisions as disagreement, not proof of a quality tie or removal of position bias.
Keep deterministic failures, grader disagreement, and missing evidence visible.

Predeclare the sampling unit, repetitions, important slices, uncertainty method,
and acceptable regression for the decision. Use paired comparisons when cases are
shared and account for related cases or repeated outputs. Justify sample size and
margins; do not copy a universal percentage, agreement score, or dataset ratio.
Protect critical contracts separately from aggregate quality. Zero observed failures
does not establish zero risk. Measure latency and usage on actual comparable runs;
they are not free observations merely because no model grader is involved.

## Close the offline loop

Treat retries, edits, rephrasing, and abandonment as leads with competing explanations,
not automatic negative labels. Compare targeted failure samples with a representative
sample so selection bias remains visible. Use already authorized, minimized evidence;
do not collect or export private prompts, code, or user content by default.

For each confirmed failure, propose a minimized regression case, its expected behavior,
the change owner, and the evidence needed for acceptance. Scrub sensitive content or
use a faithful synthetic case. Keep the mapping to the failure under the appropriate
access boundary. Review whether the rubric missed the same failure, but do not replace
an independent calibration decision with prompt tuning. Check for three stalled
handoffs: captured feedback never changes cases; new cases never reach a regression
gate; or the gate runs with a grader that no longer matches human intent. Define
review and retirement conditions without enabling new telemetry or scheduled runs.
