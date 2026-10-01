# Measured Skills Catalog: A Reader Guide

The Measured Skills catalog contains 86 portable agent skills organized into 11 focused plugins. One canonical skill source produces client-specific distributions for Codex and Claude. Compatible distributions do not establish equivalent behavior across clients.

This guide explains what each plugin is for, what every skill does, and how explicit-only invocation works. It is intended for readers who want to understand the catalog before installing or using it.

## How the catalog is organized

The 11 plugins separate broad workflow categories so you can install only what you need:

1. `measured-skills` contains the core verification, research, diagnosis, security, and publication workflows.
2. `measured-engineering-build` contains problem framing, module and interface design, implementation planning, test strategy, and test-driven change workflows.
3. `measured-engineering-review` contains accessibility, API-compatibility, application-security, code-change, data-migration, dependency, motion, observability, operational-readiness, performance, and test-quality review workflows.
4. `measured-engineering-delivery` contains branch, merge-conflict, multi-agent, plan-execution, prototype, and code-review request and response workflows.
5. `measured-stack-profiles` adds focused guidance for specific programming languages and infrastructure tools.
6. `measured-operations` contains requirements, governance, measurement, adoption, incident, and stakeholder workflows.
7. `measured-reasoning` contains alignment, explanation, writing, decision, configuration, and continuity workflows.
8. `measured-ai-systems` contains optional AI evaluation, context reliability, and source-to-output conformance workflows.
9. `measured-agent-platforms` contains human-facing Google ADK, agent architecture, tool, protocol, security, and retrieval workflows.
10. `measured-swift-workflows` contains bounded SwiftUI delivery, concurrency diagnosis, persistence review, and fixture-backed journey verification.
11. `measured-nextjs-workflows` contains bounded Next.js delivery, cache and authorization review, and measured React rendering diagnosis.

The counts, groupings, and invocation policies below are reconciled against the [canonical skill sources](../skills/) and the catalog's [metadata parser](../scripts/cataloglib.py). Generated plugin trees are projections, not the inventory authority.

| Plugin | Skill count | Explicit-only skills |
| --- | ---: | --- |
| `measured-skills` | 12 | `publish-change-safely`, `research-to-publication-lifecycle`, `skill-import-provenance` |
| `measured-engineering-build` | 5 | None |
| `measured-engineering-review` | 11 | None |
| `measured-engineering-delivery` | 9 | `acceptance-evidence-ledger`, `finish-development-branch`, `merge-conflict-reconciliation`, `multi-agent-orchestration`, `plan-execution`, `prototype-spike`, `request-code-review` |
| `measured-stack-profiles` | 11 | None |
| `measured-operations` | 11 | None |
| `measured-reasoning` | 11 | `decision-evidence-trace`, `guided-configuration`, `task-handoff`, `workflow-retrospective` |
| `measured-ai-systems` | 3 | None |
| `measured-agent-platforms` | 6 | None |
| `measured-nextjs-workflows` | 3 | `nextjs-feature-delivery` |
| `measured-swift-workflows` | 4 | `ios-journey-verification`, `swiftui-feature-delivery` |
| **Total** | **86** | **17 skills** |

Most skills can activate implicitly when a request clearly matches their routing description. Skills marked `explicit-only` must be selected directly.

## What explicit-only means

An explicit-only skill requires direct selection. Verify the receiving client's invocation controls before enabling it; unverified surfaces must keep it unavailable. A metadata field or discovery check alone does not establish enforcement.

| Client surface | Verified selection form |
| --- | --- |
| ChatGPT web, desktop, and mobile | Type `@` and select the installed skill. The displayed selector entry can vary by installation and client version. |
| Codex CLI and IDE extension | `$measured-engineering-delivery:plan-execution Execute the approved plan. Stop if its scope or authority changes.` |
| Claude Code CLI and the Code area in Claude Desktop | `/measured-engineering-delivery:plan-execution Execute the approved plan. Stop if its scope or authority changes.` |
| Claude.ai | No direct command is claimed. Anthropic documents enabling an uploaded custom skill and automatic selection from a matching request; current catalog evidence does not establish explicit-only behavior on this surface. |

