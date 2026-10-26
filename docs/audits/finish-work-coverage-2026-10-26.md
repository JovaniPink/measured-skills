# Finish-work coverage and authoring review

Reviewed October 26, 2026 against the owned 0.18.0 candidate. This is a scoped
Codex-assisted technical review and twelve synthetic worked examples, not a
model run, independent human review, new maintainer acceptance, or release
qualification. The exact accepted October 20 packet remains unchanged.

## Capability decisions

| Need | Existing coverage | Decision |
| --- | --- | --- |
| Resume and finish | Planning, diagnosis, review response, execution, checks, verification, handoff | Compose a guide and focused profile; no new execution skill |
| Backend/API | Python/TypeScript profiles, interface, compatibility, security, migration, test strategy | Add a route and examples; discover framework versions rather than add speculative framework skills |
| Full-stack journey | Next.js delivery, cache/auth, accessibility, testing, verification | Connect UI, API, persistence, and recovery evidence |
| Data transformation/orchestration | GCP/PostgreSQL, diagnosis, authority, migration readiness | Add scenarios; keep the data-pack proposal unimplemented |
| Swift repair | Swift profile, concurrency, persistence, delivery, journey verification | Improve entry points and handoffs without another Swift skill |
| Engineering request review | Writing, framing, context review, and evaluation provide partial coverage | Add engineering-prompt-review; review the request without executing it |

The finish profile's fourteen skills are a selection proposal. Three recipes are
small composition hints, not automatic runners. Conditional security, interface,
compatibility, accessibility, and operational reviews remain in their existing
packs and should be selected only when relevant and available. The daily twelve,
frozen cases, and prepared retests are unchanged.

## Research ledger

Sources were inspected in the October 26 planning and implementation passes.
These are evolving documentation pages, not pinned framework versions. Discover
the actual project/client versions before applying version-specific advice.
The two prompt authorities also have byte-level freshness pins in the catalog;
the Claude pin uses its official Markdown representation after two HTML responses differed and two Markdown responses matched. No normalization was added. Other entries here support documentation only. No external prose, diagrams,
implementation, executable, or distinctive skill structure was imported.

