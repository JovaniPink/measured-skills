# 0.19.0 install lifecycle results

Status: observed on November 5, 2026. All three CLIs passed every step for all four
packs. This covers packaging only. No model prompt ran, so it does not show that a
skill loads or works in a fresh task.

Each CLI ran against a throwaway configuration, so no personal install changed:
`CLAUDE_CONFIG_DIR` for Claude Code, `CODEX_HOME` for Codex, and a throwaway `HOME` for
Antigravity. A before-and-after hash of 4,038 real client configuration files showed no
change. See the
[0.17.0 lifecycle record](../manual-smoke-tests.md#0170-isolated-install-lifecycle-2026-09-23)
for the method.

Allowed results are `pass`, `fail`, `blocked`, `not_supported`, and `not_run`.
A `blocked` row is not a claim.

Frozen candidate: `63156e05a9c7c5f25ed50920cc49b8c49bd00cfe`.
Rollback target: `v0.16.0`.

| Check | Value |
| --- | --- |
| Claude Code version | 2.1.316 |
| Codex version | 0.161.0 |
| Antigravity version | 1.4.7 |
| Machine | One Mac, macOS kernel Darwin 27.0.0 |
| Lifecycle commands | 225, all exited 0 |

| CLI | Pack | Files | Install | Upgrade from `v0.16.0` | Downgrade to `v0.16.0` | Uninstall | Reinstall |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Claude Code | measured-workflows | 98 | pass | pass | pass | pass | pass |
| Claude Code | measured-quality | 70 | pass | pass | pass | pass | pass |
| Claude Code | measured-stacks | 85 | pass | pass | pass | pass | pass |
| Claude Code | measured-operations | 27 | pass | pass | pass | pass | pass |
| Codex | measured-workflows | 129 | pass | pass | pass | pass | pass |
| Codex | measured-quality | 96 | pass | pass | pass | pass | pass |
| Codex | measured-stacks | 104 | pass | pass | pass | pass | pass |
| Codex | measured-operations | 37 | pass | pass | pass | pass | pass |
| Antigravity | measured-workflows | 58 | pass | pass | pass | pass | pass |
| Antigravity | measured-quality | 66 | pass | pass | pass | pass | pass |
| Antigravity | measured-stacks | 73 | pass | pass | pass | pass | pass |
| Antigravity | measured-operations | 26 | pass | pass | pass | pass | pass |

## How each step ran

1. Install all four packs from the frozen source, then read them back.
2. Uninstall them and confirm that none are listed.
3. Install `v0.16.0`: seven packs on Claude Code (135 files) and Codex (214 files),
   or the offline preview on Antigravity (103 files).
4. Upgrade: disable the old packs, install the new ones, then remove the old ones.
5. Downgrade: reverse step 4.
6. Uninstall `v0.16.0`, reinstall the four packs, then remove everything.

After every step, the enabled inventory was read back, and each pack's installed files
were compared by SHA-256 with the source it came from. Before the run, each source pack
matched its hash in the manifest. On Claude Code, the folder a session reads from was
compared as well. Antigravity's `plugin.json` has no version field, so file hashes are
its identity check.

The first Antigravity run reported failures on the 0.19 steps. The cause was the test
script, which compared that missing field with `0.19.0`. All files matched. The script
was corrected and the whole lifecycle reran from a clean folder. The table shows the
second run. Raw receipts are retained privately, outside this repository.

## What this does not cover

- No fresh task ran, so loading, reference reads, explicit-only behavior, and removal as
  seen by a session are unchecked. Those need a signed-in configuration.
- Desktop apps, web apps, and the second Mac were not checked.
- The sources were local folders, not a marketplace reached over the network.

## What the clients did

- **Claude Code:** uninstall and marketplace removal left 426 files in `plugins/cache/`.
  The inventory stopped listing those packs. A directory marketplace reports its own
  folder as `readFromFolder`, so check that folder as well as the cache.
- **Codex:** version 0.161.0 still has no disable command, so disabling set
  `enabled = false` in that configuration's `config.toml`. Removal left no cache files.
- **Antigravity:** `plugin list --json` showed each pack as enabled right after install,
  before any `plugin enable` ran. Earlier versions did not enable on install. Removal
  left no plugin files.
- **Upgrade and downgrade** cross the rename from `jovanipink-*` to `measured-*`. Disable
  the old identities before enabling new ones.
