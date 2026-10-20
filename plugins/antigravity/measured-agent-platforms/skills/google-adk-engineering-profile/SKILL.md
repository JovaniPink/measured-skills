---
name: google-adk-engineering-profile
description: "Reviews Google ADK architecture when asked about sessions, tools, models, evaluations, or deployment compatibility; checks exact versions and does not equate framework defaults with safety."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-agent-platforms"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Google ADK Engineering Profile

Review a Google Agent Development Kit design without confusing framework support with product authority. Read [the ADK version boundaries reference](references/adk-version-boundaries.md) when identifying an API, runtime skill, evaluation, session, or deployment contract.

## Preconditions

Identify the repository, language, installed ADK version, intended users, runtime environment, model provider, registered tools, session service, memory service, artifact service, and decision under review. If any version-sensitive behavior is material, verify it against the documentation for the exact installed version.

## Workflow

1. Separate the developer assistant from the product agent. A skill that helps a person build an ADK application is not automatically a safe runtime bundle for a SaaS user.
2. Inventory the agent hierarchy, models, instructions, callbacks, planners, tools, toolsets, sessions, state, memory, artifacts, retrieval, evaluation, and deployment boundaries actually present.
3. Pin the language, ADK package version, model or provider configuration, and relevant experimental features. Record observed support separately for Python, TypeScript, and Go.
4. Trace identity and authority from the product user through the host application to each agent and tool. Skill prose cannot create credentials, permissions, approvals, or a registered tool.
5. If `SkillToolset` is proposed, describe the runtime bundle, allowed content, integrity checks, release state, revocation, and progressive resource loading. Treat runtime Agent Skills as experimental until exact-version tests establish the required behavior.
6. Compose with `agent-context-state-memory-design`, `agent-tool-action-boundary-review`, `agentic-system-security-review`, `retrieval-grounding-quality-review`, `agent-evaluation-design`, and `observability-design` where their focused questions apply.
7. Separate local architecture evidence, synthetic tests, provider evaluation, authentication, infrastructure creation, deployment, and production acceptance. This workflow does not authorize deployment or any external action.
8. Report confirmed behavior, version-sensitive assumptions, missing evidence, and the smallest safe next test.

## Boundaries

- Google Agents CLI is optional developer tooling, not an ADK runtime dependency or a source of product authority.
- Experimental tool confirmation is not durable approval for real external writes. A production design needs authenticated approvers, external decision state, idempotency, replay protection, and audit evidence.
- An ADK runtime bundle must not be downloaded from a mutable branch during a run.
- Framework availability does not establish security, evaluation quality, production readiness, or client parity.
- This skill does not authorize deployment, cloud access, authentication, billing, publication, or release.

## Output

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return `Decision`, `Exact versions`, `Developer and runtime planes`, `Agent composition`, `State and memory`, `Tool boundaries`, `Runtime skills`, `Evaluation`, `Security`, `Operational boundaries`, `Confirmed evidence`, `Experimental or version-sensitive behavior`, `Missing evidence`, and `Next safe test`.

## Example

Synthetic example; not an observed client result.

Input: A design assumes agent sessions survive restarts without a configured store.

Output: Persistence is unverified. Identify the exact ADK session service and storage configuration; an in-memory session does not prove restart recovery.
