---
name: terraform-engineering-profile
description: Apply focused Terraform engineering judgment after repository gate discovery. Use for modules, providers, state, plans, upgrades, compatibility, and infrastructure review; validation never implies apply authority.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-stack-profiles"
  invocation: "implicit"
  provenance: "clean-room"
  risk_class: "read-only"
---

# Terraform Engineering Profile

Use this profile only after repository discovery identifies the stack. Read [focused checks](references/checks.md) when stack-specific gates or hazards determine the result.

## Workflow

1. Discover Terraform files, module structure, required providers, dependency lockfiles, backend declarations, workspaces, and repository scripts.
2. Follow repository-defined commands and pinned tool versions before suggesting defaults.
3. Review idiomatic design and material hazards, especially resource-address churn, unsafe `for_each` keys, sensitive state, provider defaults, lifecycle misuse, implicit dependencies, broad IAM, replacement, and drift.
4. Select proportionate gates from repository scripts, formatting, initialization with controlled backend behavior, validation, static analysis, policy checks, and reviewed plans without applying.
5. Review compatibility across Terraform and provider versions, module interfaces, state moves, import blocks, backend behavior, upgrade guides, and plan changes across environments.
6. Report every missing tool, skipped command, unsupported platform, or unavailable environment as incomplete rather than passing.

## Boundaries

- Do not invent one universal command or replace repository policy with generic preferences.
- Do not install, upgrade, publish, deploy, apply, or mutate shared state merely to run a gate.
- Separate static review, executed checks, build evidence, provider state, and live behavior.

## Output

Return Discovery, Hazards, Commands selected, Results, Compatibility, Missing evidence, and Next safe gate.

