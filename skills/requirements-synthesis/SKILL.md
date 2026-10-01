---
name: requirements-synthesis
description: Synthesize interviews, documents, issues, observations, and constraints into traceable requirements. Use when multiple sources must become a decision-ready scope without turning proposals or preferences into ratified facts.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-operations"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Requirements Synthesis

Use generic terminology and preserve the status of every material statement: observed fact, proposal, ratified decision, rejected decision, unresolved question, measured result, estimate, or causal claim.

## Workflow

1. Inventory sources, stakeholders, dates, authority, and material limitations.
2. Extract needs, outcomes, constraints, risks, dependencies, acceptance evidence, and unresolved questions.
3. Normalize duplicates while preserving disagreements, source ownership, and context.
4. Separate observed facts, reported needs, proposals, ratified decisions, rejected decisions, and estimates.
5. Write requirements with actor, behavior, condition, outcome, priority, rationale, and acceptance evidence.
6. Trace every material requirement back to one or more sources and flag unsupported additions.
7. Identify conflicts that require a named decision owner rather than silently resolving them.

## Boundaries

- Do not invent consensus, priority, scope, or acceptance criteria.
- Do not expose confidential source details in public outputs.
- Do not begin implementation or ratify requirements unless separately authorized.

## Output

Return Source inventory, Findings, Requirement set, Traceability, Conflicts, Open questions, and Decisions needed.

