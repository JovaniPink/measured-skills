# Agent Platform Boundaries

This project separates skills used by people from skills loaded inside a product agent.

```text
Jovani and developers
    -> ChatGPT, Codex, Claude, or Antigravity CLI
    -> JovaniPink/measured-skills
    -> Research, planning, engineering, and business workflows

SaaS user
    -> Product interface
    -> Product ADK agent
    -> JovaniPink/jovanipink-adk runtime adapter
    -> Private released product skill bundle
    -> Separately authorized tools and data
```

## User-assistant plane

The public `JovaniPink/measured-skills` catalog helps a person direct a general-purpose assistant. It contains portable instructions and focused references. It has no skill-level executables, hooks, MCP servers, bundled agents, dependencies, credentials, or broad grants.

Its skills can organize evidence and recommend a workflow. They cannot turn prose into enforcement. The assistant host, repository scripts, client permissions, and user authority remain controlling.

## Runtime-agent plane

The public `JovaniPink/jovanipink-adk` repository provides a content-addressed adapter, synthetic examples, policy checks, and evaluations for loading reviewed skills into an ADK runtime. It does not contain product facts or deploy a service in v0.1.

Private product repositories own product-specific skills, schemas, authority contracts, customer facts, tool definitions, release approvals, and operational identities. A product bundle becomes runtime eligible only after its immutable artifact, evaluation evidence, attestation, compatibility, and release decision pass deterministic policy.

The runtime adapter never clones a mutable skill repository during a request. Skill text never grants a tool, credential, tenant, role, production capability, or approval.

## Three security reviews

- `application-security-review` covers conventional application and service controls.
- `skill-security-review` covers skill packages, instructions, references, dependencies, hooks, and installation effects.
- `agentic-system-security-review` covers agent identity, tools, memory, retrieval, delegation, guardrails, protocol boundaries, and model-mediated action.

Use the reviews together when the system crosses all three boundaries. Do not use one as a substitute for another.

## Mounted repositories are trusted inputs

Anthropic documents that repository-mounted skills become agent instructions at session start. Anyone who can change the mounted repository can change those instructions, and available tools give the instructions practical reach. Treat the repository revision, contributors, dependency graph, and `.claude/skills` directory as part of the agent trust boundary.

The same general rule applies to any runtime that discovers skills from a repository or archive: verify exact content before use, pin immutable revisions, minimize tools, isolate tenants and sessions, and preserve revocation and emergency-stop controls.

## Tool and action boundary

Tools are registered by the host. A skill may describe when a tool would help, but it cannot add the tool or expand its permission.

For write-capable actions, production approval eventually needs durable external state, authenticated approvers, idempotency keys, replay protection, and an auditable decision record. Experimental in-model or framework confirmation is not enough for irreversible effects.

## API surfaces are separate products

Do not infer API behavior from a desktop or CLI observation.

- OpenAI Skills API manages project skills and immutable versions. Its evidence belongs to an API-specific compatibility row.
- Anthropic Skills API manages custom skills for API use. Messages API skills use a code-execution container and have their own data-retention and beta requirements.
- Anthropic Managed Agents can attach skills or discover repository-mounted skills in a managed session. Its trust and permission model differs from Claude Code and Claude.ai.
- Antigravity CLI is the primary future Google developer-client lane for individuals. Historical Gemini CLI observations do not establish Antigravity behavior.
- Gemini CLI Enterprise is a conditional compatibility lane requiring an intentionally in-scope enterprise license and its own observation.
- Antigravity Desktop, Antigravity SDK, and Gemini Managed Agents each require separate evidence.
- Google ADK runtime skills execute inside an application-owned agent runtime and belong to the separate ADK repository's test matrix.

## Primary resources

- [OpenAI Skills API](https://developers.openai.com/api/reference/go/resources/skills)
- [Anthropic Skills API guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide)
- [Anthropic Managed Agents skills](https://platform.claude.com/docs/en/managed-agents/skills)
- [Google's Gemini CLI to Antigravity CLI transition](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/)
- [Antigravity Agent Skills](https://antigravity.google/docs/skills/)
- [ADK Agent Skills](https://adk-labs.github.io/adk-docs/skills/)
- [OWASP Agentic Security Initiative](https://genai.owasp.org/initiatives/agentic-security-initiative/)
- [NIST identity and authorization for software agents](https://www.nist.gov/news-events/news/2026/02/new-concept-paper-identity-and-authority-software-agents)
