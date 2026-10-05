# Measured Skills Cheatsheet

Use this page to find a skill fast. The catalog contains 86 skills in 11 packs. Each row names one skill, says what it does, and says how it gets picked.

The [glossary](glossary.md) defines the words on this page. To install a pack, read [How to Use Measured Skills](README.md). For a longer write-up of each skill, read the [Skill Catalog Reader Guide](skill-catalog-reader-guide.md).

## How skills get picked

- `Implicit`: the client may pick this skill on its own when your request matches what it does. You can also pick it yourself.
- `Explicit-only`: you have to pick this skill yourself. Picking it does not grant permission to push, merge, delete, publish, deploy, or use a credential. Those still need your approval.

Here is how you pick a skill yourself in each client.

| Client | Form |
| --- | --- |
| ChatGPT | Type `@`, then select the installed skill. |
| Codex | Use `$plugin-name:skill-name`. |
| Claude Code | Use `/plugin-name:skill-name`. |
| Claude.ai | Ask in plain words. We have not confirmed that you can pick an explicit-only skill here. |

## Core: measured-skills

Use this pack to check claims, research a question, find the cause of a problem, map who owns what data, and review what is safe to publish.

| Skill | What it does | Invocation |
| --- | --- | --- |
| `authority-boundary-review` | Maps authoritative stores, writers, readers, projections, custody, and reconciliation paths. | Implicit |
| `claim-verification` | Checks whether claims such as complete, fixed, merged, deployed, or live have current evidence. | Implicit |
| `cross-stack-quality-gates` | Discovers and runs the validation commands defined by the repository instead of assuming universal commands. | Implicit |
| `finding-consolidation` | Merges findings from several completed reviews into one owned, ranked list. | Implicit |
| `prelaunch-readiness` | Reviews repository, provider, deployment, and live evidence before a public launch. | Implicit |
| `public-private-boundary-review` | Finds secrets, private details, proprietary material, and unsupported public claims before publication. | Implicit |
| `publish-change-safely` | Verifies identity, repository, remote, branch, diff, checks, push, and pull request state. | Explicit-only |
| `research-to-publication-lifecycle` | Connects research, forecasts, observations, evaluations, retrospectives, corrections, and public-safe findings. | Explicit-only |
| `skill-import-provenance` | Gates owned original skill transfers and rejects third-party catalog material as an implementation source. | Explicit-only |
| `skill-security-review` | Audits skills and plugins for unsafe instructions, permissions, dependencies, hooks, and data exposure. | Implicit |
| `source-grounded-research` | Researches current questions with primary sources, URLs, dates, provenance, and uncertainty. | Implicit |
| `systematic-diagnosis` | Reproduces and narrows a defect to establish a causal boundary without silently implementing a fix. | Implicit |

## Engineering build: measured-engineering-build

| Skill | Purpose | Invocation |
| --- | --- | --- |
| `implementation-planning` | Produces a decision-complete plan with interfaces, steps, tests, rollout controls, and stopping conditions. | Implicit |
| `module-interface-design` | Designs smaller, clearer, and more stable module boundaries, vocabulary, and contracts. | Implicit |
| `problem-framing` | Defines users, outcomes, evidence, constraints, unknowns, options, and measurable success before implementation. | Implicit |
| `test-driven-change` | Guides behavioral changes through red, green, refactor, and documented exception evidence. | Implicit |
| `test-strategy` | Selects risk-proportionate unit, integration, contract, end-to-end, property, migration, and manual tests. | Implicit |

## Engineering review: measured-engineering-review

| Skill | Purpose | Invocation |
| --- | --- | --- |
| `accessibility-review` | Reviews semantics, keyboard use, assistive technology needs, and visual presentation against WCAG 2.2. | Implicit |
| `api-contract-compatibility-review` | Checks API, event, schema, and client changes for backward, forward, and rollout compatibility. | Implicit |
| `application-security-review` | Reviews authentication, authorization, input handling, data protection, sessions, configuration, and abuse risks. | Implicit |
| `code-change-review` | Reviews an exact diff for correctness, regressions, security, compatibility, test quality, and maintainability. | Implicit |
| `data-migration-readiness` | Reviews migration authority, sequencing, compatibility, reconciliation, rollback, and operational evidence. | Implicit |
| `dependency-supply-chain-review` | Reviews dependencies, lockfiles, registries, CI actions, artifacts, provenance, and compromise risk. | Implicit |
| `functional-motion-review` | Checks whether motion clarifies a reader task while preserving evidence, accessibility, and user control. | Implicit |
| `observability-design` | Designs logs, metrics, traces, alerts, and user-impact signals around operational decisions. | Implicit |
| `operational-readiness-review` | Reviews monitoring, capacity, failure handling, runbooks, recovery, incidents, and support ownership. | Implicit |
| `performance-scalability-diagnosis` | Diagnoses latency, throughput, resource use, contention, and capacity problems from measurements. | Implicit |
| `test-quality-review` | Checks whether tests have meaningful assertions, defect sensitivity, isolation, determinism, and risk coverage. | Implicit |