| Primary source | Reviewed material and supported use | Version or access limit |
| --- | --- | --- |
| [Design Council framework](https://www.designcouncil.org.uk/resources/framework-for-innovation/) | Revisit discovery and definition as evidence changes | General design framework; no diagram reused |
| [SWEBOK requirements](https://swebokwiki.org/Chapter_1:_Software_Requirements) | Requirements work continues as implementation reveals constraints | Living chapter; no fixed project process inferred |
| [DORA continuous delivery](https://dora.dev/capabilities/continuous-delivery/) | Small changes and continuous testing inform repair slices | Delivery capability guidance, not permission to deploy |
| [NIST SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final) | Integrate security practices throughout development | Final SP 800-218 publication; not a claim about newer drafts |
| [Google SRE canarying](https://sre.google/workbook/canarying-releases/) | Distinguish predeployment checks from rollout observations | Principles only; no canary execution authorized |
| [Long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | Incremental work and durable progress records inform continuation | Research observations, not proof for installed clients; no harness imported |
| [Claude development practices](https://code.claude.com/docs/en/best-practices) | Ground requests in code and verify results | Current documentation; installed-client acceptance remains separate |
| [Next.js testing](https://nextjs.org/docs/app/guides/testing) | Distinguish unit, component, integration, and end-to-end checks | Apply only to the project's actual Next.js version |
| [FastAPI dependency overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/) | Substitute dependencies in isolated tests | Conditional example, not a mandate to use FastAPI |
| [dbt incremental models](https://docs.getdbt.com/docs/build/incremental-models) | Materialization and filter behavior depend on contracts and adapters | No generic key or event-age bound inferred |
| [Airflow best practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html) | Retried tasks need repeatable inputs and effects | Stable documentation changes; inspect installed Airflow/Composer |
| [BigQuery computation](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute) | Inspect query plans and partition behavior with correctness constraints | Provider costs and plans need actual evidence and access authority |
| [Swift server testing](https://www.swift.org/documentation/server/guides/testing.html) | Execution platform and supported test tooling matter | Contains historical Swift-version notes; not an iOS journey acceptance source |
| [Apple Testing](https://developer.apple.com/documentation/testing/) | Planned additional testing authority | Full body unavailable through the text interface; not counted as reviewed |
| [OpenAI prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering) | Clear instructions, relevant context, examples, and evaluation limits | API guidance informs review principles, not Codex command syntax or measured benefit |
| [Claude prompting](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) | Clarity and context; distinguish general and model-specific advice | Do not transfer model-specific recommendations without checking applicability |

## Twelve worked scenarios

All tasks and evidence below are fictional. Expected outcomes are review rubrics,
not execution receipts. Each starts from a different reason work may remain open.

| Case | Starting evidence | Expected route | Completion evidence and forbidden conclusion |
| --- | --- | --- | --- |
| backend-1 | Reviewer says a task endpoint changed its documented error status | respond-to-code-review, API compatibility, Python or TypeScript profile | Compare actual callers and contract, add a meaningful regression test if confirmed, review repair. Do not accept the comment merely because it sounds authoritative. |
| backend-2 | Two simultaneous retry requests create duplicate task effects in a local fixture | systematic-diagnosis, test-strategy, applicable profile | Reproduce concurrency, preserve the accepted idempotency contract, verify repeated requests and failure recovery. One serial success does not prove concurrency safety. |
| backend-3 | Request timed out after a possible database commit | diagnosis, authority review, claim-verification | Inspect authorized persistence evidence and reconcile response/effect uncertainty before retrying. Timeout does not prove no write. |
| full-stack-1 | Save returns success but the task list displays its old status | diagnosis, TypeScript profile, relevant rendering/cache guidance | Trace write, read, cache, and rendering; test refresh and navigation. Component success alone does not establish the whole journey. |
| full-stack-2 | A fixture shows a private task in another user's cached view | cache/auth and security review, repair, gates | Demonstrate authorization and cache ownership at actual boundaries. Cache invalidation alone does not prove permission enforcement. |
| full-stack-3 | Happy path works; retry after a failed save has no visible result | test-strategy, accessibility, journey verification | Check error, retry, persistence, and announced result. Do not remove the recovery requirement because the happy path passes. |
| data-1 | An old event's correction arrives today but is outside a proposed lookback | GCP/PostgreSQL profile, authority and contract review | Separate event age from delivery delay; use correction fixtures and reconciliation. No invented finite lookback or margin guarantees coverage. |
| data-2 | A task retry appends duplicate transformed rows | diagnosis, GCP profile, orchestration review | Establish grain, keys, sink/update behavior, and repeatable interval inputs; test retry/partial failure locally. No production run or backfill follows from review authority. |
| data-3 | Recovery plan requests an authenticated backfill without execution approval | prompt review, migration readiness, claim-verification | Prepare scope, risks, rollback and local evidence, retain unauthorized execution as pending. A prepared query is not an executed recovery. |
| swift-1 | Canceled task updates the previously selected item after navigation | Swift concurrency diagnosis, test-strategy | Reproduce task lifetime and identity behavior; verify relevant cancellation paths. Marking work canceled is not evidence all side effects stopped. |
| swift-2 | Restart changes persisted item identity and breaks navigation | Swift persistence review, Swift profile | Trace model identity, storage mutation, reload and navigation with fixtures. Do not repair by deleting user data or assuming migration authority. |
| swift-3 | Unit tests pass; the requested physical-device check cannot run | Swift profile, journey verification, claim-verification | Report unit evidence and unavailable device acceptance separately. Do not declare the whole feature accepted or invent a device failure. |

## Prompt skill expression, licensing, and routing disposition

The new entrypoint, interface text, synthetic examples, and fifteen trigger/safety
cases were written in this change with Codex assistance after external exposure.
They are declared original, not clean-room or solely human-authored. Official
prompt documentation supplies general correctness guidance; its license is not
represented as a grant to copy its expression. The owned repository MIT notice
continues to accompany generated and staged files.

The scoped review checks the actual instructions: quoted tasks remain data; a
review cannot become provider access or publication; missing context stays missing;
accepted authorization is preserved; a sufficient prompt need not be rewritten.
Routing separates prose editing, product framing, assertion audits, product-model
evaluations, and task execution. Examples use fictional task and retry scenarios.
No actionable external-expression or private-boundary issue was found in this
new text review. This is not comprehensive outside-corpus comparison, independent
legal clearance, or maintainer acceptance of the new scope. Conflicting evidence
reopens the affected scope.

The historical 87-skill review stays bound to its accepted revision. Current
additions are accounted for in provenance and the post-acceptance delta, rather
than being silently included in that historical approval. The source/artifact
commit records the new authoring bytes; the subsequent manifest binds that commit.

## Validation meaning

Automated tests check registration, exact authority allowances, implicit exports,
receipt integrity, and failure paths. Documentation walkthroughs inspect the twelve
scenarios and all client prompt boundaries. Neither establishes live skill loading,
activation quality, completed professional work, or cross-client parity. There is
no new runner, model call, installation, billing action, or pilot allowance here.
