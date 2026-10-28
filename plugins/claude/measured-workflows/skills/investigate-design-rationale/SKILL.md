---
name: investigate-design-rationale
description: "Investigates why a design exists when asked why code was written that way or which constraint drove it; distinguishes historical evidence from plausible explanations."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.19.0"
  plugin: "measured-workflows"
  invocation: "implicit"
  provenance: "original"
  risk_class: "network-read"
---

# Design Rationale Investigation

Establish what is known about a design decision and what remains inference.

## Workflow

1. Define the exact decision, time window, system boundary, and question the answer will inform.
2. Inspect current code and tests to establish mechanics before investigating history.
3. Prefer direct evidence: decision records, commit history, linked issues, review discussions, release notes, incident records, and named documentation.
4. Search only authorized sources relevant to the named decision. Ask before reading private chat, broad activity history, or unrelated repositories.
5. Build competing hypotheses and test each against dates, changes, constraints, rejected alternatives, and later corrections.
6. Classify every conclusion as `Direct evidence`, `Strong inference`, `Weak hypothesis`, `Contradiction`, or `Unknown`.
7. Recheck the current system before recommending action because historical reasons may no longer apply.

## Done when

The investigation is done when each conclusion is classified and its implication for the current decision is stated. Stop and ask before widening the search beyond the authorized sources.

## Boundaries

- Do not treat commit order, code comments, or repeated claims as proof of intent by themselves.
- Do not enumerate every available tool, data source, or conversation by default.
- Do not spawn agents or access external systems without host and user authority.
- Do not rewrite history or implementation as part of the investigation.

## Output

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return `Current mechanics`, `Timeline`, `Evidence`, `Hypotheses`, `Contradictions`, `Confidence`, `Expired assumptions`, and `Decision implications`.

## Example

Synthetic example; not an observed client result.

Input: A comment says the cache avoids a slow legacy query; no decision record exists.

Output: The comment supports that rationale, but its current relevance is unverified. Compare the query and history before treating the cache as necessary or obsolete.
