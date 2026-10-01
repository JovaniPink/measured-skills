---
name: decision-governance-records
description: Create or review decision records that preserve context, options, evidence, ownership, status, consequences, and review triggers. Use when a proposal must be distinguished from a ratified, rejected, superseded, or unresolved decision.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-operations"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Decision and Governance Records

Use generic terminology and preserve the status of every material statement: observed fact, proposal, ratified decision, rejected decision, unresolved question, measured result, estimate, or causal claim.

## Workflow

1. Identify the decision question, scope, affected capabilities, authority, and required decision date.
2. Record current evidence, constraints, assumptions, and unresolved questions.
3. Compare feasible options using explicit criteria, risks, reversibility, and downstream effects.
4. Name the decision owner, consulted parties, and the evidence required for ratification.
5. Record status as proposed, ratified, rejected, superseded, or unresolved; never infer status.
6. Document consequences, obligations, follow-up actions, review date, and supersession path.
7. Link related decisions and explain conflicts or dependency order.

## Boundaries

- Do not mark a proposal ratified without evidence from the named owner.
- Do not rewrite history when a decision changes; supersede it with traceability.
- Do not use a governance record as authorization for implementation, publication, or deployment.

## Output

Return Decision question, Status, Context, Options, Evidence, Owner, Consequences, Follow-up, and Review triggers.

