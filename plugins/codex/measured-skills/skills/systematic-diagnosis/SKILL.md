---
name: systematic-diagnosis
description: Diagnose a defect, failure, regression, or confusing behavior by reproducing it, narrowing the causal boundary, and reporting evidence. Use when the user asks why something fails or requests diagnosis without necessarily authorizing a fix.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-skills"
  invocation: "implicit"
  provenance: "original"
  risk_class: "bounded-execution"
---

# Systematic Diagnosis

Determine the most strongly supported cause before changing the system.

## Workflow

1. Capture the observed symptom, expected behavior, environment, and smallest known reproduction.
2. Reproduce safely when possible. Preserve the exact command, input, output, and revision.
3. Map the path from input to failure and identify the first boundary where observed state diverges from expected state.
4. Form a small set of competing hypotheses with discriminating tests.
5. Run the cheapest read-only or reversible test that can eliminate a hypothesis.
6. Check whether the failure is isolated, environment-specific, order-dependent, intermittent, or shared by related paths.
7. Stop when one cause is supported well enough to explain the evidence, or report the remaining uncertainty explicitly.

## Boundaries

- Diagnosis does not authorize implementation. Do not edit files, restart shared services, change remote state, or deploy unless the user also requested a fix.
- Do not label correlation, a passing standalone test, or the last changed file as the cause without a causal check.
- Treat sandbox, permission, network, and provider failures as environment evidence until product behavior is independently implicated.

## Output

Report `Symptom`, `Reproduction`, `Cause`, `Evidence`, `Alternatives eliminated`, `Impact`, and `Fix direction`. If no cause is established, say `Diagnosis incomplete` and name the next discriminating observation.
