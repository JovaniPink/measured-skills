# Choose Your Skills

Install the smallest set of skills that covers the work in front of you. A pack is a group of skills you install together. A profile names which skills to turn on for one kind of work.

Install less than you think you need. Before your client picks a skill, it reads the name and short description of every skill you have installed. Skills you do not need take up that room and make a wrong pick more likely.

OpenAI gives Codex a skill-list budget of 2 percent of the context window, or 8,000 characters when the size is unknown. This catalog warns at 6,000, because your own instructions share that room.

Pack sizes live in [`catalog/packs.json`](../catalog/packs.json). Profiles and their sizes for each client live in [`catalog/profiles.json`](../catalog/profiles.json). These sizes count only the short descriptions a client reads to pick a skill. They do not count the full instructions.

## Pick one pack first

| Need | Start with |
| --- | --- |
| Verify claims, research, diagnose, or review public exposure | `measured-skills` |
| Frame, design, plan, and test a slice | `measured-engineering-build` |
| Review correctness and risk | `measured-engineering-review` |
| Coordinate execution and delivery | `measured-engineering-delivery` |
| Apply stack-specific judgment after repository discovery | `measured-stack-profiles` |
| Work on requirements, decisions, measurement, adoption, or incidents | `measured-operations` |
| Improve alignment, explanation, writing, continuity, or skill authoring | `measured-reasoning` |
| Evaluate AI behavior, context reliability, or source conformance | `measured-ai-systems` |
| Review an agent architecture, Google ADK design, tool boundary, protocol, security model, or retrieval system | `measured-agent-platforms` |
| Deliver or review bounded SwiftUI and iOS work | `measured-swift-workflows` |
| Deliver or review bounded Next.js and React work | `measured-nextjs-workflows` |

Read the [current candidate checks](client-candidate-v0.18.0.md) before relying on a renamed pack. Historical checks are not current installation or behavior proof.

Each of the three engineering packs is under the 6,000-character warning line. That line is our own guardrail. No client publishes it as a limit. Installed together, the three packs' descriptions total 6,466 characters, which is over it. Counting skill names and paths too, the catalog estimates all three at 9,126 characters for Codex, above the 8,000 Codex uses when the context size is unknown. Install only the engineering packs your task needs. For a narrow task, pick the one skill you need and leave the other packs off.

## Experimental activation profile

`delivery-typescript-experimental` turns on seven named skills for one small TypeScript delivery task. It exists so we can compare a run that uses them against a run that does not. It is not a recommendation. Do not call it tested in a live client until reviewed records say so.

Each client has its own budget. We record what Codex does with its first skill list, including where it shortens or drops an entry. We record Claude Code's budget, cut-off, and overrides on their own. We do not claim one character limit that holds everywhere.

## Small recipes

A recipe is a suggested set of skills. It is not something you install. Do not assume a client can install a recipe by itself unless we have watched it do that.

| Work | Skills |
| --- | --- |
| Verify a completion claim | `claim-verification`, `acceptance-evidence-ledger` |
| Plan a safe code change | `problem-framing`, `implementation-planning`, `test-strategy` |
| Review a public release | `public-private-boundary-review`, `prelaunch-readiness`, `publish-change-safely` |
| Diagnose with evidence | `systematic-diagnosis`, `claim-verification` |
| Review an AI workflow | `agent-evaluation-design`, `context-reliability-review`, `source-output-conformance-audit` |
| Secure an agent system | `agent-context-state-memory-design`, `agent-tool-action-boundary-review`, `agentic-system-security-review` |
| Review a Google ADK system | `google-adk-engineering-profile`, `agent-evaluation-design`, `agentic-system-security-review` |
| Review a service release | `application-security-review`, `operational-readiness-review`, `observability-design` |
| Write a decision brief | `source-grounded-research`, `decision-governance-records`, `stakeholder-technical-communication` |
| Connect research to evaluated public findings (not measured) | `research-to-publication-lifecycle`, `source-grounded-research`, `workflow-retrospective` |
| Learn after launch | `iteration-postlaunch-learning`, `kpi-outcome-measurement`, `production-incident-analysis` |

We measure ten of the eleven recipes on this page. Each measured recipe has to stay under 8,000 characters of description text, and the validator fails if a measurement is out of date or a recipe runs over. The recipe marked "not measured" has no recorded size yet.

## Add a stack profile only when the repository needs it

Use `cross-stack-quality-gates` to find the commands a repository really uses. Add the matching stack profile when you need judgment about that language or platform. A profile does not replace the repository's own scripts, lockfiles, CI, or platform records.

## Add agent-platform skills only for agent work

Use `measured-agent-platforms` when you are designing or reviewing an agent system in ChatGPT, Codex, Claude, or Antigravity CLI. Gemini CLI is an enterprise-only compatibility surface after Google's transition of individual users to Antigravity CLI. This pack is not a runtime bundle for a hosted agent.

Read [Google agent surfaces](google-agent-surfaces.md), [Google ADK](google-adk.md), and [Agent platform boundaries](agent-platform-boundaries.md) before using those workflows in a Google agent project.

## Check how a skill gets picked, and how mature it is

You have to pick an explicit-only skill yourself. Picking it starts the workflow. It does not grant permission to push, merge, publish, deploy, delete, or write to an outside system.

Use [`catalog/skills.json`](../catalog/skills.json) to check how a skill gets picked, how risky it is, how mature it is, what pairs well with it, and where it may collide with another skill. Use [`catalog/evidence.json`](../catalog/evidence.json) for what we have actually seen in a live client. These are two different claims. A workflow can be mature and still have no live record.

## Primary resources

- [OpenAI skill-building guide](https://learn.chatgpt.com/docs/build-skills)
- [Agent Skills specification](https://agentskills.io/specification)
- [Google's Gemini CLI to Antigravity CLI transition](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/)
- [Antigravity Agent Skills](https://antigravity.google/docs/skills/)
