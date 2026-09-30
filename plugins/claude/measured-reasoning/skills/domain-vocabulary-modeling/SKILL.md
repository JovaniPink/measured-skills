---
name: domain-vocabulary-modeling
description: "Build a proposed domain vocabulary from current code, documents, and stakeholder language, including concepts, definitions, relationships, invariants, authorities, examples, and contradictions. Use when inconsistent terms are causing design or communication errors; do not treat the result as ratified without owner evidence."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.17.1"
  plugin: "measured-reasoning"
  invocation: "implicit"
  provenance: "clean-room"
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

Return the vocabulary table, relationship notes, contradictions, ratification needs, and migration implications.
