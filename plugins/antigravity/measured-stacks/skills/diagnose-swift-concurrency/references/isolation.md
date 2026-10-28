# Isolation and task diagnosis

Record SWIFT_VERSION, strict checking, default actor isolation and upcoming features per module. Nonisolated async execution depends on NonisolatedNonsendingByDefault; inspect toolchain availability before proposing @concurrent. A suspension permits actor reentrancy. Structured child cancellation differs from unstructured Task and Task.detached lifetimes; trace handles and terminal callbacks. MainActor.run may be legitimate synchronous actor-bound work: judge the actual call boundary. Do not silence transfer errors with unchecked conformance.

Authority: [Isolation and task diagnosis](https://www.swift.org/swift-evolution/). Documentation informs correctness; it is not evidence that this workflow ran successfully in an installed client.
