---
name: research-to-publication-lifecycle
description: "Coordinate an explicitly requested source-to-publication learning lifecycle across research, evidence tracing, model or forecast evaluation, corrections, and retrospective findings. Invoke explicitly when the user wants traceable knowledge objects or a public-safe research index; do not use for a one-off search, ordinary summary, or automatic publication."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.17.1"
  plugin: "measured-skills"
  invocation: "explicit"
  provenance: "original"
  risk_class: "bounded-execution"
---

# Research-to-Publication Lifecycle

Coordinate existing evidence skills into one traceable learning lifecycle without replacing their specialist workflows. Read [the knowledge-object handoff reference](references/knowledge-object-handoff.md) before proposing IDs, relationships, or a public index.

## Preconditions

Confirm the research question, project-scoped identifier, intended audience, evidence and editorial owners, visibility boundary, authorized sources, declared evaluation window, and whether the result stays in chat or may be written to a named path. A request for research does not authorize file writes, publication, deployment, paid services, private-data access, or provider changes.

## Composition workflow

1. Invoke `source-grounded-research` for current source discovery and its source-ledger handoff. Preserve exact publisher URLs, retrieval dates, as-of meaning, licenses, access conditions, and limitations.
2. Use `decision-evidence-trace` only when the user explicitly requested an auditable decision trail. Keep public reasons separate from hidden reasoning, transcripts, and source authority.
3. Define the question and the smallest needed `knowledge-contract.v1` objects. Preserve legacy IDs as aliases and do not rewrite published URLs merely for uniformity.
4. When a parser, model, forecast, or persistence path must prove source fidelity, invoke `source-output-conformance-audit`. Keep source snapshots, derived metrics, model output, human judgment, observations, and evaluations separate.
5. For a forecast, freeze its evidence snapshot at the declared cutoff. Reject post-outcome or later-as-of input. Link corrections as new versions instead of overwriting the original forecast.
6. Link observed outcomes only after their authority and observation time are established. Apply the declared metrics and sample requirements before making a skill or outcome claim.
7. Invoke `workflow-retrospective` after a meaningful completed or paused interval. Link findings and remaining unknowns to the evaluated objects without changing the original record.
8. Before a public projection, use `public-private-boundary-review`. Exclude private-source objects, internal paths, personal identifiers, restricted datasets, and relationships that reveal excluded objects.
9. Validate stable IDs, known relationships, correction history, canonical metadata, accessible semantic output, and the pinned contract version and digest using repository-defined checks.
10. Return the proposed local index, public projection, missing gates, and next authorized action. Write, publish, merge, deploy, or promote only under separate explicit authority.

## Boundaries

- Do not duplicate the specialist steps inside this routing skill; invoke the installed skill that owns each stage.
- Do not treat tags, a catalog entry, or schema validity as authority, endorsement, licensing, freshness, or model fitness.
- Do not claim predictive skill until the declared evaluation window and sample requirements are met.
- Do not centralize identity, personal data, private datasets, or operational state merely to connect research objects.
- Do not force a shared runtime, CMS, database, framework, or visual design.
- If a required companion skill is not installed, name the missing stage and provide a handoff rather than silently approximating it.

## Output

Return `Question and decision`, `Authority and visibility`, `Source ledger`, `Knowledge objects`, `Relationships`, `Cutoff and leakage checks`, `Outcome and evaluation`, `Retrospective`, `Public projection`, `Corrections`, `Validation`, `Missing gates`, and `Next authorized action`.
