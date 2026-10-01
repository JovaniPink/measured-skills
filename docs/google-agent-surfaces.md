# Google Agent Surfaces

Setup policy updated: 2026-09-30. Older runtime research remains separate.

Check each Google app or tool on its own. A skill that works in Antigravity CLI may still need changes for the desktop app or IDE. Record the results separately in [`catalog/google-surfaces.json`](../catalog/google-surfaces.json). Start with [Antigravity setup](clients/antigravity.md).

## Surface map

| Surface | Evidence question | Current catalog position |
| --- | --- | --- |
| Gemini model | Which exact model and effort minimize cost per successful case? | Execution-envelope variable, not a skill-compatibility claim. Availability and pricing come from current API release and deprecation records. |
| Antigravity CLI | Does a focused treatment improve a clean local Google coding agent? | Setup and manual tests may proceed now, independently of Codex. Useful behavior remains unverified. |
| Gemini CLI Enterprise | Does intentionally licensed enterprise access load the projection? | Conditional compatibility only. Gemini CLI 0.56.0 evidence is historical and does not establish this claim. |
| Antigravity Desktop | Does usefulness survive the visual surface? | Independent manual checks; no CLI result is required to start. |
| Antigravity SDK | Can the same semantics run safely through Google's Python harness? | Separate runtime-harness lane even if it shares implementation with the CLI. |
| Gemini Managed Agent | Can a mounted skill improve a hosted sandboxed agent? | Separate synthetic/public hosted lane with a preregistered cost ceiling and retention policy. |
| Google ADK | Can an immutable bundle load without granting authority? | Separate runtime-compatibility lane owned by `jovanipink-adk`. |
| Agents CLI | Can a coding agent safely evaluate or prepare Google deployments? | Lifecycle-tool lane. Provider actions require explicit RELEASE authority and readback. |
| Data Agent Kit | Can vendor skills and MCP tools support governed data work? | Conditional tool/plugin lane; confirm the exact feature's launch stage and compatibility before use. |
| Gemini Enterprise Agent Platform | Can an application meet production identity, governance, runtime, memory, evaluation, and observability requirements? | Product/runtime evidence, never blended with skill behavior. |

## Setup and study checks

Antigravity setup, packaging, and manual checks have equal priority with Codex and Claude. The offline preview builder adds no client runner. Any future automated runner needs its own reviewed plan, fixed client version and file hash, isolated test account or container, and scoped authentication. Keep personal skills, memories, conversations, and vendor packs out of controlled studies.

Each paired run must use fresh pinned worktrees, a natural empty configuration home, fixed model and effort, sandboxed scoped permissions, a fixed network policy, and headless JSON or stream-JSON evidence. The grader must parse terminal result status and tool events; process exit code zero is not sufficient evidence of success.

The Delivery TypeScript profile includes the explicit-only `publish-change-safely` skill. Version 0.17.1 excludes it and every other explicit-only workflow from Antigravity packs. Google's documented skill fields do not establish an automatic-selection control. The disposable CLI 1.2.9 package checks cover all nine implicit-only packs; full catalog behavioral qualification remains pending.

## Packaging boundary

Agent Plugins 1.0 and Antigravity's native plugin format are not treated as identical. The portable specification uses `plugin.json` with `mcp.json`; the reviewed Antigravity documentation describes its own manifest schema and `mcp_config.json`. A skills-only Agent Plugins proof package is deferred until a selected conformant client accepts a minimal package. Antigravity-native packaging remains a separate projection unless live evidence proves compatibility.

Packaging never establishes installation trust, sandboxing, credential scope, permission safety, provenance, or behavioral improvement.

## Cost, freshness, and authority

Hosted agents and vendor data tools need separate tests, cost limits, and data rules. An Antigravity CLI result does not cover them.

Do not hard-code a preferred Gemini model into a portable skill. Record exact model and effort in each execution envelope, check current Gemini API release and deprecation records, and compare cost per successful case.

Do not install, authenticate, deploy, publish, or enable provider actions as part of deterministic catalog validation. Agents CLI `infra`, `deploy`, and `publish` commands require explicit RELEASE authority and post-action provider readback. Managed Agent calls require separate credential, cost, retention, environment-deletion, tool, and network authorization.

## Primary sources

- Google, [Gemini CLI to Antigravity CLI transition](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/)
- Google, [Antigravity Agent Skills](https://antigravity.google/docs/skills/)
- Google, [Antigravity plugins by surface](https://www.antigravity.google/docs/plugins?tab=cli)
- Agent Plugins, [Agent Plugins 1.0 specification](https://agent-plugins.org/specification)
- Google, [Antigravity headless mode](https://antigravity.google/docs/cli/headless/)
- Google, [Antigravity SDK](https://www.antigravity.google/docs/sdk/overview)
- Google, [Gemini Managed Agents](https://ai.google.dev/gemini-api/docs/agents)
- Google Cloud, [Data Agent Kit overview](https://docs.cloud.google.com/data-agent-kit/overview)
- Google, [Gemini model documentation](https://ai.google.dev/gemini-api/docs/latest-model)
- Google, [Agents CLI](https://developers.googleblog.com/agents-cli-in-agent-platform-create-to-production-in-one-cli/)
- Google Cloud, [Gemini Enterprise Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform/overview)
