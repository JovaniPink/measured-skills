# Antigravity setup

Antigravity setup and testing have equal priority with Codex and Claude. Candidate 0.18.0 generates 11 modular packs under `plugins/antigravity/`. Its installed-client behavior remains unqualified; see the [candidate record](../client-candidate-v0.18.0.md). The generated `.gemini/plugins/marketplace.json` remains an unverified preview format. The native local-folder installation route was checked for the nine 0.17.1 packs on CLI 1.2.9; Google's current marketplace UI and inline commands do not establish support for this generated file. An offline preview builder is also provided via `scripts/build_antigravity.py`.

A one-skill package passed native install and skill-menu checks in CLI 1.1.26; package and menu checks were repeated on 1.1.27. The [0.12.0 candidate record](../client-candidate-v0.12.0.md) adds a two-skill check on CLI 1.1.27. The motion reference and fixture loaded, but the answer invented evidence. The [0.14.0 record](../client-candidate-v0.14.0.md) adds a four-skill check on CLI 1.1.28. Nine of ten cases met their expectation and no reply invented evidence. That is one partial run on a different version, so the expansion, then 64 skills, remained held. The [0.15.0 candidate record](../client-candidate-v0.15.0.md) adds a five-skill check on CLI 1.2.0 (`accessibility-review`, `code-change-review`, `functional-motion-review`, `performance-scalability-diagnosis`, and `finding-consolidation`). Near-miss case 3 was re-examined under diagnostic bypass flags (`--dangerously-skip-permissions`), confirming routing to `performance-scalability-diagnosis` when commands are permitted, while standard headless permission denial remains a documented non-interactive boundary. The 0.15.0 SARIF finding vocabulary was observed live on `code-change-review`, and `finding-consolidation` passed both multi-review merging and single-review refusal.

The normal packs and preview builder include 69 implicit skills. All 17 explicit-only workflows are excluded until native automatic-selection controls are verified for the exact surface and version. Google's documented fields do not establish that control. No installable preview override is provided. Selecting an excluded workflow fails before writing output. Codex and Claude adapters remain separate.

## Check what is there

```sh
agy --version
agy plugin list
```

The command is `agy`. An empty imported-plugin list does not mean the client has no skills. Built-in, global, and project skills may also load.

In the desktop app, open **Settings > Customizations** and inspect the skill list. Check the IDE separately. Keep installed, enabled, listed, and used as separate facts.

## Install modular packs

Google's [combined plugin guide](https://www.antigravity.google/docs/plugins?tab=cli) documents `agy plugin install` for a local plugin folder, plus `list`, `enable`, `disable`, and `uninstall`. It also describes an interactive marketplace and inline `/plugin` commands. Clone and review the repository, then install one pack from its folder:

```sh
agy plugin install /absolute/path/to/skills/plugins/antigravity/measured-skills
agy plugin enable measured-skills
agy plugin list
```

Repeat with another folder under `plugins/antigravity/` for each pack you want. Each generated `plugin.json` holds only `name` and `description`, the fields in Google's documented schema.

The expected slash commands use the installed plugin namespace. This form has not been observed on agy for these packs:

```text
/measured-skills:claim-verification Check which completion claims have evidence.
/measured-skills:systematic-diagnosis Investigate this failure.
```

## Prepare a preview

To prepare a self-contained preview directory for inspection or offline testing:

```sh
python3 scripts/build_antigravity.py --skill claim-verification --output dist/antigravity-check
```

The result contains `plugin/` and `bundle.json`. The latter lists selected skills, exclusions, and file hashes. Omit `--skill` to prepare the 69 eligible implicit skills. The builder does not install anything and refuses to overwrite an existing folder.

The preview keeps `skills/<name>/SKILL.md` and linked notes. It omits Codex's `agents/` folder and excludes explicit-only skills. The directory layout loaded correctly on CLI 1.1.28; recheck it on a version you have not tested. Do not flatten files by hand or lose their links.

## Install after review

Once the selected preview and test setup are ready, the native local install command is:

```sh
agy plugin install /absolute/path/to/antigravity-check/plugin
agy plugin list
```

In CLI 1.1.26, the native installer placed the tested preview under `~/.gemini/config/plugins/`, and the menu listed `/measured-antigravity-preview:claim-verification`. Native validation, file hashes, disable/enable, removal, and reinstall checks passed. These results cover one skill and this CLI version.

Record the names and path your client actually shows. Follow the [shared client checks](../client-support.md) in a fresh task. Verify live use and linked notes before widening the install. Keep personal and product skills separate from this public preview.

