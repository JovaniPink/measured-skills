---
name: explain-codebase
description: "Explains existing code when asked how a request flows, where behavior lives, or what a module does; grounds the explanation in current files rather than inferred historical intent."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.19.0"
  plugin: "measured-workflows"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Codebase Explanation

Explain mechanics from the code that exists now.

Read [context map](references/context-map.md) when the explanation must support later navigation or a resumed session.

## Workflow

1. Clarify the behavior or path the user wants explained and bound the relevant component.
2. Locate entrypoints, public interfaces, owners of state, configuration, and the main callers and consumers.
3. Trace control flow and data flow separately. Name validation, transformations, persistence, concurrency, retries, and error paths where present.
4. Cite concrete files and symbols. Distinguish runtime code from tests, fixtures, generated output, documentation, and proposed designs.
5. Verify important claims through tests, call sites, configuration, or safe execution when appropriate and authorized.
6. Explain the smallest coherent model first, then add edge cases and uncertainty.

## Boundaries

Use `investigate-design-rationale` for historical intent or why a design was chosen.

- Current code can establish mechanics, not historical intent. Label rationale as inference unless direct evidence supports it.
- Do not change code merely because the explanation reveals a defect or awkward design.
- Do not imply that an unexecuted path, configuration, or deployment is active.

## Output

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Lead with a plain-language summary, then provide `Entrypoints`, `Flow`, `State and ownership`, `Interfaces`, `Failure paths`, `Evidence`, and `Unknowns`.

## Example

Synthetic example; not an observed client result.

Input: Requests enter Router, call InvoiceService, and persist through InvoiceStore.

Output: Router handles transport, InvoiceService applies invoice rules, and InvoiceStore owns persistence. Those observed calls define the current request path.
