# How to Use Measured Skills

Codex, Claude Code, and Antigravity have equal priority for setup, documentation, and testing. The same source skills feed their packages. Each app and CLI needs its own checks before we call it tested. See the [client support guide](client-support.md) for current package limits and a checklist for each client.

This guide explains how to choose, install, invoke, verify, update, and remove the skills safely.

Use the [five-minute quickstart](quickstart.md) for a local start. Use [Choose Your Skills](choose-your-skills.md) and the [skill cheatsheet](skill-cheatsheet.md) for selection. Read the [skill catalog reader guide](skill-catalog-reader-guide.md) for the complete 79-skill inventory, verified plugin grouping, explicit-only map, and client-specific selection boundaries.

## Start with the security boundary

Before installation:

1. Review the repository source and license.
2. Use a reviewed commit or release tag when possible.
3. Run the repository validation commands if you have a local clone.
4. Install only the plugins needed for the current work.
5. Start a fresh client session after installation or an update.

The catalog contains instructions and reference files. It does not contain hooks, MCP servers, bundled agents, skill-level executables, package dependencies, or broad tool permissions. A skill can guide judgment, but it cannot replace host permissions, tests, access controls, or human approval.

Read these files before using the catalog for sensitive work:

- [Security policy](../SECURITY.md)
- [Security model](security-model.md)
- [Public and private catalog policy](catalog-policy.md)
- [Observed client evidence](manual-smoke-tests.md)

## Choose a plugin

Install the smallest plugin that covers the work.

| Plugin | Use it for |
| --- | --- |
| `measured-skills` | Verification, research, diagnosis, authority review, quality gates, launch review, safe publication, public boundary review, and skill security |
| `measured-engineering-build` | Frame, design, plan, and test a vertical slice |
| `measured-engineering-review` | Review correctness, compatibility, security, and operational risk |
| `measured-engineering-delivery` | Coordinate bounded execution, Git, and delivery evidence |
| `measured-stack-profiles` | Focused Adobe AEM, C# and .NET, Go, Java and Spring, PHP and Drupal, Python, Salesforce and Apex, Swift and SwiftUI, TypeScript and JavaScript, PostgreSQL and SQL, and Terraform guidance |
| `measured-operations` | Requirements, decisions, workshops, measurement, value evidence, adoption, dependencies, stakeholder communication, postlaunch learning, incidents, and data authority decisions |
| `measured-reasoning` | Alignment, domain vocabulary, code explanation, design rationale, change impact, technical writing, decision traces, portable skill authoring, guided configuration, task handoff, and workflow retrospectives |
| `measured-ai-systems` | AI evaluation contracts, context reliability, and exact source-to-output conformance. Written from the author's own practice, with NIST test, evaluation, verification, and validation (TEVV) resources and the W3C PROV provenance standard used only as correctness authorities |
| `measured-agent-platforms` | Google ADK architecture, agent context, tool boundaries, protocols, agentic security, and retrieval grounding |

Installing every plugin at once increases the amount of skill description text loaded by a client. It can also increase trigger collisions. Start with one plugin and add another only when the work needs it.

## Get the repository

You can use the public GitHub repository directly or clone it for review.

```sh
git clone https://github.com/JovaniPink/measured-skills.git
cd measured-skills
```

For higher risk work, review and check out a specific commit or release tag before installation. A mutable branch such as `main` can change after review.

## Choose your client

Follow the focused guides for [Codex](clients/codex.md), [Claude](clients/claude.md), or [Antigravity](clients/antigravity.md). Each covers the current package, local checks, and app limits. Antigravity setup does not wait on a Codex study. Its preview excludes skills that require direct selection until that control is verified.

The sections below keep the full Codex and Claude command reference.

## Install for Codex CLI and ChatGPT desktop

Add the GitHub repository as a marketplace:

```sh
codex plugin marketplace add JovaniPink/measured-skills
```

If you cloned the repository, you can add the local repository path instead:

```sh
codex plugin marketplace add /path/to/skills
```

Install one or more focused plugins:

```sh
codex plugin add measured-skills@measured-skills
codex plugin add measured-engineering-build@measured-skills
codex plugin add measured-engineering-review@measured-skills
codex plugin add measured-engineering-delivery@measured-skills
codex plugin add measured-stack-profiles@measured-skills
codex plugin add measured-operations@measured-skills
codex plugin add measured-reasoning@measured-skills
codex plugin add measured-ai-systems@measured-skills
codex plugin add measured-agent-platforms@measured-skills
```

Verify the installed version and enabled state:

```sh
codex plugin list --json
```

Start a fresh Codex task or ChatGPT desktop task after installation. An existing task may keep the skill set that was available when that task started.

