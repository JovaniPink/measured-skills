# Use skills in any of the three clients

Codex, Claude Code, and Antigravity have equal priority in this project. Each gets a setup guide, package checks, and its own use tests. Work on one client does not need to wait for a good result from another.

Equal priority does not mean every feature already works everywhere. We record what each client can load and what we have tested.

## Start with your client

| Client | What we prepare | Where to start |
| --- | --- | --- |
| Codex | Native plugins with all 86 skills | [Codex setup](clients/codex.md) |
| Claude Code | Native plugins with all 86 skills; separate ZIP files for account uploads | [Claude setup](clients/claude.md) |
| Antigravity | Native plugins with 69 implicit skills; 17 explicit-only workflows are excluded pending verified controls | [Antigravity setup](clients/antigravity.md) |

A plugin is a group of skills. A skill is a set of instructions for a kind of task. A CLI is an app you use by typing commands in a terminal.

The [current candidate record](client-candidate-v0.17.1.md) lists install results and active holds. A prepared package is not a recommendation to enable it before its checks pass.

## What each client must pass

Use a fresh test task with made-up data. Save the result in a private check record if it includes local paths or account details.

1. **Find it.** The client lists the expected skill and its source. Check for an older copy with the same name.
2. **Choose it.** A direct request opens the right skill. A related request selects only a suitable skill.
3. **Respect direct selection.** A skill marked explicit-only must stay inactive until the user selects it. A slash command alone does not prove this rule works.
4. **Read its files.** The client can open the skill's linked notes. It can also open the result file it creates.
5. **Keep the facts.** The answer leads with the result. Failed checks, unknowns, and unfinished work remain visible. A request for detail still gets detail.
6. **Resume work.** Interrupt a small task with a status question. Resume it and check the goal, files, tests, and next step. Then change the goal on purpose and check that the new goal takes over.
7. **Update it.** After a package update and a fresh task, verify the new files by hash. A hash is a file fingerprint; a version label alone is not enough.
8. **Remove it.** In the test setup, remove the test package and confirm that it no longer appears in a fresh task. Keep the old package available for rollback.

These checks apply separately to each row below. Do not fill one row with a result from another.

| App or command | Separate check record |
| --- | --- |
| Codex CLI | Terminal commands and a fresh CLI task |
| Codex desktop | App plugin list, new task, files, and resume |
| ChatGPT Work | Its own skill library, files, and resume |
| ChatGPT web/chat | Its own available skills and file access |
| Claude Code CLI | Terminal commands and a fresh CLI task |
| Claude desktop, Code mode | Local or remote task type, plugin source, files, and resume |
| Claude.ai | Account skill library, files, and resume |
| Claude desktop, Chat/Cowork | Each mode's skill list, files, and resume |
| Antigravity CLI | Native package layout, skill list, files, and resume |
| Antigravity desktop | App skill list, rules, files, and resume |
| Antigravity IDE | IDE skill list, rules, files, and resume |

APIs, hosted agents, SDKs, ADK, and enterprise Gemini CLI keep separate future checks. This work adds no runtime or automated client runner for them.

## Keep a short check record

```text
Date and exact app or CLI:
Client version and model, if a model was used:
Source commit and package file hashes:
Install location and scope:
Skill names, old copies, and missing skills:
Instructions that actually loaded:
Prompt and observed result:
Files or screenshots that support the result:
Passed, failed, or not checked:
Next step, if needed:
```

Use **prepared**, **installed**, **listed**, **used**, and **tested** as separate states. A file on disk proves only that the file is there. A good reply does not prove which skill produced it.

## Make updates without losing work

First list the current packages and compare their files with the reviewed source. Save a copy of the old setup. Prepare the new package, then change one client at a time. Start a fresh task when it is safe to do so; do not restart an active task just to refresh skills.

Keep personal writing preferences outside the catalogs. This short preference can be reviewed for each client's own instruction file or rules page:

> Lead with the supported result or current decision. Preserve uncertainty, failed checks, and requested detail. Make interrupted work easy to resume, and identify the next action when one is needed.

Check that the preference loaded before calling it active. Keep the same wording when comparing clients.

The study that measures whether revised skills help is separate from these setup checks. A study needs complete runs and human review. An install check cannot prove that the skills improve task results.
