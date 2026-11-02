# Understand client usage and delegated permissions

A task can involve more model work than its visible user messages suggest.
Measure the work that completed the task, with its failures and limitations, before
claiming savings. A useful comparison preserves outcome quality and elapsed time.
This guide describes published behavior reviewed November 2, 2026; it does not
measure a particular account or certify an installed client.

## Keep the quantities separate

| Quantity | What it describes | What it cannot establish alone |
| --- | --- | --- |
| User requests and sessions | Authorized task boundaries | Number of inference calls or tokens |
| Request counts | Observed calls, classified by purpose and model where possible | Cost without token/cache/rate information |
| Input, cached input, output and reasoning tokens | Model usage in the observed scope | A final bill or subscription allowance consumption |
| Estimated model cost | Usage multiplied by an identified pricing basis | Charged spend, taxes, credits, or complete task economics |
| Account allowance and billed spend | Provider/account-specific consumption | Which feature caused it without attribution evidence |
| Task outcome and elapsed time | Whether the work advanced at the intended quality | Causation from one feature change alone |

Do not interchange percentages with different denominators, populations or time
windows. A zero count for one request category is not zero total auxiliary work.
Check whether cache and reasoning subtotals are already included before summing
reported totals. HTTP attempts, stream events and completed model calls are not
interchangeable units. A transcript can omit client-managed activity; missing
evidence remains unknown.
A provider estimate, a UI percentage and an invoice are different authorities.

## Published client behavior

| Client area | Supported conclusion | Verification limit |
| --- | --- | --- |
| Claude usage | Local token-cost estimates differ from authoritative billing; cache reads still contribute usage | Read the account, window and pricing basis before comparison |
| Claude background controls | Disabling background tasks changes several capabilities and leaves documented exceptions | It is not a summary-only control or proof of no auxiliary inference |
| Codex subagents | Delegated workers perform their own model/tool work | There is no universal token multiplier or savings percentage |
| Codex memories | Enabled memory extraction and consolidation can process eligible prior chats in the background | Generation and reuse are separate; flags do not prove execution or cost |
| Codex status display | Documented commands configure displayed fields and inspect session state | The inspected docs do not establish a recurring transcript-summary mechanism for those fields; absence of documentation is not proof of absence |
| Codex observability | OpenTelemetry export and analytics/health traffic have separate controls | No exporter in one user file does not prove no network activity or model usage |

## Permissions are inherited, not created by a reviewer role

Current OpenAI documentation says custom agents inherit the parent's permissions,
provider and MCP servers. Custom-agent files can change supported model settings,
instructions or disable supported capabilities; they cannot replace the inherited permission policy.
A role described as read-only does not create a separate sandbox.

Confirm the exact app/CLI and version, parent permissions, effective tools and
managed requirements before using a reviewer. File configuration, runtime readback
and observed behavior are different evidence. Do not run an extra model probe or
install an agent merely to close an evidence gap. Optional independent review stays
unavailable if its billing route or required isolation cannot be established.

## Observe only within the task's authority

1. Record the task, source snapshot, observation window, exact client/model/effort,
   permitted actions and intended finish line. Identify main, delegated and
   client-managed work without inventing counts.
2. Inspect relevant configuration sources and any existing usage evidence. Include
   memory-generation/reuse controls and eligibility where supported. A user file
   alone does not establish effective desktop, project or managed settings.
3. Use existing traces first. If new instrumentation is authorized, minimize data,
   approve the destination and retention, and check identifiers as well as prompts,
   responses, tool contents and raw API bodies. Keep private raw evidence outside Git.
4. Attribute observed requests and tokens by available purpose/model fields. Record
   sampling, retries, missing intervals and categories that cannot be distinguished.
   Do not fabricate a Claude-style query category in another client.
5. Compare completed work and elapsed time alongside usage. Keep original failures
   and repeated attempts. Unknown accounting is not permission to enable collection,
   restart shared services, patch a runtime or switch billing routes.

This is guidance, not a collector or new trial authorization. It does not alter
installed settings, launch reviewers, or run a model evaluation. The existing
narrow Haiku retest keeps its own frozen task, ceilings and fresh-control gates;
do not expand it into a usage experiment.

## Sources and review record

All links below are primary publisher documentation inspected November 2.
They describe current published contracts, not guaranteed support in every version.

| Source | Inspected material | Limit |
| --- | --- | --- |
| [Claude costs](https://code.claude.com/docs/en/costs) | Estimates, cache statistics and usage scope | No local savings measurement |
| [Claude environment controls](https://code.claude.com/docs/en/env-vars) | Background-task restrictions and remaining mechanisms | No setting changed or runtime pass observed |
| [OpenAI subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | Parent permission/provider/MCP inheritance | Actual host enforcement still needs evidence |
| [OpenAI memories](https://learn.chatgpt.com/docs/customization/memories) | Background generation, reuse and eligibility controls | No generation count or account cost observed |
| [OpenAI advanced configuration](https://learn.chatgpt.com/docs/config-file/config-advanced) | OTel events, analytics and configuration layers | Collection coverage and effective policy remain task-specific |
| [OpenAI developer commands](https://learn.chatgpt.com/docs/developer-commands) | Session, usage and display inspection | Command availability requires installed-version checks |

The official subagent Markdown was downloaded twice: both 22,907-byte responses
matched the existing SHA-256 pin
`e7469d41c5a18a4ee66ee40ca4a9a2617a697e42554a0198ac4481e1e597357f`.
The incorrect override claim was a defect in our local guidance, not demonstrated
upstream fingerprint drift. No pin or freshness policy changed, and these two
observations do not establish an online pass for all other authorities.
The text web reader rejected Markdown; direct read-only retrieval was used instead.

See the [earlier runtime review](audits/client-runtime-observation-2026-10-30.md)
for the original scoped change and preserved trial boundary. External comparisons
and machine/account observations remain in private research notes. This public
synthesis imports no external implementation and extends no maintainer acceptance.
