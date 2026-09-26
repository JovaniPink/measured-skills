# Quickstart

Choose the client you want to use: Codex, Claude Code, or Antigravity. You can prepare and check any of them without waiting for another client.

## 1. Get the skills

```sh
git clone https://github.com/JovaniPink/measured-skills.git
cd measured-skills
git status --short --branch
```

Check out the reviewed tag so your copy cannot move under you:

```sh
git checkout v0.16.0
```

A full commit works too. Try not to test from the default branch, because it changes.

## 2. Check the files

Use PyYAML 6.0.3 from a trusted Python environment. See [Testing](testing.md) for the full setup.

```sh
python3 scripts/check_workflows.py
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

Passing checks mean the source and packages agree. You still need to check that your client loads them.

## 3. Choose a pack

Start with the skills your task needs. A pack is a group of skills you install together.

- `measured-skills`: check claims, research, and find causes of problems.
- `measured-engineering-build`: frame, design, plan, and test a vertical slice.
- `measured-engineering-review`: review correctness and risk.
- `measured-engineering-delivery`: coordinate bounded execution and delivery.
- `measured-reasoning`: explain code, improve writing, and hand off work.

Read the [current candidate checks](client-candidate-v0.17.0.md) before you rely on a renamed pack. Before 0.17.0, one engineering pack held all of this work. It was held after a live motion-review failure, and both command lines cleared it on 2026-09-10. That result stays in the [0.16.0 record](client-candidate-v0.16.0.md). It does not carry over to the three new engineering packs.

The [selection guide](choose-your-skills.md) lists the other packs.

## 4. Follow your client's setup guide

| Client | Guide | Current package |
| --- | --- | --- |
| Codex | [Setup and checks](clients/codex.md) | Native plugins |
| Claude Code | [Setup and checks](clients/claude.md) | Native plugins; separate account ZIPs |
| Antigravity | [Setup and checks](clients/antigravity.md) | Offline preview; loading check still needed |

First list existing skills and look for old copies. Then review the package before installing it. Use a fresh task for the check.

Gemini CLI is a separate, conditional enterprise check. It is not the Antigravity CLI. See [Google clients and tools](google-agent-surfaces.md).

## 5. Try a small task

```text
Check this task summary against its evidence. State the supported result first. Keep failed checks, unknowns, and unfinished work visible. Make no changes.
```

Confirm which skill the client used. Open one of its linked notes. Ask a status question, then resume the task and check that the original goal is still clear.

Use the [client checklist](client-support.md) to record the version, files, result, and anything you could not check. Test the CLI and app separately.

## If it does not work

Check these in order.

1. The pack is installed. Run your client's plugin list command and look for it by name.
2. The pack is enabled. Installing does not always enable. Some clients report a successful install and leave the pack off.
3. The reply carries the skill's own named sections. This is the one that catches people.

A reasonable-sounding answer is not proof that a skill loaded. In one recorded check, ten cases ran against a pack that was installed but disabled. Every reply read well, and not one contained the skill's named sections. Before you judge a skill, confirm its shape appears in the output.
