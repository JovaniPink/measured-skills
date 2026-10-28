# Complete skill catalog

Generated from canonical metadata. Start with [the task chooser](start.md).

This preview contains 90 portable agent skills. Packs are distribution units, not recommended activation sets.

## measured-operations

### Analyze an incident

[`analyze-incident`](../skills/analyze-incident/SKILL.md)

Analyzes an incident when asked what happened, why recovery took time, or how to prevent recurrence; builds an evidence-backed timeline without assigning unsupported blame.

Invocation: implicit. Risk class: read-only.

Historical name: production-incident-analysis.

### Explain a technical decision

[`explain-to-stakeholders`](../skills/explain-to-stakeholders/SKILL.md)

Explains technical evidence when asked for a stakeholder update, decision brief, or plain-language status; preserves the decision needed and material limitations without unnecessary approval requests.

Invocation: implicit. Risk class: read-only.

Historical name: stakeholder-technical-communication.

### Learn after launch

[`learn-after-launch`](../skills/learn-after-launch/SKILL.md)

Reviews postlaunch learning when asked what worked, what to change, or which feedback deserves investigation; uses observed outcomes rather than treating deployment as success.

Invocation: implicit. Risk class: read-only.

Historical name: iteration-postlaunch-learning.

### Map capability dependencies

[`map-capability-dependencies`](../skills/map-capability-dependencies/SKILL.md)

Maps cross-team dependencies when asked what blocks delivery, who owns an input, or which decisions must happen first; records ownership and failure paths without inventing commitments.

Invocation: implicit. Risk class: read-only.

Historical name: cross-capability-dependency-mapping.

### Measure outcomes

[`measure-outcomes`](../skills/measure-outcomes/SKILL.md)

Defines outcome measures when asked how to measure success, choose a KPI, or distinguish activity from impact; specifies population, units, baseline, and decision use.

Invocation: implicit. Risk class: read-only.

Historical name: kpi-outcome-measurement.

### Plan adoption

[`plan-adoption`](../skills/plan-adoption/SKILL.md)

Plans adoption when a new process or product needs people to change how they work; connects training, incentives, support, and feedback to observable behavior.

Invocation: implicit. Risk class: read-only.

Historical name: change-adoption-planning.

### Plan a workshop

[`plan-workshop`](../skills/plan-workshop/SKILL.md)

Plans or synthesizes a workshop when asked to prepare an agenda or turn session notes into decisions; ties activities to outcomes and leaves unresolved ownership visible.

Invocation: implicit. Risk class: read-only.

Historical name: workshop-planning-synthesis.

### Prepare a migration decision

[`prepare-migration-decision`](../skills/prepare-migration-decision/SKILL.md)

Prepares a migration decision when owners must approve data writers, cutover, reconciliation, and rollback; records a proposal and evidence without granting approval itself.

Invocation: implicit. Risk class: read-only.

Historical name: data-authority-migration-ratification.

### Record decisions and evidence

[`record-decisions`](../skills/record-decisions/SKILL.md)

Writes or reviews a decision record when asked to document options, rationale, ownership, or approval status; separates a proposal from a ratified decision.

Invocation: implicit. Risk class: read-only.

Historical name: decision-governance-records.

### Review evidence for value claims

[`review-value-evidence`](../skills/review-value-evidence/SKILL.md)

Assesses value claims when asked whether a change saved time, reduced risk, or caused an outcome; separates observed results, estimates, attribution, and unsupported conclusions.

Invocation: implicit. Risk class: read-only.

Historical name: value-attribution-evidence-maturity.

### Synthesize requirements

[`synthesize-requirements`](../skills/synthesize-requirements/SKILL.md)

Combines interviews, documents, and issues when asked to turn conflicting inputs into requirements; traces each requirement to evidence and keeps unresolved decisions visible.

Invocation: implicit. Risk class: read-only.

Historical name: requirements-synthesis.

## measured-quality

### Check launch readiness

[`check-launch-readiness`](../skills/check-launch-readiness/SKILL.md)

Reviews launch readiness when asked for a go/no-go assessment or public-launch checklist; separates source checks, provider configuration, and live user journeys.

Invocation: implicit. Risk class: bounded-execution.

Historical name: prelaunch-readiness.

### Consolidate review findings

[`consolidate-findings`](../skills/consolidate-findings/SKILL.md)

