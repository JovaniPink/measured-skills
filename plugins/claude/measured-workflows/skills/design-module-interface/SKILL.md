---
name: design-module-interface
description: "Designs module boundaries when asked to untangle coupling, simplify an API, or clarify ownership; makes caller contracts concrete before implementation."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.19.0"
  plugin: "measured-workflows"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Module Interface Design

Propose a coherent boundary that reduces caller knowledge without hiding important authority or failure behavior.

Read [behavior-preserving refactoring](references/behavior-preserving-refactoring.md) when untangling existing code without intentionally changing its contract.

## Workflow

1. Establish the user outcome, current modules, callers, dependencies, vocabulary, invariants, and change pressure.
2. Identify knowledge duplicated across callers, unstable details that leak through interfaces, and state or authority that lacks a clear owner.
3. Define the smallest useful contract: inputs, outputs, errors, state transitions, compatibility promises, and operational signals. Name the requirement each component or layer serves, and drop any that serve none.
4. Compare at least two viable boundaries when the tradeoff is material. Include the cost of keeping the current design.
5. Test each option against common use, difficult use, invalid use, migration, partial rollout, and future change.
6. Recommend a boundary with explicit reasons, rejected alternatives, and unresolved decisions.
7. Describe a staged migration and verification approach without performing the redesign.

## Boundaries

- Prefer evidence from actual callers over abstract purity.
- Prefer extending a coherent existing module over adding a parallel abstraction. Name who owns each state transition and demonstrate the proposed seam with one end-to-end slice.
- For unfamiliar technology, explain the state model, failure modes, and rejected alternative before asking the user to approve the design.
- A deeper module is not permission to conceal data authority, security decisions, or failure modes.
- Do not force one architecture pattern across unrelated stacks.
- Treat redesign, deletion, migration, and compatibility breaks as proposals until separately approved.

## Output

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return `Current pressure`, `Vocabulary`, `Invariants`, `Candidate boundaries`, `Recommended interface`, `Hidden implementation`, `Compatibility`, `Migration`, `Tradeoffs`, and `Open decisions`.

## Example

Synthetic example; not an observed client result.

Input: Callers need one price but currently depend on an internal pricing table.

Output: Expose the price calculation as a stable contract with explicit inputs and errors; keep table layout behind the module boundary.
