---
name: cross-stack-quality-gates
description: Discover and run the repository's real validation gates across supported application, language, data, and infrastructure stacks without assuming a universal command. Use after changes, before review, or when asked whether a codebase passes its checks.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.17.1"
  plugin: "measured-skills"
  invocation: "implicit"
  provenance: "clean-room"
  risk_class: "bounded-execution"
---

# Cross-Stack Quality Gates

Discover the project's contract before running validation. Read [gate discovery](references/gate-discovery.md) only for the stacks present in the target scope.

## Workflow

1. Inspect repository instructions, manifests, CI configuration, and documented scripts.
2. Determine which components changed and which gate owns each relevant invariant.
3. If an installed stack profile matches the component, use it for stack-specific hazards, compatibility, and gate judgment. The profile does not override repository instructions.
4. Choose the narrowest useful sequence, normally fast static checks before slower tests and builds.
5. Run commands exactly as the repository defines them. Do not silently substitute package managers, add flags, rewrite snapshots, format files, apply Terraform, or update dependencies.
6. Record command, working directory, exit status, duration when material, and the first actionable failure.
7. Distinguish a missing gate from a passing gate. Do not skip an unavailable command and report the suite green.
8. Report environment restrictions separately from product failures.

## Scope rules

- A monorepo may require multiple component-specific gates; do not run every workspace blindly.
- Builds may create ignored artifacts or caches but must not rewrite tracked source.
- SQL validation must state whether it was syntax/static only or executed against a real engine.
- Terraform validation is not an apply. Plans are proposals and must not be reported as deployed state.
- Simulator or preview checks do not prove device, production, or provider behavior.

## Output

Return the overall verdict `PASS`, `FAIL`, or `INCOMPLETE` first, followed by the complete gate table with `Component`, `Command`, `Result`, and `Evidence`, and any coverage gaps.

## Continuity and evidence

Lead with PASS, FAIL, or INCOMPLETE, derived from the required gates. Retain the complete command and evidence table, unavailable checks, and the first actionable failure. A missing required gate cannot become a pass through summarization.

Read [the original acceptance example](references/continuity-example.md) when checking this behavior.
