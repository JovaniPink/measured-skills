---
name: problem-framing
description: "Frames a feature or problem when asked what to build, which outcome matters, or whether a proposed fix addresses the need; establishes users, constraints, and success before implementation."
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

Framing is done when the recommendation names the next step and the evidence that step needs, so the user can approve it or choose another option. Stop and ask when a material unknown can only be answered by the user or a decision owner.

## Boundaries

- Do not treat a requested solution as proof of the underlying problem.
- Do not invent users, requirements, metrics, or authority.
- Do not begin implementation unless the request also authorizes it and the problem is sufficiently bounded.
- Escalate choices that would materially change scope, risk, cost, or ownership.

## Output

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return `Problem`, `Affected parties`, `Evidence`, `Constraints`, `Unknowns`, `Options`, `Success criteria`, `Non-goals`, and `Recommended next step`. Mark each statement as observed, reported, assumed, proposed, or ratified when the distinction matters.

## Example

Synthetic example; not an observed client result.

Input: A team requests a dashboard, but has not identified its users, decision, evidence of delay, or deadline.

Output: The reported request is a dashboard; the underlying problem remains unverified. Affected users and their decision are unknown. No delay measurements or constraints were supplied. Options are to inspect the current decision process or interview its users before selecting a solution. Proposed success is a measurable improvement in that decision; its target still needs agreement. Building the dashboard is outside this framing step. Next: identify who makes the decision and what information is missing.
