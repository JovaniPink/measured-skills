# Audit prompt feedback loops

Use this guide when a code change modifies prompts, skills, agent retries, tools,
or the checks that judge their output. Follow the behavior through execution,
review, and later learning. A convincing answer, a passing grader, and a useful
production outcome are different claims.

This is design guidance. It does not add a telemetry service or a model-judge CI
pipeline to Measured Skills. The repository has separate [structural checks](testing.md),
[paid native evaluation arms](../evals/plugin-eval/README.md), and
[manual client observations](manual-smoke-tests.md). Their evidence and permission
boundaries still apply. [Supplemental review scenarios](../evals/review-feedback-loops.json)
are prepared for this guidance, outside the existing paid arms. Provider-backed work needs its own scoped data, tools,
budget, and authorization; this guide grants none.

Use the [code review workflow](code-review-workflow.md) for the review request,
[systems thinking guide](review-systems-thinking.md) for dependencies and outcomes,
and [research evidence note](research/review-and-feedback-evidence-2026-11-18.md)
for the source claims behind this direction.

## Separate the two loops

| Loop | Question | Evidence | Stop or handoff |
| --- | --- | --- | --- |
| Runtime: within one task | Can this attempt recover within its contract? | Check results, tool receipts, state observations, remaining budget | Finish, stop without progress, or hand unresolved work to an owner |
| Offline: across versions | Should a changed prompt, skill, or evaluator replace the baseline? | Reviewed failures, representative cases, human labels, comparable runs | Accept or reject a candidate under a recorded decision policy |

A runtime retry may repair one output while leaving the recurring cause intact.
An offline score may improve while a production dependency still fails. Assign
an owner and a measurable exit condition to each loop.

Keep three decisions separate: whether the candidate meets its contract, whether
the evaluator can recognize relevant failures, and whether deployed behavior
serves the intended user outcome. Agreement among models is evidence to inspect,
not a substitute for any of those decisions.

## Inspect runtime recovery

