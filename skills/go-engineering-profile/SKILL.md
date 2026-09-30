---
name: go-engineering-profile
description: Apply focused Go engineering judgment after repository gate discovery. Use for Go modules, packages, concurrency, APIs, tests, dependencies, compatibility, and build concerns; defer exact commands to repository evidence.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.17.1"
  plugin: "measured-stack-profiles"
  invocation: "implicit"
  provenance: "clean-room"
  risk_class: "read-only"
---

# Go Engineering Profile

Use this profile only after repository discovery identifies the stack. Read [focused checks](references/checks.md) when stack-specific gates or hazards determine the result.

## Workflow

1. Discover `go.mod`, `go.work`, Go source, toolchain directives, and repository scripts.
2. Follow repository-defined commands and pinned tool versions before suggesting defaults.
3. Review idiomatic design and material hazards, especially goroutine leaks, cancellation loss, races, nil interfaces, error wrapping, resource lifetime, map or slice aliasing, and unstable public APIs.
4. Select proportionate gates from repository scripts, `gofmt`, compilation, tests, vetting, race checks, fuzzing, vulnerability checks, and builds when configured and safe.
5. Review compatibility across module paths, minimum Go version, build tags, generated code, cgo, platform targets, and semantic import versioning.
6. Report every missing tool, skipped command, unsupported platform, or unavailable environment as incomplete rather than passing.

## Boundaries

- Do not invent one universal command or replace repository policy with generic preferences.
- Do not install, upgrade, publish, deploy, apply, or mutate shared state merely to run a gate.
- Separate static review, executed checks, build evidence, provider state, and live behavior.

## Output

Return Discovery, Hazards, Commands selected, Results, Compatibility, Missing evidence, and Next safe gate.

