# Client control investigation, October 21

No new model case ran. The [Claude retest plan](claude-retest-plan-2026-10-21.md)
was prepared before the [source repairs](claude-source-repairs-2026-10-21.json).
The earlier pilot results and frozen inputs are preserved.

## Codex CLI 0.161.0

A fresh native app-server inspection used only initialization, skill listing,
account reading with token refresh disabled, and rate-limit reading. It returned
twelve enabled repository skills, eight disabled user entries, and no discovery
errors under the previously reviewed per-process overrides. No thread or turn
was started. This establishes that inventory under those overrides, not the
context or behavior of a future model request.

The account uses subscription authentication. Ordinary usage was allowed and
the response reported available credits. These fields do not identify a
per-request zero-credit guarantee or prove which credits would fund a later
request. No balance or account identifier is published here.

The installed experimental protocol schema has no credit-use or spending-limit
field in `ThreadStartParams` or `TurnStartParams`. Its
`allowProviderModelFallback` field concerns substituting a provider's default
model when the requested model is unavailable. Setting it to false would not
establish a billing boundary. `CreditsSnapshot` reports credit availability;
`spendControlReached` reports whether a backend spend control was reached. A
false or unavailable value is not a zero-spend setting. The read-only API offers
no verified way to impose that guarantee for this pilot.

The current [pricing documentation](https://learn.chatgpt.com/docs/pricing)
describes credits continuing usage after included limits. The
[configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
does not document a credit opt-out key. The
[app-server reference](https://learn.chatgpt.com/docs/app-server) describes credit
and quota observations, not a per-turn no-credit switch. This bounded search did
not establish that no such control could exist elsewhere; the lane remains
blocked under the requested no-paid-fallback condition. Do not consume reset
credits, change billing, add an API key, or send a limit-notification email.

Private receipt hashes:

- Native metadata: `b5c8b58230d55871ea87c9550c3e1a0e0287d9d5c0ccf5ea3b3e700e38a9bf82`.
- Installed `ClientRequest` schema: `b65bc353ccfbccaf04eb0934aa63220d73757d4f8001c6b13d3f2ed54e6af078`.

## Antigravity CLI 1.4.3

In the previously reviewed empty disposable workspace, native `/skills` again
listed 111 skills. `/context` showed an automatically loaded global instruction
file as well as zero user-message, response, and tool-call tokens awaiting the
first generation. Neither command sent a model case. No private instruction
content was imported into the repository.

The installed JSON configuration guide says explicit include/exclude filters do
not filter customizations inherited from the user's environment. The
[CLI reference](https://antigravity.google/docs/cli/reference) and installed help
provide no verified session-only replacement for those inherited sources.
`--sandbox` constrains tool execution; it does not isolate skill or instruction
discovery. `--disable-slash-commands` disables skills in print mode, which cannot
test the selected profile's activation.

The [agent selector](https://www.antigravity.google/docs/cli/commands/agents)
documents custom agent instructions and tools, without establishing removal of
inherited user context. The [SDK's skill paths](https://antigravity.google/docs/sdk/tools)
belong to a different execution surface. Neither is evidence that this installed
CLI can load only the staged profile. No SDK runner or custom agent was added.

The native Use AI Credits control remained off on readback. Billing was not
changed. Isolation still fails for both skills and inherited instructions, so
the lane remains unrun. A supported session-only exclusion mechanism needs an
effective inventory and context check before any case. A separately provisioned
account/environment would need its own sign-in, policy, and acceptance review;
do not copy credentials or modify ordinary installations to manufacture a pass.

## Remaining acceptance

The Claude source repair is a candidate until the proposed retest is authorized
and observed. Codex still lacks a verified no-paid-fallback route; Antigravity
still lacks effective context isolation. App-mode, M5, full-catalog benefit, and
cross-client parity remain unobserved. Repository checks and source-file hashes
do not close those gaps.
