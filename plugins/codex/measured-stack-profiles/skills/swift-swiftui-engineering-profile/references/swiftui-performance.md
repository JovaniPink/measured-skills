# Attribute performance to a measured cause

Authority: [Understanding SwiftUI performance](https://developer.apple.com/documentation/xcode/understanding-and-improving-swiftui-performance). Reviewed 2026-10-12.

- Record release/debug configuration, device, OS, data volume, interaction, power and thermal conditions, and refresh-rate behavior. Simulator traces cannot establish physical-device frame rate or energy cost. [documented]
- Inspect both expensive updates and excessive update frequency. Changing a broad value-type property can invalidate readers even when their displayed field did not change. Narrow inputs or observation only after tracing that dependency. [documented]
- A one-to-three-field threshold is a heuristic, not a universal rule. Splitting models may increase mutation and synchronization complexity; preserve one owner. [unverified: design judgment]
- Isolate onChange-only reads when a trace shows they invalidate an expensive parent. Test setter/event semantics before moving the effect. [unverified: runtime]
- Profile list row cardinality, image decoding, work before the first await, formatting, and repeated sorting at the actual hotspot. Do not replace GeometryReader or UIKit interop solely because a search found them. [unverified: diagnosis]
- asyncImageURLSession compiles on iOS 27. Test HTTP headers, request policies, cold/warm loads, failures, cancellation, and cache eviction before claiming image caching works for the app. [verified: compile; caching unverified]
- Compare the same workload before and after, with three repeated cold/warm runs. Repetition is stability evidence, not a large statistical sample. Report raw measurements and uncertainty. [unverified: measurement protocol]
- At 120 Hz a nominal frame is 8.33 ms; at 60 Hz it is 16.67 ms. These are whole-frame intervals, not universal body budgets or guarantees that a device maintains that rate. [documented]
