# Full catalog qualification

Cover every canonical skill and each independently deployed copy on every applicable supported client surface. Package checks, actual source loading, routing, semantic quality, task outcomes, and benefit over baseline are separate claims.

## Cases and runs

For each skill define at least three positive, three near-miss, and one safety case. Preserve richer existing suites. Cases and their mandatory obligation IDs are frozen and hashed before execution; graders cannot remove obligations to make a record pass. Include ambiguous routing and catalog-level interference. Synthetic graders test the grading contract, not client behavior.

Run baseline and skill conditions three times per case, rotating order and holding model, permissions, tools, fixtures, and configuration constant. For each skill also probe positive, boundary, and safety behavior at turns 1, 8, and 20 with fixed hashed prefixes. Repetitions measure stability, not independent coverage. Record context size and compaction. A finite sample establishes observed performance only.

## Evidence and disposition

Use [record schema v1](../evals/qualification-schema-v1.json). Validate and summarize a record with `python3 scripts/grade_qualification.py RECORD.json --case FROZEN_CASE.json`. The CLI requires a reviewed frozen case conforming to [case schema v1](../evals/qualification-case-schema-v1.json). It checks the exact case hash and every obligation ID, kind, and mandatory flag. Freeze the prompt, fixture references, and assertions together before either condition runs. This grades declared assertions; it does not independently establish whether the declarations are true. Each declaration must be checked against frozen case obligations and actual evidence by deterministic or human-calibrated graders. All safety and authority assertions must pass in every observed trial. Every failed mandatory case remains visible.

Human-review all safety failures, disputed grades, and a blinded calibration sample. Preserve source hashes and actual loading observations independently of response headings. A blocked run is not a pass. Permission bypass results cannot establish acceptance under ordinary permissions. Presentation is scored separately.

## Surfaces and lifecycle

Use every row of [client support](client-support.md); Claude Chat and Cowork are distinct conditions. Installed, enabled, listed, loaded, and behaviorally tested remain separate. For every applicable pack test install, update, downgrade, disable, uninstall, reinstall, fresh-task absence, focused-reference reads, interruptions, and intentional goal changes. Unsupported cells need evidence; blocked cells remain unfinished. APIs, SDKs, hosted agents, and ADK are outside this campaign.

Antigravity explicit-only skills are held and absent from installable output. Test exclusion; do not install them to test whether they happen to stay inactive.

## Budget and release

Run deterministic repairs and lifecycle smoke checks first. Estimate token use and operator time from a small bounded calibration batch. Calculate the remaining campaign estimate, then obtain a numeric ceiling before paid expansion. Stop at the ceiling and retain unrun cells. Never infer all-catalog benefit from installation or a few successful prompts.

Keep raw traces and private inventories out of this public repository. Commit synthetic fixtures and reviewed redacted receipts only. Recheck affected cases when workflow semantics, client adapters, models, permissions, or client versions change. Qualification does not authorize publication or global promotion.

## Bounded workflow pilot

The [three-condition preparation kit](../evals/behavior-study/README.md) keeps
24 selected cases, three repetitions, and both CLI lanes separate. Its 432 core
cells are not full-catalog qualification. The 324 later-context cells remain a
separate stage. Every cell is not run; the kit has no model execution option.

## October 7 repaired draft

The [v2 workflow kit](../evals/behavior-study-v2/README.md) binds the repaired
canonical source while preserving v1 bytes. Both remain unregistered and unrun.
Use the [current client packet](client-qualification-preparation-2026-10-07.md)
for help/version observations and unresolved native prerequisites.
