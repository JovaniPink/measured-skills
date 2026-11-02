# Finish an investigation or review decision

Start with the [chooser](start.md). Two routes make existing capabilities usable
without another pack, agent system, or installed configuration.

| Situation | Choose | Provide | Receive | Stop |
| --- | --- | --- | --- | --- |
| A test passes alone but fails in the suite | Diagnose an intermittent failure | Repository and original failure; order, seed and environment if known | Bounded local experiments, supported cause or specific uncertainty | Before edits, quarantine, CI changes or publication |
| Reviewers demand incompatible changes | Resolve conflicting review findings | Findings, reviewed revisions and governing requirements | Evidence-backed options, recommendation and actual decision status | Before edits, check execution, replies or policy changes |

The chooser generates client-specific prompts. Codex and Claude Code selectors
require the actual installed entry; ordinary wording is the fallback. Antigravity
uses eligible implicit skills. The decision route's record-decisions entry is in
Measured Operations and outside finish-work-core. A selectable route does not
establish installation, loading, or extra authority. Neither route launches a
second model or expands the three-round review budget.

## Intermittent failures

An imaginary Python cache test fails after an authentication test. Capture the
first failure and reproduce the recorded order within the available local budget.
Compare isolated/serial/parallel conditions one at a time. A repeated green result
cannot explain away the original failure. Do not change production data, install
a plugin, add retry logic or weaken the assertion just to finish the investigation.

The default ceiling is ten executions or five minutes, whichever comes first.
That is a chosen investigation limit, not a statistical confidence threshold.
If the user's narrower constraints forbid execution, inspect supplied logs and
source only. If repair is already authorized, carry the supported cause into a
small repair and compare before/after evidence under the same relevant conditions.

Read the [standalone diagnosis reference](../skills/diagnose-failure/references/nondeterministic-failures.md).
No reproduction, worker, provider job or model evaluation was executed to author it.

## Conflicting findings

Imagine one review requires validating an untrusted upload and another objects
to repeated copies. First establish whether both describe the same revision and
boundary. Compare validation once at the trust boundary with validation at every
caller. Keep required protections and show unknown latency rather than inventing
performance measurements. A model vote or silence cannot waive the requirement.

Use the existing decision owner's authority for material product/policy choices;
make routine authorized engineering choices without adding another approval loop.
The [standalone decision reference](../skills/record-decisions/references/conflicting-reviews.md)
connects findings to requirements, feasible options, remaining evidence and status.
Consolidation can deduplicate claims; it cannot ratify a trade-off.

## Use existing routes for other operational work

- **Compare documents with implementation** checks current contracts, READMEs or
  runbooks against source and supplied results. It does not run continuously or
  automatically rewrite requirements to match code.
- **Review a replay or backfill** checks existing SQL/GCP and migration contracts.
  Execution plans, lock behavior, state changes and recovery require engine-specific
  evidence and separate provider-execution authority where applicable.
- **Review a change** can select operational readiness or observability guidance
  when rollout, canaries, trace propagation, cardinality or retention are material.
  A plan or static review does not establish safe deployment or live correlation.
- **Refactor without changing behavior** starts with observed behavior and includes
  characterization coverage. A deterministic codemod does not prove universal
  equivalence; distributed cutovers need additional migration and recovery evidence.

Do not add another skill simply because a technique has a name. Use a concrete task
to expose a missing input, step, output, or permission boundary first.

## Evidence and next use

These are original, synthetic examples reviewed against existing contracts and
primary documentation on November 2, 2026: [pytest's flaky-test explanation](https://docs.pytest.org/en/stable/explanation/flaky.html)
and [Google SRE on explicit risk trade-offs](https://sre.google/sre-book/embracing-risk/).
Neither source establishes that these prompts work in an installed client. The
examples are not executed evaluations, financial benefits, or release acceptance.

The original ten-card human exercise and narrow Haiku retest remain unchanged.
For later separately observed use, record whether the route was found, what loaded,
what work advanced, what instructions had to be repeated, and which requirements
survived continuation. Unknown observations stay unknown. Keep private task details
and raw session evidence outside this public repository.
