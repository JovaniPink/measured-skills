---
name: stack-swift-swiftui
description: "Reviews Swift and SwiftUI changes when state, identity, layout, concurrency, or SDK compatibility need focused checks; separates compiler, simulator, device, and release evidence."
license: MIT
metadata:
  author: "Measured Studios"
  version: "0.19.0"
  plugin: "measured-stacks"
  invocation: "implicit"
  provenance: "original"
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

- [API currency](references/api-currency.md): replacement table, minimum OS, SDK availability, and concrete builder diagnostics.
- [State and environment](references/state-and-environment.md): initialization, retained objects, dependency reads, and Binding setter semantics.
- [Identity and collections](references/identity-and-collections.md): stable record IDs, lazy row shape, draft reordering, and accessible movement.
- [Animations](references/animations.md): synthesized versus custom interpolation, interruption, completion, and Reduce Motion.
- [Toolbars and presentation](references/toolbars-and-presentation.md): overflow, semantic action placement, keyboard access, and stable sheet ownership.
- [Adaptive layout](references/adaptive-layout.md): container sizing, optional size classes, safe areas, and scene continuity.
- [Localization](references/localization.md): extraction, generated keys, plurals, bundle lookup, and accessible copy.
- [SwiftUI performance](references/swiftui-performance.md): causal profiling, observation granularity, list construction, and image workloads.
- [Release readiness](references/release-readiness.md): built metadata, privacy, purchase qualification, and separate provider gates.
- [Folding displays](references/folding-displays.md): new-SDK qualification, reserved geometry, transition journeys, and device gaps.

Each rule carries a label. `[verified]` rules identify SDK inspection, compile, simulator, or device evidence and its toolchain; `[documented]` rules come from Apple documentation or Swift Evolution; `[unverified]` rules are review judgment. Recheck `[verified]` rules against the repository's own toolchain and deployment targets before reporting them as current.

Read [memory and lifetime diagnosis](references/memory-diagnosis.md) when allocations, retained objects, memory growth, or UI stalls need investigation.

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

Lead with the answer. Use the shortest format that retains the required evidence and limits; expand when requested or needed. The items below describe required content, not mandatory headings.

Return Discovery, Hazards, Commands selected, Results, Compatibility, Missing evidence, and Next safe gate.

## Example

Synthetic example; not an observed client result.

Input: A view loses draft input after its identity changes.

Output: Trace state ownership and identity across the transition. A stable owner may be needed; verify the actual target SDK and behavior before changing state wrappers.
