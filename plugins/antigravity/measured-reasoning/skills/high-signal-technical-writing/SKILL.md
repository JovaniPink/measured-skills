---
name: high-signal-technical-writing
description: "Edits technical writing when asked to tighten a status update, clarify documentation, or remove vague and repetitive prose; preserves evidence, uncertainty, and the author's meaning."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
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

Return the revised text first, followed only by material meaning-preservation
notes, unresolved factual gaps, and useful alternatives. The revision should
lead with the supported result or current decision while retaining failed
checks, uncertainty, requested detail, and unfinished work. Match depth to the
audience; do not impose a word limit or hide essential evidence in an inaccessible
appendix.

Read [the original acceptance example](references/continuity-example.md) when checking this behavior.

## Example

Synthetic example; not an observed client result.

Input: Tighten: everything works, except the integration checks could not run.

Output: Local checks passed. Integration behavior remains unverified because the required checks could not run.
