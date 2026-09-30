---
name: source-output-conformance-audit
description: Audit whether exact source identity and expected values survive parsing or extraction, validation, persistence, and readback using source-cited oracles and mutation-sensitive tests. Use for end-to-end source-to-output fidelity claims; use test-quality-review for test-suite quality and authority-boundary-review for ownership architecture alone.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.17.1"
  plugin: "measured-ai-systems"
  invocation: "implicit"
  provenance: "original"
  risk_class: "bounded-execution"
---

# Source-Output Conformance Audit

Establish what evidence supports each stage from exact source bytes to observed output. Read [the conformance matrix reference](references/conformance-matrix.md) before executing fixtures or making a completeness claim.

## Preconditions

Define the authorized source set, expected output contract, parser or extractor path, validation rules, persistence boundary, readback path, and allowed local commands. Preserve source bytes. If the source set lacks custody authority, a source-cited oracle, or permission for a write-bearing test environment, report the missing gate instead of expanding access.

## Workflow

1. Pin source identity with a stable path or object identity, byte count, media type, and cryptographic digest. Record aliases and duplicate handling without changing the source.
2. Build an expected-value oracle independently from the implementation output. Cite the exact source location for every expected field, record, relationship, or deliberate absence.
3. Trace the actual production path through decoding, parsing or extraction, normalization, validation, rejection, write preparation, persistence, and readback. Identify bypasses and lossy transformations.
4. Compare each stage with the oracle. Preserve raw, normalized, rejected, written, and read-back representations so a mismatch can be localized.
5. Add mutation-sensitive tests that change source facts, order, formatting, omissions, duplicates, invalid values, and boundary cases. Confirm that the expected downstream signal changes or rejects the mutation.
6. Exercise only repository-defined, locally authorized checks. Writes must target an isolated disposable fixture or test store. Do not use customer data, production services, paid models, credentials, uploads, migrations, or deployments without separate authority.
7. Check retries, partial failure, duplicate delivery, idempotency, and reconciliation when the path can persist or replay data.
8. Classify evidence separately:
   - correctness: observed outputs match cited expected values for tested cases;
   - completeness: the authorized source population and required fields are represented;
   - storage correctness: committed values, identities, constraints, and readback match the write contract;
   - reproducibility: the same pinned inputs and configuration can reproduce the observation;
   - unresolved evidence: required proof is missing, inaccessible, or contradictory.
9. Report defects by first divergent stage. Do not infer full correctness from parser tests, a manifest, successful writes, or a repeated model response alone.

## Knowledge lifecycle handoff

When the audited path participates in `knowledge-contract.v1`, retain the exact IDs for source or dataset snapshots, method records, model runs, observations, and evaluations. The conformance matrix should identify which record can support each relationship. Keep raw facts, derived values, model output, human judgment, and retrospective interpretation in separate objects.

For forecast paths, reject any source snapshot whose as-of time is later than the declared cutoff. Do not overwrite a forecast after its cutoff; corrections create linked versions. Route a complete question-to-publication workflow to `research-to-publication-lifecycle` when that skill is installed.

## Routing Boundaries

- Use `test-strategy` to choose general software test layers.
- Use `test-quality-review` to assess existing test sensitivity and determinism.
- Use `acceptance-evidence-ledger` for a durable multi-gate completion contract.
- Use `authority-boundary-review` to decide owners, writers, readers, and source-of-truth rules.
- A product-specific model review belongs to its product catalog unless it asks for source-to-persisted-output fidelity.

## Output

Return `Scope and authority`, `Pinned source identity`, `Oracle`, a conformance matrix with `Stage`, `Input identity`, `Transformation`, `Expected`, `Observed`, `Evidence`, and `Result`, followed by `Mutation results`, `Correctness`, `Completeness`, `Storage correctness`, `Reproducibility`, `Unresolved evidence`, `Defects by first divergence`, and `Next authorized checks`. When requested, add the proposed knowledge-object IDs and relationship evidence without publishing or writing them automatically.
