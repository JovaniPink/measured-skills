# Gemini 3.8 Flash Behavioral Trial Preparation

Status: `prepared_not_run`. Prepared November 2, 2026.

This protocol establishes a frozen, bounded trial definition for evaluating skill discovery and execution fidelity using **Gemini 3.8 Flash** on the **Antigravity IDE / CLI** surface. It conforms to the repository's audit and evaluation architecture and does not authorize or trigger model execution.

## Upstream Evidence and Execution Envelope

The upstream review record (`catalog/upstream-reviews.json`) notes:
- The [latest-model documentation](https://ai.google.dev/gemini-api/docs/latest-model) documents Gemini 3.8 Flash and time-limited introductory pricing.
- Model availability, pricing basis, and thinking level remain volatile execution-envelope facts.
- Portable skills in `skills/` must remain model-agnostic; model parameters and thinking configurations belong to per-run execution receipts.

The trial configuration prepared here records:
- **Surface**: Antigravity IDE / CLI loading plugin packages from `.gemini/plugins/` (and projected in `plugins/antigravity/`).
- **Model**: `Gemini 3.8 Flash`.
- **Thinking Effort**: `High` (observed local envelope).
- **Candidate Revision**: `d85c7b5947adfe3f4e4c2a9fec9068559b975c3e` (PR #83 head).

## Bound Scope and Selected Skills

Antigravity distributions package implicit-invocation skills (73 canonical skills) while excluding explicit-only skills (17 canonical skills, such as `coordinate-agents`).

The [preparation record](gemini-flash-trial-preparation-2026-11-02.json) binds exact hashes for three implicit skills across two plugin packs:
1. `explain-codebase` (`measured-workflows`)
2. `verify-claims` (`measured-quality`)
3. `run-project-checks` (`measured-quality`)

All staged file hashes for `SKILL.md`, `LICENSE`, and reference documentation are recorded in the accompanying JSON artifact.

## Four Case Sessions and One Follow-up

| Order | Source Case | Selection Mode | Expected Behavior |
| --- | --- | --- | --- |
| 1 | `explain-codebase-positive-1` | Implicit | Implicit activation of `explain-codebase`; traces flow from entrypoint to storage with concrete file links and failure paths without speculating on unexecuted intent. |
| 2 | `verify-claims-positive-2` | Implicit | Implicit activation of `verify-claims`; assesses claims against log evidence without inventing unobserved test success. |
| 3 | `run-project-checks-positive-1` | Implicit | Implicit activation of `run-project-checks`; preserves incomplete state and reports evidence without applying changes. |
| 4 | `near-miss-1` | Implicit (Control) | General response without activating a specialized engineering skill. |

### Follow-up Continuation
- **After Case 1**: In the same conversation, issue the frozen status continuity prompt. The model must preserve the original goal, report findings and unfinished checks, and refrain from editing files or broadening scope.

## Execution Ceilings and Stopping Conditions

1. **Ceiling**: Exactly four case sessions (three positive, one near-miss control) and one continuity follow-up. Zero replacement retries.
2. **Prior Authorization Required**: Model execution requires explicit maintainer authorization, a verified billing/credit quota check on the Google Cloud / Gemini API account, and execution in an isolated disposable workspace.
3. **No Automated Inferences**: Neither unit tests nor deterministic catalog checks may call model endpoints.
4. **Stopping Condition**: If ambient or overlapping plugin copies are detected, or if billing accounts cannot be verified before execution, the trial must halt immediately before any inference request is sent.
