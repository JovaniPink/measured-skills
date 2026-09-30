---
name: source-grounded-research
description: Research a question using current primary sources, preserving publisher URLs, dates, units, provenance, and uncertainty. Use for web investigations, fact checks, comparisons, or recommendations where current evidence and precise attribution matter.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-skills"
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

The source record is a handoff, not a publication decision. Catalog inclusion does not prove endorsement, permission, maintenance, or model fitness. Route an authorized end-to-end research, model, outcome, evaluation, and publication workflow to `research-to-publication-lifecycle` when that skill is installed.

## Evidence rules

- Link the page that directly supports each material claim.
- Keep quotations short; prefer faithful paraphrase.
- Preserve original publisher URLs rather than search-result or repost links.
- State when access limitations required an alternative readback method.
- Do not manufacture precision from incomplete, stale, or differently defined data.

## Output

Lead with the conclusion, then give a concise evidence table containing `Finding`, `Status`, `Source`, `Date`, and `Limit`. End with unresolved questions or recommended verification where needed. When a knowledge-lifecycle handoff was requested, also return the proposed source IDs and public-safe source fields without writing them unless the user authorized a named destination.
