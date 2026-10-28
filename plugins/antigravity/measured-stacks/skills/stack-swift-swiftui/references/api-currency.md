# Establish API compatibility

Authority: [SwiftUI source compatibility](https://developer.apple.com/documentation/technotes/tn3211-resolving-swiftui-source-incompatibilities-for-state-and-contentbuilder). Reviewed 2026-10-12.

- Record compiler, SDK, language mode, minimum OS, architecture, and each module's isolation settings separately. A deployment target is not an SDK version. [documented]
- A runtime availability branch cannot make a symbol absent from the build SDK resolve. Test both the new API and the oldest supported fallback. [verified: compile, Xcode 27.0]
- `@ContentBuilder` and private `@State` compile with Swift 5 mode and an iOS 17.6 target using Xcode 27.0. This does not establish old-OS runtime behavior. Existing `@ViewBuilder` code need not change just for spelling. [verified: compile]
- Diagnose concrete builder failures: overloaded ShapeStyle expressions, nested concrete tuple constraints, MapKit empty content, and deeply branching Charts. Use the correction for the actual diagnostic. [documented]
- SDK attributes such as `deprecated: 100000.0` describe future deprecation and may produce no warning. The local `foregroundColor` probe is warning-free; this is not evidence that every call must be rewritten. [verified: SDK inspection and compile]
- Prefer a supported replacement when it preserves semantics and removes a real compatibility or maintenance problem. Keep appropriate old-target APIs when the replacement raises the required OS. [unverified: project decision]

The repository-level SDK inventory records direct attributes and exact interface hashes. It does not resolve inherited availability, conditional compilation, Objective-C declarations, or binary-only symbols. Treat it as a search index, not a complete API oracle.

## Concrete replacements

This authored table uses the installed SDK's migration messages and declaration
availability, not a generated completeness claim. Recheck the exact overload.
`deprecated: 100000.0` is a future marker; `onChange` below is ordinarily deprecated.

| Existing use | Candidate replacement | Compatibility and semantic check |
| --- | --- | --- |
| `foregroundColor(.teal)` | `foregroundStyle(.teal)` | View modifier iOS 15; Text-returning overload iOS 17. Preserve inheritance when the old color is nil. |
| `accentColor(color)` | `tint(color)` or the asset catalog accent | iOS 15 for tint; check controls and inherited accent behavior. |
| `cornerRadius(radius)` | `clipShape(RoundedRectangle(cornerRadius: radius))` | iOS 13; preserve the intended rounding and antialiasing. The inspected SDK defaults both RoundedRectangle and `.rect(cornerRadius:)` to continuous; explicitly select style when matching older rendering. |
| `NavigationView` | `NavigationStack` or `NavigationSplitView` | iOS 16; choose stack versus columns, then verify path, selection, dismissal and restoration. |
| `onChange(of:perform:)` with one argument | zero- or two-argument `onChange(of:)` | iOS 17; retain equal-write and effect timing contracts; this does not replace custom Binding setters. |
| `.tabItem { ... }` | `Tab` declarations inside `TabView` | iOS 18; retain supported tabItem below 18, or gate a separately tested hierarchy. Preserve selection types and tags. |

The old declarations and replacement floors were inspected on Xcode 27.0. The
`api-replacements` probe checks the compatible examples at iOS 17.6 / Swift 5;
`old-target-tab-rejected` and `old-target-tab-fallback` cover the Tab boundary.
These are compiler checks, not evidence of equivalent navigation or styling.
[verified: SDK inspection; see dated compile receipts for execution status]

```swift
Text("Current week")
    .foregroundStyle(.secondary)
    .padding()
    .background(.thinMaterial)
    .clipShape(RoundedRectangle(cornerRadius: 12))
```

For a builder error, reduce the failing expression first. A concrete return type
such as `TupleView` is more brittle than `some View`; an explicit `EmptyView()`
can disambiguate an empty Group when MapKit is imported. Keep Charts mark-building
in a function returning `some ChartContent` when deep branches fail at an older
deployment target. Do not replace every builder or raise the target to hide the
error. [documented: TN3211; original positive/negative probes]
