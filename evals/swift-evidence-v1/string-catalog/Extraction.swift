import SwiftUI

struct ExtractionFixture: View {
    var body: some View {
        VStack {
            Text("Inventory")
            Text(verbatim: "Synthetic diagnostic")
            Text(String(localized: "Available items", comment: "Synthetic status label"))
        }
    }
}
