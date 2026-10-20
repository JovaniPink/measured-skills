---
name: workflow-retrospective
description: "Reviews a completed workflow when explicitly asked what caused friction or what to improve next; uses observed task evidence without diagnosing people or claiming unmeasured benefit."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-reasoning"
  invocation: "explicit"
  provenance: "clean-room"
  risk_class: "read-only"
disable-model-invocation: true
---

# Workflow Retrospective

Turn observed execution evidence into a small, testable workflow improvement.

## Workflow

1. Define the reviewed interval, objective, expected workflow, supplied artifacts, and evidence boundary.
2. Reconstruct observable events, decisions, delays, rework, failures, recoveries, and outcomes without inferring private motives.
3. Identify contributing conditions across problem framing, information, tools, ownership, sequencing, validation, and authority.
4. Separate causal evidence from correlation, hindsight, preference, and unsupported explanation.
5. Preserve useful behavior and name the smallest material friction or risk worth changing.
6. Propose one bounded experiment with an owner, success signal, guardrail, review date, and rollback or rejection condition.
7. Record what remains unknown and what evidence would change the conclusion.

## Knowledge lifecycle handoff

When the reviewed workflow participates in `knowledge-contract.v1`, prepare a `retrospective` object with a stable project-scoped ID, review period, subject IDs, findings, remaining unknowns, evidence status, limitations, and relationships to the evaluated work. Preserve correction history rather than rewriting an earlier retrospective.

A retrospective is after-the-fact interpretation. It does not change the original source snapshot, scenario, forecast, observation, or evaluation. Route a complete research-to-publication workflow to `research-to-publication-lifecycle` when that skill is installed.

## Boundaries

- Use the current task and explicitly supplied artifacts. Do not search raw chats, private histories, unrelated repositories, or broad connector data by default.
- Do not expose chain-of-thought or treat a transcript as an objective record of causality.
- Do not automatically edit skills, repository policy, automation, or configuration.
- Do not turn one event into a universal rule without repeated evidence.

## Output

Report the scope, observed timeline, what helped or hindered, contributing
conditions, evidence limits, improvement experiment, owner, review date, and
rejected generalizations. Include observable communication friction: finding
results, repeated discovery, lost evidence, unnecessary decisions, and corrections
needed to resume. Separate measured effort from estimates and preferences.

Compare the current workflow, a small preference change, and a focused skill
revision before recommending general adoption. For a requested knowledge-lifecycle
handoff, include the proposed retrospective ID, subject relationships, findings,
unknowns, and limitations without automatically writing or publishing them.

Read [the original acceptance example](references/continuity-example.md) when checking this behavior.

## Example

Synthetic example; not an observed client result.

Input: Two status updates omitted a failed required check.

Output: Record the omission and its recovery cost, then propose a focused evidence-retention change. Do not infer personal traits or unmeasured productivity gains.
