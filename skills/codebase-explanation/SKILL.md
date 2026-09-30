---
name: codebase-explanation
description: "Explain how an existing codebase works using current repository evidence: entrypoints, ownership, control and data flow, state, interfaces, failures, and concrete files. Use when the user asks how code behaves; use design-rationale-investigation instead for historical intent or why a design was chosen."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-reasoning"
  invocation: "implicit"
  provenance: "clean-room"
  risk_class: "read-only"
---

# Codebase Explanation

Explain mechanics from the code that exists now.

## Workflow

1. Clarify the behavior or path the user wants explained and bound the relevant component.
2. Locate entrypoints, public interfaces, owners of state, configuration, and the main callers and consumers.
3. Trace control flow and data flow separately. Name validation, transformations, persistence, concurrency, retries, and error paths where present.
4. Cite concrete files and symbols. Distinguish runtime code from tests, fixtures, generated output, documentation, and proposed designs.
5. Verify important claims through tests, call sites, configuration, or safe execution when appropriate and authorized.
6. Explain the smallest coherent model first, then add edge cases and uncertainty.

## Boundaries

- Current code can establish mechanics, not historical intent. Label rationale as inference unless direct evidence supports it.
- Do not change code merely because the explanation reveals a defect or awkward design.
- Do not imply that an unexecuted path, configuration, or deployment is active.

## Output

Lead with a plain-language summary, then provide `Entrypoints`, `Flow`, `State and ownership`, `Interfaces`, `Failure paths`, `Evidence`, and `Unknowns`.
