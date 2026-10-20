---
name: iteration-postlaunch-learning
description: "Reviews postlaunch learning when asked what worked, what to change, or which feedback deserves investigation; uses observed outcomes rather than treating deployment as success."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-operations"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Iteration and Postlaunch Learning

Use generic terminology and preserve the status of every material statement: observed fact, proposal, ratified decision, rejected decision, unresolved question, measured result, estimate, or causal claim.

## Workflow

1. Restate the intended outcomes, guardrails, launch scope, population, and observation window.
2. Collect product, operational, support, qualitative, accessibility, security, and business evidence with source dates.
3. Compare observed behavior to baseline, target, expectation, and known confounders.
4. Separate defects, usability friction, adoption barriers, operational issues, unexpected benefits, and unresolved signals.
5. Assess whether changes are warranted now, require more evidence, or should be deferred.
6. Prioritize iterations by user impact, risk, confidence, effort, reversibility, and learning value.
7. Define the next experiment or change with success, failure, rollback, and review conditions.

## Boundaries

- Do not call a release successful from deployment, traffic, or anecdotes alone.
- Do not conceal negative evidence or repeatedly move targets after observing results.
- Do not implement, deploy, or message users unless separately authorized.

## Output

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return Intended outcomes, Observed evidence, Variance, Learning, Priorities, Next experiments, and Claim limits.

## Example

Synthetic example; not an observed client result.

Input: Support tickets rose after launch, but usage also doubled.

Output: Compare ticket rate and categories against usage before attributing deterioration to the release. Preserve the raw counts and missing segmentation.
