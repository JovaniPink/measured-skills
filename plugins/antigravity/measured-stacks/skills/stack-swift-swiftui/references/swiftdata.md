# SwiftData, CloudKit, and predicates

Evidence labels: [verified] means compiled or run with Xcode 27.0 (Swift 6.4, macOS 27.0 SDK) on 2026-09-22. [documented] means stated in the linked Apple documentation but not executed here. [unverified] means review judgment; confirm it in the project.

Authorities: [Syncing model data across a person's devices](https://developer.apple.com/documentation/swiftdata/syncing-model-data-across-a-persons-devices), [Creating a Core Data model for CloudKit](https://developer.apple.com/documentation/coredata/creating-a-core-data-model-for-cloudkit), and the SwiftData interface in the installed SDK.

## CloudKit-compatible models

Check every `@Model` type when any `ModelConfiguration` uses a CloudKit database. The first three rules fail at store load with `NSCocoaErrorDomain` code 134060. [verified]

- No unique constraints. Both `@Attribute(.unique)` and `#Unique` are rejected. [verified]
- Every stored property is optional or has a default value. [verified]
- Every relationship is optional. [verified]
- No `.deny` delete rule. [documented]
- Give each relationship an inverse. Set it explicitly when SwiftData cannot infer it, because records can arrive out of order. [documented]
- After the CloudKit schema is promoted to production, it is additive only. You cannot delete a model type or change an existing attribute. [documented]
- Sync needs the iCloud capability with a CloudKit container and the Background Modes capability with remote notifications. [documented]

What was not proven: a compliant model loads with a CloudKit configuration, but no sync ran because the test process had no entitlements. [verified load only] A command-line process logs the incompatibility and then aborts for a missing bundle identifier. Run schema checks from an app-hosted test target. [unverified]

## Unique constraints without CloudKit

Inserting a second model with the same unique value updates the existing row instead of failing. The in-memory test ended with one row holding the newer value. [verified] Review any code that expects an insert to reject duplicates.

## Predicate pitfalls

| Pattern in `#Predicate` | Result |
| --- | --- |
| Global or custom function call | compile error [verified] |
| `lowercased()` and similar String methods | compile error; `localizedStandardContains` works [verified] |
| Enum case literal such as `.walk` | compile error "key path cannot refer to enum case" [verified] |
| Property of a captured non-model struct | compile error; copy it to a local `let` first [verified] |
| Captured local constant | works [verified] |
| Optional chain such as `$0.owner?.name == name` | works [verified] |
| Computed, non-stored property | compiles, then traps at fetch with "Couldn't find" key path [verified] |

- The computed-property case is the most dangerous because the compiler accepts it and the app crashes at run time. Require a test that executes every predicate against a real container. [verified]
- A captured enum value worked at run time on macOS 27. Older OS versions were not tested. Storing the raw value is the most portable choice. [unverified]

## Concurrency

- `ModelContext` is explicitly not `Sendable`: "contexts cannot be shared across concurrency contexts." [verified]
- `PersistentIdentifier` is `Sendable`. Pass identifiers between actors and fetch again on the other side. [verified]
- Use `@ModelActor` for background import or processing. [verified compiles]
- The container's `mainContext` belongs to the main actor. [documented]

## Schema migrations

- Version shipped schemas with `VersionedSchema` and a `SchemaMigrationPlan`. [verified compiles]
- In Swift 6 mode, `static var versionIdentifier` is a compile error for global mutable state. Declare it `static let`. [verified]

## Tests

- `ModelConfiguration(isStoredInMemoryOnly: true)` gives an isolated store for unit tests. [verified]
- In-memory tests do not exercise CloudKit rules or file-based migration. Report those as untested unless a separate test covers them.
