# Codex setup

Use the generated Codex plugin for terminal or desktop code work. Check ChatGPT Work and web separately. They may have different loading and file access.

Check the [current candidate record](../client-candidate-v0.18.0.md) before enabling an update. The former engineering pack was held from 0.12.0, when an original motion safety case failed. That hold was lifted on 2026-09-10 after all ten original cases met their expectation on CLI 0.153.2 at 0.14.0. The [0.16.0 record](../client-candidate-v0.16.0.md) keeps that history. It does not carry over to the three packs that replaced the former pack. Codex CLI 0.154.0 copies each added plugin into `plugins/cache/<marketplace>/<plugin>/<version>/` under its home folder, and `codex plugin remove` deletes that copy. A changed checkout is therefore not the installed version until the plugin is added again. Compare the cached files, not the checkout.

## Check what is there

```sh
codex --version
codex plugin list --json
```

Save both the list and any warnings. If the remote list fails, the local list may still be useful, but it is incomplete.

Look for old copies in personal or project skill folders as well as the plugin cache. Compare the installed files with `plugins/codex/` from the reviewed checkout. Do not assume that a matching version means matching files.

## Install one reviewed pack

Replace the example path with your local checkout. These commands change your install:

```sh
codex plugin marketplace add /absolute/path/to/skills
codex plugin add measured-skills@measured-skills
codex plugin list --json
```

Open a fresh task after the install. Select a skill by its full plugin name:

```text
$measured-skills:claim-verification Check which completion claims have evidence. Make no changes.
```

For skills that require direct selection, the generated `agents/openai.yaml` sets `allow_implicit_invocation: false`. Test that behavior before relying on it.

## Check the apps

In Codex desktop, inspect the plugin page and open a fresh test task. Verify the selected skill, a linked reference, a result file, and interruption recovery. If an active task still uses older files, record that task separately.

In ChatGPT Work or web, inspect that surface's own library. Do not treat the CLI list as its install record.

For a web account update, download the old skill first. In **Plugins > Skills**, choose **Create > Upload from your computer** and upload a reviewed ZIP that includes the skill folder and its linked files. If ChatGPT finds the same name, check the named skill before choosing **Replace existing**. Reload the page and inspect both the instructions and each linked file. A success notice alone is not enough.

The observed web editor flattened individually uploaded files. Use the complete archive to keep reference folders intact. The first detail view after replacement also showed stale files and a load error; a page reload showed the saved replacement. These observations cover one skill, not a bulk account update.

Review personal preferences in Codex user instructions separately from the package. Keep repository rules in `AGENTS.md`.

Follow the [shared client checks](../client-support.md) for updates, removal, and evidence. Check native `--help` before an update or uninstall; command forms can change.

If a check fails, stop that pack's update batch. Turn it off in plugin settings, or restore the saved reviewed package through the native install route. Check the resulting state in a fresh test task. Keep the other packs and active user tasks intact.

Sources: [OpenAI skill guide](https://learn.chatgpt.com/docs/build-skills), [OpenAI plugin guide](https://developers.openai.com/plugins/build/plugins).
