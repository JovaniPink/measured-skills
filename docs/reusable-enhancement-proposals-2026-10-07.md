# Reusable enhancement proposals

Prepared October 7, 2026. These independently authored proposals use fictional
examples and public authorities. They add no canonical skill, implementation,
installation, qualification result or release commitment. New targets are
unassigned. Measured Skills remains the 0.18.0 candidate. No benefit is measured.

## Firestore engineering profile: planned

Trigger: review a Firestore-backed change whose correctness depends on SDK,
field-path, read/write or concurrency semantics. Near misses: general database
selection, provisioning, security-rule-only review and ordinary API design.
Output: an SDK-specific transition review, affected readers/writers, invariants,
failure cases and a verification plan with its actual limits.

Separate server-library authorization and transaction behavior from mobile/web
SDK behavior. Inspect escaped leaf paths rather than treating identifiers as
path syntax. Read-dependent changes require a transaction or an evidenced
alternative concurrency contract. Retrying a transaction must not duplicate an
external effect. Application generation/lease checks need their own contract;
they are not a database guarantee. Emulator success cannot establish production
contention, indexes or limits.

Fictional example: two editors update an inventory item named `part.blue` while
an old invoice render finishes. Review sibling-field conservation and refusal
of the obsolete generation. Do not invent a schema or assume an emulator proves
production behavior. Entry requires pinned SDK authorities, independently
reviewed cases, narrow routing, client loading evidence and bounded comparison.

## Asynchronous delivery: overlap review first

Start with `api-contract-compatibility-review` for event identity and compatible
consumers, `observability-design` for attempts versus confirmed effects, and
`operational-readiness-review` for replay and recovery ownership. A new skill is
warranted only if a distinct trigger and output remain after those workflows
are reviewed. Do not create a generic queue skill by counting integrations.

Fictional example: a duplicated receipt-notification task observes an ambiguous
network timeout. Separate durable obligation, attempt, external acknowledgment
and business completion. A successful enqueue or handler invocation does not
prove delivery. Evaluate duplicate execution, stale work, partial acknowledgments
and safe recovery without sending anything. Cloud Tasks documents possible
duplicates; apply that fact only where the application's selected queue supports
it. An application must define its own idempotency and custody contract.

## Enhance source-output-conformance-audit

Extend the existing audit rather than introducing a second artifact skill.
Trace source identity and independently established observations through
transformation, rendering, persisted bytes and publication receipt. Require each
observation to have an authorized destination, justified exclusion or unresolved
hold. Matching aggregate totals cannot establish identity conservation. Compare
the current downloaded artifact's identity with its source and audit; an older
usable artifact is distinct from saved pending work.

Fictional example: a laboratory report renderer faithfully paints a wrong
sample identifier. Rendering fidelity passes while independent source accuracy
fails. A mock painter cannot establish placement or actual-library readback.
Publication evidence must bind exact bytes; no universal receipt schema is
proposed. Keep the audit read-only and implementation/publication separately
authorized. Qualification needs missing-observation, swapped-identity and
stale-artifact cases with an oracle independent of the candidate output.

## Deferred candidates

ADK evaluation refinements should extend `google-adk-engineering-profile` and
`agent-evaluation-design`: separate trajectory/tool-use, grounding and final
outcome checks; verify grader validity and actual environmental outcomes.
Fictional library-search cases must score unsupported citations and denied
effects independently of a plausible final answer. No ADK runner is proposed.

An explicitly selected engineering-learning workflow can combine codebase
explanation, planning, handoff and evaluation. Task completion and learner
understanding are separate outcomes. Fictional inventory work should test whether
the learner can explain a transition, identify a failure and reason about a new
variation without coaching. Record introduced concepts separately from demonstrated
reasoning; assent is not understanding. Ordinary autonomous delivery remains the
default. Restoration hooks, clinical claims and learner collection are excluded.

## Refine existing browser and CI tracks

`web-journey-verification` already exists in the roadmap. Add authenticated
role/record context, exact current artifact/status evidence, durable refusal and
reload recovery. Distinguish API assertions, rendered behavior and browser
observations. A missing browser remains blocked; installed scripts are not proof
of execution. Playwright's retrying assertions inform bounded waits, not a
requirement to install or use that tool.

`ci-workflow-review` already exists. Refine its cases around permissions, fork
and trusted triggers, immutable dependencies, reusable-workflow inputs, caching,
job dependencies and required deploy gates. Successful component jobs do not
prove the combined release is compatible. Preserve review-only authority;
reruns, settings, edits and deployment require separate task authorization.

## Primary-source packet

Read October 7, 2026. These are reference-only observations, not copied skill
text. Pin exact source identities and review license applicability before any
canonical authoring. Google's documentation identifies CC BY 4.0 prose and
Apache-2.0 samples subject to stated exceptions; no sample code is reused here.
Other authorities are linked for technical review only; their licenses are not
treated as permission to copy. No third-party skill or client material is included.

| Authority | Applicability and limit |
| --- | --- |
| [Firestore field updates](https://firebase.google.com/docs/firestore/manage-data/add-data) | Nested updates and SDK examples; inspect exact SDK field-path APIs. |
| [Firestore contention](https://docs.cloud.google.com/firestore/native/docs/transaction-data-contention) | Server versus mobile/web transaction modes; not an application generation contract. |
| [Firestore emulator](https://docs.cloud.google.com/firestore/native/docs/emulator) | Local concurrency/index/limit differences; not production acceptance. |
| [Cloud Tasks pitfalls](https://docs.cloud.google.com/tasks/docs/common-pitfalls) | Duplicate execution and operational behavior; not confirmed business delivery. |
| [ADK evaluation](https://adk.dev/evaluate/) | Outcome and trajectory evaluation; native runs and grader review remain required. |
| [Anthropic agent evaluation](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Trajectories, environmental outcomes and grader validity; not independent acceptance by narration. |
| [Playwright assertions](https://playwright.dev/docs/test-assertions) | Targeted observable assertions and bounded retry; no deployment or account authority. |
| [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use) | Workflow security boundaries; not a complete compatibility or release review. |

## Adoption prerequisites

Resolve overlap, assign a reviewer, pin a public source packet, author fictional
cases independently and review hidden-answer separation. Register only after
model, native inventory/isolation, permissions, bounded tools and budget are
settled. Preserve separate client lanes and unavailable evidence. Existing
workflow and communication studies remain draft, unregistered and unrun with
zero collection budget; neither qualifies these proposals. Human rubric review
and measured comparisons remain pending.
