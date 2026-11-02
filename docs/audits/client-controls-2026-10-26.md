# Client acceptance controls, October 26

No client lane qualified in this follow-up. Codex still lacks a verified
no-paid-fallback boundary. Antigravity still fails the native isolation check.
Claude has a newly staged, bounded diagnostic proposal, not a new result.
The [sanitized receipt](client-controls-2026-10-26.json) records observations and
hashes; the [October 21 record](client-controls-2026-10-21.md) remains historical.
No model request, paid evaluation, billing change, merge, or release occurred.

## Codex: account metadata is not a spending limit

The installed CLI reports 0.161.0. Its native app-server handled only initialize,
account/read with refreshToken false, and account/rateLimits/read. No thread or
turn was started. The response reports ChatGPT authentication, available credits,
and spendControlReached false. This is account state, not an instruction to stop
before consuming credits. Balances and account identity are not published.

The locally generated experimental ThreadStartParams and TurnStartParams schemas
expose no dedicated per-request zero-credit limit. A generic config field is not
evidence that an invented billing key works. allowProviderModelFallback concerns
replacement of an unavailable model, not credit fallback. The official
configuration reference inspected below also supplies no such credit control.
These bounded inspections do not prove that no control exists anywhere.

Keep the model lane blocked. Do not infer safety from available quota, a paid
subscription, Standard speed, or a false spendControlReached value. Do not change
billing, consume credits, redeem resets, or use an API/proxy fallback to test it.
The next useful evidence is an applicable, supported account or per-run control
whose actual state rules out paid continuation for this receiving account.

## Antigravity: a selected agent still reports ambient context

The initial version command returned 1.4.4. On reopening the native interface,
the banner and version command returned 1.4.7, and the executable bytes changed.
No update command was issued. The cause of the change was not established; do not
claim that 1.4.4 was the version used for the observations below. Recheck versions
and executable identity before any future model case.

An empty disposable workspace still showed 111 skills in /skills. The /context
panel reported a global instruction file as auto-loaded. Its pre-generation
estimate showed zero user, response, and tool tokens. The /credits panel said
AI Credits were not enabled. No toggle or purchase action was selected.

A second metadata-only session selected a disposable custom agent with
inheritCustomizations false, twelve staged daily-profile skill paths, an empty
tool list, and command execution off. The status line confirmed that agent was
selected. Nevertheless, /skills still showed 111 entries and /context still
reported the global instruction file, alongside the local agent directory.
The profile files were staged from the same source as Claude; no ordinary
installation or global configuration was replaced.

This does not establish the exact eventual model prompt: discovery lists and
pre-generation estimates can differ from runtime inclusion. It does establish
that the required native readback did not demonstrate isolation. Do not run a
model case to find out whether unwanted material is sent. Keep the lane blocked.
The installed configuration guide still says explicit-path exclusion filters do
not filter inherited user customizations. A hidden flag string found in the
binary is not a supported isolation contract and was not used to start a session.

Automatic approval review initially blocked accepting the workspace-trust prompt
because it grants read, edit, and execute access. The user then explicitly allowed
that one disposable inspection. Only native metadata panels were used; no model
task or tool execution was requested. Trust is not isolation or model authority.
Both inspection sessions were closed. Raw account details stay outside Git.

## Claude: exact staging, limited native format evidence

Claude Code reports 2.1.306. The existing machine kit staged the twelve-skill daily
profile from 3c5cc3a794918773ac649e072ccd58e4f0bced5f. All 50 receipt-listed
files match, including 38 plugin files and twelve account-upload archives. The
kit's verify operation separately confirms the plugin files; neither comparison
establishes installation, loading, or behavior.

Native strict plugin-manifest validation returned success without manifest
errors or warnings. Its report contained zero content checks. Passing a skills
directory also returned zero content checks; a skill directory or SKILL.md file
was not accepted as a plugin manifest. These probes do not establish native
skill-body validation. The report's directory-submission advice is a different
check, not requested for this disposable local wrapper; it includes a missing
README. No directory submission or installation occurred.

The [new retest preparation](claude-routing-contract-retest-plan-2026-10-26.md)
binds exact inputs and files. Fresh Claude account, credits, isolation, model,
and effort observations remain prerequisites. The prior allowances are consumed;
preparing this proposal does not authorize another model session.

## Primary-source ledger

All sources below were inspected October 26, 2026. These are operational research
references, not changed catalog pins. No freshness policy or source pin changed.

| Source | Supported conclusion | Limit |
| --- | --- | --- |
| [OpenAI pricing](https://learn.chatgpt.com/docs/pricing) | Available credits can continue usage after included limits. | Does not prove this account has a no-credit execution route. |
| [OpenAI configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) | Published agent configuration is distinct from account billing. | No credit opt-out found; absence in this page is not proof of universal absence. |
| [Antigravity CLI reference](https://antigravity.google/docs/cli/reference) | Native skills, context, usage, and credits panels are available. | Published commands do not establish effective isolation. |
| [Antigravity agent selection](https://antigravity.google/docs/cli/commands/agents) | A custom agent can be selected for a fresh session. | Selection alone does not prove its ambient context was removed. |
| [Antigravity changelog](https://antigravity.google/docs/changelog?tab=cli) | The v1.1.14 entry describes an inheritance switch for custom agents. | The 1.4.7 native readback did not satisfy this pilot's isolation requirement. |
| [Antigravity custom agents](https://antigravity.google/docs/subagents) | Documents local agent definitions, skill paths, tools, and command policy. | No delegated agent was invoked and no model behavior was tested. |

The web reader could not render the Antigravity Markdown reference/agents URLs;
HTML pages were inspected instead. Installed help, schemas, and built-in guide
text were checked separately from web documentation. No third-party skill
implementation or publisher prose is imported into the catalog.
