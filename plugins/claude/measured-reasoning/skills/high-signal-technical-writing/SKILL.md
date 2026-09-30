---
name: high-signal-technical-writing
description: "Edit technical prose for clarity, evidence density, specificity, rhythm, and audience fit while preserving meaning and repository voice. Use for completion reports, status updates, or documentation that sounds vague, repetitive, promotional, or machine-generic; do not use style heuristics as evidence of authorship."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.17.1"
  plugin: "measured-reasoning"
  invocation: "implicit"
  provenance: "clean-room"
  risk_class: "read-only"
---

# High-Signal Technical Writing

Make technical writing direct, specific, and trustworthy without flattening its voice.

Read [editing checklist](references/editing-checklist.md) for a full revision pass or when the draft has several different failure modes.

## Workflow

1. Identify the audience, decision, genre, house style, and facts that must not change.
2. Preserve claims, uncertainty, attribution, terminology, and deliberate tone before shortening anything.
3. Replace generic framing with concrete subjects, actions, evidence, limits, and consequences.
4. Remove repetition, empty transitions, inflated claims, canned contrast, and conclusions unsupported by the body.
5. Vary sentence length and structure only when it improves comprehension. Keep necessary nuance and domain terms.
6. Read the revision for meaning drift, overstatement, accidental certainty, and lost author voice.

## Boundaries

- Repository or publication style guidance overrides this skill.
- Style patterns can guide editing; they cannot determine whether a human or model wrote the text.
- Do not make prose more opinionated by inventing opinions, evidence, or results.
- Do not remove accessibility, legal, security, or operational detail merely to make text shorter.

## Output

Return the revised text first. Then list only material meaning-preservation notes, unresolved factual gaps, and optional alternatives.

## Continuity and evidence

Lead with the supported result or current decision. Preserve failed checks, uncertainty, requested detail, and requested work still unfinished. Match depth to the audience; do not impose a word limit or move essential evidence into an inaccessible appendix.

Read [the original acceptance example](references/continuity-example.md) when checking this behavior.
