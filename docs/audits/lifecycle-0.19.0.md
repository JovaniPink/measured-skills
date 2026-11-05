# 0.19.0 install lifecycle results

Status: not run. This record holds the results of release process step 5. It does
not claim that any install has happened.

Fill it in only from observed results on the frozen candidate. Each CLI runs against
a throwaway configuration, so no personal install changes: `CLAUDE_CONFIG_DIR` for
Claude Code, `CODEX_HOME` for Codex, and a throwaway `HOME` for Antigravity. These
steps send no model prompt. See the
[0.17.0 lifecycle record](../manual-smoke-tests.md#0170-isolated-install-lifecycle-2026-09-23)
for the method.

Allowed results are `pass`, `fail`, `blocked`, `not_supported`, and `not_run`.
A `blocked` row is not a claim.

Frozen candidate: not yet set.

| Check | Value |
| --- | --- |
| Claude Code version | not recorded |
| Codex version | not recorded |
| Antigravity version | not recorded |
| Machine | not recorded |

| CLI | Pack | Install | Upgrade from `v0.16.0` | Downgrade to `v0.16.0` | Uninstall | Reinstall |
| --- | --- | --- | --- | --- | --- | --- |
| Claude Code | measured-workflows | not_run | not_run | not_run | not_run | not_run |
| Claude Code | measured-quality | not_run | not_run | not_run | not_run | not_run |
| Claude Code | measured-stacks | not_run | not_run | not_run | not_run | not_run |
| Claude Code | measured-operations | not_run | not_run | not_run | not_run | not_run |
| Codex | measured-workflows | not_run | not_run | not_run | not_run | not_run |
| Codex | measured-quality | not_run | not_run | not_run | not_run | not_run |
| Codex | measured-stacks | not_run | not_run | not_run | not_run | not_run |
| Codex | measured-operations | not_run | not_run | not_run | not_run | not_run |
| Antigravity | measured-workflows | not_run | not_run | not_run | not_run | not_run |
| Antigravity | measured-quality | not_run | not_run | not_run | not_run | not_run |
| Antigravity | measured-stacks | not_run | not_run | not_run | not_run | not_run |
| Antigravity | measured-operations | not_run | not_run | not_run | not_run | not_run |

After each step, read back the enabled inventory and compare file hashes with the
manifest. Record anything left behind. Known traps:

- Claude Code uninstall can leave files in `plugins/cache/`, and a directory
  marketplace can load from its folder. See [Claude notes](../clients/claude.md).
- Antigravity install does not enable a plugin. See
  [Antigravity notes](../clients/antigravity.md). Its packs exclude explicit-only skills.
- `v0.16.0` uses different names: marketplace `jovanipink-skills` and `jovanipink-*`
  plugins. Upgrade and downgrade cross that rename, so disable the old identities
  before enabling new ones.
- Check whether Codex 0.161.0 has a disable command. Codex 0.154.0 did not.
