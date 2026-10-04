# Architecture

## Source and adapters

`skills/` is the canonical, client-neutral source. A canonical skill has:

- standards-compatible YAML frontmatter in `SKILL.md`
- focused workflow instructions
- optional references loaded only when needed
- `agents/openai.yaml` for Codex presentation and invocation policy
- a matching provenance record and trigger matrix
- a matching strict taxonomy record with maturity evidence

`scripts/build_distributions.py` creates three tracked adapters:

```text
skills/ --> plugins/codex/<metadata.plugin>/skills/
        --> plugins/claude/<metadata.plugin>/skills/
        --> plugins/antigravity/<metadata.plugin>/skills/
```

The Codex copy retains `agents/openai.yaml` and rewrites its direct-invocation prompt to the installed plugin namespace. The Claude copy omits that client-specific directory and adds `disable-model-invocation: true` to explicit-only skill frontmatter. The Antigravity copy omits the directory too, and leaves explicit-only skills out until a selection control is verified. No client adapter changes the workflow body.

Plugins are packaging routes, not the complete taxonomy. `catalog/skills.json` adds capability, lifecycle, target, risk, invocation, maturity, companion, and routing-conflict facets. `catalog/packs.json` measures plugin and recipe discovery-description sizes.

## Antigravity distribution and preview

In addition to tracked distributions under `plugins/antigravity/` and `.gemini/plugins/marketplace.json`, `scripts/build_antigravity.py` prepares a self-contained review folder from the same source. It keeps skill text and references, omits Codex metadata, and rejects explicit-only skills before it writes anything. A separate `bundle.json` records file hashes and the unverified loading state. It adds no runner and changes no installed client. See [Antigravity setup](clients/antigravity.md).

## Invocation classes

Implicit skills are read-only or diagnostic by default. They may activate when their descriptions clearly match the user's task. Explicit-only skills coordinate side effects or trust decisions and require the user to name the skill. Native adapters encode the distinction, while the workflow text still states its authorization boundary.

Invocation metadata is portable repository metadata, not a replacement for host enforcement:

- canonical: `metadata.invocation`
- Codex: `policy.allow_implicit_invocation`
- Claude: `disable-model-invocation`
- Antigravity: `disable-model-invocation`

Direct invocation is also client-native and namespaced after plugin installation:

- Codex plugin: `$measured-skills:skill-name`
- Claude plugin: `/measured-skills:skill-name`
- Antigravity plugin: `/measured-skills:skill-name`

Canonical unnamespaced forms remain useful when a client installs an individual skill rather than the plugin.

## Enforcement boundary

Skills provide judgment, sequencing, and reporting structure. Deterministic requirements belong in repository scripts, tests, CI, or client permissions. Prose cannot guarantee that an agent will obey a permission boundary, detect every secret, or run a gate correctly.

## Lifecycle

1. Author in `skills/`.
2. Review provenance, security, and invocation class.
3. Add trigger cases.
4. Generate client distributions and Claude.ai archives.
5. Run deterministic validation.
6. Record each client surface's observed behavior.
7. Release only when automated and required manual evidence is complete.

API-managed skills and runtime-agent skills have separate compatibility and security records. OpenAI Skills API, Anthropic Skills API, Anthropic Managed Agents, Antigravity CLI, conditional enterprise Gemini CLI, Gemini Managed Agents, and Google ADK runtime behavior are not inferred from local Codex or Claude plugin output. ADK runtime skills belong to the separate runtime-adapter repository and private product overlays.

Unready work remains in `incubator/`. Retired skills move to `deprecated/` with a migration notice and are removed from generated catalogs.