Consolidates completed reviews when findings overlap or disagree in severity; assigns each root cause one owner and reports discarded duplicates without running another review.

Invocation: implicit. Risk class: read-only.

Historical name: finding-consolidation.

### Design agent evaluations

[`design-agent-evaluations`](../skills/design-agent-evaluations/SKILL.md)

Designs AI evaluations when asked how to test an agent, compare prompts, or measure answer quality; requires representative cases and a baseline rather than one favorable response.

Invocation: implicit. Risk class: read-only.

Historical name: agent-evaluation-design.

### Design agent state and memory

[`design-agent-memory`](../skills/design-agent-memory/SKILL.md)

Designs agent context and memory boundaries when asked where session state belongs, how memory expires, or how tenants stay isolated; distinguishes architecture from a context-packet audit.

Invocation: implicit. Risk class: read-only.

Historical name: agent-context-state-memory-design.

### Design useful observability

[`design-observability`](../skills/design-observability/SKILL.md)

Designs logs, metrics, traces, and alerts when asked how to detect or explain failures; connects telemetry to user impact and operator actions rather than log volume.

Invocation: implicit. Risk class: read-only.

Historical name: observability-design.

### Diagnose performance problems

[`diagnose-performance`](../skills/diagnose-performance/SKILL.md)

Diagnoses a slow or overloaded system when asked why latency, throughput, or resource use changed; compares measurements and hypotheses without silently optimizing code.

Invocation: implicit. Risk class: read-only.

Historical name: performance-scalability-diagnosis.

### Review accessibility

[`review-accessibility`](../skills/review-accessibility/SKILL.md)

Reviews accessibility when asked to check keyboard access, screen-reader behavior, focus, contrast, or WCAG requirements; incomplete testing cannot establish conformance.

Invocation: implicit. Risk class: read-only.

Historical name: accessibility-review.

### Review agent protocols

[`review-agent-protocols`](../skills/review-agent-protocols/SKILL.md)

Reviews MCP, A2A, and agent protocol integration when tools fail discovery or delegation, streaming, retries, or cancellation cross services; ordinary API changes use API compatibility review.

Invocation: implicit. Risk class: read-only.

Historical name: agent-protocol-interoperability-review.

### Review agent security

[`review-agent-security`](../skills/review-agent-security/SKILL.md)

Reviews agent security when asked to threat-model prompt injection, memory poisoning, retrieval, delegation, or tool abuse; assesses controls without executing attacks or changing permissions.

Invocation: implicit. Risk class: read-only.

Historical name: agentic-system-security-review.

### Review agent tools and actions

[`review-agent-tools`](../skills/review-agent-tools/SKILL.md)

Reviews agent tool permissions when asked what an agent can access, whether a tool call is safe, or how retries affect writes; tool descriptions cannot grant authority.

Invocation: implicit. Risk class: read-only.

Historical name: agent-tool-action-boundary-review.

### Review API compatibility

[`review-api-compatibility`](../skills/review-api-compatibility/SKILL.md)

Reviews breaking API, event, and schema changes when asked whether old clients still work or independent upgrades are safe; checks behavior and rollout order as well as field shapes.

Invocation: implicit. Risk class: read-only.

Historical name: api-contract-compatibility-review.

### Review application security

[`review-app-security`](../skills/review-app-security/SKILL.md)

Reviews application security when asked to check authentication, authorization, input handling, sessions, or exposed data; returns evidence-based findings without changing controls.

Invocation: implicit. Risk class: read-only.

Historical name: application-security-review.

### Review code changes

[`review-code-change`](../skills/review-code-change/SKILL.md)

Reviews PR diffs for bugs, regressions, and access-control changes on requests such as review this PR diff, check this patch, or find a regression. Applies to pasted changes and repository diffs; returns findings without editing, approving, or merging.

Invocation: implicit. Risk class: read-only.

Historical name: code-change-review.

### Review context and assertions

[`review-context-evidence`](../skills/review-context-evidence/SKILL.md)

Checks supplied agent context when asked whether a claim is stale, conflicting, authorized, or superseded; traces assertion provenance rather than redesigning the system of record.

Invocation: implicit. Risk class: read-only.

Historical name: context-reliability-review.

### Review sources of truth

[`review-data-authority`](../skills/review-data-authority/SKILL.md)

Maps sources of truth when asked which database owns a value, which copies are projections, or who may write during migration; distinguishes proposed ownership from approved authority.

