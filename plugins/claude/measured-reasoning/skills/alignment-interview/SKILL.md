---
name: alignment-interview
description: "Clarifies an underspecified request when the desired result, constraints, or success criteria are unclear; asks only material questions and does not reopen settled decisions."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-reasoning"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Alignment Interview

Reach decision readiness before implementation starts.

## Workflow

1. Inspect the evidence already available in the request, repository, issue, plan, and named documents before asking the user to repeat facts.
2. Maintain the current understanding as `Goal`, `Users`, `Constraints`, `Known evidence`, `Unknowns`, and `Success criteria`; present only the material change during the interview.
3. Rank unknowns by how much their answers could change scope, architecture, authority, safety, cost, or acceptance.
4. Ask one material question at a time. Explain why it matters and recommend a default when current evidence supports one.
5. Update the shared model after each answer and identify contradictions rather than smoothing them over.
6. Stop when the remaining unknowns do not prevent a responsible next decision. Summarize the agreed model, assumptions, rejected options, unresolved questions, and next authorized action.

## Boundaries

- Do not implement, edit files, publish, or create external records while interviewing unless separately authorized.
- Do not ask the user to repeat facts that can be discovered safely from the authorized workspace.
- Do not treat persistence or question count as quality. Stop when the decision is ready.
- Route broad product discovery to problem framing and concrete implementation design to implementation planning.

## Output

During the interview, present the current material question and only the changed
understanding needed to answer it. Do not reopen settled decisions unless new
evidence creates a material conflict. At readiness, summarize the full agreed
understanding, evidence, decisions, assumptions, open questions, readiness, and
any next authorized action.

Read [the original acceptance example](references/continuity-example.md) when checking this behavior.

## Example

Synthetic example; not an observed client result.

Input: Storage is already chosen; only retention is undecided.

Output: How long must records remain available, and what deletion obligations constrain that period?
