---
name: problem-framing
description: Frame a proposed feature, defect, workflow, or system change before implementation by identifying users, outcomes, evidence, constraints, unknowns, options, and measurable success. Use when a request is important but the problem or desired result is not yet decision-ready.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-engineering-build"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Problem Framing

Turn an ambiguous request into a bounded problem statement before choosing an implementation.

## Workflow

1. Identify the affected users, operators, or systems and the outcome each needs.
2. Record current evidence separately from assumptions, reports, and preferences.
3. Describe the current state, triggering condition, impact, and why action is warranted now.
4. List constraints, authority boundaries, dependencies, and decisions already ratified.
5. Name material unknowns and the cheapest evidence that would resolve each one.
6. Compare at least two plausible response options, including leaving the system unchanged when credible.
7. Define success criteria, failure signals, exclusions, and stopping conditions.
8. Recommend whether to research, diagnose, plan, prototype, implement, or defer next.

## Done when

Framing is done when the user can choose the next step from the recommendation without needing new facts. Stop and ask when a material unknown can only be answered by the user or a decision owner.

## Boundaries

- Do not treat a requested solution as proof of the underlying problem.
- Do not invent users, requirements, metrics, or authority.
- Do not begin implementation unless the request also authorizes it and the problem is sufficiently bounded.
- Escalate choices that would materially change scope, risk, cost, or ownership.

## Output

Return `Problem`, `Affected parties`, `Evidence`, `Constraints`, `Unknowns`, `Options`, `Success criteria`, `Non-goals`, and `Recommended next step`. Mark each statement as observed, reported, assumed, proposed, or ratified when the distinction matters.