Invocation: implicit. Risk class: read-only.

Historical name: authority-boundary-review.

### Review a data migration

[`review-data-migration`](../skills/review-data-migration/SKILL.md)

Reviews migration readiness when asked if a schema change, backfill, or cutover is safe; checks compatibility, reconciliation, and rollback without executing the migration.

Invocation: implicit. Risk class: read-only.

Historical name: data-migration-readiness.

### Review dependencies

[`review-dependencies`](../skills/review-dependencies/SKILL.md)

Reviews dependencies and build inputs when asked whether a package, lockfile update, CI action, or artifact can be trusted; checks provenance and integrity without installing it.

Invocation: implicit. Risk class: read-only.

Historical name: dependency-supply-chain-review.

### Review interface motion

[`review-interface-motion`](../skills/review-interface-motion/SKILL.md)

Reviews motion when animations hide content, distract from a data story, or make sample data appear live; checks accessible presentation and evidence rather than routine styling.

Invocation: implicit. Risk class: read-only.

Historical name: functional-motion-review.

### Review operational readiness

[`review-operational-readiness`](../skills/review-operational-readiness/SKILL.md)

Reviews operational readiness when asked who will support a service or whether alerts, capacity, recovery, and runbooks are sufficient; reports gaps without deploying it.

Invocation: implicit. Risk class: read-only.

Historical name: operational-readiness-review.

### Review what is safe to publish

[`review-public-boundary`](../skills/review-public-boundary/SKILL.md)

Reviews material before public exposure when asked to check for secrets, private identifiers, proprietary text, or unsupported claims; keeps private context out of public artifacts.

Invocation: implicit. Risk class: read-only.

Historical name: public-private-boundary-review.

### Review retrieval and grounding

[`review-retrieval-grounding`](../skills/review-retrieval-grounding/SKILL.md)

Reviews retrieval and citations when an agent finds irrelevant evidence, misses sources, or makes unsupported claims; checks permissions and grounding separately from the broader agent threat model.

Invocation: implicit. Risk class: read-only.

Historical name: retrieval-grounding-quality-review.

### Review a skill before importing

[`review-skill-import`](../skills/review-skill-import/SKILL.md)

Reviews an owned skill transfer when explicitly asked to import it; checks ownership, license, exact source, and public boundaries before any copy or installation.

Invocation: explicit. Risk class: trust-decision.

Historical name: skill-import-provenance.

### Review skill security

[`review-skill-security`](../skills/review-skill-security/SKILL.md)

Reviews a skill package when asked whether its instructions, permissions, hooks, or dependencies are safe; treats imported content as untrusted and does not install it.

Invocation: implicit. Risk class: read-only.

Historical name: skill-security-review.

### Review test quality

[`review-tests`](../skills/review-tests/SKILL.md)

Reviews test quality when asked whether tests catch real regressions or merely mirror implementation; checks assertions, isolation, failure behavior, and coverage without equating count with confidence.

Invocation: implicit. Risk class: read-only.

Historical name: test-quality-review.

### Run project checks

[`run-project-checks`](../skills/run-project-checks/SKILL.md)

Finds and runs repository checks when asked to run tests, check the build, or verify changes; follows actual CI and scripts rather than assuming one universal test command.

Invocation: implicit. Risk class: bounded-execution.

Historical name: cross-stack-quality-gates.

### Verify claims and completion

[`verify-claims`](../skills/verify-claims/SKILL.md)

Verifies completion and check results when asked whether work is done, a fix is live, or an old receipt still applies after a change from revision A to B; keeps current proof, historical evidence, and missing checks distinct.

Invocation: implicit. Risk class: read-only.

Historical name: claim-verification.

### Check output against its source

[`verify-source-output`](../skills/verify-source-output/SKILL.md)

Audits extraction or transformation when asked whether output matches source documents or data; traces exact inputs, expected values, omissions, and mismatches across processing stages.

Invocation: implicit. Risk class: bounded-execution.

Historical name: source-output-conformance-audit.

## measured-stacks

### Deliver a Next.js feature

[`deliver-nextjs-feature`](../skills/deliver-nextjs-feature/SKILL.md)

Implements a named Next.js App Router feature when explicitly requested within approved routes and files; follows installed-version docs and repository gates without adding unrequested infrastructure.

Invocation: explicit. Risk class: bounded-execution.

Historical name: nextjs-feature-delivery.

