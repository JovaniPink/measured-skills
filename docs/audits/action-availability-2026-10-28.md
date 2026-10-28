# Action availability and maturity clarification

## Objective

Make each action's package requirements visible beside its prompt. Separate observed use, repeatable acceptance, and comparative benefit without changing classifications or granting authority.

## Current evidence

Review checkpoint: e996688062a24dca93d4fd9ba50308e8ecac2fda. Both chooser views described the route's primary skill even when a later action used a different entry. Finish-work assessment uses plan-change; repair uses execute-plan; maintenance uses publish-change. The latter two are explicit-only and outside finish-work-core. Antigravity excludes them. Ordinary requests remain usable without implying that those entries loaded.

The taxonomy defined field-tested through observations but also required a baseline comparison before any promotion. That conflated use with benefit. All current candidate labels and existing release gates remain unchanged.

## Interfaces and implementation steps

1. Derive per-action, per-client guidance from the actual command skill, canonical packaging/invocation metadata, and core profile membership. Keep the workflow registry as the route owner; do not hand-maintain a second availability inventory.
2. Render the same guidance beside each prompt in Markdown, bundled references, static HTML, enhanced offline HTML, and the website. Keep details available without JavaScript. Identify ordinary-request paths separately from native command paths.
3. Clarify maturity thresholds in taxonomy documentation. Preserve historical records and current classifications. Comparative benefit needs its own comparison evidence.
4. Regenerate the discovery bundle, skill projections, and archives. Preserve source ancestry and the clean-source/manifest commit sequence. Pin the website export to the reviewed artifact commit.

## Research ledger

Inspected October 28, 2026:

- [Agent Skills specification](https://agentskills.io/specification): metadata describes a skill and its intended use; format compliance does not establish successful task behavior. No upstream definition of this repository's maturity states is asserted.
- [Claude Code skills](https://code.claude.com/docs/en/skills): selection and user-only invocation controls are client-specific. Published capabilities are not observations of installed 0.19 sources. No client or model was launched.
- [Progressive disclosure](https://www.nngroup.com/articles/progressive-disclosure/): keep primary choices accessible and defer specialist detail. Application here is an original design judgment, not measured usability improvement.

No upstream material defines our promotion thresholds. These are repository policy clarifications, not research-proven performance levels. No source pins were repinned and no external implementation was imported.

## Test strategy and checkpoints

Exercise the action/client matrix, including assessment versus repair/maintenance, Antigravity exclusions, web upload holds, and implicit specialists outside the core profile. Test both website rendering and actual offline enhancement. Check the static fallback. Rebuild twice and compare archive hashes; run repository gates and affected website checks.

Checkpoint: the prompt and its adjacent availability refer to the same action entry. No availability text claims installation, successful loading, or new authority. The candidate inventory and 17 explicit-only classifications must remain unchanged.

## Rollout, rollback, risks, and stopping conditions

Update existing drafts only. No installation, model evaluation, merge, deployment, billing change, or release. Roll back with ordinary corrective commits and regenerate dependent artifacts; do not rewrite source anchors. A source revert alone does not roll back installed copies.

The ten-card human exercise remains prepared, not run. Do not substitute automated rendering tests for user acceptance. Stop expansion if these changes require a new skill, permissions, maturity promotion, or inferred client qualification. Remaining naming concerns are hypotheses for that exercise, not reasons for speculative renames.