Start with checks whose result has a clear meaning: schema constraints, argument
types, compilation, existing tests, exit codes, and observable state. Run them
only within the authorized scope. A successful syntax check establishes syntax;
it does not establish correct intent or safe effects. Choose model critique for
questions that require judgment and retain human adjudication for unresolved
material decisions. [Anthropic's evaluation guidance](https://www.anthropic.com/research/demystifying-evals-for-ai-agents)
describes these complementary grader types and their limits.

Return useful diagnostics rather than an unexplained instruction to try again.
Identify the violated rule, observed condition, expected condition, supporting
receipt, and allowed next step. Distinguish a known failure from missing evidence.
The following record is synthetic; it describes no executed check:

```json
{
  "case_id": "dispatch-recovery-example",
  "rule": "one durable job per operation ID",
  "observed": "dispatch timed out; commit state is unknown",
  "expected": "recovery preserves the original operation identity",
  "evidence": "illustrative timeout receipt for attempt 1",
  "next_step": "inspect durable job status within read authority",
  "repeat_write_allowed": false,
  "stop_if": "status cannot be established within the agreed budget"
}
```

A timeout does not prove a write failed. Before repeating a write, inspect its
state or establish an idempotency contract: repeating the operation has the same
durable effect. Check identity reuse, concurrent requests, storage constraints,
and effects outside the transaction. A retry limit alone cannot prevent duplicate
work. If the outcome remains unknown, preserve that uncertainty and escalate;
do not invent a successful rollback or start a fresh operation identity.

Choose the recovery structure from the failure:

| Need | Suitable approach | Review question |
| --- | --- | --- |
| Repair a structural violation | Generate, check, then retry with the diagnostic | Are constraints compatible and the check authoritative? |
| Examine a judgment | A separate, scoped critique | Can the reviewer test the claim and search for counter-evidence? |
| Reduce overloaded responsibilities | Stages with explicit input and output contracts | Can an early error propagate unnoticed? |
| Improve an otherwise valid draft | Bounded refinement against the original goal | Does another pass add value or merely change style? |

A staged pipeline need not contain a retry loop. Adding critics to every stage
can create more review work than useful evidence. State which context a reviewer
receives and which author rationale is withheld. Give it the requirement, exact
candidate, relevant system evidence, and constraints. Isolation must not remove
the facts needed for a sound review.

Self-critique has conditional results. [Huang and colleagues](https://proceedings.iclr.cc/paper_files/paper/2024/hash/8b4add8b0aa8749d80a34ca5d941c355-Abstract-Conference.html)
found limitations in reasoning correction without external feedback;
[Self-Refine](https://proceedings.neurips.cc/paper_files/paper/2023/hash/91edff07232fb1b55a505a9e9f6c0ff3-Abstract-Conference.html)
reported gains from separate feedback and refinement steps using the same model.
Neither supports a universal guarantee. [Research on multi-agent judges](https://aclanthology.org/2025.findings-emnlp.941/)
also found bias amplification in the debate configurations studied. A fresh call
or another model does not establish independent errors.

Set task-specific ceilings for attempts, elapsed time, usage, and effects,
including nested workers. Stop when a failure repeats without new evidence or
progress. No universal eight-to-ten-attempt ceiling follows from these sources.
When shortening context, preserve the goal, valid findings, unresolved conditions,
and evidence references. Summarize superseded attempts without erasing their audit
history or carrying every dead end into the next prompt.

## Bind each evaluation to its inputs

Version the behavior and the means of judging it. Co-location in a repository is
useful; an external dataset also needs an immutable version, controlled access,
and a recorded relationship to the run. This illustrative record is a proposed
contract, not an implemented runner schema:

```yaml
evaluation:
  candidate_revision: "<commit or content hash>"
  baseline_revision: "<commit or content hash>"
  prompt_or_skill_revision: "<revision>"
  rubric_revision: "<revision>"
  dataset_revision: "<revision>"
  tool_schema_revision: "<revision>"
  context_policy_revision: "<revision>"
  harness_revision: "<revision>"
  model:
    requested_id: "<provider-documented model ID>"
    served_id: "<returned identifier or unavailable>"
    configuration_revision: "<revision>"
  decision:
    owner: "<responsible owner>"
    budget: "<authorized scope and ceiling>"
    policy_revision: "<thresholds and rationale>"
    insufficient_evidence: "hold for review"
```

Preserve run dates, environment details, permitted input/context references,
tool receipts, outputs, and criterion results under appropriate access controls.
Record unavailable evidence. A hash supports identity; it cannot reconstruct data
that was never retained. Retention and deletion rules still govern reconstruction.

Use the provider's documented version semantics. Do not invent a dated suffix or
assume every dateless identifier is mutable. [Claude's versioning documentation](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions)
identifies `claude-sonnet-4-6` as a pinned model, while noting that serving
infrastructure can affect behavior. Record configuration and remaining uncertainty;
zero temperature is not a reproducibility guarantee.

## Evaluate the candidate and the evaluator

Version coupling records dependencies. It does not require changing a judge
whenever a candidate fails. Approve changes to the expected behavior through the
governing requirement and owner, then calibrate the evaluator independently.

Human calibration cases should include historical failure modes and representative
recent work. Keep held-out cases separate from examples used to tune the prompt
or rubric. Have reviewers label without seeing model verdicts where practical,
record disagreement, and adjudicate ambiguous requirements. Report false accepts
and false rejects by material criterion, alongside agreement and sample sizes.

Judge staleness and rubric drift are different problems. A stale judge misses a
changed task population or requirement. A changed rubric may alter preferences
even when an old benchmark still passes. [Ding and colleagues' RIPD study](https://proceedings.colm.cc/paper_files/paper/2026/hash/9ad307ab459fb93163248a0a56959307-Abstract-Conference.html)
demonstrates this second risk, including adversarial rubric changes. It does not
show that every ordinary revision drifts.

Score baseline and candidate with the same qualified evaluator. When the evaluator
changes, re-score both or document a comparison that separates evaluator effects
from candidate effects. Retain the old rubric, reasons for change, and human
anchor judgments. Never soften a criterion solely to clear the candidate's gate.

## Use a three-stage decision funnel

1. **Check contracts and operating limits.** Inspect deterministic failures first.
   Measure resource use on comparable executions. Candidate generation, latency
   measurement, and tool use can cost money even when no model judge runs.
2. **Apply a qualified grader where needed.** Use criteria that state what evidence
   supports passing or failing. Binary checks fit binary properties; ordinal or
   comparative judgments need their own calibration. Record abstention and missing
   evidence. Blocking failures cannot be offset by a weighted average.
3. **Assess the whole result and important slices.** Keep critical contracts,
   ordinary tasks, recent failures, and affected subgroups visible. A global gain
   cannot clear a failed critical invariant.

For pairwise grading, hide treatment labels and swap response order. Record
consistent wins, losses, explicit ties, and order-inconsistent decisions
separately. [The MT-Bench study](https://arxiv.org/html/2306.05685v4) used a
conservative rule that counted inconsistent decisions as ties. If using that
aggregation, retain the inconsistency rate and a review threshold: it does not
prove equal quality or remove every bias.

Define the acceptable regression before viewing candidate results. A
non-inferiority decision asks whether deterioration larger than a justified
margin can be ruled out. Use paired comparisons when the same tasks are evaluated
and account for related cases and repeated trials. Repeating one case does not
create independent task coverage. Include uncertainty from the judge and its
calibration, not only variation across test cases; [Lee and colleagues](https://proceedings.mlr.press/v306/lee26bl.html)
explain why naive judge scores can be biased.

Choose sample sizes, slice allocation, confidence methods, and margins for the
decision's risk and required precision. A two-percent margin, a particular kappa
score, fixed dataset percentages, or a 200-to-300-case anchor set is not a universal
standard. Insufficient precision means insufficient evidence, not parity. Zero
observed critical failures does not establish zero production risk.

## Turn production evidence into reviewed changes

Use already authorized evidence. Retrying, editing, rephrasing, or abandoning a
task can suggest trouble, but can also reflect exploration, changed intent, or an
interruption. [Research on implicit feedback](https://proceedings.mlr.press/v306/wang26jq.html)
identifies selection bias and missing definitive negative examples. Claims that
nearly every user avoids ratings or that implicit events provide a fixed multiple
of useful signal need population-specific evidence.

Combine targeted failure samples with a representative comparison sample. Minimize
and redact data before triage; consent, access, and retention rules apply to both
collection and export. Do not copy private code, prompts, or raw traces into this
public catalog. Prefer faithful synthetic reproductions or authorized public cases.
This guide does not enable collection of site visitor prompts or repository content.

An owner should confirm the failure, identify the violated contract, minimize a
regression case, and decide whether the prompt, tools, workflow, or evaluator needs
change. A hotfix should carry its reproduction; if an emergency prevents that,
record the exception, owner, and follow-up rather than inventing coverage.

Check three stalled handoffs:

| Stall | Observable gap | Useful next result |
| --- | --- | --- |
| Evidence accumulates | Reviewed failures never change cases or criteria | A triaged failure with expected behavior and an owner |
| Calibration improves | Newly confirmed failures never reach the regression gate | A minimized case linked to the accepted repair |
| Cases grow | The grader keeps passing failures that humans now recognize | A separately reviewed rubric revision and held-out calibration |

Retire obsolete examples deliberately, preserving critical failures and rationale.
Review judge drift on a fixed canary and population change on recent samples;
neither replaces the other. Set cadence and alert limits from measured variation
and acceptable false alarms. [NIST's control-chart guidance](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc31.htm)
explains that these limits express a risk choice. A weekly 100-case, two-sigma
rule is an example to justify, not a default guarantee.

## Wire CI without inventing a gate

Before writing a workflow, identify the actual runner, check dependencies,
credentials, fixtures, costs, and required status semantics. GitHub's
[`changed_files` field](https://docs.github.com/en/rest/pulls/pulls) is a count,
not a filename list. Applying `contains(..., 'rubrics/')` to it does not detect
rubric edits.

Use a complete, validated base-to-head diff or a verified PR-files query. GitHub's
files endpoint caps the entire result at 3,000 files, even with pagination. Check
completeness against the pinned PR and its count, and ensure its head did not
change during collection. Use a verified local comparison or report
`detection_failed` when the list is incomplete. Inspect both names for renames
and include prompt, rubric, tool-schema, model-routing, context-policy, and
harness changes. Record `required`, `not_required`, or `detection_failed`.
Accept `not_required` only after successful complete detection; a skipped job
alone does not establish that calibration was unnecessary. Fetch and identify
the baseline used for comparison.

Keep untrusted fork code away from provider credentials. Use a separately trusted,
authorized evaluation environment for paid runs; do not obtain secrets by running
fork code in a privileged workflow. Structural CI, qualified behavioral evidence,
and release authority remain distinct.

## Copy a focused review request

```text
Review [exact base and head, or supplied diff] for changes to prompts, skills,
retry behavior, tools, or evaluators. The intended behavior is [contract].
Separate runtime recovery from learning across versions. Inspect diagnostics,
attempt and resource limits, uncertain writes, context preservation, and exits.
Trace candidate, rubric, dataset, model, and harness versions. Check whether the
evaluator is qualified independently and whether baseline comparisons use the
same criteria. Preserve critical failures, slice results, and missing evidence.
For each material concern, give its conditions, location, evidence, counter-
evidence, and smallest useful next check. Prepare findings only; do not edit,
run checks or paid evaluations, collect telemetry, publish, approve, or merge.
```
