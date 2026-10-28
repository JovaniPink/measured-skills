---
name: research-sources
description: "Researches a question when asked to look up, compare, or verify current facts; uses primary sources and preserves dates, links, and uncertainty without turning claims into findings."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.19.0"
  plugin: "measured-workflows"
  invocation: "implicit"
  provenance: "original"
  risk_class: "network-read"
---

# Source-Grounded Research

Build conclusions from evidence that can support the exact claim being made.

## Workflow

1. Restate the research question and the decision it informs.
2. Search current sources when facts may have changed, the user asks for research, or direct attribution would help.
3. Prefer primary authorities: official documentation, original datasets, statutes, filings, research papers, provider status, or first-party announcements.
4. Use discovery pages, aggregators, and community discussion to find leads or understand reactions, not as substitutes for factual authority.
5. Capture the source URL, publisher, publication or observation date, relevant units or population, and any material limitation.
6. Compare sources on the same definition and time basis. Flag incompatible scopes instead of forcing a ranking.
7. Distinguish observed facts, source claims, inference, proposal, and unresolved questions.
8. Recheck volatile facts immediately before reporting them.

## Knowledge lifecycle handoff

When the user is building a traceable research or publication lifecycle, prepare source records compatible with `knowledge-contract.v1` rather than inventing a second schema. For each material source, preserve a stable project-scoped ID, canonical publisher URL, publisher and author identity, publication and retrieval dates, as-of meaning, access conditions, license, methodology warnings, domains, topics, tags, entities, verification status, limitations, and relationships.

The source record is a handoff, not a publication decision. Catalog inclusion does not prove endorsement, permission, maintenance, or model fitness. Route an authorized end-to-end research, model, outcome, evaluation, and publication workflow to `run-research-workflow` when that skill is installed.

## Evidence rules

- Link the page that directly supports each material claim.
- Keep quotations short; prefer faithful paraphrase.
- Preserve original publisher URLs rather than search-result or repost links.
- State when access limitations required an alternative readback method.
- For a claim that could not be confirmed, say so and name the sources checked.
- Do not manufacture precision from incomplete, stale, or differently defined data.

## Output

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Lead with the conclusion, then give a concise evidence table containing `Finding`, `Status`, `Source`, `Date`, and `Limit`. End with unresolved questions or recommended verification where needed. When a knowledge-lifecycle handoff was requested, also return the proposed source IDs and public-safe source fields without writing them unless the user authorized a named destination.

## Example

Synthetic example; not an observed client result.

Input: Two reports disagree about a date, and only one links the original record.

Output: Inspect the original record and distinguish its event date from publication dates. Keep the discrepancy visible until the evidence resolves it.
