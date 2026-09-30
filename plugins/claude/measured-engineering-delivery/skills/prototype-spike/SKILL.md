---
name: prototype-spike
description: "Run a bounded prototype or technical spike to answer a named uncertainty with disposable or isolated work and explicit evidence. Invoke explicitly when the user authorizes implementation for learning but has not authorized production adoption, merge, or release."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.17.1"
  plugin: "measured-engineering-delivery"
  invocation: "explicit"
  provenance: "clean-room"
  risk_class: "bounded-execution"
disable-model-invocation: true
---

# Prototype Spike

Build only enough to answer a specific question, then make the result and disposition explicit.

## Preconditions

Confirm the question, success and failure evidence, time or cost bound, allowed environment, authorized writes, and whether the work must be isolated. If the question cannot change a decision, do not build a prototype.

## Workflow

1. Record the hypothesis, alternatives, constraints, and decision the evidence will inform.
2. Isolate the work from production state and unrelated changes. Use fixtures, fakes, local data, or a worktree when appropriate and authorized.
3. Choose the smallest implementation that can falsify the important assumption.
4. Add focused checks that make the result repeatable. A prototype may use lighter coverage, but it cannot invent success or bypass safety controls.
5. Run the experiment and record inputs, environment, observations, failures, and uncertainty.
6. Compare the result with the predefined threshold and decide `discard`, `extend`, `adopt as a proposal`, or `inconclusive`.
7. Stop at the authorized boundary and list production work that would still be required.

## Boundaries

- A successful spike is evidence about the tested question, not production readiness.
- Do not commit, merge, deploy, migrate, publish, or promote the prototype unless separately authorized.
- Do not use real sensitive data or production credentials merely because the implementation is temporary.
- Preserve an abort path and remove temporary state only when cleanup is authorized and the target is exact.

## Output

Return `Question`, `Hypothesis`, `Bounds`, `Prototype`, `Evidence`, `Result`, `Limitations`, `Disposition`, and `Production gaps`.
