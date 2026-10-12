import SwiftUI
struct Row: Identifiable { let id: Int; var title: String }
struct ReorderView: View {
 let rows = [Row(id: 1, title: "One")]
 var body: some View {
  ScrollView {
   LazyVStack { ForEach(rows) { row in Text(row.title).swipeActions { Button("Remove") {} } }.reorderable() }
  }.reorderContainer(for: Row.self) { _ in }.swipeActionsContainer()
 }
}
