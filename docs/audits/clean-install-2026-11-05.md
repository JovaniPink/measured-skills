# Clean install and cleanup on November 5, 2026

Status: observed on one Mac. This covers local plugin copies and git leftovers. No model
prompt ran, so it does not show that a skill loads or works in a fresh task. It adds no
claim to the [release decision](release-decision-0.19.0.md).

## Install route for each surface

| Surface | Route | Source |
| --- | --- | --- |
| Claude Code CLI, desktop Code tab, VS Code | Plugins at user scope. These surfaces read the same user settings | [Claude Code plugin docs](https://code.claude.com/docs/en/plugins/install.md) |
| Claude Code, same-named account skills | Account skills download one way into `~/.claude/skills/synced/`. Set `syncClaudeAiSkills` to `false` to stop that | [Claude Code skills docs](https://code.claude.com/docs/en/skills) |
| Claude Chat and Cowork | Upload a ZIP under Customize > Skills. Cowork reads account skills, not `~/.claude` | [Claude help article](https://support.claude.com/en/articles/12512180-using-skills-in-claude) |
| Codex CLI and ChatGPT desktop Codex | Plugins. The IDE extension does not support plugins | [Codex plugins](https://learn.chatgpt.com/docs/plugins), [enterprise skills](https://learn.chatgpt.com/codex/enterprise/skills) |
| ChatGPT web Chat and Work | Not confirmed. The official pages give no upload or delete path | [Build skills](https://learn.chatgpt.com/docs/build-skills) |
| Antigravity CLI and App | `agy plugin install`. Plugins live in `~/.gemini/config/plugins` | [Antigravity plugins](https://antigravity.google/docs/plugins), [skills](https://antigravity.google/docs/skills) |

Not documented, so unknown: whether the ChatGPT app and the Codex CLI share a plugin cache, how
the Claude Chat tab gets skills, whether the Antigravity IDE and App share state, and a manual
cleanup procedure for the Claude Code plugin cache.

## What the check found

- The four packs matched their manifest hashes on all three CLIs: 12 of 12 trees.
- The Claude desktop app kept cached account skills for two accounts. In each, 69 of 86 skills
  were old 0.18 names. Claude Code showed these as `anthropic-skills:*` next to the new packs,
  so one task could list two names for the same job. Local deletion cannot remove them. The
  account owner removes them in claude.ai.
- Claude Code's own synced folder held only 1 old name. The two counts disagree and the
  account list was not read.
- A stray user-level copy of a read-only scope review skill was still installed. It matches no 0.19 skill name.
- Eleven old 0.18 pack folders sat in the Claude Code plugin cache, and eleven empty old pack
  folders sat in Antigravity's data folder.

## What was removed

- The eleven old Claude Code cache folders, the stray user skill, and the empty old Codex and
  Antigravity folders.
- Two old private install runs, their backups, and three old private task folders.
- Three ignored build copies of 0.18 packs in other personal repositories.
- Five clean worktrees, 31 merged local branches, and 40 merged remote branches.

## What was kept

- The live install source, because the Claude Code and Codex marketplaces read the packs from it.
- Private lifecycle and review receipts, and the unrun Claude task packet.
- The branch for an open pull request, the `v0.16.0` tag, and any branch that was not merged.
- Every skill, plugin, worktree, and branch that is not part of Measured Skills.

After the cleanup, the packs still matched 12 of 12 hashes and each CLI listed its four packs.
A hash snapshot of 3,266 real plugin and settings files changed only in the removed cache
folders, in `settings.json` (the sync flag), and in the Codex config, which the Codex app
rewrote on its own.

This Mac no longer keeps a local copy of 0.18 or of the earlier freeze. The public rollback
target stays `v0.16.0`.

## Still open

- Old account skills remain in the Claude accounts and the ChatGPT account until their owner
  deletes them. Permanent account deletions are not done by an assistant.
- The 73 account uploads are not done.
- The Antigravity IDE is still over its 20,000 token customization budget, and the check did not
  separate Google's plugins from ours.
- The second Mac was not checked.
