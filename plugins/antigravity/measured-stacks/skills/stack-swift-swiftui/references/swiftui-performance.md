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

## Decide from a trace

| Observation | Next discriminating check | Avoid concluding |
| --- | --- | --- |
| Many body evaluations | which changed property each body reads | every environment-injected model broadcasts all changes |
| One slow update | sampled stack, allocation and synchronous work | a new state framework is necessary |
| List hitch on insertion | row cardinality, identity, image decode | every conditional is slow |
| Warm image still loads | request headers, cache policy and server request count | URLCache alone proves AsyncImage caching |

A small simulator experiment found that mutating an unread observed property did
not reevaluate the measured child, whereas a read property did. Preserve this
bounded result: it is not an Instruments trace or a claim about a whole app.
[verified: simulator, Xcode 27.0 / iOS 27.0]

## Read an Instruments capture before choosing a repair

The official [Markdown guide](https://developer.apple.com/documentation/xcode/understanding-and-improving-swiftui-performance.md)
was inspected on 2026-10-28. Locate the affected interaction on the SwiftUI track,
then distinguish a slow update from many individually cheap updates. Use Time
Profiler samples to inspect synchronous work and the cause graph to inspect update
triggers. A displayed dependency is evidence about that capture, not all possible
causes. If samples are insufficient, retain uncertainty rather than invent a stack.
[documented]

Synthetic fixture, not a captured run: a search edit precedes repeated list updates,
while a supplied sample points to synchronous formatting. Investigate both update
frequency and formatting cost, preserve the search/error behavior, and recapture
the same interaction after a change. This fixture proves neither a performance
improvement nor device acceptance. [unverified: synthetic example]