### Deliver a SwiftUI feature

[`deliver-swiftui-feature`](../skills/deliver-swiftui-feature/SKILL.md)

Implements a named SwiftUI feature when explicitly requested within approved targets and files; follows actual SDK and state ownership and keeps missing required checks visible.

Invocation: explicit. Risk class: bounded-execution.

Historical name: swiftui-feature-delivery.

### Diagnose React rendering

[`diagnose-react-rendering`](../skills/diagnose-react-rendering/SKILL.md)

Diagnoses React rerenders or request waterfalls when an observed interaction is slow; requires profiler and boundary evidence rather than blanket memoization or speculative speed claims.

Invocation: implicit. Risk class: read-only.

Historical name: react-rendering-performance-diagnosis.

### Diagnose Swift concurrency

[`diagnose-swift-concurrency`](../skills/diagnose-swift-concurrency/SKILL.md)

Diagnoses Swift actor, Sendable, task-lifetime, and cancellation issues when compiler errors or runtime behavior indicate concurrency problems; uses exact language and isolation settings.

Invocation: implicit. Risk class: read-only.

Historical name: swift-concurrency-diagnosis.

### Review Next.js caching and access

[`review-nextjs-cache-auth`](../skills/review-nextjs-cache-auth/SKILL.md)

Reviews Next.js cache and authorization when user data leaks across requests, invalidation is unclear, or server mutations need checks; excludes unrelated UI and authentication installation.

Invocation: implicit. Risk class: read-only.

Historical name: nextjs-cache-auth-boundary-review.

### Review Swift persistence

[`review-swift-persistence`](../skills/review-swift-persistence/SKILL.md)

Reviews Swift persistence when SwiftData identity, context ownership, deletion, migration, or sync behavior is uncertain; does not assume CloudKit or authorize data mutation.

Invocation: implicit. Risk class: read-only.

Historical name: swift-persistence-contract-review.

### Adobe AEM guidance

[`stack-adobe-aem`](../skills/stack-adobe-aem/SKILL.md)

Reviews AEM code, Sling, OSGi, Dispatcher, and content packages when an Adobe Experience Manager change needs stack-specific checks; follows discovered versions and Cloud Manager authority.

Invocation: implicit. Risk class: read-only.

Historical name: adobe-aem-engineering-profile.

### C# and .NET guidance

[`stack-csharp-dotnet`](../skills/stack-csharp-dotnet/SKILL.md)

Reviews C# and .NET changes when ASP.NET, Entity Framework, async code, packages, or target frameworks need focused checks; follows repository SDK and build contracts.

Invocation: implicit. Risk class: read-only.

Historical name: csharp-dotnet-engineering-profile.

### GCP data guidance

[`stack-gcp-data`](../skills/stack-gcp-data/SKILL.md)

Reviews BigQuery query plans and dbt/Dataform incremental models for partition pruning, late corrections, and data contracts, including supplied snippets without cloud access. Also reviews Dataflow, Spark, and Airflow pipelines; excludes generic SQL questions and does not authorize provider execution or spend.

Invocation: implicit. Risk class: read-only.

Historical name: gcp-data-engineering-profile.

### Go guidance

[`stack-go`](../skills/stack-go/SKILL.md)

Reviews Go changes when goroutines, modules, APIs, dependencies, or tests need language-specific checks; follows repository toolchain and gate definitions.

Invocation: implicit. Risk class: read-only.

Historical name: go-engineering-profile.

### Google ADK guidance

[`stack-google-adk`](../skills/stack-google-adk/SKILL.md)

Reviews Google ADK architecture when asked about sessions, tools, models, evaluations, or deployment compatibility; checks exact versions and does not equate framework defaults with safety.

Invocation: implicit. Risk class: read-only.

Historical name: google-adk-engineering-profile.

### Java and Spring guidance

[`stack-java-spring`](../skills/stack-java-spring/SKILL.md)

Reviews Java and Spring changes when transactions, concurrency, services, dependencies, or JVM compatibility need focused checks; follows repository wrappers and toolchains.

Invocation: implicit. Risk class: read-only.

Historical name: java-spring-engineering-profile.

### PHP and Drupal guidance

[`stack-php-drupal`](../skills/stack-php-drupal/SKILL.md)

Reviews PHP and Drupal changes when modules, themes, entities, caching, or configuration need focused checks; follows Composer locks, repository tests, and supported versions.

