# Measured Skills

This repository holds 87 Agent Skills for AI coding assistants.

A skill is a short set of written instructions for one kind of task. Reviewing a code change is one kind of task. Checking whether a claim has evidence is another. Your assistant reads the matching skill and follows its steps.

A skill is only text. It installs no programs and grants no new permissions. It changes how your assistant works through a task, not what it is allowed to do.

Maintained by [Measured Studios](https://measuredstudios.com). This is the 0.18.0 workflow candidate; see the [migration guide](docs/measured-migration.md) before changing an existing install.

Start with the [daily-work guide](docs/daily-agent-operating-model.md) for a small selection and five example requests.

Building a feature? Follow the [feature-development workflow](docs/feature-development-workflow.md), with step-by-step prompts and a shorter three-request path for Codex, Claude Code, and Antigravity.

## Install one pack

A pack is a group of related skills you install together. There are 11. Start with one. The commands below target the GitHub source repository (`JovaniPink/measured-skills`); you can also provide a local reviewed checkout path, as described in each client setup guide and the [migration guide](docs/measured-migration.md).

For Claude Code:

```sh
claude plugin marketplace add JovaniPink/measured-skills --scope user
claude plugin install measured-skills@measured-skills --scope user
claude plugin list --json
```

For Codex:

```sh
codex plugin marketplace add JovaniPink/measured-skills
codex plugin add measured-skills@measured-skills
codex plugin list --json
```

For Antigravity, this repository's reviewed local-folder route is:

```sh
agy plugin install /absolute/path/to/measured-skills/plugins/antigravity/measured-skills
agy plugin enable measured-skills
agy plugin list
```

Google also documents native marketplace discovery. That does not qualify this repository's generated marketplace preview or establish its installed behavior. Explicit-only skill controls remain unverified on Antigravity. See its setup guide for the generated pack contents and explicit-only exclusions.

For Claude and Codex, the install name has the form `plugin@marketplace`. A marketplace is a place your client looks for packs. This repository is the marketplace, and it is named `measured-skills`. One pack carries that same name. So `measured-skills@measured-skills` is correct, not a repeated word. Every other pack reads like `measured-engineering-build@measured-skills`.

See [Antigravity setup](docs/clients/antigravity.md).

Now start a fresh task and name a skill:

```text
/measured-skills:claim-verification Check which completion claims have evidence. Make no changes.
```

Codex uses `$` in place of `/`.

For work where the risk is high, clone the repository first. Read the source, check out a reviewed revision, then add your local folder as the marketplace. The [five-minute quickstart](docs/quickstart.md) walks through that path.

## What these skills do for you

Skills help frame outcomes, design coherent interfaces, build vertical slices, and review risk at the right checkpoint. They keep evidence and unknowns visible without granting authority. These are intended behaviors, not demonstrated productivity gains.

A few examples:

- `claim-verification` tests whether done, fixed, merged, or deployed is backed by evidence.
- `systematic-diagnosis` finds a cause instead of quietly changing your code.
- `code-change-review` reviews one exact diff and grades each finding.
- `source-grounded-research` keeps sources, dates, and uncertainty attached to the answer.

These are authored instructions, not measured benefits. We wrote the skills to produce those habits. We have not run a study that shows they improve your results.

## The 11 packs

Install the smallest pack that covers your work.

| Pack | Use it for |
| --- | --- |
| `measured-skills` | Verify claims, research, diagnose problems, review what is safe to publish |
| `measured-engineering-build` | Frame outcomes, design interfaces, plan and test behavior |
| `measured-engineering-review` | Review correctness, compatibility, security, and readiness |
| `measured-engineering-delivery` | Coordinate bounded execution, Git work, and delivery evidence |
| `measured-reasoning` | Explain code, improve writing, hand off work |
| `measured-operations` | Requirements, decisions, measurement, adoption, incidents |
| `measured-stack-profiles` | Language and platform guidance, such as Python, Go, and Terraform |
| `measured-ai-systems` | Evaluate AI behavior, context reliability, and source-to-output checks |
| `measured-agent-platforms` | Review agent architecture, tools, protocols, and retrieval |
| `measured-swift-workflows` | Bounded SwiftUI delivery, concurrency and persistence review, fixture journeys |
| `measured-nextjs-workflows` | Bounded Next.js delivery, cache/auth review and measured React diagnosis |

The [skill cheatsheet](docs/skill-cheatsheet.md) lists all 87 skills with one line each. [Choose Your Skills](docs/choose-your-skills.md) helps you pick. The [skill catalog reader guide](docs/skill-catalog-reader-guide.md) explains every skill in full.

## How a skill gets picked

Every skill is marked implicit or explicit-only.

Implicit means your client may pick the skill on its own when your request matches it. You can still name it directly. 70 skills are implicit.

Explicit-only means you must name the skill before using it. Naming it does not authorize a push, merge, deletion, release, or deployment. You still approve those yourself. 17 skills are explicit-only.

The cheatsheet shows the marking for each skill. The [glossary](docs/glossary.md) defines the other terms used here.

## What each client can do today

Codex, Claude Code, and Antigravity get equal attention here. Equal attention does not mean every feature works everywhere yet.

| Client | What we ship | Setup guide |
| --- | --- | --- |
| Codex CLI and ChatGPT desktop | Native packs with all 87 skills | [Codex setup](docs/clients/codex.md) |
| Claude Code | Native packs with all 87 skills, plus separate ZIP files for account uploads | [Claude setup](docs/clients/claude.md) |
| Antigravity CLI and IDE | Native packs with 70 implicit skills; 17 explicit-only workflows held | [Antigravity setup](docs/clients/antigravity.md) |

Claude Code packs and Claude account uploads are two separate installs. Updating your Code packs does not update the skill library that Chat uses. Check both.

For Claude.ai, build one-skill ZIP files from a local clone with `python3 scripts/package_claude_ai.py`. Upload them one at a time from `dist/claude-ai/`.

The 17 explicit-only skills are on hold for Claude.ai uploads. A hold means the files are ready, but we decided not to ship them yet, because a check we named has not passed. The missing check here is a control that stops Claude.ai from picking the skill on its own. A metadata field does not prove that control. Neither does a working slash command.

Client behavior changes on its own schedule. The [client support checklist](docs/client-support.md) lists what to test in each app and CLI. A result in one app does not carry to another.

## Evidence and status

This project keeps two words apart.

Authored means we wrote it. It says what the instructions intend.

Observed means we ran it and wrote down what happened, with the exact client, version, and date.

The current candidate is 0.18.0: 87 skills in 11 packs. The [candidate record](docs/client-candidate-v0.18.0.md) separates structural checks from behavior still requiring observation.

Historical engineering checks retain their original versions. They do not establish behavior for renamed packs or edited skills. No 0.18.0 installed-client benefit is claimed.

The October 20 pilot and [October 21 retest](docs/audits/claude-retest-observations-2026-10-21.json) include continuity follow-ups. They found review-selection and evidence errors; the later GCP answer also exceeded its supplied contract. These bounded observations do not establish long-session reliability or qualify the profile. The [next diagnostic plan](docs/audits/claude-routing-contract-retest-plan-2026-10-21.md) remains unrun, and the broader [turn-depth study](docs/turn-depth-study.md) remains separate. Read the [readiness record](docs/release-readiness-2026-10-20.md) for current decisions and dated evidence.

We do not claim that these skills improve your results. That claim would need a separate study with complete runs and human review. That study has not been run.

## Safety

The catalog ships instructions and reference notes. It ships no skill-level programs, hooks, MCP servers, bundled agents, or broad tool grants. Nothing installs or runs on its own.

This matters because a skill you install can shape every later task. Keeping it to text means you can read the whole thing before you trust it. It also means your client's own permission rules stay in charge.

A skill can recommend an action. Your permissions, your tests, and your approval decide whether it happens.

Read the [security policy](SECURITY.md) and the [security model](docs/security-model.md) before you use the catalog for sensitive work.

## License and origin

The repository offers its owned contributions under the [MIT license](LICENSE). [Provenance records](provenance/catalog.json) distinguish original declarations from four owned adaptations. The maintainer [accepted the scoped originality decision](docs/audits/originality-acceptance-0.18.0.json), `originality-018-owned-inventory-20261020`, for exact revision `36a4e56c7fcde0411d2b3c7052c9f2b889d05aa7`, including its candidate gate change. The [preserved proposal](docs/audits/originality-approval-2026-10-20.md) records prior exposure, AI assistance, and review limits. Later changes have a [scoped delta review](docs/audits/post-acceptance-delta-2026-10-20.json), not automatic new acceptance. This decision does not certify universal originality, independent legal clearance, client acceptance, or release readiness.

Private product facts stay out of this catalog. [Private overlays](docs/private-overlays.md) explains how they are kept apart.

The source format is the open [Agent Skills format](https://agentskills.io/specification).

## Contribute or build it yourself

Skills are authored in `skills/`. The `plugins/` folders are generated, so do not edit them by hand.

Read [CONTRIBUTING.md](CONTRIBUTING.md) before you open a pull request. [Repository architecture](docs/architecture.md) describes the folder layout. [Testing](docs/testing.md) lists the exact build and check commands, plus the tool versions they need. The [editorial style guide](docs/editorial-style.md) covers the writing rules.

## Where to go next

- [Five-minute quickstart](docs/quickstart.md): install and test one skill
- [Glossary](docs/glossary.md): what the terms mean
- [Skill cheatsheet](docs/skill-cheatsheet.md): all 87 skills at a glance
- [Client support checklist](docs/client-support.md): what to test in each app and CLI
- [How to use Measured Skills](docs/README.md): the full guide
