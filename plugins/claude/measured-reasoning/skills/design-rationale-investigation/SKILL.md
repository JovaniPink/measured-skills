---
name: design-rationale-investigation
description: "Investigate why code, architecture, or an operational design exists by comparing direct historical evidence, current behavior, and competing hypotheses. Use for design history and rationale questions; do not infer intent from code shape alone or search unrelated private sources."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.17.1"
  plugin: "measured-reasoning"
  invocation: "implicit"
  provenance: "clean-room"
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

## Boundaries

- Do not treat commit order, code comments, or repeated claims as proof of intent by themselves.
- Do not enumerate every available tool, data source, or conversation by default.
- Do not spawn agents or access external systems without host and user authority.
- Do not rewrite history or implementation as part of the investigation.

## Output

Return `Current mechanics`, `Timeline`, `Evidence`, `Hypotheses`, `Contradictions`, `Confidence`, `Expired assumptions`, and `Decision implications`.
