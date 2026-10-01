---
name: respond-to-code-review
description: Evaluate code review feedback against current code, tests, contracts, and authority before accepting, rejecting, or deferring it. Use when review comments contain claims or requested changes that require technical verification.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-engineering-delivery"
  invocation: "implicit"
  provenance: "clean-room"
  risk_class: "bounded-execution"
---

# Respond to Code Review

Treat review comments as hypotheses and decisions to evaluate, not commands that automatically override current evidence.

## Workflow

1. Capture every comment with its author, location, revision, requested outcome, and whether it is still current.
2. Restate the technical claim and inspect the relevant code, contract, test, or platform evidence.
3. Classify the comment as `accept`, `reject`, `defer`, `clarify`, or `already addressed`, with evidence.
4. Resolve conflicting feedback by identifying the governing requirement or decision owner.
5. Implement accepted in-scope changes only when the user authorized implementation.
6. Add regression evidence for defect claims and rerun affected gates.
7. Prepare concise responses that explain evidence, changes, and remaining uncertainty.
8. Send responses or resolve threads only when that external write is authorized.

## Boundaries

- Do not accept feedback merely because it sounds authoritative.
- Do not dismiss feedback without checking the actual claim.
- Do not resolve a thread as a substitute for implementing or verifying the agreed change.
- Review approval, passing checks, merge, and deployment remain separate states.

## Output

Return a table with `Comment`, `Verdict`, `Evidence`, `Action`, and `Response`, followed by validation and unresolved decisions.
