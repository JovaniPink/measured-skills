# Native CLI package smoke checks for 0.17.1

Observed on 2026-09-30 in disposable client configurations. The current canonical package artifacts are bound by the [release manifest](../releases/0.17.1/manifest.json) to source commit `044c8fa`. No active global installation was replaced.

| Client | Version | Installed packs | Installed skill entrypoints | File comparison |
| --- | --- | --- | --- | --- |
| Codex CLI | 0.154.0 | 9 | 79 | Every installed skill file matches its generated adapter |
| Claude Code CLI | 2.1.281 | 9 | 79 | Every installed skill file matches its generated adapter |
| Antigravity CLI | 1.2.9 | 9 | 65 | Every installed skill file matches its generated adapter; all explicit-only skills absent |

All three native CLIs installed and listed the nine packs. Codex's disposable plugin configuration was disabled and read back through its native list command; Claude and Antigravity used native disable commands. Native removal left each fresh-process installed/imported list empty. All packs were reinstalled. Cache-file retention and client registration are separate observations; a remaining cache is not evidence of activation.

Codex and Claude selected historical 0.17.0 artifacts, verified all nine listed versions and skill-file trees, then returned to 0.17.1. These version-selection checks used local marketplace re-registration and native installation. Antigravity downgrade to 0.17.0 is held because that historical artifact contains explicit-only workflows that current policy excludes. It was not installed.

A second check preserved a fixed local marketplace path, changed that owned snapshot from 0.17.0 to 0.17.1, and ran native updates for all nine packs. Codex used `plugin add` to select the new local version; Claude used marketplace refresh and `plugin update`. Every listed version and installed skill-file tree matched 0.17.1. No running model session was restarted or observed refreshing.

These checks do not establish fresh model discovery, routing, focused loading, interruption recovery, in-session refresh, semantic obligations, task success, or benefit over baseline. Desktop, Work, account-upload, Chat, Cowork, and IDE surfaces remain separate unfinished qualification cells. Native package acceptance does not close those gaps.

A separate read-only Codex calibration loaded a project-scoped claim-verification skill and a focused reference. It used 29,905 input tokens and 262 output tokens in approximately 19 seconds. Its response retained the difference between local checks, unrun hosted CI, and unobserved deployment. The client did not report the selected model in the captured trace; no paired benefit claim, exact cost claim, preregistered result, or full catalog qualification follows from this observation.

Raw command output, client configuration paths, and calibration traces remain private. Use the [qualification protocol](qualification-campaign.md) and independently reviewed frozen cases before wider model runs.
