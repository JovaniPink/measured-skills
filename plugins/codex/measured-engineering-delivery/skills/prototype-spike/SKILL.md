---
name: prototype-spike
description: "Runs an isolated technical experiment when explicitly asked to test feasibility or answer an implementation uncertainty; disposable evidence does not authorize production adoption."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-engineering-delivery"
  invocation: "explicit"
  provenance: "clean-room"
  risk_class: "bounded-execution"
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

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return `Question`, `Hypothesis`, `Bounds`, `Prototype`, `Evidence`, `Result`, `Limitations`, `Disposition`, and `Production gaps`.

## Example

Synthetic example; not an observed client result.

Input: Test whether a parser library supports one unusual syntax in an isolated experiment.

Output: Build the smallest representative case and report support, failure, or uncertainty. A successful spike is not approval to adopt the dependency.
