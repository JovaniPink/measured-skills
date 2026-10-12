# Establish API compatibility

Authority: [SwiftUI source compatibility](https://developer.apple.com/documentation/technotes/tn3211-resolving-swiftui-source-incompatibilities-for-state-and-contentbuilder). Reviewed 2026-10-12.

- Record compiler, SDK, language mode, minimum OS, architecture, and each module's isolation settings separately. A deployment target is not an SDK version. [documented]
- A runtime availability branch cannot make a symbol absent from the build SDK resolve. Test both the new API and the oldest supported fallback. [verified: compile, Xcode 27.0]
- `@ContentBuilder` and private `@State` compile with Swift 5 mode and an iOS 17.6 target using Xcode 27.0. This does not establish old-OS runtime behavior. Existing `@ViewBuilder` code need not change just for spelling. [verified: compile]
- Diagnose concrete builder failures: overloaded ShapeStyle expressions, nested concrete tuple constraints, MapKit empty content, and deeply branching Charts. Use the correction for the actual diagnostic. [documented]
- SDK attributes such as `deprecated: 100000.0` describe future deprecation and may produce no warning. The local `foregroundColor` probe is warning-free; this is not evidence that every call must be rewritten. [verified: SDK inspection and compile]
- Prefer a supported replacement when it preserves semantics and removes a real compatibility or maintenance problem. Keep appropriate old-target APIs when the replacement raises the required OS. [unverified: project decision]

The repository-level SDK inventory records direct attributes and exact interface hashes. It does not resolve inherited availability, conditional compilation, Objective-C declarations, or binary-only symbols. Treat it as a search index, not a complete API oracle.
