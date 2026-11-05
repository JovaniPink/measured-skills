# 0.18 to 0.19 upgrade results

Status: observed on November 5, 2026. The rehearsal and one real upgrade passed on
Claude Code, Codex, and Antigravity CLIs. This covers packaging only. No model prompt
ran, so it does not show that a skill loads or works in a fresh task. It adds no claim
to the [release decision](release-decision-0.19.0.md).

The [lifecycle record](lifecycle-0.19.0.md) tested `v0.16.0`. This record covers the
other starting point: the untagged 0.18 candidate, which the maintainer's Mac was running.

Source: earlier frozen candidate `63156e05a9c7c5f25ed50920cc49b8c49bd00cfe`. The
[safety fixes](release-decision-0.19.0.md#amendment-on-november-5-2026-safety-fixes) later replaced
it. The installs were refreshed to the new candidate the same day, and the old copies were removed. See
[the cleanup record](clean-install-2026-11-05.md).
Starting point: `c2d10443fe683228994dad72b0461ae7fd6ebdfa`, 11 packs.

| Check | Value |
| --- | --- |
| Claude Code version | 2.1.316 |
| Codex version | 0.161.0 |
| Antigravity version | 1.4.7 |
| Machine | One Mac, macOS kernel Darwin 27.0.0 |

## Rehearsal

Each CLI ran in a throwaway configuration, with one unrelated plugin that had to survive.
All 416 commands exited 0. Installed file hashes matched the source at every step.

| Step | Claude Code | Codex | Antigravity |
| --- | --- | --- | --- |
| Start on 11 packs at 0.18 | `pass` | `pass` | `pass` |
| Upgrade to 4 packs | `pass` | `pass` | `pass` |
| Roll back to 0.18 | `pass` | `pass` | `pass` |
| Stop at 2 of 4 packs, then roll back | `pass` | `pass` | `pass` |
| Upgrade again | `pass` | `pass` | `pass` |

A before-and-after hash of 2,758 real plugin and configuration files showed no change.

## Real upgrade

The same order then ran on the maintainer's real configurations, Codex first, in 59
commands that all exited 0.

| CLI | Packs | Files matching the source | Other plugins |
| --- | --- | --- | --- |
| Claude Code | 4 at 0.19.0, enabled | 280 | None installed |
| Codex | 4 at 0.19.0, enabled | 366 | 29 unchanged |
| Antigravity | 4, enabled | 223 | 5 unchanged |

## What was learned

- 0.18 and 0.19 cannot sit side by side. They share the `measured-skills` marketplace name
  and the `measured-operations` pack name. Uninstall the 11 packs, remove the marketplace,
  add it from the new source, then install the 4 packs.
- The CLI has no Measured Skills during that swap, and sessions already running keep the old
  skills until restarted.
- Claude Code kept old files in `plugins/cache/`, but `readFromFolder` pointed at the new
  source. No old entries remained in its `settings.json` or in Codex's `config.toml`.
- An upgrade that stopped halfway rolled back cleanly.

## App read-back

After the real upgrade, each app's own skill list was read on the same Mac. This was before the
safety-fix refresh, so it shows the earlier candidate. No task ran, so this shows what each app
lists, not that a skill loads.

| App | Version | Observed |
| --- | --- | --- |
| Antigravity IDE | 2.6.0 | 143 skills in one project, with all 73 expected names listed |
| Antigravity desktop | 2.25.0 | 9 plugins, including the 4 packs and no 0.18 packs. `measured-workflows` showed 19 commands, matching the pack |
| Claude desktop, Code tab | 4.16336.0 | One session's skill list showed the 4 packs with their new names |

The IDE reported 21,101 of its 20,000 token budget for customizations. It excluded 6 entries, all
Google skills, and none from these packs. The packs use roughly a third of that budget, so a client
with more customizations could exclude some of them. How the IDE chooses what to exclude was not
tested.

Claude desktop Chat and Cowork were not read, because Computer Use cannot control Claude's own app.

## Not covered

- Skill loading or behavior in a fresh task.
- Claude desktop Chat and Cowork, the ChatGPT app, web accounts, and a second Mac.
- Account uploads. All 69 account skills from 0.18 were renamed, so they cannot be replaced
  in place.
