import SwiftUI
struct Row: Identifiable { let id: Int }
struct ReorderView: View { var body: some View { Text("Rows").reorderContainer(for: Row.self) { _ in } } }
