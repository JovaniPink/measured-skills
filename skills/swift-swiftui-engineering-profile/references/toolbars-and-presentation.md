# Actions in constrained space

Authority: [Toolbars](https://developer.apple.com/documentation/swiftui/toolbars). Reviewed 2026-10-12.

| Capability | Installed SDK evidence |
| --- | --- |
| ToolbarOverflowMenu, visibilityPriority, topBarPinnedTrailing | iOS 27 availability; compile probe passes |
| toolbarMinimizationBehavior, contentMarginsRemoved | iOS 27 SDK declarations; minimization probe passes |
| presentationPlacement | iOS 27 declaration and compile probe |
| ToolbarItem hidden | Unavailable for iOS in Xcode 27.0; negative compile probe passes |

These are [verified: SDK inspection or compile] results, not interaction evidence.

Choose semantic placements based on the action's purpose. Test which actions overflow at the smallest supported width and largest text size. A pinned item consumes scarce space; do not pin every action or remove readable labels to make a crowded bar fit. [unverified: design and runtime]

Attach presentation to a stable owner. Test optional-item dismissal, selection changes while a sheet is open, keyboard obstruction, restoration, and cancellation. An inspector, trailing presentation, and modal sheet have different navigation and accessibility consequences. [unverified: runtime]

Use system status-bar visibility only when the product benefits, and verify that required context and dismissal remain available. Keep future SDK experiments out of the supported build until positive and negative availability probes pass. [unverified: application decision]

## Test actions where they are used

Keep destructive confirmation and editor Save attached to the edited record,
not to an unrelated global toolbar owner. A selected-item sheet should clear or
retain selection according to the product contract when dismissed. Move focus
intentionally before a keyboard-dependent action disappears. [unverified:
application semantics]

Verify each essential action in a narrow layout, with long translated labels,
with the keyboard open, and at accessibility text sizes. Inspect overflow and
VoiceOver order; an item existing in the hierarchy does not establish that it is
reachable. A keyboard toolbar and a top-bar action have different lifetimes, so
switching placement requires an end-to-end editing check. [unverified: runtime]
