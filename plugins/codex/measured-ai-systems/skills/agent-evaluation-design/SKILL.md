---
name: agent-evaluation-design
description: Design an evaluation contract for an AI agent, model-assisted workflow, or prompt-driven system using representative cases, baselines, configurations, graders, error classes, thresholds, cost, latency, human review, and limitations. Use when the decision depends on measured AI behavior across cases; use test-strategy for ordinary software coverage and test-quality-review for an existing test suite.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-ai-systems"
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

## Routing Boundaries

- Use `test-strategy` to select software test layers for deterministic application behavior.
- Use `test-quality-review` to assess the defect sensitivity and quality of existing tests.
- Use `acceptance-evidence-ledger` when the user wants a durable completion contract across substantial work.
- A product-specific model architecture or provider review belongs to its product catalog unless the request specifically asks for a comparative evaluation design.

## Output

Return an evaluation contract with `Decision`, `System under evaluation`, `Population and cases`, `Baseline`, `Configurations`, `Oracles and graders`, `Error taxonomy`, `Metrics`, `Thresholds`, `Human review`, `Cost and latency`, `Execution authority`, and `Limitations`.

## Continuity and evidence

Declare planned case, arm, and repetition coverage before collection. Bind every result to a unique study, case, arm, repetition, client, source, instructions, and execution envelope; reject duplicate or mismatched identities rather than overwriting. Check coverage and evidence integrity before outcome scoring. Keep failed execution, missing evidence, deterministic diagnostics, and pending human review distinct. Isolate treatment setup from task grading and protect the test contract independently.

Read [the original acceptance example](references/continuity-example.md) when checking this behavior.
