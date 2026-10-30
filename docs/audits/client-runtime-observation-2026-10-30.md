# Client runtime and usage evidence

Reviewed October 30, 2026. Original instruction-only synthesis after external
research; no external implementation, runtime patch, or source text is imported.
This is a technical delta, not new maintainer acceptance or client qualification.

## Focused change

`coordinate-agents` separates authorized worker/session limits from client-managed
inference and actual account usage. Its self-contained client reference explains
observation scope, supported controls, and private-data boundaries.
`design-agent-evaluations` separates task requests, inference requests, estimates,
allowance, and bills. Outcomes and elapsed time remain part of any comparison.
No new skill, permission, profile, executable, telemetry configuration, or model
trial is introduced. Existing source pins and freshness policy remain unchanged.

## Primary-source review

All three official pages were inspected on October 30. They describe current
published behavior, not a guarantee for an installed client. Existing provenance
bindings remain intact; this supplemental review does not repin those sources.

| Source | Supported conclusion | Limit |
| --- | --- | --- |
| [Claude cost documentation](https://code.claude.com/docs/en/costs) | Clients can perform auxiliary model work; local token-cost estimates differ from authoritative billing | No local overhead percentage or account allowance result follows |
| [Claude monitoring documentation](https://code.claude.com/docs/en/monitoring-usage) | Request-source and token/cache metadata can support attribution; logging can expose identifiers and optional session content | Availability, coverage, destination, and retention need exact-client review before use |
| [Claude environment variables](https://code.claude.com/docs/en/env-vars) | Background-execution controls have specific capability effects and exclusions | Disabling one mechanism does not establish zero background activity |

External discussion prompted these questions but supplies no portable behavior
rule or performance claim. No universal token multiplier, savings percentage,
or complete API-call count is asserted.

## Preservation and next action

The [original Haiku assessment and narrow retest](haiku-evidence-followup-2026-10-29.md)
remain unchanged. Its two sessions and continuation had no delegation tools;
this review does not attribute their evidence/reporting failures to background
agents. Their full request counts and cost remain unmeasured.

The prepared one-session/one-continuation retest remains unrun, with its existing
scope, ceilings, fresh-control requirements, and separate execution authority.
Do not add a usage experiment, telemetry setup, or background worker to that
packet. If a later task needs usage observation, authorize it separately and
retain its private raw evidence outside this repository.

## Prepared review scenarios

These are source-review scenarios, not executed model cases:

- Two user sessions with unknown internal calls: report two sessions, unknown
  request count; do not infer zero overhead from absent transcript entries.
- A passing file receipt with a runtime preload: file correspondence remains
  valid, but runtime equivalence is unverified.
- A cheaper run with an incomplete task: do not label it an outcome improvement.
- A supported background-disable flag: inspect its documented scope and lost
  capabilities; do not describe it as a summary-only or all-network control.
- Missing telemetry: retain unknown usage; do not enable collection or rerun work
  without authority.

Existing reference, canonical-delta, export, invocation, and boundary checks cover
packaging. No tests merely asserting this prose are added. Local validation and
GitHub status are recorded in the delivery PR; neither establishes client behavior.
