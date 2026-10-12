# Motion with a testable purpose

Authority: [Animatable](https://developer.apple.com/documentation/swiftui/animatable). Reviewed 2026-10-12.

- The Animatable macro and AnimatableIgnored compile with the installed Xcode 27.0 SDK. Check compiler and runtime availability for each supported build. [verified: compile]
- Keep manual animatableData when the setter intentionally clamps, normalizes, or derives values. Macro synthesis is not equivalent to every custom interpolation. [documented]
- Use completion semantics when a second operation depends on animation completion. Fixed delays are not proof of completion; cancellation and repeated taps can invalidate the assumed sequence. [documented]
- Keep required information available with Reduce Motion and during interrupted transitions. Do not put persistence or authorization exclusively in a visual completion callback. [unverified: application contract]
- Compare scrollTransition or visualEffect with state-driven geometry updates only when a measured hot path exists. Verify hit testing, focus, and visual continuity after the change. [unverified: runtime]
