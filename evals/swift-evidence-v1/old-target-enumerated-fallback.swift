import SwiftUI
struct Row: Identifiable { let id: Int }
struct Rows: View { let rows: [Row]; var body: some View {
 ForEach(Array(rows.enumerated()), id: \.element.id) { entry in Text("\(entry.offset)") }
} }