## Engineering delivery: measured-engineering-delivery

| Skill | Purpose | Invocation |
| --- | --- | --- |
| `acceptance-evidence-ledger` | Tracks substantial work against current evidence, freshness, blockers, and visible abandonments. | Explicit-only |
| `finish-development-branch` | Presents evidence-based pull request, merge, retention, and cleanup choices for a development branch. | Explicit-only |
| `merge-conflict-reconciliation` | Reconciles merge, rebase, or cherry-pick conflicts while preserving both sides' intent. | Explicit-only |
| `multi-agent-orchestration` | Coordinates authorized, independent tasks with ownership, evidence contracts, cost awareness, and reconciliation. | Explicit-only |
| `plan-execution` | Executes a named approved plan with checkpoints, validation, deviation tracking, and stopping boundaries. | Explicit-only |
| `prototype-spike` | Builds a bounded disposable experiment to answer one technical uncertainty. | Explicit-only |
| `request-code-review` | Prepares an evidence-bounded review packet and sends it only with separate authorization. | Explicit-only |
| `respond-to-code-review` | Verifies review feedback against current code, tests, contracts, and authority before acting on it. | Implicit |
| `worktree-isolation` | Assesses whether dirty or concurrent Git work should be isolated before worktree changes are authorized. | Implicit |

## Stack profiles: measured-stack-profiles

Add one of these only after you know the commands and tools the repository actually uses.

| Skill | What it does | Invocation |
| --- | --- | --- |
| `adobe-aem-engineering-profile` | Adds focused guidance for AEM product generations, Sling and OSGi, content packages, Dispatcher, caching, compatibility, and builds. | Implicit |
| `csharp-dotnet-engineering-profile` | Adds focused guidance for .NET projects, async behavior, dependency injection, Entity Framework, packages, compatibility, and builds. | Implicit |
| `go-engineering-profile` | Adds focused guidance for Go modules, packages, concurrency, APIs, tests, dependencies, and builds. | Implicit |
| `java-spring-engineering-profile` | Adds focused guidance for JVM toolchains, concurrency, Spring configuration and transactions, tests, dependencies, and builds. | Implicit |
| `php-drupal-engineering-profile` | Adds focused guidance for PHP, Composer, Drupal extensions, entities, configuration, caching, tests, and builds. | Implicit |
| `postgresql-sql-engineering-profile` | Adds focused guidance for schemas, queries, transactions, indexes, migrations, and database testing. | Implicit |
| `python-engineering-profile` | Adds focused guidance for packaging, typing, asynchronous behavior, tests, dependencies, and builds. | Implicit |
| `salesforce-apex-engineering-profile` | Adds focused guidance for Salesforce metadata, Apex, LWC, permissions, governor limits, tests, and org evidence boundaries. | Implicit |
| `swift-swiftui-engineering-profile` | Adds focused guidance for Swift concurrency, SwiftUI state, tests, compatibility, and Apple builds. | Implicit |
| `terraform-engineering-profile` | Adds focused guidance for modules, providers, state, plans, upgrades, and infrastructure review. | Implicit |
| `typescript-javascript-engineering-profile` | Adds focused guidance for type safety, asynchronous behavior, tests, dependencies, and browser or Node builds. | Implicit |

## Operations: measured-operations

Use this pack for requirements, decisions, measurement, adoption, and incidents.

