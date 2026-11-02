# Knowledge-object handoff

Use this reference to keep handoffs compatible with `knowledge-contract.v1`. The private governance authority and its checksummed public-safe JSON Schema remain authoritative. This reference is a field guide, not a second schema.

## Common fields

Every object needs:

- `schemaVersion`: pinned contract version;
- `id`: stable `project-id:kind:local-id` identifier;
- `projectId`, `kind`, `legacyIds`, `title`, and `summary`;
- creation, update, publication, retrieval, as-of, and review dates when applicable;
- provenance through source IDs, method IDs, and an exact snapshot digest when available;
- semantic facets: controlled domains and topics, normalized tags, and typed entities;
- evidence status, editorial status, visibility, limitations, relationships, and correction history.

The supported kinds are `source`, `note`, `claim`, `dataset`, `scenario`, `model-run`, `forecast`, `observation`, `evaluation`, `retrospective`, and `publication`.

## Semantic and evidence boundaries

- Domains are controlled broad areas. Topics are controlled project subjects. Tags describe; they do not establish authority.
- Entities are typed people, organizations, places, teams, policies, instruments, or institutions.
- A claim nature is observation, source claim, interpretation, forecast, scenario, or recommendation.
- Verification status is unreviewed, source-reviewed, corroborated, contested, superseded, or corrected.
- Visibility is public, sanitized, or private-source.

## Relationship checks

Every target ID must resolve in the local index or an approved external public index. Removing a private object from a public projection must also remove relationships and provenance references that would reveal it. A correction identifies the replaced object and a distinct replacement object.

Forecast source snapshots must have an as-of time at or before the forecast cutoff. Observations and evaluations link forward without modifying the original prediction. A publication links the exact objects it presents and retains their limitations.

## Handoff table

| Stage | Primary object | Required distinguishing evidence |
| --- | --- | --- |
| Curated source | `source` or `dataset` | Publisher, URL, retrieval and as-of dates, access, license, warnings |
| Working analysis | `note` or `claim` | Source IDs, claim nature, verification status, limitations |
| Simulation | `scenario` and `model-run` | Assumptions, synthetic boundary, method version, inputs, outputs, run time |
| Prediction | `forecast` | Cutoff, snapshot IDs, snapshot as-of time, target, horizon, method, probability |
| Outcome | `observation` | Observation time, source authority, statement |
| Measurement | `evaluation` | Subject IDs, declared metrics, evaluation time, conclusion |
| Learning | `retrospective` | Review period, subject IDs, findings, remaining unknowns |
| Public finding | `publication` | Canonical URL, publication time, presented object IDs, correction history |

Do not populate a field with unsupported precision. Mark missing authority or evidence as a gate instead of inventing a value.
