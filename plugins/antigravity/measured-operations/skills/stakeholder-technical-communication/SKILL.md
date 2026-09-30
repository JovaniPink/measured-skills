---
name: stakeholder-technical-communication
description: Translate technical evidence for a named stakeholder decision without overstating certainty, hiding risk, or exposing inappropriate detail. Use for executive summaries, review packets, status updates, decision briefs, and cross-functional explanations.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.17.1"
  plugin: "measured-operations"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Stakeholder Technical Communication

Use generic terminology and preserve the status of every material statement: observed fact, proposal, ratified decision, rejected decision, unresolved question, measured result, estimate, or causal claim.

## Workflow

1. Identify the audience, decision, prior context, time horizon, and level of technical detail needed.
2. Lead with the decision-relevant outcome, status, and evidence boundary.
3. Separate observed fact, proposed change, ratified decision, rejected option, unresolved question, estimate, and causal claim.
4. Explain tradeoffs, risks, dependencies, alternatives, and consequences in plain US English.
5. Use precise units, dates, environments, versions, and source links where they affect meaning.
6. Tailor depth without removing material uncertainty, dissent, or security constraints.
7. Identify decisions, owners, actions, and next evidence when the audience needs them; informational updates need no invented action.

## Boundaries

- Do not simplify away material risk or present estimates as measured results.
- Do not expose secrets, private paths, customer facts, or internal topology.
- Do not send, publish, or represent stakeholder approval without separate authority.

## Output

Return Audience and decision, Executive summary, Evidence, Tradeoffs, Risks, Decisions needed, and Appendix as required.


## Continuity and evidence

For an informational update, state the supported outcome without manufacturing a decision or action request. When a decision is needed, identify its owner, exact scope, evidence, and consequence. Preserve material dissent, uncertainty, and requested technical detail.

Read [the original acceptance example](references/continuity-example.md) when checking this behavior.
