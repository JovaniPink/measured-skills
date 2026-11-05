# Skill security review on November 5, 2026

Status: review finished and its five warnings fixed in skill text. The verdict was
`APPROVE WITH CONDITIONS`, with no errors. The fixes were the condition. This is not a
penetration test, a safety guarantee, or a client behavior result.

## What was reviewed

The maintainer asked for a security review of all four packs before a tag. It covered all
90 canonical skills and their references, plus the generated Claude Code, Codex, and
Antigravity packages, at `63156e05a9c7c5f25ed50920cc49b8c49bd00cfe`.

The method was static. Reviewers read the text and every warning below was checked
against the exact lines. No skill ran against a live system.

The packs ship no hooks, MCP servers, tool grants, or skill-level executables. Plain
instructions are still influence, so the review looked at what each skill tells an
assistant to do, and when.

## Warnings and fixes

| Skill | Warning | Fix |
| --- | --- | --- |
| `run-project-checks` | It ran repository commands with no warning about repositories the user has not said they trust | Read what a command runs and ask first in such a repository. Scripts, hooks, and tests run code with your permissions |
| `check-launch-readiness` | Its platform access was not limited to reads | Use read-only queries, and only when the request covers it. Do not submit production forms, sign-ins, payments, or test transactions, or create accounts or data, without explicit authorization. Otherwise mark the item `UNVERIFIED` |
| `review-public-boundary` | It read as a review but could edit files and run tests, and it had no rule for secrets in findings | Edit files only when the request asks for redaction. Re-run tests only after an authorized redaction. Never quote a secret: give its type and location, and mask the value |
| `stack-terraform` | It allowed `init` and `plan` against real backends | Treat those as provider access: they use credentials, can lock state, and call provider APIs. Prefer static checks and `terraform init -backend=false` with `terraform validate`. Run a real plan only with authorization |
| All 13 `stack-*` skills | They can load on their own and suggested repository gates under a review label | Run a gate only when the user asked for checks and trusts the repository. Otherwise, name it as the next safe gate |

Descriptions did not change, so this edit should not change how skills are listed or
routed. That is an inference from unchanged text, not a routing test.

[`tests/test_skill_safety_text.py`](../../tests/test_skill_safety_text.py) pins these rules.
[The canonical delta](workflow-depth-2026-10-28.json) records all 16 changed skill files.

## What the fixes cost

These fixes changed `measured-quality` and `measured-stacks` bytes on all three clients,
16 Claude.ai ZIPs, and the discovery export. `measured-workflows` and `measured-operations`
bytes did not change. Under [the freeze rules](release-decision-0.19.0.md#freeze), that
ended the old freeze. The result is in
[the amendment](release-decision-0.19.0.md#amendment-on-november-5-2026-safety-fixes).

## Limits

- Text rules guide an assistant. They do not enforce anything. A client's permission
  system is the actual control.
- No fresh task tested whether an assistant follows the new rules.
- The file counts reviewers reported differed slightly from the real counts, so full
  coverage of every reference is likely but not proven.
- A review of a third-party skill or a future skill change needs its own run.
