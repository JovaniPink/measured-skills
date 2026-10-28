---
name: model-domain-vocabulary
description: "Clarifies domain terms when teams use the same word differently or code and documents disagree; proposes definitions and examples without declaring owner approval."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.19.0"
  plugin: "measured-workflows"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Domain Vocabulary Modeling

Create a traceable proposed language model for the domain.

## Workflow

1. Name the scope, intended users, and authoritative evidence sources.
2. Extract terms as they are actually used. Preserve conflicting definitions and overloaded words.
3. For each concept, record `Term`, `Proposed definition`, `Evidence`, `Examples`, `Non-examples`, `Relationships`, `Invariants`, `Authority`, and `Status`.
4. Separate business concepts from storage names, API fields, UI labels, implementation classes, and vendor terminology.
5. Identify synonyms, homonyms, missing concepts, ambiguous boundaries, and terms whose meaning changes by context.
6. Test the model against representative scenarios and existing interfaces. Record contradictions rather than silently choosing a definition.
7. Mark every entry as observed, proposed, ratified, rejected, or unresolved. Name the decision owner for ratification when known.

## Boundaries

- Do not rename code, schemas, or public interfaces without separate implementation authority.
- Do not declare a proposed definition canonical from repetition alone.
- Keep private product language in its owning repository or private overlay.

## Output

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return the vocabulary table, relationship notes, contradictions, ratification needs, and migration implications.

## Example

Synthetic example; not an observed client result.

Input: Sales uses account for a company; billing uses it for a payment ledger.

Output: Define separate Company and Billing Account concepts, with an explicit relationship. These are proposed terms until the domain owners confirm them.
