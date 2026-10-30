---
name: design-agent-evaluations
description: "Designs AI evaluations when asked how to test an agent, compare prompts, or measure answer quality; requires representative cases and a baseline rather than one favorable response."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.19.0"
  plugin: "measured-quality"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Agent Evaluation Design

Turn an AI-reliability question into a decision-ready evaluation contract. Read [the evaluation contract reference](references/evaluation-contract.md) when defining the case set, graders, or acceptance rule.

## Preconditions

Identify the system version, decision owner, intended users, operating environment, available evidence, and decision the evaluation must support. If the target behavior or decision is not defined, return the missing decisions before inventing metrics.

## Workflow

1. State the evaluation question and the change, configuration, or baseline being compared.
2. Define the population of real tasks without embedding private inputs. Partition representative, boundary, adversarial, abstention, recovery, and known-failure cases.
3. Pin the system configuration: model or agent version, instructions, tools, context policy, sampling settings, dependencies, and environment.
4. Define a baseline that makes improvement or regression interpretable. Use the current system, a simpler workflow, human performance, or a justified no-system baseline.
5. Assign an oracle or grader to each behavior. Prefer deterministic checks for objective facts; define calibrated human review or rubric-based grading where judgment is unavoidable.
6. Create an error taxonomy that separates wrong answers, missing required content, unsupported claims, unsafe actions, routing failures, refusals, tool failures, and evidence gaps.
7. Define metrics, units, aggregation, confidence or uncertainty treatment, cost, latency, and subgroup slices. Prevent averages from hiding severe or safety-critical failures.
8. Set thresholds and stopping rules before observing candidate results. State which failures are release blockers and which require human review.
9. Document sampling limits, grader limitations, contamination risks, nonindependence, and what the evaluation cannot establish.
10. Produce the evaluation contract. Do not run a paid or external evaluation without separate authority for the provider, data, budget, and network action.

For usage measurements, distinguish user task requests, delegated work, and
client-managed inference. Record the observation window, request categories,
models, input/output and cache usage where available, and gaps in collection.
Do not equate session counts with API calls or estimated token cost with billed
spend or subscription allowance. Compare task outcomes and elapsed time alongside
usage; fewer requests alone do not establish improvement. Instrumentation is a
separate configuration and data-export decision, not implicit evaluation authority.

## Routing Boundaries

- Use `plan-tests` to select software test layers for deterministic application behavior.
- Use `review-tests` to assess the defect sensitivity and quality of existing tests.
- Use `track-acceptance` when the user wants a durable completion contract across substantial work.
- A product-specific model architecture or provider review belongs to its product catalog unless the request specifically asks for a comparative evaluation design.

## Output

Return a concise evaluation contract covering the decision, system, population,
cases, baseline, configurations, graders, error classes, metrics, thresholds,
human review, cost, latency, execution authority, and limitations.

Declare planned case, arm, and repetition coverage before collection. Bind each
result to a unique study, case, arm, repetition, client, source, instructions,
and execution envelope. Reject duplicate or mismatched identities rather than
overwriting. Check coverage and evidence integrity before scoring; keep failed
execution, missing evidence, deterministic diagnostics, and pending human review
distinct. Isolate treatment setup from grading and protect the test contract.

Read [the original acceptance example](references/continuity-example.md) when checking this behavior.

## Example

Synthetic example; not an observed client result.

Input: One of twelve planned cases has a favorable answer.

Output: The comparison is incomplete. One response cannot establish the agent's success rate or justify adoption.