| Skill | What it does | Invocation |
| --- | --- | --- |
| `change-adoption-planning` | Plans the people, behavior, capability, incentives, support, measurement, and feedback needed for change. | Implicit |
| `cross-capability-dependency-mapping` | Maps dependencies across products, teams, data, platforms, decisions, and operating capabilities. | Implicit |
| `data-authority-migration-ratification` | Prepares authority, cutover, reconciliation, rollback, and acceptance evidence for a decision owner. | Implicit |
| `decision-governance-records` | Records decision context, options, evidence, ownership, status, consequences, and review triggers. | Implicit |
| `iteration-postlaunch-learning` | Uses observed behavior, incidents, feedback, experiments, and measures to decide what changes next. | Implicit |
| `kpi-outcome-measurement` | Defines outcomes with units, populations, baselines, targets, data authority, and decision use. | Implicit |
| `production-incident-analysis` | Reconstructs incidents from timestamped evidence and identifies justified learning without manufacturing blame. | Implicit |
| `requirements-synthesis` | Converts interviews, documents, issues, observations, and constraints into traceable requirements. | Implicit |
| `stakeholder-technical-communication` | Explains technical evidence for a named stakeholder decision without hiding risk or uncertainty. | Implicit |
| `value-attribution-evidence-maturity` | Distinguishes observations, estimates, contribution, attribution, and causal value claims. | Implicit |
| `workshop-planning-synthesis` | Plans decision-focused workshops and records evidence, decisions, actions, and unresolved questions. | Implicit |

## Reasoning: measured-reasoning

Use this pack to agree on scope, explain code, weigh the impact of a change, write clearly, and hand work off.

| Skill | What it does | Invocation |
| --- | --- | --- |
| `alignment-interview` | Establishes shared understanding by inspecting evidence and asking one material question at a time. | Implicit |
| `change-impact-analysis` | Traces change effects across callers, contracts, storage, jobs, clients, security, rollout, and operations. | Implicit |
| `codebase-explanation` | Explains current code through entry points, ownership, control flow, data flow, state, interfaces, and failures. | Implicit |
| `decision-evidence-trace` | Maintains an auditable decision log without storing hidden reasoning, secrets, or raw transcripts. | Explicit-only |
| `design-rationale-investigation` | Investigates why a design exists using history, current behavior, constraints, and competing hypotheses. | Implicit |
| `domain-vocabulary-modeling` | Builds a proposed vocabulary of concepts, definitions, relationships, invariants, authorities, and contradictions. | Implicit |
| `guided-configuration` | Guides a person through protected configuration steps and verifies each observable result. | Explicit-only |
| `high-signal-technical-writing` | Makes technical writing clearer, more specific, less repetitive, and easier to act on without changing its meaning. | Implicit |
| `portable-skill-authoring` | Designs portable skills with precise routing, invocation policy, provenance, security boundaries, and evaluations. | Implicit |
| `task-handoff` | Creates a continuation record with revisions, evidence, decisions, blockers, and authority boundaries. | Explicit-only |
| `workflow-retrospective` | Reviews completed work to identify what helped, what failed, and which bounded improvement to test next. | Explicit-only |

## AI systems: measured-ai-systems

Use this pack to test how an AI system behaves, check whether its context is reliable, and confirm that its output matches its sources.

| Skill | What it does | Invocation |
| --- | --- | --- |
| `agent-evaluation-design` | Defines representative cases, baselines, configurations, graders, errors, thresholds, cost, latency, human review, and limits for an AI evaluation. | Implicit |
| `context-reliability-review` | Reviews context assertions for provenance, authority, time, freshness, permissions, conflict, supersession, and revocation. | Implicit |
| `source-output-conformance-audit` | Audits exact source identity through extraction, validation, isolated persistence, and readback with mutation-sensitive evidence. | Implicit |

## Agent platforms: measured-agent-platforms

Use this pack when you are designing or reviewing an agent system. It is not a runtime bundle. It grants no tools and no deployment authority.

| Skill | What it does | Invocation |
| --- | --- | --- |
| `agent-context-state-memory-design` | Designs context, session, state, memory, artifact, identity, retention, isolation, and poisoning boundaries. | Implicit |
| `agent-protocol-interoperability-review` | Reviews exact-version A2A, MCP, and agent protocol compatibility, identity, delegation, lifecycle, and failure semantics. | Implicit |
| `agent-tool-action-boundary-review` | Reviews registered tools, identity, permissions, arguments, network reach, effects, approval, replay, and recovery. | Implicit |
| `agentic-system-security-review` | Reviews agent identity, tools, memory, retrieval, delegation, protocols, supply chain, outputs, resources, and stopping controls. | Implicit |
| `google-adk-engineering-profile` | Reviews an exact-version Google ADK design and routes focused security, evaluation, context, retrieval, and operations questions. | Implicit |
| `retrieval-grounding-quality-review` | Reviews corpus authority, access isolation, retrieval metrics, claim support, citations, abstention, poisoning, and injection. | Implicit |

