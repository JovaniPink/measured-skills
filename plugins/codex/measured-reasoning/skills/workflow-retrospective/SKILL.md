---
name: workflow-retrospective
description: "Review a completed or paused workflow using supplied artifacts and current task evidence to identify what helped, what failed, why, and which bounded improvement to test next. Invoke explicitly after meaningful work; do not mine private histories or automatically rewrite policy or skills."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-reasoning"
  invocation: "explicit"
  provenance: "clean-room"
  risk_class: "read-only"
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

Return `Scope`, `Observed timeline`, `What helped`, `What hindered`, `Contributing conditions`, `Evidence limits`, `Improvement experiment`, `Owner and review date`, and `Rejected generalizations`. If a knowledge-lifecycle handoff was requested, add the proposed retrospective ID, subject relationships, findings, unknowns, and limitations without writing or publishing them automatically.

## Continuity and evidence

Review observable communication friction: time spent finding results, repeated discovery after interruption, lost evidence, unnecessary decisions, and corrections needed to resume. Distinguish measured effort from estimates and preference. Compare the current workflow, a small preference change, and a focused skill revision before proposing general adoption.

Read [the original acceptance example](references/continuity-example.md) when checking this behavior.
