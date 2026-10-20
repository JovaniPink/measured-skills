# Quickstart

Choose one task, one client, and a small set of skills. This is the unreleased
0.18.0 candidate; use a reviewed source revision and keep its identity with your
installation. Historical release checks do not qualify a changed candidate.

## 1. Choose a small set

Start with the [daily-work guide](daily-agent-operating-model.md) for five example
requests and an experimental profile, or [choose one pack](choose-your-skills.md).
A pack is an installation unit; a profile is a selection of skills for a task.
Do not install every pack merely to try one skill.

## 2. Follow your client's setup

| Client | Guide |
| --- | --- |
| Codex | [Codex setup and checks](clients/codex.md) |
| Claude Code and account uploads | [Claude setup and checks](clients/claude.md) |
| Antigravity CLI and IDE | [Antigravity setup and limits](clients/antigravity.md) |

Use a reviewed local checkout when exact source control matters. The
[current candidate record](client-candidate-v0.18.0.md) states what has and has
not been observed. Do not substitute an older differently named release.

## 3. Try one request and inspect the result

Ask for a concrete task, such as "Review this PR diff; do not edit it." Inspect
which skill actually loaded and whether the response addresses the task with
evidence. Keep invocation and answer quality as separate observations.

If a skill fails to appear, check the installed inventory, duplicate uploads,
version, and discovery budget for that exact client before changing its text.

## For contributors

Maintainers regenerate distributions and run the full checks in
[Testing and validation](testing.md). The [contribution guide](../CONTRIBUTING.md)
explains the separate source and manifest commits. These are authoring checks,
not a prerequisite to every end-user request.
