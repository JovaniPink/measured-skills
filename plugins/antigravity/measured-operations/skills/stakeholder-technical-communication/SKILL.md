---
name: stakeholder-technical-communication
description: "Explains technical evidence when asked for a stakeholder update, decision brief, or plain-language status; preserves the decision needed and material limitations without unnecessary approval requests."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
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

Lead with the supported outcome for the named audience. An informational update
needs no manufactured decision or action request. When a decision is required,
state its owner, exact scope, evidence, tradeoffs, and consequence. Retain material
risks, dissent, uncertainty, and requested technical detail; use an appendix only
when it helps the audience access supporting evidence.

Read [the original acceptance example](references/continuity-example.md) when checking this behavior.

## Example

Synthetic example; not an observed client result.

Input: Give an informational update: local tests passed; hosted checks are pending.

Output: Local checks passed. Hosted behavior is still unverified; no release decision is requested by this update.
