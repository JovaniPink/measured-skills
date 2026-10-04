# Authoring Guide

## Scope

One skill should express one reusable capability. Put activation context in the frontmatter description and procedural content in the body. Keep `SKILL.md` concise; move substantial lookup material into focused `references/` files.

Use lowercase, hyphenated names that are no longer than 64 characters. The directory name and frontmatter `name` must match.

Use ASCII, US English, and approachable language in canonical skills, references, comments, evaluations, and documentation. Follow the [editorial style guide](editorial-style.md). Edit canonical sources and regenerate client distributions instead of hand-editing generated files.

## Required frontmatter

```yaml
---
name: example-skill
description: What the skill does and the concrete situations that should activate it.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-skills"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---
```

All metadata values are strings. Invocation is either `implicit` or `explicit`. Use explicit invocation when the workflow primarily coordinates publication, deployment, destructive mutation, credentialed writes, import of untrusted code, or a similarly consequential trust decision. `plugin` selects the generated distribution. `provenance` records implementation method, while the catalog separately records capability disposition. `risk_class` is one of `read-only`, `bounded-execution`, `network-read`, `external-write`, or `trust-decision`.

## Codex interface

Every canonical skill includes `agents/openai.yaml`:

```yaml
interface:
  display_name: "Example Skill"
  short_description: "A compact interface description"
  default_prompt: "Use $example-skill to ..."
policy:
  allow_implicit_invocation: true
```

The canonical default prompt must mention the skill with `$skill-name`. Set the policy to `false` for explicit-only skills. Generation rewrites that prompt to `$measured-skills:skill-name` for the installed plugin namespace.

## Workflow rules

- Name the authority capable of proving each conclusion.
- Distinguish observation, inference, proposal, and unresolved questions.
- Preserve the boundary between diagnosis and remediation.
- Do not assume one quality command, branch name, remote, identity, provider, framework, or deployment target.
- State stop conditions and missing-evidence outcomes.
- Keep deterministic enforcement in scripts, tests, CI, or host permissions.
- Do not encode workspace-specific private facts in a public skill.

## References and scripts

References must be directly linked from `SKILL.md`, use relative paths, and be necessary to execute the workflow. The catalog does not permit skill-level scripts, hooks, MCP servers, dependencies, bundled agents, or executable payloads.

## Client authoring limits

The receiving client sets these limits. They are published guidance rather than repository preference, so treat them as constraints on any new skill.

- `name`: at most 64 characters, lowercase letters, numbers, and hyphens.
- `description`: at most 1,024 characters, written in third person, stating what the skill does and when to use it. Third person matters because the description is loaded into the system prompt, where a mixed point of view makes selection less reliable.
- `SKILL.md` body: under 500 lines. Split longer content into references.
- References: one level deep from `SKILL.md`. A reference that points to another reference may be read only in part.
- A reference longer than 100 lines: give it a table of contents, so a partial read still shows its full scope.

The catalog met all five when checked on 2026-09-10: no skill body exceeded 57 lines, no reference exceeded 100 lines, every description fell between 211 and 419 characters, and none used first or second person.

Published guidance also says a skill is under-selected more often than over-selected, so a description should name the situations that should reach it, not only the capability it provides. The 0.13.0 motion-review routing gap was an instance of exactly that.

Source: [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), read 2026-09-10.

## Completion checklist

- Confirm that the skill structure is valid under the supported standards.
- Confirm the native Codex and Claude invocation mappings.
- Add a provenance record.
- Confirm that the workflow is authored from owned original work and only primary authorities needed for format, interoperability, or correctness.
- Do not track, cite, mirror, compare, or use third-party skill catalogs as implementation sources.
- Add three positive, three near-miss, and one conflict or safety trigger case.
- Add at least three output-quality criteria and an installed-versus-baseline record.
- If a new or revised skill reports findings, grade each finding with the severity words in the [finding vocabulary](finding-vocabulary.md), and add a finding state when the skill reviews a pinned change. Do not invent a local scale.
- Adoption is partial. Skills released before that rule keep their own wording until they are revised, and the vocabulary records which have adopted it.
- Add one strict taxonomy record with maturity evidence, companions, and routing conflicts.
- Run reference and link validation.
- Run the public and private boundary scan.
- Run the originality and repository-independence scans.
- Confirm that generated trees match the canonical sources.
- Record client-specific smoke evidence when the release policy requires it.