Invocation: implicit. Risk class: read-only.

Historical name: php-drupal-engineering-profile.

### PostgreSQL and SQL guidance

[`stack-postgresql-sql`](../skills/stack-postgresql-sql/SKILL.md)

Reviews PostgreSQL schemas, queries, indexes, transactions, and migrations when database changes need focused checks; does not mutate shared data merely to validate a proposal.

Invocation: implicit. Risk class: read-only.

Historical name: postgresql-sql-engineering-profile.

### Python guidance

[`stack-python`](../skills/stack-python/SKILL.md)

Reviews Python changes when typing, async code, packaging, dependencies, or tests need focused checks; follows discovered Python versions and repository commands.

Invocation: implicit. Risk class: read-only.

Historical name: python-engineering-profile.

### Salesforce and Apex guidance

[`stack-salesforce-apex`](../skills/stack-salesforce-apex/SKILL.md)

Reviews Salesforce Apex changes when governor limits, bulk processing, triggers, sharing, or tests need focused checks; keeps deployment and org writes separately authorized.

Invocation: implicit. Risk class: read-only.

Historical name: salesforce-apex-engineering-profile.

### Swift and SwiftUI guidance

[`stack-swift-swiftui`](../skills/stack-swift-swiftui/SKILL.md)

Reviews Swift and SwiftUI changes when state, identity, layout, concurrency, or SDK compatibility need focused checks; separates compiler, simulator, device, and release evidence.

Invocation: implicit. Risk class: read-only.

Historical name: swift-swiftui-engineering-profile.

### Terraform guidance

[`stack-terraform`](../skills/stack-terraform/SKILL.md)

Reviews Terraform changes when plans, state, modules, providers, or drift need focused checks; discovers backend and version constraints without applying or changing shared infrastructure.

Invocation: implicit. Risk class: read-only.

Historical name: terraform-engineering-profile.

### TypeScript and JavaScript guidance

[`stack-typescript-javascript`](../skills/stack-typescript-javascript/SKILL.md)

Reviews TypeScript and JavaScript changes when async code, modules, types, dependencies, or builds need focused checks; uses repository runtimes, lockfiles, and commands.

Invocation: implicit. Risk class: read-only.

Historical name: typescript-javascript-engineering-profile.

### Verify an iOS journey

[`verify-ios-journey`](../skills/verify-ios-journey/SKILL.md)

Verifies a named iOS journey when explicitly asked to run fixture-based acceptance steps on selected schemes; excludes inferred live-data journeys, device claims, and broad simulator resets.

Invocation: explicit. Risk class: bounded-execution.

Historical name: ios-journey-verification.

## measured-workflows

### Address review findings

[`address-review`](../skills/address-review/SKILL.md)

Evaluates reviewer comments when asked to address feedback or decide whether a requested fix is valid; checks current code and tests before accepting, rejecting, or deferring it.

Invocation: implicit. Risk class: bounded-execution.

Historical name: respond-to-code-review.

### Agree on the decisions

[`align-on-decisions`](../skills/align-on-decisions/SKILL.md)

Clarifies an underspecified request when the desired result, constraints, or success criteria are unclear; asks only material questions and does not reopen settled decisions.

Invocation: implicit. Risk class: read-only.

Historical name: alignment-interview.

### Assess the impact of a change

[`assess-change-impact`](../skills/assess-change-impact/SKILL.md)

Traces a change's blast radius when asked what might break, which callers depend on it, or what else needs updating; separates traced dependencies from hypotheses.

Invocation: implicit. Risk class: read-only.

Historical name: change-impact-analysis.

### Choose a safe worktree

[`assess-worktree-isolation`](../skills/assess-worktree-isolation/SKILL.md)

Assesses checkout isolation when concurrent edits or dirty files may collide with a new task; reuses safe worktrees and preserves unrelated work rather than creating or deleting blindly.

Invocation: implicit. Risk class: bounded-execution.

Historical name: worktree-isolation.

### Author a portable skill

[`author-skill`](../skills/author-skill/SKILL.md)

Authors portable skills when asked to create or revise SKILL.md workflows and client distributions; preserves routing, provenance, and invocation controls rather than treating ordinary docs as skills.

Invocation: implicit. Risk class: bounded-execution.

Historical name: portable-skill-authoring.

### Build a focused prototype

[`build-spike`](../skills/build-spike/SKILL.md)

