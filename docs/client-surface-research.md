# Client Surface Research

Reviewed: 2026-09-04

This note separates documented product support from observed installation and invocation behavior. It does not claim parity between clients, APIs, or runtimes.

## OpenAI assistant surfaces

OpenAI documents skills for ChatGPT and Codex with different selection forms and installation paths. ChatGPT uses an `@` selector. Codex uses `$` and supports plugin marketplaces for local and repository distribution.

Codex limits the initial skill discovery list to 2 percent of the context window, or 8,000 characters when the context size is unknown. This repository therefore measures every plugin and recipe and recommends focused installation.

The repository's v0.8 matrix records 42 blocked rows across Codex CLI, ChatGPT Desktop, and ChatGPT Web plus the Anthropic surfaces. Those rows do not establish current installation, activation, reference loading, update, or removal behavior for v0.9.

Primary sources:

- OpenAI, [Build skills](https://learn.chatgpt.com/docs/build-skills), reviewed 2026-08-25.
- OpenAI, [Build plugins](https://developers.openai.com/plugins/build/plugins), reviewed 2026-08-25.

## OpenAI Skills API

OpenAI separately documents a project Skills API for creating, listing, retrieving, deleting, and versioning uploaded skills. API-managed skills are not the same observation surface as ChatGPT or Codex plugin installation.

An API row must record the exact API and SDK version, project, skill version, uploaded artifact digest, request, response, cost authority, and data-handling boundary. No Skills API call is made by repository validation.

Primary source:

- OpenAI, [Skills API reference](https://developers.openai.com/api/reference/go/resources/skills), reviewed 2026-08-25.

## Anthropic local and web surfaces

Claude Code and Claude Desktop use plugin and local skill paths. Claude.ai custom skills use individual uploads. These distribution paths are tested separately.

The current v0.8 matrix contains no passing receiving-client observation. Earlier version observations remain historical evidence for those exact packages only.

Primary sources:

- Anthropic, [Claude Code on desktop](https://code.claude.com/docs/en/desktop), reviewed 2026-08-25.
- Anthropic, [Discover and install plugins](https://code.claude.com/docs/en/discover-plugins), reviewed 2026-08-25.
- Anthropic, [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces), reviewed 2026-08-25.
- Anthropic, [Use Skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude), reviewed 2026-08-25.

## Anthropic Skills API and Managed Agents

Anthropic documents two API-related skill paths.

The Skills API creates and versions custom skills. Messages API use requires the code-execution container and has separate beta and data-retention conditions. Anthropic Managed Agents can attach uploaded skills or discover `.claude/skills` from a mounted GitHub repository at session start.

Anthropic explicitly warns that a mounted repository is part of the agent trust boundary. A contributor or compromised dependency can change instructions, and session tools give those instructions practical reach. Pin the repository commit, review `.claude/skills`, minimize tools, and keep API observations separate from Claude Code and Claude.ai.

Primary sources:

- Anthropic, [Using Agent Skills with the API](https://platform.claude.com/docs/en/build-with-claude/skills-guide), reviewed 2026-08-25.
- Anthropic, [Managed Agents skills](https://platform.claude.com/docs/en/managed-agents/skills), reviewed 2026-08-25.

## Antigravity CLI and enterprise Gemini CLI

Google transitioned individual free, Google AI Pro, and Google AI Ultra users from Gemini CLI to Antigravity CLI. Antigravity CLI is therefore the primary future Google developer-client key. Gemini CLI remains a conditional compatibility surface for intentionally licensed Gemini Code Assist Standard or Enterprise and paid Agent Platform use.

The repository preserves its Gemini CLI 0.56.0 rows as historical evidence for that exact package and workspace-link observation. Those rows do not establish current individual guidance or enterprise compatibility. A future Antigravity row must record the exact `agy` version and binary digest, model and effort, clean configuration home, source revision, discovery, activation, focused-reference loading, permissions, sandbox, network policy, normalized terminal and tool events, and removal result. Exit code zero alone is insufficient when a permission denial can be soft-denied while execution continues.

The Delivery TypeScript profile includes the explicit-only `publish-change-safely` skill. In version 0.17.0, Antigravity packs included it with `disable-model-invocation: true`. Version 0.17.1 and later leave it and every other explicit-only workflow out, because that control is unverified on Antigravity: Google's skill docs list only `name` and `description`, and no agy run has shown that the field stops automatic selection. Claude Code behavior does not carry over.

Primary sources:

- Google, [Gemini CLI to Antigravity CLI transition](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/), reviewed 2026-09-04.
- Google, [Antigravity Agent Skills](https://antigravity.google/docs/skills/), reviewed 2026-09-04.
- Google, [Antigravity headless mode](https://antigravity.google/docs/cli/headless/), reviewed 2026-09-04.

## Google ADK runtime

Google ADK can load open-format skills into an application agent through experimental `SkillToolset` support. This surface can expose skill loading, resource loading, and skill-script execution facilities. It therefore has a different threat model from an assistant plugin.

ADK runtime observations belong in `JovaniPink/jovanipink-adk`, where immutable bundle verification, tool registration, session isolation, malicious-input tests, and exact ADK version evidence can be tested together. They are intentionally excluded from this repository's assistant compatibility matrix.

Primary source:

- Google, [ADK Agent Skills](https://adk-labs.github.io/adk-docs/skills/), reviewed 2026-08-25.

## Security boundary

Generated plugin and archive validation does not establish receiving-client behavior. Repository-mounted or uploaded skills are instructions inside a host trust boundary. Review exact content before installation, use the smallest useful pack, start a fresh session, and record each surface separately.

No Antigravity or Gemini installation, API credential, model call, cloud deployment, marketplace publication, or runtime ADK operation is part of deterministic repository validation.
