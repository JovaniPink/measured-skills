# Swift concurrency in Swift 6.2 and later

Evidence labels: [verified] means compiled or run with Xcode 27.0 (Swift 6.4) on 2026-09-22. [documented] means stated in a Swift Evolution proposal or Apple documentation but not executed here. [unverified] means review judgment.

Authorities: Swift Evolution proposals SE-0304 (structured concurrency), SE-0306 (actors), SE-0461 (nonisolated async functions on the caller's actor), SE-0466 (default actor isolation), SE-0470 (isolated conformances), and SE-0472 (`Task.immediate`), listed on the [Swift Evolution dashboard](https://www.swift.org/swift-evolution/).

## Read the settings for each module first

Concurrency behavior depends on per-module settings. Review each target on its own.

| Setting | Where | Effect |
| --- | --- | --- |
| Language mode | `SWIFT_VERSION`, `swiftLanguageModes` | Swift 6 turns data-race checks into errors |
| Default isolation | `SWIFT_DEFAULT_ACTOR_ISOLATION`, `.defaultIsolation(MainActor.self)` | unannotated code becomes main-actor isolated |
| Approachable Concurrency | `SWIFT_APPROACHABLE_CONCURRENCY` | turns on several upcoming features |

- Xcode 27 app templates set default isolation to `MainActor` and Approachable Concurrency to `YES`. The base project settings still set `SWIFT_VERSION` to 5.0. [verified in the installed templates]
- Approachable Concurrency enables `NonisolatedNonsendingByDefault`, `InferIsolatedConformances`, `InferSendableFromCaptures`, `GlobalActorIsolatedTypesUsability`, and `DisableOutwardActorInference`. [verified in the installed build settings]
- Swift packages default to `nonisolated`. `.defaultIsolation(MainActor.self)` works per target with tools version 6.2. [verified]
- A module's default isolation applies to its public API. Another module calling that API from nonisolated code gets a compile error. [verified]

## Where a `nonisolated async` function runs

| Mode | Runs on |
| --- | --- |
| `NonisolatedNonsendingByDefault` on | the caller's actor [verified] |
| Swift 6 or Swift 5 mode without that feature | the global concurrent executor [verified] |
| `nonisolated(nonsending)` spelled out | the caller's actor, in either mode [verified] |
| `@concurrent` | the global concurrent executor, in either mode [verified] |

- Before accepting a claim that code "runs off the main actor," confirm the feature setting for that module.
- Mark CPU-heavy async work `@concurrent` so it leaves the caller's actor. `@concurrent` on a synchronous function is a compile error. [verified]
- Use `extension Model: @MainActor SomeProtocol` for a conformance that only holds on the main actor. [verified compiles]

## Reentrancy

- Actor state can change at every `await`. In a test, two concurrent withdrawals that checked the balance before an `await` and subtracted after it both succeeded, leaving a negative balance. [verified]
- Fix it by checking and changing state with no suspension in between, or by checking again after the `await`. The re-check version kept the balance correct. [verified]
- Main-actor code is reentrant in the same way. Review any check, then `await`, then act sequence in view models. [unverified]

## Cancellation

- Canceling a parent task cancels `async let` children and task-group children. [verified]
- An unstructured `Task { }` does not see its creator's cancellation. In the test it ran to completion after the outer task was canceled. Keep its handle and cancel it yourself. [verified]
- `Task.detached` does not inherit actor isolation or task-local values, and it is not canceled with its creator. Keep its handle. [documented]
- Use `withTaskCancellationHandler` to stop callback-based work. The handler runs right away on cancellation, even if the operation never checks. It can run at the same time as the operation, so it must be safe to call from any context. [documented]

## Other checks

- `Task.immediate` needs iOS 26 or later. [verified]
- `MainActor.assumeIsolated` traps when the assumption is wrong. Prefer an isolation annotation. [documented]
- `Thread.isMainThread` is unavailable in async contexts in Swift 6 mode. Use isolation annotations or `MainActor.assertIsolated()`. [verified]
