---
name: portable-skill-authoring
description: "Design or revise a portable Agent Skill with precise routing, invocation policy, focused references, provenance, security boundaries, evals, and generated client adapters. Use for cross-client SKILL.md catalog work; do not trigger for ordinary documentation or client-specific command files."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-reasoning"
  invocation: "implicit"
  provenance: "clean-room"
  risk_class: "bounded-execution"
---

# Portable Skill Authoring

Create one canonical workflow source and validate its client projections.

Read [client adapters](references/client-adapters.md) when invocation controls, packaging, or generated Codex and Claude output are in scope.

## Workflow

1. Establish the capability gap, target requests, near misses, conflicting skills, supported clients, and authority boundary.
2. Confirm that the capability belongs in public core, a private overlay, or neither. Resolve license and source provenance before writing.
3. Choose a concise name and a discriminating description whose first clause carries the main trigger.
4. Keep the entrypoint focused on decisions the host would not make reliably without it. Move conditional detail into small, linked references.
5. Choose implicit or explicit invocation from workflow intent. Do not grant tools merely because the workflow might use them.
6. Add positive, near-miss, conflict or safety, output-quality, and installed-versus-baseline evaluations.
7. Generate native adapters and packages from canonical source. Validate schema, links, policy mapping, deterministic output, package layout, provenance, originality, and public boundaries.
8. Record observed behavior separately for every client surface. Do not infer parity from compatible files or another client result.

## Boundaries

- Prefer the host's native skill creator when the task is limited to that host, but preserve this catalog's portable acceptance contract.
- Do not copy a popular skill because its repository is public. Pin license and revision, review the full influence surface, and author independently when clean-room treatment is required.
- Do not bundle hooks, agents, MCP servers, dependencies, broad permissions, or executables without an explicit later release decision.

## Output

Return `Capability`, `Routing`, `Invocation`, `Canonical files`, `Adapters`, `Provenance`, `Security`, `Evaluations`, `Validation`, and `Observed client limits`.

## Continuity and evidence

Separate required semantic content from optional presentation. Test concise and requested long-form outputs, competing instructions, partial failure, stale handoffs, and interruptions. Keep shared workflow meaning canonical and client-native loading and invocation controls in generated adapters. Do not claim explicit-only support from a slash command alone or distribute an explicit-only workflow to an unverified surface.

Read [the original acceptance example](references/continuity-example.md) when checking this behavior.
