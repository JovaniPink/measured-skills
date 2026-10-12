# SwiftUI data flow and modern APIs

Evidence labels: [verified] means compiled or run with Xcode 27.0 (Swift 6.4, iOS 27.0 SDK) on 2026-09-22. [documented] means stated in the linked Apple documentation but not executed here. [unverified] means review judgment; confirm it in the project before reporting it as fact.

Authorities: [Managing model data in your app](https://developer.apple.com/documentation/swiftui/managing-model-data-in-your-app), [Migrating to the Observable macro](https://developer.apple.com/documentation/swiftui/migrating-from-the-observable-object-protocol-to-the-observable-macro), [State()](https://developer.apple.com/documentation/swiftui/state()), [Bindable](https://developer.apple.com/documentation/swiftui/bindable), and the SwiftUI interface in the installed SDK.

## Pick one owner for each piece of state

| Situation | Declaration |
| --- | --- |
| Value owned by this view | `@State private var` |
| Observable model created by this view | `@State private var model = Model()` |
| Model passed in, view needs bindings | `@Bindable var model: Model` |
| Model passed in, read only | plain `let` or `var` property |
| Model shared down a subtree | `.environment(model)` and `@Environment(Model.self)` |

- Apply the `@Observable` macro. Conforming to the `Observable` protocol alone adds no tracking. [documented]
- A view updates only when `body` reads a property that changes. Values read only inside a later closure, such as a button action, do not create a dependency. [documented]
- Mark caches and other non-display properties `@ObservationIgnored`. [documented]
- To get bindings from an environment model, declare `@Bindable var model = model` inside `body`. [documented]
- Treat a mix of `ObservableObject` and `@Observable` types as a behavior difference to review. The older system updates on any published change; Observation updates only on properties `body` reads. [documented]
- `@Observable` needs iOS 17, macOS 14, or later. Check the deployment target before recommending it. [documented]

## Xcode 27 changed `@State`

- With Xcode 27, `@State` expands to the `State()` macro, even at an iOS 17 deployment target. The expansion wraps the default value in a closure. [verified]
- Apple documents that the macro creates the default value the first time SwiftUI creates the view. The older property wrapper created it on every view initialization. [documented] Whether older OS versions get the lazy behavior at run time was not tested. [unverified]
- `_value = State(initialValue: x)` inside `init` still compiles under the macro. [verified]
- Keep state initializers free of side effects. A project that also builds with Xcode 26 or earlier still gets eager creation. [documented]

## Environment values

- Declare custom values with `@Entry` in an `EnvironmentValues` extension instead of a hand-written key type. [verified]

## API currency

Use the API currency reference linked from the skill entrypoint for silent deprecations, compiler/SDK versus runtime availability, and builder compatibility. A warning-free build does not establish current API use.

## Navigation and empty states

- Use `NavigationStack(path:)` with value-based `navigationDestination(for:)`. [verified]
- Use `ContentUnavailableView` for empty and error states on iOS 17 or later. [verified]
- `#Preview` with `@Previewable @State` compiles for local preview state. [verified]

## Async work tied to a view

- Put view-lifetime work in `.task` or `.task(id:)`. SwiftUI cancels it when the view goes away or the `id` changes. [documented]
- The current `.task` documentation says the task starts with `Task.immediate`. Code before the first `await` runs synchronously on the main actor. [documented] Keep that prefix short. Runtime timing was not measured. [unverified]
- A `Task { }` started in `onAppear` is not canceled with the view. Unstructured tasks ignore the cancellation of their surroundings (see the concurrency reference). [verified for tasks; SwiftUI lifetime unverified]
- `Task.immediate` needs iOS 26 or later. [verified]
