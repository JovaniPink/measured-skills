---
name: go-engineering-profile
description: "Reviews Go changes when goroutines, modules, APIs, dependencies, or tests need language-specific checks; follows repository toolchain and gate definitions."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-stack-profiles"
  invocation: "implicit"
  provenance: "original"
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

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return Discovery, Hazards, Commands selected, Results, Compatibility, Missing evidence, and Next safe gate.

## Example

Synthetic example; not an observed client result.

Input: A goroutine writes to a map while the request handler reads it.

Output: warning: concurrent access lacks synchronization. Inspect ownership and run the repository's race checks before selecting a fix.
