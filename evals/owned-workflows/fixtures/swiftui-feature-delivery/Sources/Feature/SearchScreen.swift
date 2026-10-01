import SwiftUI
struct SearchScreen: View {
    @State private var query = ""
    let items: [String]
    var body: some View { List(items, id: \.self) { Text($0) } }
}