Runs an isolated technical experiment when explicitly asked to test feasibility or answer an implementation uncertainty; disposable evidence does not authorize production adoption.

Invocation: explicit. Risk class: bounded-execution.

Historical name: prototype-spike.

### Choose a workflow

[`choose-workflow`](../skills/choose-workflow/SKILL.md)

Suggests a workflow when a user asks which skill to use, where to start, or how to finish existing work. Returns a route, context needs, and a copyable prompt without executing it.

Invocation: implicit. Risk class: read-only.

Historical name: new in 0.19.

### Coordinate authorized agents

[`coordinate-agents`](../skills/coordinate-agents/SKILL.md)

Coordinates delegated work when explicitly asked for independent workers or a bounded reviewer; defines ownership, evidence, and budgets without duplicating edits or delegating irreversible decisions.

Invocation: explicit. Risk class: bounded-execution.

Historical name: multi-agent-orchestration.

### Design a module interface

[`design-module-interface`](../skills/design-module-interface/SKILL.md)

Designs module boundaries when asked to untangle coupling, simplify an API, or clarify ownership; makes caller contracts concrete before implementation.

Invocation: implicit. Risk class: read-only.

Historical name: module-interface-design.

### Design web motion

[`design-web-motion`](../skills/design-web-motion/SKILL.md)

Designs web motion when asked to animate a design, plan an interaction, or create a product showcase. Specifies choreography, state, responsive behavior, and static alternatives; does not implement or publish.

Invocation: implicit. Risk class: read-only.

Historical name: new in 0.19.

### Diagnose a failure

[`diagnose-failure`](../skills/diagnose-failure/SKILL.md)

Diagnoses failures when asked \"why is the build failing\", \"why did this regress\", or \"what caused this error\"; reproduces and tests hypotheses before proposing a fix.

Invocation: implicit. Risk class: bounded-execution.

Historical name: systematic-diagnosis.

### Edit technical writing

[`edit-technical-writing`](../skills/edit-technical-writing/SKILL.md)

Edits technical writing when asked to tighten a status update, clarify documentation, or remove vague and repetitive prose; preserves evidence, uncertainty, and the author's meaning.

Invocation: implicit. Risk class: read-only.

Historical name: high-signal-technical-writing.

### Implement an agreed plan

[`execute-plan`](../skills/execute-plan/SKILL.md)

Executes an identified implementation plan when explicitly authorized to implement it; tracks checkpoints, tests, deviations, and unfinished work without expanding scope.

Invocation: explicit. Risk class: bounded-execution.

Historical name: plan-execution.

### Understand a codebase

[`explain-codebase`](../skills/explain-codebase/SKILL.md)

Explains existing code when asked how a request flows, where behavior lives, or what a module does; grounds the explanation in current files rather than inferred historical intent.

Invocation: implicit. Risk class: read-only.

Historical name: codebase-explanation.

### Finish a development branch

[`finish-branch`](../skills/finish-branch/SKILL.md)

Assesses next steps for a finished branch when explicitly asked to wrap up development; presents PR, retention, or cleanup options without assuming merge or deletion authority.

Invocation: explicit. Risk class: external-write.

Historical name: finish-development-branch.

### Define the problem

[`frame-problem`](../skills/frame-problem/SKILL.md)

Frames a feature or problem when asked what to build, which outcome matters, or whether a proposed fix addresses the need; establishes users, constraints, and success before implementation.

Invocation: implicit. Risk class: read-only.

Historical name: problem-framing.

### Guide a configuration change

[`guide-configuration`](../skills/guide-configuration/SKILL.md)

Guides account or device setup when explicitly asked to help with a protected configuration step; verifies visible results without requesting secrets or claiming unseen completion.

Invocation: explicit. Risk class: bounded-execution.

Historical name: guided-configuration.

### Hand off unfinished work

[`handoff-work`](../skills/handoff-work/SKILL.md)

Prepares a continuation record when explicitly asked to hand off or resume work elsewhere; records exact state, unfinished work, evidence, and existing authority without transferring new permissions.

Invocation: explicit. Risk class: bounded-execution.

Historical name: task-handoff.

### Implement with a failing test first

[`implement-test-first`](../skills/implement-test-first/SKILL.md)

Implements a bounded behavior change when explicitly asked to use test-driven development; establishes a meaningful failing test, makes it pass, and refactors within authorized scope.

Invocation: implicit. Risk class: bounded-execution.

