---
name: swift-swiftui-engineering-profile
description: Apply focused Swift and SwiftUI engineering judgment after repository gate discovery. Use for packages, applications, SwiftUI data flow, SwiftData and CloudKit models, Swift 6 concurrency and actor isolation, Swift Testing, iOS accessibility, HealthKit authorization, compatibility, and builds; require observed macOS evidence for Apple toolchain claims.
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.17.1"
  plugin: "measured-stack-profiles"
  invocation: "implicit"
  provenance: "clean-room"
  risk_class: "read-only"
---

# Swift and SwiftUI Engineering Profile

Use this profile only after repository discovery identifies the stack. Read [focused checks](references/checks.md) when stack-specific gates or hazards determine the result.

## Focused references

Read only the reference that matches the code under review:

- [SwiftUI data flow and modern APIs](references/swiftui.md): state ownership, Observation, the Xcode 27 `@State` macro, silent deprecations, and view tasks.
- [SwiftData](references/swiftdata.md): CloudKit-compatible models, unique constraints, predicate pitfalls, model concurrency, and migrations.
- [Swift concurrency](references/concurrency.md): per-module default isolation, where `nonisolated async` code runs, `@concurrent`, reentrancy, and cancellation.
- [Swift Testing](references/swift-testing.md): parallel runs, suites, expectations, parameterized tests, and isolation.
- [iOS accessibility](references/ios-accessibility.md): Dynamic Type, VoiceOver labels on custom controls, Reduce Motion, Differentiate Without Color, and touch targets.
- [HealthKit](references/healthkit.md): just-in-time authorization, private read status, limited history, and denied states.

Each rule carries a label. `[verified]` rules were compiled or run with one Xcode 27.0 toolchain; `[documented]` rules come from Apple documentation or Swift Evolution; `[unverified]` rules are review judgment. Recheck `[verified]` rules against the repository's own toolchain and deployment targets before reporting them as current.

## Workflow

1. Discover `Package.swift`, Xcode projects or workspaces, schemes, package resolution, deployment targets, and repository scripts.
2. Follow repository-defined commands and pinned tool versions before suggesting defaults.
3. Review idiomatic design and material hazards, especially actor isolation, `Sendable` gaps, retain cycles, value versus reference semantics, optionals, task cancellation, view identity, state ownership, and main-thread work. Read each module's language mode, default isolation, and upcoming-feature settings before judging where async code runs.
4. Select proportionate gates from repository scripts, formatting or linting, Swift package tests and builds, selected Xcode scheme tests, static analysis, and simulator or device checks when available.
5. Review compatibility across Swift language mode, package versions, OS deployment targets, availability annotations, data migrations, and SwiftUI behavior across supported devices.
6. Report every missing tool, skipped command, unsupported platform, or unavailable environment as incomplete rather than passing.

## Boundaries

- Do not invent one universal command or replace repository policy with generic preferences.
- Do not install, upgrade, publish, deploy, apply, or mutate shared state merely to run a gate.
- Separate static review, executed checks, build evidence, provider state, and live behavior.
- Do not change entitlements, capabilities, signing, HealthKit authorization, or CloudKit schemas to make a check pass. Report the gap and name who can approve the change.

## Output

Return Discovery, Hazards, Commands selected, Results, Compatibility, Missing evidence, and Next safe gate.

