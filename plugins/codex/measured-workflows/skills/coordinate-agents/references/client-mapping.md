# Client mapping

Client capabilities change independently. Verify current official documentation and record the exact client and version before claiming support.

## Portable invariants

- Delegation requires host and user authorization.
- Each worker receives a bounded task, ownership boundary, evidence contract, and stop condition.
- Parallel tasks must be independent enough to reconcile safely.
- Worker completion is an input to integration review, not proof of correctness.
- Publication, deletion, deployment, and merge decisions stay with the authorized integration owner.

## Usage evidence

Client-managed model work can occur outside visible worker messages. A session
count, selected model, transcript, or matching skill hash is not a complete usage
account. Record the observation window, client version, configuration sources,
and accounting coverage before attributing overhead or savings. Distinguish
request categories and cache usage where observed; do not invent missing counts.
Subscription allowance, estimated token cost, and actual billed spend are separate.

Use supported controls only within existing authority. A control that disables
background execution can also remove useful capabilities and may leave other
background mechanisms active. It is not proof of zero auxiliary inference.
Do not inject runtime patches, replace launchers, restart shared daemons, or
silently change model or billing routes to reduce overhead.

If usage observation is separately authorized, collect only needed metadata to
an approved destination. Check identifier exposure and retention as well as
prompt, response, tool-content, and raw-body logging. Preserve unknown coverage;
do not export private session contents to make a cost claim more precise.

## Codex

Codex can expose subagents and inspectable threads depending on the surface and version. Current OpenAI documentation describes delegation after a direct request or applicable project or skill instruction in local Codex clients. Local subagents inherit the current sandbox, while permission behavior is surface-specific; child model and reasoning settings may inherit or be configured separately. ChatGPT Work availability and triggering differ by account and intelligence level; eligible Ultra sessions can delegate suitable work proactively. Record the exact surface, account capability, model, reasoning level, permission mode, and version. Do not treat one trigger path as proof for another. Consult the current [OpenAI subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents) before describing behavior.

Each subagent performs its own model and tool work, so parallel work uses more tokens than a comparable single-agent run. Use the smallest useful fanout and keep write-heavy work isolated; verify the actual configuration instead of assuming it.

Current Codex documentation describes custom agents that change supported model settings or instructions, or disable supported capabilities. They inherit the parent session's permissions, provider, and MCP servers; a custom-agent file cannot replace those settings. A read-only instruction does not create a read-only sandbox. Inspect the actual host version, effective parent permissions, custom-agent configuration, registered tools, active trust boundary, and managed requirements before assigning work. A role label is not permission to broaden the parent's authority; published behavior is not proof that an installed version enforces it.

When enabled, Codex can generate memories from eligible prior chats in the
background. Memory extraction/consolidation and reading existing memory are
different operations. Record generation/reuse controls, model overrides, relevant
chat eligibility and collection coverage where observable. A configured flag does
not prove that generation ran or establish its cost. Consult the [official memory
documentation](https://learn.chatgpt.com/docs/customization/memories).

Codex documents analytics/health traffic separately from optional OpenTelemetry
export. Disabling export is not proof of zero networking or zero inference.
A user configuration file is only one layer; inspect effective session and managed
configuration when authorized, without changing settings to satisfy a measurement.

Content binding: [official subagent Markdown](https://learn.chatgpt.com/docs/agent-configuration/subagents.md). Read exact installed-version and managed-policy evidence before selecting a supported role or capability. This documentation does not authorize delegation or override inherited permissions.

## Claude

Claude Code can expose subagents, and some versions can expose experimental agent teams with different coordination behavior. Consult the current [Claude subagent documentation](https://code.claude.com/docs/en/sub-agents) and [Claude agent team documentation](https://code.claude.com/docs/en/agent-teams). Record unsupported behavior as unsupported rather than inferring parity.