## Quick selection by need

| If you need to... | Start with... |
| --- | --- |
| Verify whether work is actually complete or live | `claim-verification` |
| Research a current technical question | `source-grounded-research` |
| Connect research to a traceable public finding | `research-to-publication-lifecycle` |
| Diagnose a defect without immediately changing code | `systematic-diagnosis` |
| Clarify a vague request | `problem-framing` or `alignment-interview` |
| Turn an approved direction into executable steps | `implementation-planning` |
| Execute an approved plan | `plan-execution` |
| Track a substantial implementation against current acceptance evidence | `acceptance-evidence-ledger` |
| Review a diff | `code-change-review` |
| Decide what tests are needed | `test-strategy` |
| Review whether existing tests are meaningful | `test-quality-review` |
| Design a comparative AI-agent evaluation | `agent-evaluation-design` |
| Review whether AI context is current and authorized | `context-reliability-review` |
| Prove source-to-readback field fidelity | `source-output-conformance-audit` |
| Check a change's downstream effects | `change-impact-analysis` |
| Explain an unfamiliar codebase | `codebase-explanation` |
| Check application security | `application-security-review` |
| Check an agent skill or plugin for security risks | `skill-security-review` |
| Review the security of a complete agentic system | `agentic-system-security-review` |
| Review an agent tool that can read sensitive data or cause an effect | `agent-tool-action-boundary-review` |
| Review a Google ADK architecture | `google-adk-engineering-profile` |
| Review retrieval and grounding quality | `retrieval-grounding-quality-review` |
| Prepare a safe repository publication | `publish-change-safely` |
| Prevent private details from entering public work | `public-private-boundary-review` |
| Prepare requirements from several sources | `requirements-synthesis` |
| Record a decision and its evidence | `decision-governance-records` |
| Explain technical evidence to a stakeholder | `stakeholder-technical-communication` |
| Improve technical documentation | `high-signal-technical-writing` |
| Continue work in another session or client | `task-handoff` |

## Next.js workflows: measured-nextjs-workflows

| Skill | Purpose | Invocation |
| --- | --- | --- |
| `nextjs-cache-auth-boundary-review` | Review Next.js authorization and cache boundaries across reads, server mutations, cookies, invalidation, and user-specific data. Read-only; do not trigger for unrelated UI, installing authentication, or enabling Cache Components without a requirement. | Implicit |
| `nextjs-feature-delivery` | Deliver an explicitly requested Next.js App Router feature within approved routes and files using installed-version documentation. Use for bounded implementation and repository gates; do not trigger for read-only audits or adding infrastructure without a product requirement. | Explicit-only |
| `react-rendering-performance-diagnosis` | Diagnose React rendering or request-waterfall costs using an observed interaction, profiler evidence, and actual server/client boundaries. Read-only; do not trigger for speculative blanket memoization, styling, or unmeasured speed claims. | Implicit |

## Swift workflows: measured-swift-workflows

| Skill | Purpose | Invocation |
| --- | --- | --- |
| `ios-journey-verification` | Verify an explicitly named iOS user journey with deterministic fixtures, selected schemes, and observable acceptance steps. Use for bounded test execution; do not trigger for inferred live-data journeys, broad simulator resets, or claims of physical-device inference. | Explicit-only |
| `swift-concurrency-diagnosis` | Diagnose Swift actor isolation, Sendable diagnostics, task lifetime, cancellation, or reentrancy using actual compiler settings. Read-only; do not trigger for formatting, ordinary synchronous logic, or implementation without a concurrency question. | Implicit |
| `swift-persistence-contract-review` | Review Swift persistence mutation authority, SwiftData model identity, deletion, migration compatibility, or synchronization contracts. Read-only; do not trigger for visual styling, generic database advice, or executing a migration. | Implicit |
| `swiftui-feature-delivery` | Deliver an explicitly requested SwiftUI feature within approved files and targets. Use for bounded implementation with state ownership, availability, accessibility, and test evidence; do not trigger for read-only review or generic Swift questions. | Explicit-only |

## Safety reminder

A skill guides workflow and judgment. It does not replace repository protections, host permissions, tests, access controls, or human approval. Keep local, committed, pushed, reviewed, merged, deployed, and live states separate.
