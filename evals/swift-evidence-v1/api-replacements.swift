import SwiftUI
struct CurrencyProbe: View {
    @State private var count = 0
    var body: some View {
        NavigationStack {
            Text("Current week")
                .foregroundStyle(.secondary)
                .padding()
                .background(.thinMaterial)
                .clipShape(RoundedRectangle(cornerRadius: 12))
                .tint(.teal)
                .onChange(of: count) { _, _ in }
        }
    }
}
