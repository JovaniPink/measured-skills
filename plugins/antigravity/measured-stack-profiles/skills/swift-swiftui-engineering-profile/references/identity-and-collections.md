# Identity, row construction, and movement

Authorities: [ForEach](https://developer.apple.com/documentation/swiftui/foreach), [ReorderDifference](https://developer.apple.com/documentation/swiftui/reorderdifference), and [SwiftUI performance](https://developer.apple.com/videos/play/wwdc2025/306/). Reviewed 2026-10-12.

- Identify records independently of position and display text when users can insert, delete, filter, or move them. Do not allocate a new ID during rendering. Position can remain appropriate for a truly immutable numbered sequence. [documented]
- Distinguish conditional styling from a deliberate change of hierarchy. For styling, stable modifier types can preserve the intended view identity; AnyShapeStyle can reconcile unlike styles without erasing the view. [verified: compile]
- In lazy containers, review whether the number of views produced by an element is knowable without building every row. A container around conditional content can help, but may also change spacing and accessibility. Measure before applying it throughout a codebase. [documented]
- Treat `-LogForEachSlowPath YES` as a version-sensitive diagnostic aid. Confirm its output on the selected OS; an empty log alone cannot prove a fast path. [unverified: runtime]
- Reorder containers and ScrollView swipe containers compile for iOS 27. They require availability checks below that target. Existing List editing is still valid. [verified: compile]
- Apply move intent in the draft or authoritative mutation owner, never in a second unsynchronized copy. Preserve record IDs, draft fields, focus, and selection. Commit order only at the product's save boundary. [unverified: application contract]
- Define behavior for first/last moves, empty input, invalid IDs, stale snapshots, duplicate IDs, multi-section moves, no-ops, and canceled drags. Reject ambiguous identity rather than moving the wrong item. [unverified: application contract]
- Provide operable move actions for users who cannot drag. Verify accessibility order after the move and persistence after reopening. [documented]

## Review a move as a transaction

1. Locate source and destination by stable ID in the current draft snapshot.
2. Reject missing or duplicate IDs. Treat a same-position move as a no-op.
3. Move the complete draft, including incomplete numeric strings, without
   regenerating IDs. A duplicated record instead needs a new ID.
4. Keep focus and selection attached to identity; explicitly define deletion
   fallback when that identity disappears.
5. Save through the current mutation owner; on failure preserve the draft, and
   on Cancel leave the durable snapshot unchanged.

This is an application contract, not a claim about ReorderDifference semantics.
Native differences need separate stale-snapshot and cross-section tests before
using them as persistence commands. [unverified: per-application behavior]

A row wrapper stabilizes cardinality only at the lazy container boundary where
it is inserted. Compare `ForEach(items) { Row(item: $0) }` with conditional output
at that boundary; putting a Group around branches does not necessarily create a
layout node. Verify row construction and accessibility instead of mechanically
adding stacks. [documented: performance authority; runtime cost unverified]
