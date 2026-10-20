---
name: python-engineering-profile
description: "Reviews Python changes when typing, async code, packaging, dependencies, or tests need focused checks; follows discovered Python versions and repository commands."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.18.0"
  plugin: "measured-stack-profiles"
  invocation: "implicit"
  provenance: "clean-room"
  risk_class: "read-only"
---

# Python Engineering Profile

Use this profile only after repository discovery identifies the stack. Read [focused checks](references/checks.md) when stack-specific gates or hazards determine the result.

## Workflow

1. Discover `pyproject.toml`, lockfiles, package layout, environment files, tox or nox configuration, and repository scripts.
2. Follow repository-defined commands and pinned tool versions before suggesting defaults.
3. Review idiomatic design and material hazards, especially mutable defaults, import cycles, dynamic typing gaps, async cancellation, context-manager cleanup, serialization, timezone handling, and environment drift.
4. Select proportionate gates from repository scripts, formatting, linting, static typing, unit and integration tests, package builds, and dependency or vulnerability checks when configured.
5. Review compatibility across supported Python versions, packaging metadata, public imports, typing behavior, platform wheels, database drivers, and deprecations.
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

Input: An async Python handler calls a blocking network library directly.

Output: warning: the call may block the event loop. Confirm library behavior and cancellation needs against the pinned environment before choosing a change.