If a check fails, run `agy plugin disable measured-antigravity-preview` for this named preview. In 1.1.27, `agy plugin list` showed imports but did not show enabled state. Readback of the native plugin configuration showed this preview's `enabled` value as `false`. In CLI 1.2.8 that state is in `~/.gemini/config/config.json`, under `plugins.<name>.enabled`. Record that separate state check. To restore a saved preview, use the native install command with its backup folder. Verify its files and state before using it again. Do not add another copy to force discovery.

## Enable the preview after installing it

`agy plugin install` reports success and lists the skills it processed. It does not enable the plugin. A preview that was disabled earlier stays disabled through a reinstall. In CLI 1.2.8, `agy plugin uninstall` removed the enabled-state entry as well as the folder, so a later install again started disabled. Run the enable step and check it:

```sh
agy plugin install /absolute/path/to/antigravity-check/plugin
agy plugin enable measured-antigravity-preview
```

This matters because an unskilled reply looks reasonable. In a 1.1.28 check, ten cases ran against a disabled preview and returned fluent reviews with none of the skill's own output: no named sections, no evidence-kind labels, and no WCAG levels. The same ten cases returned all of that once the plugin was enabled. Before scoring any run, confirm source loading independently, then grade semantic obligations. Named sections are a secondary diagnostic. A plausible answer is not proof the skill loaded.

Enabling also changed permission behavior. Three cases returned an empty reply while the preview was disabled, because the client kept trying to run a command to find files that were not there. With the skill enabled, those same cases answered from the skill's procedure and needed no command.

Check the version with `agy --version`, not with the package manager. The Homebrew cask recorded 1.1.26 while the binary had updated itself through 1.1.28 to 1.2.0 via its auto-update mechanism. Record the version the binary reports.

For a print-mode check, verify where the client looks for files. One observed run used its scratch folder instead of the shell's working directory. A retry with the exact file path was denied because the noninteractive session could not ask for read permission. It exited with code 0 and reported `SUCCESS`, but returned an empty response and a denied action. Treat that as blocked. Do not bypass permissions to make the check pass. Diagnostic evaluation of tool routing under `--dangerously-skip-permissions` demonstrates that routing logic functions when permission prompts are bypassed, but that represents an altered test condition, not a production resolution.

A third check with synthetic facts in the prompt returned the correct verdict. This tested the response, not access to a project file. The running desktop app still returned no match for the preview skill. Keep those findings separate from the CLI menu and install results.

The general skill guide lists workspace `.agents/skills/` folders and global `~/.gemini/config/skills/` folders. The web CLI guide also names a CLI-specific global directory. The observed native install used the shared folder instead. Let the installer choose its path and verify the result. A running desktop app may still show its previous skill list.

Published guidance names several skill folders, and they are not read by the same surfaces. Treat this as a map to check against your own install rather than a settled contract. The plugin folder is the one this preview uses and the only row checked here:

| Folder | Reported readers |
| --- | --- |
| `<workspace>/.agents/skills/` | app, CLI, and IDE |
| `~/.gemini/config/skills/` | app, CLI, and IDE |
| `~/.gemini/antigravity/skills/` | app and IDE |
| `~/.gemini/antigravity-cli/skills/` | CLI and IDE |
| `~/.gemini/config/plugins/<plugin>/skills/` | skills installed as part of a plugin |

The September 30 combined plugin guide gives `~/.gemini/config/plugins/` for manual global installation and `~/.gemini/antigravity-cli/plugins/` in its CLI filesystem section. The disposable 1.2.9 native package check used the shared configuration path. Record your installer's actual path, enabled state, and file hashes; the two documented locations are not evidence that a second copy should be created.

Keep repository rules in the existing `AGENTS.md` files and `.agents/rules/*.md`. The installed CLI guide says it reads `AGENTS.md` and `GEMINI.md` from the working directory up to the repository root, as well as modular markdown rules under `.agents/rules/`. Verify that loading in a fresh task before relying on it. Avoid a second copy that could drift.

Use the app or IDE's own rules page for a reviewed personal preference. Confirm that it loaded. Do not infer CLI rule loading from an IDE result.

Sources: [Antigravity skills](https://antigravity.google/docs/skills/), [plugins by surface](https://www.antigravity.google/docs/plugins?tab=cli), [IDE rules](https://antigravity.google/docs/ide/rules/). The folder table also draws on a community survey of skill locations, [Where does Antigravity look for Agent Skills?](https://atamel.dev/posts/2026/07-01_where_agy_agent_skills/), read 2026-09-10. That is not a vendor source; only the plugin row was checked here.
