# 0.19.0 release decision

Status: accepted by the maintainer on November 5, 2026. This acceptance covers the
claims, tag gates, freeze, drift rule, and rollback target in this record. It does not
authorize a tag, a Release, an install, a paid run, or any publication. Each stays a
separate decision.

Earlier records say that a smaller result or narrower claim needs its own reviewed
decision, not a passing label. This is that decision for 0.19.0.

## What a stable 0.19.0 would claim

- Copied requests work with nothing installed.
- The four packs install, upgrade, downgrade, uninstall, and reinstall on Claude Code
  CLI, Codex CLI, and Antigravity CLI. This claim covers packaging only, and only
  where [the lifecycle record](lifecycle-0.19.0.md) shows `pass`.
- Skills behave as described on Claude Code CLI, on one model at one setting, for the
  bounded task that was run. It is not a general quality or benefit claim.

Skills stay an optional addition to copied requests. This matches the launch framing
the maintainer chose on November 5.

## What it would not claim

| Surface | Why it stays unclaimed | What would change that |
| --- | --- | --- |
| Codex behavior | No per-request zero-credit control is known | A supported control, then an authorized task |
| Antigravity behavior | Isolation is unproven. An empty workspace showed 111 skills | A native readback that shows isolation, then an authorized task |
| Gemini in Antigravity IDE | Packet unrun, and the host and model are unverified | Rebind the packet, then a separate authorization |
| Desktop and web apps | No 0.19 observations | Checks on each app |
| Second Mac | No 0.19 observations | Checks on that machine |

No unclaimed surface gets a compatibility row for 0.19.0. Its absence means "not
claimed", not "fails". Dated observations stay in
[the client record](../client-candidate-v0.19.0.md).

## Which gates block the tag

| Gate | Effect |
| --- | --- |
| Repository checks on the tagged commit | Blocks the tag |
| Reviewed sources and final online check | Blocks the tag |
| Freeze | Blocks the tag |
| Install lifecycle on all three CLIs | Blocks the tag for each CLI claimed |
| Ten-card exercise | Blocks the tag. It must be scored against its targets, with a miss reported as a miss |
| Exploration account check | Blocks the tag |
| Claude Code acceptance task | Blocks the behavior claim. If it fails or does not run, that claim is removed |
| Public chooser and Studio PR 143 | Gates the website, not the tag |
| Dotfiles PR 39 | Not a tag gate. No release rule depends on it |
| Python 3.15 (PR 73) | Not a tag gate. It cannot pass today, because PyYAML has no Python 3.15 wheels |

Any result that misses a target is reported as it happened. Changing a target needs
a new decision, not a passing label.

## Freeze

The frozen candidate is the commit named as `source_commit` in
[the manifest](../../releases/0.19.0/manifest.json) after the review of November 5
sources and any resulting edits have merged.

After the freeze, ordinary docs and evidence records may land. Among files the
manifest covers, only `catalog/upstream-pins.json` and
`catalog/upstream-reviews.json` may change, and only through a reviewed repin. Plugin
trees, ZIPs, and the discovery export must keep their exact bytes. To check, compare
the manifest's artifact hashes at the freeze with those at the tag.

If any other covered byte changes, the freeze ends. Rerun the lifecycle and
acceptance steps for each changed plugin.

## Source drift

Sources move often: 30 of 69 changed in three days. A pass on the exact tagged commit
is still required, because the online check has to end clean on that commit. Review
each later drift on its own, repin by the same method, and keep the failed receipt.
Drift of this kind does not reset client acceptance, because no plugin byte changes.

Keep the reviewed page bodies privately, outside this repository, so the next review
can compare against them.

## Rollback target

Roll back to `v0.16.0`, the only public tag. It is reproducible, but it has no
accepted client behavior, so it is a known package and not a qualified one. It uses
`jovanipink-*` names, so rollback crosses the rename in
[the migration guide](../measured-migration.md).

The preserved 0.18 source was never tagged, so it is not a public rollback target.

## Text to change when tagging

These files describe the preview and are not in the manifest, so they can change after
acceptance without touching plugin bytes:

- `README.md`, `SECURITY.md`, and `docs/start.md`
- `CHANGELOG.md`, which also has to move the 0.19.0 section out of `[Unreleased]`
- `docs/client-candidate-v0.19.0.md` and `docs/release-status.md`

## Open at tag time

- Release notes and assets, including the 17 held explicit-only archives.
- Install guidance that pins the tag. `docs/quickstart.md` no longer has it, and
  marketplace entries use relative paths, so a tag alone pins nothing.
- Directory submission and account ZIP uploads, which stay separate.