OpenAI documents `@` selection in ChatGPT and `$` skill mentions in Codex. Anthropic documents `/plugin-name:skill-name` for Claude Code plugin skills. The exact catalog namespaces above are also present in the generated Codex and Claude distributions. See [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills), [Anthropic Extend Claude with skills](https://code.claude.com/docs/en/slash-commands), and [Anthropic Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

Explicit-only skills coordinate work that may become consequential, such as executing a plan, publishing a repository change, creating a review request, resolving conflicts, guiding protected configuration, or delegating work to other agents.

Direct invocation selects the workflow. It does not authorize every action mentioned by that workflow. Push, merge, deletion, publication, deployment, external communication, credential use, and other protected actions still require separate authority.

## Core skills: measured-skills

The core plugin contains 12 skills for evidence, diagnosis, security, authority, and safe publication.

### authority-boundary-review

Maps authoritative data stores, exact-byte custody, projections, writers, readers, and reconciliation paths. Use it when a system or migration has unclear source-of-truth boundaries or when proposed contracts must be separated from ratified ones.

### claim-verification

Checks whether claims such as complete, fixed, merged, deployed, or live are supported by current evidence. It keeps local checks, commits, pull requests, deployments, and public behavior as separate states.

### cross-stack-quality-gates

Discovers and runs the validation commands that the repository actually defines across supported application, language, data, and infrastructure stacks without assuming that every project uses the same commands.

### finding-consolidation

Merges findings that several completed reviews already produced into one ranked list. It assigns each root cause a single owner, regrades onto one severity scale, lists every confirmed location inside one finding, and names what was held back and what no review covered. It does not run a review or issue a verdict.

### prelaunch-readiness

Reviews whether a website, service, application, or major relaunch is ready for public use. It separates repository validation from provider configuration, deployment evidence, and observed live behavior.

### public-private-boundary-review

Examines code, documentation, examples, articles, and release artifacts for secrets, internal identifiers, private operational details, proprietary material, and unsupported public claims. Use it before open-sourcing or publishing work that may combine public and private context.

### publish-change-safely

Invocation: `explicit-only`.

Verifies GitHub identity, repository, visibility, remote, branch, diff scope, checks, commit, push, and pull request state before publishing a change. Selecting the skill does not automatically authorize a push, PR, merge, or release.

### research-to-publication-lifecycle

Invocation: `explicit-only`.

Coordinates existing research, evidence-trace, source-conformance, retrospective, and public-boundary skills into stable knowledge-object handoffs. It keeps forecast cutoffs, observations, evaluations, corrections, visibility, and publication authority distinct and does not write or publish automatically.

### skill-import-provenance

Invocation: `explicit-only`.

Reviews ownership, license, revision, security posture, local changes, and re-review policy before transferring owned original skill material. Third-party skill catalogs are rejected as implementation sources and are not tracked in Git.

### skill-security-review

Audits an agent skill or plugin for prompt manipulation, unsafe commands, excessive file or network access, dependencies, hooks, permissions, data exposure, and deceptive behavior. This skill reviews agent packages, not application security.

### source-grounded-research

Researches a question using current primary sources while preserving URLs, dates, units, provenance, and uncertainty. Use it for web investigations, comparisons, recommendations, and fact checks where current evidence matters.

### systematic-diagnosis

Reproduces and narrows a defect, regression, failure, or confusing behavior to establish a causal boundary. It reports evidence and does not silently turn diagnosis into implementation.

## Engineering build: measured-engineering-build

The engineering-build plugin contains 5 skills for problem framing, module and interface design, implementation planning, and test-driven change.

### implementation-planning

Produces a decision-complete implementation plan grounded in repository and platform evidence. A plan includes interfaces, ordered steps, tests, rollout controls, checkpoints, stopping conditions, and unresolved decisions.

### module-interface-design

Designs or reviews module boundaries, vocabulary, interfaces, and hidden implementation details. Use it when callers face unstable contracts, responsibilities are unclear, or concepts leak across layers.

### problem-framing

Defines users, desired outcomes, evidence, constraints, unknowns, options, and measurable success before implementation. Use it when a request matters but the actual problem is not yet decision-ready.

### test-driven-change

Guides feature and defect work through red, green, and refactor evidence. It also provides a clear exception path when a test-first approach is unsuitable or cannot represent the behavior responsibly.

### test-strategy

Designs risk-proportionate coverage across unit, integration, contract, end-to-end, property, migration, and manual testing. It explains why each layer is or is not needed.

## Engineering review: measured-engineering-review

The engineering-review plugin contains 11 review skills for accessibility, API compatibility, application security, code changes, data migrations, dependencies, motion, observability, operational readiness, performance, and test quality.

### accessibility-review

Reviews web or application accessibility using WCAG 2.2 success criteria, semantic structure, keyboard behavior, assistive-technology needs, visual presentation, and user impact. It reports evidence without claiming full conformance from incomplete testing.

### api-contract-compatibility-review

Reviews API, event, schema, and client changes for backward, forward, and rollout compatibility. Use it when producers and consumers may update independently or when a change can alter data shape, timing, errors, or meaning.

### application-security-review

Reviews application and service security using current threat evidence and verifiable controls. It covers authentication, authorization, input handling, data protection, sessions, errors, configuration, and abuse risks.

### code-change-review

Reviews an exact diff for correctness, regressions, security, compatibility, test quality, and maintainability. It produces evidence-backed findings rather than silently changing the code under review.

### data-migration-readiness

Reviews a proposed data or schema migration for authority, compatibility, sequencing, reconciliation, rollback, and operational evidence. It can assess a migration but cannot execute or ratify it without separate authority.

### dependency-supply-chain-review

Reviews software dependencies and build inputs for provenance, integrity, maintenance, vulnerability, and compromise risk. It covers manifests, lockfiles, registries, CI actions, artifacts, and update policy.

### functional-motion-review

Checks whether motion helps a reader task while preserving evidence labels, static content, keyboard behavior, and user control. It separates WCAG requirements from stricter catalog preferences. It does not implement animation or add analytics.

### observability-design

Reviews or designs logs, metrics, traces, alerts, and user-impact signals. The goal is to help operators detect, explain, and respond to failures instead of collecting telemetry without a clear operational purpose.

### operational-readiness-review

Reviews whether a service or application is ready for release and sustained ownership. It examines objectives, dependencies, monitoring, alerts, capacity, failure handling, incidents, runbooks, recovery, and support boundaries.

### performance-scalability-diagnosis

Diagnoses latency, throughput, resource use, contention, and capacity problems using measurements and competing hypotheses. It does not silently optimize code before the cause is established.

### test-quality-review

Reviews whether tests contain meaningful assertions, detect relevant defects, remain isolated and deterministic, cover important risks, and have reasonable maintenance cost. Passing tests alone do not prove that the tests are strong.

## Engineering delivery: measured-engineering-delivery

The engineering-delivery plugin contains 9 skills for branch completion, merge-conflict reconciliation, multi-agent orchestration, plan execution, prototyping, and code-review requests and responses.

### acceptance-evidence-ledger

Invocation: `explicit-only`.

Creates or updates an inline or explicitly authorized repository-owned acceptance ledger for substantial work. It records observable gates, evidence authorities, receipts, freshness rules, blockers, abandonments, and the next authorized action without executing ledger text or expanding merge, deployment, publication, credential, provider-write, or destructive authority.

### finish-development-branch

Invocation: `explicit-only`.

Reconciles a development branch and presents evidence-based choices for creating a PR, merging, retaining the branch, or cleaning it up. It does not assume authority to push, merge, delete, or abandon work.

### merge-conflict-reconciliation

Invocation: `explicit-only`.

Reconciles an active Git merge, rebase, or cherry-pick conflict by preserving both sides' intent and validating the combined behavior. Staging, continuing, committing, and pushing remain separately authorized actions.

### multi-agent-orchestration

Invocation: `explicit-only`.

Coordinates authorized agents on independent, bounded tasks with explicit ownership, evidence contracts, cost awareness, and final reconciliation. It avoids overlapping file ownership, tightly sequential delegation, and irreversible worker decisions.

### plan-execution

Invocation: `explicit-only`.

Executes a named and approved implementation plan with checkpoints, validation, deviation tracking, and strict stopping conditions. It stops when a deviation changes scope, interfaces, authority, security, cost, publication, deployment, or destructive behavior.

### prototype-spike

Invocation: `explicit-only`.

Builds a bounded and disposable experiment to answer one named uncertainty. A successful prototype provides learning; it does not prove production readiness or authorize adoption.

### request-code-review

Invocation: `explicit-only`.

Prepares an evidence-bounded review packet containing the exact scope, validation, risks, and unresolved decisions. It sends or publishes the request only when that external action is separately authorized.

### respond-to-code-review

Evaluates review feedback against current code, tests, contracts, and authority before accepting, rejecting, or deferring it. It treats review comments as claims to verify rather than commands to follow automatically.

### worktree-isolation

Determines whether dirty or concurrent repository work should be isolated in a Git worktree. It can recommend an isolation approach, but creating, moving, repairing, locking, or removing a worktree requires explicit authority.

## Stack profiles: measured-stack-profiles

The stack-profiles plugin contains 11 optional skills. These profiles add platform- and language-specific engineering judgment after the repository's real commands and toolchain have been discovered.

### adobe-aem-engineering-profile

Provides Adobe Experience Manager guidance for product-generation discovery, Sling and OSGi, content packages, Dispatcher, caching, compatibility, and builds. Local validation remains separate from Cloud Manager, deployment, activation, and live-delivery evidence.

### csharp-dotnet-engineering-profile

Provides C# and .NET guidance for solutions and projects, asynchronous behavior, dependency injection, Entity Framework Core, packages, compatibility, and builds. It does not install tools, change dependencies, or apply migrations merely to validate a claim.

### go-engineering-profile

Provides focused Go guidance for modules, packages, concurrency, APIs, tests, dependencies, compatibility, and builds. It defers exact commands to repository evidence.

### java-spring-engineering-profile

Provides Java and Spring guidance for JVM toolchains, concurrency, dependency injection, configuration, transactions, tests, dependencies, compatibility, and builds. It preserves repository wrappers and keeps service startup and deployment separate.

### php-drupal-engineering-profile

Provides PHP and Drupal guidance for Composer projects, custom extensions, access and entity APIs, configuration, caching, tests, compatibility, and builds. Configuration import, database updates, content writes, and deployment retain separate authority.

### postgresql-sql-engineering-profile

Provides PostgreSQL and SQL guidance for schemas, queries, transactions, indexing, migrations, compatibility, and database testing. It does not mutate shared data merely to validate a claim.

### python-engineering-profile

Provides Python guidance for packaging, typing, asynchronous behavior, tests, dependencies, compatibility, and builds. It respects the repository's selected tools and configuration.

### salesforce-apex-engineering-profile

Provides Salesforce guidance for metadata projects, Apex, Lightning Web Components, permissions, governor limits, tests, package compatibility, and deployment readiness. Credentials, org-backed validation, deployment, permission assignment, and destructive changes retain separate authority.

### swift-swiftui-engineering-profile

Provides Swift and SwiftUI guidance for packages, applications, concurrency, UI state, tests, compatibility, and builds. Claims about the Apple toolchain require observed macOS evidence.

### terraform-engineering-profile

Provides Terraform guidance for modules, providers, state, plans, upgrades, compatibility, and infrastructure review. Successful validation or planning does not authorize an apply.

### typescript-javascript-engineering-profile

Provides TypeScript and JavaScript guidance for Node and browser packages, type safety, asynchronous behavior, tests, dependencies, compatibility, and builds. It follows the repository's package manager and scripts.

## Operations skills: measured-operations

The operations plugin contains 11 skills for requirements, decisions, measurement, adoption, incidents, stakeholder communication, and operating-model work.

### change-adoption-planning

Plans change around affected people, desired behavior, capability, incentives, support, measurement, and feedback. Use it when technical delivery alone will not create the intended outcome.

### cross-capability-dependency-mapping

Maps dependencies across products, teams, data, platforms, decisions, and operating capabilities. It makes hidden sequencing, ownership, authority, and failure paths visible.

### data-authority-migration-ratification

Prepares a proposed data-authority and migration decision record covering owners, writers, readers, cutover, reconciliation, rollback, and acceptance. It supports a decision owner but cannot declare the proposal ratified.

### decision-governance-records

Creates or reviews decision records containing context, options, evidence, ownership, status, consequences, and review triggers. It distinguishes proposed, ratified, rejected, superseded, and unresolved decisions.

### iteration-postlaunch-learning

Plans and synthesizes learning from observed postlaunch behavior, incidents, feedback, experiments, and outcome measures. It helps decide what to retain, change, investigate, or stop.

### kpi-outcome-measurement

Defines outcome measures with precise units, populations, baselines, targets, data authority, and decision use. It distinguishes activity, output, outcome, and impact.

### production-incident-analysis

Reconstructs a production incident from timestamped evidence, system behavior, contributing conditions, response actions, and recovery. It identifies justified learning and remediation without manufacturing certainty or blame.

### requirements-synthesis

Converts interviews, documents, issues, observations, and constraints into traceable requirements. It keeps proposals and preferences separate from ratified scope.

### stakeholder-technical-communication

Translates technical evidence for a named stakeholder and decision. It preserves uncertainty, risk, and appropriate detail while avoiding unnecessary implementation depth or unsupported confidence.

### value-attribution-evidence-maturity

Evaluates claims about value, savings, benefits, risk reduction, and outcomes against an evidence-maturity model. It separates observations, estimates, contribution, attribution, and causal claims.

### workshop-planning-synthesis

Plans a workshop around a concrete decision or learning objective and records its evidence afterward. It supports agendas, prework, facilitation, participation, decisions, actions, and follow-up without inventing consensus.

## Reasoning skills: measured-reasoning

The reasoning plugin contains 11 skills for shared understanding, code explanation, impact analysis, decision evidence, writing, configuration, and continuity.

### alignment-interview

Establishes a shared, decision-ready understanding by inspecting available evidence and asking one material question at a time. It stops when the remaining unknowns no longer prevent a responsible next decision.

### change-impact-analysis

Traces the blast radius of a proposed or completed change across callers, contracts, storage, jobs, clients, security, rollout, and operations. It uses traced dependencies rather than unsupported speculation.

### codebase-explanation

Explains how existing code works through entry points, ownership, control flow, data flow, state, interfaces, failures, and concrete files. It explains current mechanics, not unverified historical intent.

### decision-evidence-trace

Invocation: `explicit-only`.

Maintains a bounded decision and evidence trail for long-running work. It records decisions, public reasons, evidence, results, owners, and review triggers without storing hidden reasoning, secrets, raw transcripts, or unrelated activity.

### design-rationale-investigation

Investigates why code, architecture, or an operational design exists by comparing historical evidence, current behavior, constraints, and competing hypotheses. It does not infer original intent from code shape alone.

### domain-vocabulary-modeling

Builds a proposed shared vocabulary from code, documents, and stakeholder language. It records concepts, definitions, relationships, invariants, authorities, examples, and contradictions without pretending the vocabulary is ratified.

### guided-configuration

Invocation: `explicit-only`.

Guides a person through configuration that requires their account, device, approval, credential, or external interface. It verifies each observable result while leaving protected steps with the authorized person.

### high-signal-technical-writing

Edits technical prose for clarity, evidence density, specificity, rhythm, and audience fit while preserving meaning and repository voice. It removes vague, repetitive, promotional, or machine-generic wording without pretending that style proves authorship.

### portable-skill-authoring

Designs or revises a portable Agent Skill with precise routing, invocation policy, focused references, provenance, security boundaries, evaluations, and generated client adapters. It is for cross-client skill work rather than ordinary documentation.

### task-handoff

Invocation: `explicit-only`.

Creates a precise continuation record for another session, client, person, or agent. It includes exact revisions, current state, evidence, decisions, blockers, and authority boundaries so the recipient does not have to rediscover or overstate progress.

### workflow-retrospective

Invocation: `explicit-only`.

Reviews completed or paused work to identify what helped, what failed, why it happened, and which bounded improvement to test next. It does not mine private history or automatically rewrite policies and skills.

## AI systems skills: measured-ai-systems

The optional AI-systems plugin contains three reliability workflows. Install it when work concerns measured AI behavior, the reliability of context assertions, or evidence from exact source bytes through persisted readback.

### agent-evaluation-design

Designs a decision-ready evaluation contract for an agent, model-assisted workflow, or prompt-driven system. It defines representative cases, baselines, configurations, oracles, graders, error classes, thresholds, cost, latency, human review, execution authority, and limitations without launching paid or external evaluations.

### context-reliability-review

Reviews context as atomic assertions with provenance, authority, effective and recorded time, freshness, permissions, conflicts, supersession, revocation, status, and behavioral impact. It uses synthetic or redacted public output rather than embedding private facts.

### source-output-conformance-audit

Audits exact source identity through decoding, parsing or extraction, normalization, validation, write preparation, isolated persistence, and readback. It uses source-cited expected values and mutation-sensitive tests while reporting correctness, completeness, storage correctness, reproducibility, and unresolved evidence separately.

## Agent platform skills: measured-agent-platforms

The optional agent-platform plugin contains six human-facing workflows for designing and reviewing agent systems. They do not become a SaaS runtime bundle, register tools, or authorize authentication, release, infrastructure, or deployment.

### agent-context-state-memory-design

Designs or reviews prompt context, session events, scoped state, long-term memory, retrieval, and artifacts. It maps identity, authority, provenance, freshness, retention, deletion, isolation, and poisoning without treating model summaries as product truth.

### agent-protocol-interoperability-review

Reviews A2A, MCP, or another agent-facing protocol using exact specification and implementation versions. It covers discovery, identity, delegated authority, schemas, task lifecycle, streaming, failure, retry, idempotency, cancellation, and revocation.

### agent-tool-action-boundary-review

Reviews the deterministic boundary between an agent and its host-registered tools. It covers principals, permissions, schemas, arguments, data, network reach, effect classes, durable approval, replay protection, recovery, and audit evidence.

### agentic-system-security-review

Reviews an agentic system across identity, models, instructions, tools, memory, retrieval, delegation, protocols, supply chain, outputs, resource limits, revocation, and emergency stopping. It is separate from conventional application security and skill-package security.

### google-adk-engineering-profile

Reviews a Google ADK design using its exact language, package version, model, agents, tools, sessions, memory, retrieval, evaluation, and environment evidence. It treats runtime Agent Skills and tool confirmation as experimental until exact-version tests establish the required behavior.

### retrieval-grounding-quality-review

Reviews whether retrieval selects authorized, current, relevant evidence and whether generated claims remain within that evidence. It covers access isolation, retrieval metrics, claim support, citations, abstention, conflicts, poisoning, injection, and limitations.

## Choosing a skill

Start by describing the actual outcome you need. The client can use an implicitly invocable skill when the request matches its routing description.

Use direct invocation when:

- the skill is marked `explicit-only`;
- you want to guarantee that a specific workflow is selected;
- several skills have overlapping descriptions; or
- the work requires an especially clear stopping boundary.

Installing every plugin is not required. A focused installation reduces discovery overhead and lowers the chance of routing collisions.

## Important authority boundaries

The catalog coordinates judgment and workflow. It does not replace permissions, tests, repository protections, access controls, or human decisions.

Keep these states separate:

- A local change is not necessarily committed.
- A commit is not necessarily pushed.
- A pushed branch is not necessarily represented by a pull request.
- A pull request is not necessarily reviewed or merged.
- A merge is not necessarily deployed.
- A deployment is not necessarily healthy or publicly reachable.
- A prototype is not production evidence.
- A proposal is not a ratified decision.
- A worker report is not verified integration evidence.

## Further reading

- [Measured Skills repository](https://github.com/JovaniPink/measured-skills)
- [How to use the catalog](README.md)
- [Architecture](architecture.md)
- [Authoring guide](authoring.md)
- [Editorial style](editorial-style.md)
- [Security model](security-model.md)
- [Observed client evidence](manual-smoke-tests.md)
- [Agent Skills specification](https://agentskills.io/specification)
- [OpenAI skill-building documentation](https://learn.chatgpt.com/docs/build-skills)
- [OpenAI plugin documentation](https://developers.openai.com/plugins/build/plugins)
- [Claude Code skills documentation](https://code.claude.com/docs/en/slash-commands)

## Next.js workflows: measured-nextjs-workflows

### nextjs-cache-auth-boundary-review

Review Next.js authorization and cache boundaries across reads, server mutations, cookies, invalidation, and user-specific data. Read-only; do not trigger for unrelated UI, installing authentication, or enabling Cache Components without a requirement.

### nextjs-feature-delivery

Invocation: `explicit-only`.

Deliver an explicitly requested Next.js App Router feature within approved routes and files using installed-version documentation. Use for bounded implementation and repository gates; do not trigger for read-only audits or adding infrastructure without a product requirement.

### react-rendering-performance-diagnosis

Diagnose React rendering or request-waterfall costs using an observed interaction, profiler evidence, and actual server/client boundaries. Read-only; do not trigger for speculative blanket memoization, styling, or unmeasured speed claims.

## Swift workflows: measured-swift-workflows

### ios-journey-verification

Invocation: `explicit-only`.

Verify an explicitly named iOS user journey with deterministic fixtures, selected schemes, and observable acceptance steps. Use for bounded test execution; do not trigger for inferred live-data journeys, broad simulator resets, or claims of physical-device inference.

### swift-concurrency-diagnosis

Diagnose Swift actor isolation, Sendable diagnostics, task lifetime, cancellation, or reentrancy using actual compiler settings. Read-only; do not trigger for formatting, ordinary synchronous logic, or implementation without a concurrency question.

### swift-persistence-contract-review

Review Swift persistence mutation authority, SwiftData model identity, deletion, migration compatibility, or synchronization contracts. Read-only; do not trigger for visual styling, generic database advice, or executing a migration.

### swiftui-feature-delivery

Invocation: `explicit-only`.

Deliver an explicitly requested SwiftUI feature within approved files and targets. Use for bounded implementation with state ownership, availability, accessibility, and test evidence; do not trigger for read-only review or generic Swift questions.
