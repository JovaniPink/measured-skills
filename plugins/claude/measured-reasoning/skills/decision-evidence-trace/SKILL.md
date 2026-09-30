---
name: decision-evidence-trace
description: "Maintain a bounded decision and evidence trail for a long-running task without exposing hidden reasoning, raw transcripts, secrets, or unrelated activity. Invoke explicitly when the user wants an auditable task log in chat or an authorized append-only file."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.17.1"
  plugin: "measured-reasoning"
  invocation: "explicit"
  provenance: "clean-room"
  risk_class: "bounded-execution"
disable-model-invocation: true
---

# Decision Evidence Trace

Record public reasons and observable evidence for consequential task decisions.

## Workflow

1. Confirm the task boundary, audience, retention need, and whether the trace stays in chat or may be written to a named file.
2. Default to an in-chat trace. Require explicit file authority before creating or appending to a repository artifact.
3. Record only decision-relevant entries with `timestamp`, `phase`, `decision`, `public basis`, `evidence references`, `outcome`, and `supersedes`.
4. Link to stable evidence rather than copying logs, prompts, source files, or private conversations into the trace.
5. Append corrections as new entries. Do not silently rewrite earlier entries when the trace is designated append-only.
6. At checkpoints, reconcile open decisions, invalidated assumptions, deviations, and the evidence needed next.

## Knowledge lifecycle handoff

When the trace supports a `knowledge-contract.v1` lifecycle, map observable research notes to `note` objects and externally supportable assertions to `claim` objects. Preserve stable project-scoped IDs, evidence status, editorial status, visibility, limitations, source relationships, and correction links. A correction appends a linked replacement version; it never rewrites a designated append-only entry.

Do not turn private reasoning into a claim object or treat a trace entry as source authority. Route the complete research-to-publication sequence to `research-to-publication-lifecycle` when that skill is installed.

## Boundaries

- Do not record hidden chain-of-thought, internal deliberation, raw model reasoning, or private scratch work.
- Do not include secrets, credentials, personal data, proprietary text, raw transcripts, or unrelated user activity.
- Do not create a surveillance or activity log. Record only the named task's material decisions.
- Do not treat a trace entry as proof that the referenced action succeeded; verify external state separately.

## Output

Return the current entries, unresolved evidence needs, and the trace location if a file was explicitly authorized. If a knowledge-lifecycle handoff was requested, include proposed note or claim IDs and relationships separately from the trace.
