---
name: typescript-javascript-engineering-profile
description: Apply focused TypeScript and JavaScript engineering judgment after repository gate discovery. Use for Node or browser packages, type safety, async behavior, tests, dependencies, compatibility, and builds; honor the repository package manager and scripts.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.17.1"
  plugin: "measured-stack-profiles"
  invocation: "implicit"
  provenance: "clean-room"
  risk_class: "read-only"
---

# TypeScript and JavaScript Engineering Profile

Use this profile only after repository discovery identifies the stack. Read [focused checks](references/checks.md) when stack-specific gates or hazards determine the result.

## Workflow

1. Discover `package.json`, the matching lockfile, workspace configuration, `tsconfig` files, runtime targets, and repository scripts.
2. Follow repository-defined commands and pinned tool versions before suggesting defaults.
3. Review idiomatic design and material hazards, especially implicit `any`, unsafe assertions, nullability, promise loss, module-system mismatches, environment boundaries, prototype pollution, serialization, and client-server contract drift.
4. Select proportionate gates from the selected package manager's repository scripts for formatting, linting, type checking, tests, builds, and dependency or vulnerability review.
5. Review compatibility across Node and browser targets, module format, package exports, TypeScript version, generated types, API schemas, bundlers, and lockfile changes.
6. Report every missing tool, skipped command, unsupported platform, or unavailable environment as incomplete rather than passing.

## Boundaries

- Do not invent one universal command or replace repository policy with generic preferences.
- Do not install, upgrade, publish, deploy, apply, or mutate shared state merely to run a gate.
- Separate static review, executed checks, build evidence, provider state, and live behavior.

## Output

Return Discovery, Hazards, Commands selected, Results, Compatibility, Missing evidence, and Next safe gate.

