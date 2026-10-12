# State lifetime and mutation intent

Authorities: [State](https://developer.apple.com/documentation/swiftui/state), [Entry](https://developer.apple.com/documentation/swiftui/entry()), and [source compatibility](https://developer.apple.com/documentation/technotes/tn3211-resolving-swiftui-source-incompatibilities-for-state-and-contentbuilder). Reviewed 2026-10-12.

- Name the view, scene, or model that owns each value. Keep editable drafts above layout branches when they must survive a size change. Scene navigation and shared durable records have different lifetimes. [documented]
- State initialization is not synchronization with later inputs. Test recreation, explicit identity changes, and a second window separately. Do not move persistence into State. [documented]
- Xcode 27.0 compiles a declaration default followed by `self.value = value` in an initializer. Do not assert that every two-location assignment is a compiler error. This probe does not establish which value appears at runtime. Prefer one intentional initialization path and reproduce the actual failure. [verified: compile]
- A class created in an Entry default and a raw closure default produce warnings about repeated invalidation. They do not prove an infinite loop. Review stable ownership and the update graph rather than merely wrapping the value in another type. [verified: compile, Xcode 27.0]
- Injecting one Observable object is different from replacing an EnvironmentValues scalar on every gesture frame. Observation follows properties actually read; inspect those reads before moving a store. [documented]
- A cache such as CIContext needs an explicit lifetime and concurrency contract. Owning it in State may be appropriate; creating it on every body evaluation is not a measured optimization. [unverified: profile the actual path]

## Preserve binding behavior

A setter may intentionally validate, normalize, or clear an optional presentation. Replacing it with onChange can change equal-value writes, timing, and programmatic changes. Keep numeric text drafts intact until the explicit commit action. Tests must cover invalid and incomplete text, equal assignments, cancellation, and failed saves. [unverified: verify each application contract]
