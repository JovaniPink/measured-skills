# Migrate to Measured Skills

Measured Skills is maintained by Measured Studios. The homepage is https://measuredstudios.com/skills. The GitHub source is https://github.com/JovaniPink/measured-skills. The September 26, 2026 source-location migration supersedes the earlier decision to retain `JovaniPink/skills`. Ownership remains JovaniPink; no organization transfer or installed-plugin upgrade is part of this rename.

## Identity mapping

| Previous identity | New identity |
| --- | --- |
| jovanipink-skills marketplace and core pack | measured-skills marketplace and core pack |
| jovanipink-engineering | measured-engineering-build, measured-engineering-review, measured-engineering-delivery |
| jovanipink-stack-profiles | measured-stack-profiles |
| jovanipink-operations | measured-operations |
| jovanipink-reasoning | measured-reasoning |
| jovanipink-ai-systems | measured-ai-systems |
| jovanipink-agent-platforms | measured-agent-platforms |

This is a breaking pre-1.0 identity change. Skill names remain stable; plugin-qualified invocations change. There are no installed compatibility aliases. Historical attribution, source URLs, observations, and retained 0.16.0 artifacts are not rewritten as current evidence. The existing `v0.16.0` tag resolves to `89728f930540e5cfc9de01bb1526de324fe647c8`; that immutable source and its archives remain the rollback reference, not the new working distribution.

## Upgrade and rollback

1. Record exact installed versions, enabled packs, client versions, and current configuration. Preserve a recoverable local configuration backup without publishing it.
2. Prepare the current version (the 0.18.0 candidate) in an isolated client configuration or pilot workspace. Disable old catalog plugins there before enabling new ones; never discover both identities for the same skill.
3. Install only the chosen pack through the tested client's native plugin flow. Check its inventory and generated file hashes in a fresh session. Recheck explicit-only behavior before enabling delivery workflows.
4. Promote only after the pilot criteria pass. Until then the normal configuration remains unchanged.
5. To roll back, disable new identities, restore the previous configuration and the immutable 0.16.0 distribution, then verify one copy of each intended skill in a fresh session. Do not rebuild an old release from new source or relabel new bytes 0.16.0.

## Moving from 0.17.x to 0.18.0

The 0.18.0 candidate keeps every pack name and skill name from 0.17.x, so there is no identity mapping to apply. It adds two packs, `measured-swift-workflows` and `measured-nextjs-workflows`, and seven skills. That brings the catalog to 86 skills in 11 packs. Install a new pack only if your work needs it, and check its skills in a fresh task first. Three of the new skills are explicit-only: `ios-journey-verification`, `nextjs-feature-delivery`, and `swiftui-feature-delivery`. The Antigravity packs hold the implicit skills only. See the [0.18.0 candidate record](client-candidate-v0.18.0.md) for what was and was not checked.

## Focused build selection

Enable `measured-engineering-build` and stage only `cross-stack-quality-gates` plus the primary language profile. They are available tools, not seven mandatory ceremonies.

```sh
python3 scripts/export_selected.py --client codex --output dist/build-extras-codex --skill cross-stack-quality-gates --skill typescript-javascript-engineering-profile
python3 scripts/export_selected.py --client claude --output dist/build-extras-claude --skill cross-stack-quality-gates --skill typescript-javascript-engineering-profile
```

Use a new staging directory for each export. Review its manifest before a separate, authorized installation. The tool refuses explicit-only skills; supported plugin controls remain their route. It changes no client configuration.

## Discovery size is an estimate

The catalog reports description counts and native-layout estimates including skill names and relative paths. These are not captured client prompts. Codex's documented budget is model-dependent, with an 8,000-character fallback when context size is unavailable. Absolute installed paths, other plugins, client formatting, and model context affect the actual list. Do not infer omissions or behavior from counts alone.

## Source-location migration

Update current clone and marketplace source URLs to `JovaniPink/measured-skills`. Existing releases, plugin names, installed versions, and the immutable 0.16.0 rollback reference retain their identities. Local installations must update their checkout source paths after backing up client configuration; verify one copy of each previously enabled plugin in a fresh session. Do not reinstall the 0.17.0 candidate merely to change its source location. GitHub redirects the old source repository URL; do not recreate a repository at `JovaniPink/skills`. Historical evidence retains its observed URLs and dates.
