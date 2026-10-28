# Skill Taxonomy

The catalog uses two separate organizing systems. Plugins are installable packages. Taxonomy facets describe what a skill does, when it helps, what it affects, and how much evidence supports it.

The authoritative records are in [`catalog/skills.json`](../catalog/skills.json). The strict schema is in [`catalog/skills-schema.json`](../catalog/skills-schema.json).

## Why plugins are not the taxonomy

A plugin answers, "Which marketplace unit should I install?" It does not fully answer, "Which skill fits this decision?"

For example, an engineering plugin can contain planning, execution, and review workflows. A stack profile can apply during design, testing, review, and release. The facets let a reader search across those packaging boundaries.

## Facets

Each canonical skill has one strict record with these fields:

- `capability_family`: the main kind of help the skill provides. Values are evidence, planning, execution, review, operations, communication, and AI engineering.
- `lifecycle_stages`: where the skill commonly helps. Values are discover, frame, design, build, test, review, release, operate, and learn.
- `targets`: the main artifacts or systems in scope. Values are code, repository, data, service, agent, model, organization, and publication.
- `risk_class`: the existing effect and trust boundary from canonical metadata.
- `invocation`: implicit or explicit.
- `maturity`: the evidence state for the skill.
- `composes_with`: related skills that can strengthen the same workflow.
- `conflicts_with`: nearby skills whose routing or scope must remain distinct.
- `maturity_evidence`: the repository record that supports the maturity claim.

The `plugin` field remains in `SKILL.md` metadata because generation uses it to route the canonical source into Codex and Claude distributions. Array-valued taxonomy stays outside open-standard frontmatter.

## Maturity states

Maturity is an evidence claim, not a writing-quality score.

| State | Meaning |
| --- | --- |
| `incubating` | The workflow is not ready for ordinary discovery or use. |
| `candidate` | Structure, routing, provenance, and automated checks exist, but repeatable field acceptance is incomplete. |
| `field-tested` | A retained task record shows the exact current package loaded in a named client and produced a useful result within scope, with failures and limits recorded. This does not establish repeatability or benefit over a baseline. |
| `accepted` | Required automated and manual acceptance has passed repeatably for the claimed client surfaces and tasks under a documented acceptance protocol. Acceptance does not establish comparative benefit. |
| `deprecated` | The skill remains available during a documented migration period. |
| `revoked` | Packaging and marketplace advertisement are disabled because the skill is unsafe or invalid. |

Every skill in the current catalog stays at `candidate`. This clarification does not promote any skill or waive a release gate. A generated package, successful selection, or passing schema is not a task observation.

Promotion requires a reviewed evidence record naming the package revision, client and model version, task, successful source/reference loading, result, failures, and coverage limits. `field-tested` records observed use; `accepted` additionally requires repeated passes against the stated acceptance conditions. An observation on one client or older version does not qualify another. Reassess affected claims after material changes; retain historical results as historical.

Comparative benefit is a separate claim, not another maturity state or a prerequisite for recording observed use. It requires a suitable baseline, comparable tasks and conditions, outcome measures, and explicit limits on attribution. Neither a useful task result nor repeatable acceptance alone establishes improved productivity or financial return. Existing release requirements for any claimed benefit remain controlling.

## Risk classes

| Risk class | Meaning |
| --- | --- |
| `read-only` | Reviews or organizes available evidence without changing external state. |
| `bounded-execution` | May coordinate local, reversible, scoped work within current authority. |
| `network-read` | May require current external evidence but does not write to the external system. |
| `external-write` | Can prepare or coordinate an authorized write outside the current local state. |
| `trust-decision` | Helps decide whether material is safe or permitted to enter the catalog. |

Risk metadata never grants a tool or permission. Host policy and separate user authority remain controlling.

## Related records

- [`catalog/packs.json`](../catalog/packs.json) defines plugin packs and small recipes.
- [`evals/cases.json`](../evals/cases.json) contains routing, safety, output-quality, and baseline records.
- [`provenance/catalog.json`](../provenance/catalog.json) records public authorities, declared methods, owned origins, and review limits.
- [`catalog/compatibility.json`](../catalog/compatibility.json) points to observed client evidence.

## Primary resources

- [Agent Skills specification](https://agentskills.io/specification)
- [OpenAI skill-building guide](https://learn.chatgpt.com/docs/build-skills)
- [Anthropic Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
