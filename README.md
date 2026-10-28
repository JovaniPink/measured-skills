# Measured Skills

Find the right workflow, understand its boundaries, and finish the next piece of
work without rebuilding your instructions.

**[Start here: find your next workflow](docs/start.md)**

Choose **Finish existing work** for an unfinished change, a failing check, or review
feedback. The chooser gives you a starting skill, the context to provide, an
example result, and a request you can copy for your client. Choose whether to
assess, repair locally, or maintain one identified draft PR.

**0.19.0 preview:** 90 skills in four packs. This is an unreleased redesign, separate
from the preserved [0.18 candidate](docs/client-candidate-v0.18.0.md). New names and
packages have no inherited client acceptance. No installation or model call is
needed to read the guide. [Preview status](docs/client-candidate-v0.19.0.md).

## Choose work, not a catalog

- [Open the offline chooser](dist/discovery/index.html) after saving the file locally.
- [Read the same guide in Markdown](dist/discovery/guide.md).
- [Browse all skills](docs/skill-catalog-reader-guide.md), including their former names.
- [Continue unfinished work](docs/finish-existing-work.md) or [develop a feature](docs/feature-development-workflow.md).
- [Upgrade or roll back deliberately](docs/migration-0.19.md); old and new names must not become duplicate installations.

The website preview, offline guide, and in-client `choose-workflow` reference use
one versioned registry. The website consumes a committed export; it does not fetch
mutable `main` at runtime. Selecting a route executes nothing. Sending its prompt
asks the assistant to perform the scope written in that prompt.

## Four packs, focused selections

| Pack | Capabilities | Count |
| --- | --- | --- |
| `measured-workflows` | Understand, frame, plan, diagnose, execute, research, write, hand off and deliver | 32 |
| `measured-quality` | Check, review, verify evidence, security and agent-system quality | 27 |
| `measured-stacks` | Language/platform guidance and focused application workflows | 20 |
| `measured-operations` | Requirements, decisions, adoption, measurement and incidents | 11 |

`measured-skills` is the repository and marketplace name; it is no longer a
catch-all pack. Packs are distribution units. Start with the nine-skill
`finish-work-core` profile and add a relevant stack only when needed. The existing
daily and finish-work profiles retain their history with mapped 0.19 identifiers.
[Staged exports](docs/migration-0.19.md) do not install anything.

## What is available, and what is known

Codex and Claude Code projections contain 90 skills. Antigravity contains the 73
implicit skills; all 17 explicit-only workflows remain excluded. Account archives
are prepared separately, and explicit-only uploads remain held until the receiving
surface's invocation control is verified. Packaging is not installation acceptance.

Use the [Codex](docs/clients/codex.md), [Claude](docs/clients/claude.md), or
[Antigravity](docs/clients/antigravity.md) guide for the installed interface. Check
actual selection, loading, reference reads, and results separately. Duplicate
names and stale same-version caches can obscure which source ran.

A skill is written guidance. It grants no permissions and supplies no executable
payload, hooks, MCP servers, bundled agents, or broad tool grants. Naming an
explicit workflow selects it; the user's actual request establishes the authorized
actions. Review, repairs, external writes, merge and release remain distinct.

Historical observations, including failures and continuity follow-ups, remain in
the [0.18 readiness ledger](docs/release-readiness-2026-10-26.md). Renaming a skill
does not turn those records into 0.19 results. The [0.19 acceptance exercise](docs/acceptance-0.19.md)
starts with human usability, without model calls. The later bounded real-work trial
requires separate authorization. No productivity, financial benefit, or cross-client
parity is established.

## License and origin

The repository offers its owned contributions under the [MIT license](LICENSE). [Provenance records](provenance/catalog.json) distinguish original declarations from four owned adaptations. The maintainer [accepted the scoped originality decision](docs/audits/originality-acceptance-0.18.0.json), `originality-018-owned-inventory-20261020`, for exact revision `36a4e56c7fcde0411d2b3c7052c9f2b889d05aa7`, including its candidate gate change. The [preserved proposal](docs/audits/originality-approval-2026-10-20.md) records prior exposure, AI assistance, and review limits. Later changes have a [scoped delta review](docs/audits/post-acceptance-delta-2026-10-20.json), not automatic new acceptance. This decision does not certify universal originality, independent legal clearance, client acceptance, or release readiness.

Private product facts stay out of this catalog. [Private overlays](docs/private-overlays.md) explains how they are kept apart.

The source format is the open [Agent Skills format](https://agentskills.io/specification).

## Contribute

Author under `skills/`; regenerate `plugins/` and archives. Read
[CONTRIBUTING.md](CONTRIBUTING.md), [authoring](docs/authoring.md),
[testing](docs/testing.md), and [architecture](docs/architecture.md). Preserve source
ancestry and the separate source/artifact and manifest commits. The
[research disposition](docs/audits/discovery-0.19.md) explains what this redesign
adopts, rejects, and leaves unverified.