OpenAI documents plugin skills for Chat and Work across ChatGPT web, desktop, and mobile, plus Codex in the ChatGPT desktop app and Codex CLI. A local marketplace added with the CLI is a local development and desktop testing path. It does not automatically install the plugin into a ChatGPT web account. Workspace installation and directory publication are separate administrative actions.

Official resources:

- [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills)
- [OpenAI Build plugins](https://developers.openai.com/plugins/build/plugins)

## Install for Claude Code and Claude Desktop

Add the repository marketplace at user scope:

```sh
claude plugin marketplace add JovaniPink/measured-skills --scope user
```

You can also use a reviewed local clone:

```sh
claude plugin marketplace add /path/to/skills --scope user
```

Install the focused plugins you need:

```sh
claude plugin install measured-skills@measured-skills --scope user
claude plugin install measured-engineering-build@measured-skills --scope user
claude plugin install measured-engineering-review@measured-skills --scope user
claude plugin install measured-engineering-delivery@measured-skills --scope user
claude plugin install measured-stack-profiles@measured-skills --scope user
claude plugin install measured-operations@measured-skills --scope user
claude plugin install measured-reasoning@measured-skills --scope user
claude plugin install measured-ai-systems@measured-skills --scope user
claude plugin install measured-agent-platforms@measured-skills --scope user
```

Verify the installed version and enabled state:

```sh
claude plugin list --json
```

Start a fresh Claude Code or Claude Desktop session after installation. User scope installation can make a plugin available to local Claude Code sessions, including the Code area in Claude Desktop. Cloud sessions and other surfaces can have different installation behavior, so test each surface separately.

Official resources:

- [Claude Code on desktop](https://code.claude.com/docs/en/desktop)
- [Discover and install Claude plugins](https://code.claude.com/docs/en/discover-plugins)
- [Create and distribute a Claude plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces)

## Install for Claude.ai

Claude.ai uses individual skill ZIP files instead of the Claude plugin marketplace.

From a reviewed local clone, build the reproducible archives:

```sh
python3 scripts/package_claude_ai.py
```

The archives are created under `dist/claude-ai`. Upload only the individual ZIP for the skill you want. In Claude.ai, open the skill customization area, upload the ZIP, inspect the displayed files, and enable it only after review.

Do not upload an entire plugin directory as one Claude.ai skill. Each ZIP is nested for one skill.

Official resource:

- [Use Skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude)

## Invoke a skill

Most skills support implicit invocation. Describe the work clearly and the client can select the matching skill.

Examples:

```text
Verify whether this pull request is merged, deployed, and live. Do not change anything.
```

```text
Diagnose why this test fails. Establish the cause, but do not implement a fix.
```

```text
Synthesize these notes into traceable requirements. Keep proposals separate from ratified decisions.
```

Use direct invocation when you need a specific skill or when the skill is explicit-only.

Codex example:

```text
$measured-engineering-delivery:plan-execution Run the approved plan. Stop if the scope or authority changes.
```

Claude Code example:

```text
/measured-engineering-delivery:plan-execution Run the approved plan. Stop if the scope or authority changes.
```

In ChatGPT, use the `@` skill selector documented by OpenAI. Exact display names and selection behavior can vary by installed plugin and client version.

The explicit-only skills are:

- `acceptance-evidence-ledger`
- `research-to-publication-lifecycle`
- `publish-change-safely`
- `skill-import-provenance`
- `plan-execution`
- `request-code-review`
- `finish-development-branch`
- `multi-agent-orchestration`
- `decision-evidence-trace`
- `prototype-spike`
- `merge-conflict-reconciliation`
- `guided-configuration`
- `task-handoff`
- `workflow-retrospective`

Natural language alone should not activate these workflows implicitly. Direct invocation still does not authorize a push, publication, merge, deletion, deployment, or other external action unless the user separately authorizes that action.

## Understand what a skill can and cannot prove

A skill can help gather and organize evidence. It cannot make separate states equivalent.

Examples:

- A passing local test does not prove that CI passed.
- A merged pull request does not prove that deployment completed.
- A provider deployment record does not prove that a public page works.
- A repository manifest does not prove that a client discovered or invoked a skill.
- A CLI observation does not prove the same behavior in a desktop or web client.

Use the [manual smoke test record](manual-smoke-tests.md) and [client surface research](client-surface-research.md) for observed behavior. Treat blocked or untested rows as unknown, not as passes.

## Keep API and runtime surfaces separate

OpenAI Skills API, Anthropic Skills API, Anthropic Managed Agents, Antigravity CLI, enterprise-only Gemini CLI compatibility, Gemini Managed Agents, and Google ADK runtime skills are distinct products and trust boundaries. A local plugin observation does not prove an API upload, repository mount, managed session, hosted run, or ADK runtime behavior.

Read [Agent Platform Boundaries](agent-platform-boundaries.md), [Google agent surfaces](google-agent-surfaces.md), and [Google ADK](google-adk.md) before using skills in an agent application. Runtime ADK observations belong in the separate runtime adapter repository, not in this assistant catalog.

## Update a local installation

Review upstream changes before updating. Then refresh the marketplace using the command supported by the client.

Codex:

```sh
codex plugin marketplace upgrade
codex plugin list --json
```

Claude Code:

```sh
claude plugin marketplace update measured-skills
claude plugin list --json
```

Start a fresh session and repeat the relevant smoke tests after an update.

## Remove a plugin

Codex:

```sh
codex plugin remove measured-skills@measured-skills
```

Claude Code:

```sh
claude plugin uninstall measured-skills@measured-skills --scope user
```

Replace `measured-skills` before the `@` character with the plugin you installed. Verify removal with the client plugin listing. Removing a marketplace advertisement cannot force deletion of copies that another user or client already installed.

## Validate a local clone

Run the deterministic catalog validation and unit tests:

Use PyYAML 6.0.3 from a trusted local environment, or use the reviewed Linux lock in `requirements-ci-linux.txt`.

```sh
python3 scripts/check_workflows.py
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

Check that generated distributions still match canonical sources:

```sh
python3 scripts/build_distributions.py --check
```

Check the public boundary before publication:

```sh
python3 scripts/check_public_boundary.py
```

Validation checks workflow YAML syntax, structure, metadata, links, generated drift, packages, trigger cases, and public boundary rules. It does not prove behavior in every client. Manual client observations remain separate evidence.

## Author or change a skill

Author only under `skills`. Do not hand edit files under `plugins`.

Use this workflow:

1. Read the [authoring guide](authoring.md).
2. Create or update the canonical `skills/skill-name/SKILL.md` source.
3. Add focused references only when they are needed.
4. Add positive, near-miss, safety, and output-quality evaluations.
5. Record independently authored provenance with only the applicable primary authority.
6. Regenerate the Codex and Claude plugin trees.
7. Package Claude.ai ZIP files.
8. Run all validation and unit tests.
9. Record observed client behavior without inferring parity.

Useful repository documents:

- [Glossary](glossary.md)
- [Turn-depth study design](turn-depth-study.md)
- [Architecture](architecture.md)
- [Taxonomy](taxonomy.md)
- [Choose your skills](choose-your-skills.md)
- [Agent platform boundaries](agent-platform-boundaries.md)
- [Google ADK](google-adk.md)
- [Authoring guide](authoring.md)
- [Finding vocabulary](finding-vocabulary.md)
- [Editorial style](editorial-style.md)
- [Testing guide](testing.md)
- [Provenance policy](provenance.md)
- [Release process](release-process.md)
- [Validation evidence](validation-evidence.md)
- [Behavioral evidence model](behavioral-evidence-model.md)
- [Daily agent operating model](daily-agent-operating-model.md)

## Keep private facts in private overlays

Do not put private product authorities, customer facts, infrastructure details, schemas, identities, or operational contracts in the public catalog.

Use the repository local overlay model documented in [Private overlays](private-overlays.md). Public skills provide reusable workflow logic. Private overlays provide the facts that are valid only inside their owning repository.

## Troubleshooting

If a skill is not visible:

1. Confirm the marketplace is configured.
2. Confirm the plugin is installed and enabled.
3. Confirm the installed version.
4. Start a fresh task or session.
5. Check client authentication.
6. Confirm that the target surface supports that installation path.
7. Review the client observation matrix before assuming a client bug.

If implicit invocation is unreliable, disable unrelated plugins and try a more specific prompt. Use direct invocation when the workflow must be selected explicitly.

If an action could publish, merge, deploy, delete, send, or change an external system, stop and confirm authority before proceeding.

## General resources

- [Agent Skills specification](https://agentskills.io/specification)
- [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills)
- [OpenAI Build plugins](https://developers.openai.com/plugins/build/plugins)
- [OpenAI Skills API](https://developers.openai.com/api/reference/go/resources/skills)
- [Claude Code plugins](https://code.claude.com/docs/en/discover-plugins)
- [Claude plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Claude Skills support](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
- [Anthropic Skills API guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide)
- [Anthropic Managed Agents skills](https://platform.claude.com/docs/en/managed-agents/skills)
- [Google's Gemini CLI to Antigravity CLI transition](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/)
- [Antigravity Agent Skills](https://antigravity.google/docs/skills/)
- [Google ADK Agent Skills](https://adk-labs.github.io/adk-docs/skills/)
- [Repository license](../LICENSE)
