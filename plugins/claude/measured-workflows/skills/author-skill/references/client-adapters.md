# Client adapters

Consult current official client documentation before changing these mappings.

## Canonical boundary

The canonical `SKILL.md` follows the open Agent Skills format and keeps client-native invocation controls out of its frontmatter. Portable metadata stays string-valued.

## Codex projection

- Keep `agents/openai.yaml` with interface metadata.
- Explicit-only skills set `policy.allow_implicit_invocation: false`.
- Generated default prompts use the plugin namespace when distributed through a plugin.

## Claude projection

- Omit the Codex `agents/` directory.
- Explicit-only skills add `disable-model-invocation: true` only in generated Claude frontmatter.
- A Claude.ai ZIP contains one top-level skill directory with its `SKILL.md` and focused references.

## Antigravity projection

- Generate a separate package from canonical source; omit Codex's `agents/`.
- Include only skills whose invocation policy is implicit. Exclude explicit-only
  skills until the exact client surface has a verified automatic-selection control.
- Preserve linked resources and record included files and excluded skills.
- Workspace discovery uses `.agents/skills/`; global and plugin paths vary by
  surface. Prefer the documented native install route and verify its actual path.
- Keep installation, enabled state, discovery, invocation, and outcome evidence
  separate. A slash command does not prove explicit-only enforcement.

Current format authorities, read 2026-10-13: [Agent Skills](https://agentskills.io/specification),
[Codex](https://learn.chatgpt.com/docs/build-skills),
[Claude Code](https://code.claude.com/docs/en/skills), and
[Antigravity](https://www.antigravity.google/docs/skills?tab=ide).

Compatible file layout is not behavioral parity. Record discovery, activation, reference loading, and lifecycle observations separately for every tested surface and exact client version.
