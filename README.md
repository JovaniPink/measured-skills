# Measured Skills

Make your next code review easier to reason about. Copy a scoped request, paste
it into your assistant, and inspect what changed, which concerns are real, and
what remains unverified. Copied requests work today with nothing installed.
The four optional packs supply reusable instructions and reference notes.

**[Start here: find your next workflow](docs/start.md)**

For code review, start with the work in front of you:

- [Prepare a change for review](docs/code-review-workflow.md#prepare-a-change-for-review): explain the purpose, revision, checks, and open risks.
- [Review a change](docs/code-review-workflow.md#review-a-change): inspect the diff, clear false alarms with counter-evidence, and report coverage gaps.
- [Address review feedback](docs/code-review-workflow.md#address-review-feedback): check each claim against the current code and decide what needs to change.

See what that judgment looks like before installing anything:

- [Captured review case (real repository diff)](docs/review-cases/captured-review-case-2026-11-19.md): one supported finding, one concern cleared by counter-evidence, and one unresolved coverage gap bound to exact Git revisions.
- [Review casebook and preserved corrections](docs/review-cases/README.md): concrete disconfirmation patterns and real corrections from this repository.
- [3-arm review comparison kit (prepared, not run)](evals/review-comparison-v1/README.md): compares an ordinary review request, a structured Measured request, and selected skills on the same snapshots.

The [review lifecycle guide](docs/code-review-workflow.md) connects these tasks to
system impact, verification, and learning after release. Copy one request without
installing a skill. Choose **Finish existing work** for an unfinished change, a
failing check, or an authorized repair. Its scopes let you assess, repair locally,
or maintain one identified draft PR.

For the wider engineering process, read [code review as a system](docs/review-systems-thinking.md)
and [auditing prompt feedback loops](docs/prompt-feedback-loops.md). They connect
review capacity, shared understanding, bounded retries, and regression evidence.
The [research note](docs/research/review-and-feedback-evidence-2026-11-18.md)
separates supporting evidence from product claims that still need testing.

**Version 0.19.0** includes 91 skills in four packs. The offline chooser has
22 tasks. You can copy a request without installing a pack or signing in.

We verified install, upgrade, downgrade, uninstall and reinstall on Codex CLI,
Claude Code and Antigravity CLI. Human chooser usability is unmeasured.
[Release evidence](docs/release-status.md) and [migration instructions](docs/migration-0.19.md)
cover the tested versions and the change from the old pack names.

## Choose work, not a catalog

- [Open the offline chooser](dist/discovery/index.html) after saving the file locally.
- [Read the same guide in Markdown](dist/discovery/guide.md).
- [Browse all skills](docs/skill-catalog-reader-guide.md), including their former names.
- [Follow a change through review](docs/code-review-workflow.md), from the author's packet to evidence after release.
- [Continue unfinished work](docs/finish-existing-work.md) or [develop a feature](docs/feature-development-workflow.md).
- [Upgrade or roll back deliberately](docs/migration-0.19.md); old and new names must not become duplicate installations.

Use [`draft-prompt`](skills/draft-prompt/SKILL.md) when the work
starts with a rough request and you need an instruction another assistant can
follow. The offline guide and in-client `choose-workflow` reference use one
versioned registry. The website consumes its own committed export, which can be older; it does
not fetch mutable `main` at runtime. Selecting a route executes nothing. Sending its prompt
asks the assistant to perform the scope written in that prompt.

## Four packs, focused selections

| Pack | Capabilities | Count |
| --- | --- | --- |
| `measured-workflows` | Understand, frame, plan, diagnose, execute, research, write, hand off and deliver | 33 |
| `measured-quality` | Check, review, verify evidence, security and agent-system quality | 27 |
| `measured-stacks` | Language/platform guidance and focused application workflows | 20 |
| `measured-operations` | Requirements, decisions, adoption, measurement and incidents | 11 |

`measured-skills` is the repository and marketplace name; it is no longer a
catch-all pack. Packs are distribution units. Start with the nine-skill
`finish-work-core` profile and add a relevant stack only when needed. The existing
daily and finish-work profiles retain their history with mapped 0.19 identifiers.
[Staged exports](docs/migration-0.19.md) do not install anything.

## What is available, and what is known

Codex and Claude Code projections contain 91 skills. Antigravity contains the 74
implicit skills; all 17 explicit-only workflows remain excluded. Account archives
are prepared separately, and explicit-only uploads remain held until the receiving
surface's invocation control is verified. The [release record](docs/release-status.md) identifies the
frozen packages, tested CLI versions, lifecycle checks and rollback rehearsal.

Use the [Codex](docs/clients/codex.md), [Claude](docs/clients/claude.md), or
[Antigravity](docs/clients/antigravity.md) guide for the installed interface. Check
actual selection, loading, reference reads, and results separately.
A copied request works without a skill. In a [one-model exploration](docs/audits/haiku-exploration-2026-11-05.md)
of one synthetic task, the request's wording changed results more than loading
`plan-change` did, and ordinary requests often did not load a skill. Use the native command when you want a specific skill. Duplicate
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