Historical name: test-driven-change.

### Investigate why a design exists

[`investigate-design-rationale`](../skills/investigate-design-rationale/SKILL.md)

Investigates why a design exists when asked why code was written that way or which constraint drove it; distinguishes historical evidence from plausible explanations.

Invocation: implicit. Risk class: network-read.

Historical name: design-rationale-investigation.

### Define the domain vocabulary

[`model-domain-vocabulary`](../skills/model-domain-vocabulary/SKILL.md)

Clarifies domain terms when teams use the same word differently or code and documents disagree; proposes definitions and examples without declaring owner approval.

Invocation: implicit. Risk class: read-only.

Historical name: domain-vocabulary-modeling.

### Plan a change

[`plan-change`](../skills/plan-change/SKILL.md)

Plans a change when asked for implementation steps, acceptance criteria, or a handoff-ready design; resolves interfaces and dependencies before execution without treating the plan as authorization.

Invocation: implicit. Risk class: read-only.

Historical name: implementation-planning.

### Plan test coverage

[`plan-tests`](../skills/plan-tests/SKILL.md)

Plans tests when asked what to test, which checks matter, or how to cover a risky change; selects proportionate unit, integration, contract, and journey evidence.

Invocation: implicit. Risk class: read-only.

Historical name: test-strategy.

### Prepare or maintain a draft PR

[`publish-change`](../skills/publish-change/SKILL.md)

Commits, pushes, or opens a PR only when explicitly requested; verifies identity, destination, diff, and checks while keeping merge, deployment, and release separately authorized.

Invocation: explicit. Risk class: external-write.

Historical name: publish-change-safely.

### Prepare a review request

[`request-review`](../skills/request-review/SKILL.md)

Prepares a review packet when explicitly asked to request review of a change; states scope, tests, and risks, and sends it only when the destination and action are authorized.

Invocation: explicit. Risk class: external-write.

Historical name: request-code-review.

### Research with sources

[`research-sources`](../skills/research-sources/SKILL.md)

Researches a question when asked to look up, compare, or verify current facts; uses primary sources and preserves dates, links, and uncertainty without turning claims into findings.

Invocation: implicit. Risk class: network-read.

Historical name: source-grounded-research.

### Resolve merge conflicts

[`resolve-merge-conflicts`](../skills/resolve-merge-conflicts/SKILL.md)

Resolves a named Git conflict when explicitly asked to reconcile a merge, rebase, or cherry-pick; preserves both intents and keeps continuation, commit, and push authority separate.

Invocation: explicit. Risk class: bounded-execution.

Historical name: merge-conflict-reconciliation.

### Review an engineering prompt

[`review-engineering-prompt`](../skills/review-engineering-prompt/SKILL.md)

Reviews a request for an engineering assistant when asked to check a prompt, clarify coding instructions, or improve a repair request. Checks outcome, context, scope, permissions, and completion evidence; returns feedback without executing the quoted task.

Invocation: implicit. Risk class: read-only.

Historical name: engineering-prompt-review.

### Reflect on the workflow

[`review-workflow`](../skills/review-workflow/SKILL.md)

Reviews a completed workflow when explicitly asked what caused friction or what to improve next; uses observed task evidence without diagnosing people or claiming unmeasured benefit.

Invocation: explicit. Risk class: read-only.

Historical name: workflow-retrospective.

### Manage a research workflow

[`run-research-workflow`](../skills/run-research-workflow/SKILL.md)

Coordinates a research lifecycle when explicitly asked to maintain traceable knowledge, evaluation, and corrections; excludes one-off search and never implies automatic publication.

Invocation: explicit. Risk class: bounded-execution.

Historical name: research-to-publication-lifecycle.

### Trace decisions to evidence

[`trace-decisions`](../skills/trace-decisions/SKILL.md)

Maintains a decision log when explicitly asked to record choices, evidence, and unresolved work across a task; excludes hidden reasoning, raw transcripts, and unrelated private context.

Invocation: explicit. Risk class: bounded-execution.

Historical name: decision-evidence-trace.

### Track acceptance evidence

[`track-acceptance`](../skills/track-acceptance/SKILL.md)

Creates a completion ledger when explicitly asked to track acceptance criteria and current evidence; preserves blocked and abandoned requirements.

Invocation: explicit. Risk class: bounded-execution.

Historical name: acceptance-evidence-ledger.
