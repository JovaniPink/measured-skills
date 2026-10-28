# Focused checks

Primary documentation: [official Swift and SwiftUI Engineering Profile reference](https://docs.swift.org/latest/documentation/). Verify version-sensitive behavior against the repository's pinned toolchain.

## Discovery

Inspect `Package.swift`, Xcode projects or workspaces, schemes, package resolution, deployment targets, and repository scripts. Resolve nested modules, workspaces, generated sources, and CI commands before selecting gates.

## Judgment focus

Review actor isolation, `Sendable` gaps, retain cycles, value versus reference semantics, optionals, task cancellation, view identity, state ownership, and main-thread work.

## Gate families

Consider repository scripts, formatting or linting, Swift package tests and builds, selected Xcode scheme tests, static analysis, and simulator or device checks when available. Run only commands supported by repository evidence and the current authorization boundary.

## Compatibility

Check Swift language mode, package versions, OS deployment targets, availability annotations, data migrations, and SwiftUI behavior across supported devices. Record unavailable tools and environments explicitly; never manufacture a passing result.


## Scope and semantic evidence

This profile selects read-only checks. Do not run global mutating formatters or automatic fixes. For a separately authorized change, derive an explicit path set from the task and repository rules, including approved new files. Git diff is evidence of existing changes, not the complete authority boundary. Exclude generated and vendor paths; an empty operation scope returns no action needed. Verify final changed paths.

Resolve pinned tools through repository scripts and PATH, then documented local locations when needed. Report the exact locations checked if unavailable. Do not install or upgrade a missing tool to manufacture evidence.

Capture each target's effective language mode, default actor isolation, upcoming features, deployment target, and toolchain. SourceKit-LSP diagnostics require matching build settings and current modules; compiler builds and runtime tests remain separate. Prefer declared actor isolation over blanket MainActor.run wrappers, but do not mechanically replace a synchronous actor hop with an await. Review the actual isolation contract.

Reject blanket unchecked Sendable fixes without an independently justified synchronization contract. Test cancellation, actor reentrancy, task inheritance, and API availability; a clean compiler does not prove every logical invariant.
