import SwiftUI
struct ToolbarView: View {
 var body: some View { Text("Fixture").toolbar {
  ToolbarItem(placement: .topBarPinnedTrailing) { Button("Save") {} }.visibilityPriority(.high)
  ToolbarOverflowMenu { Button("Export") {} }
 }.toolbarMinimizationBehavior(.onScrollDown) }
}
