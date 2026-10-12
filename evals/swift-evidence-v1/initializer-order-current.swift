import SwiftUI
struct Editor: View {
 let title: String
 @State private var count: Int
 init(_ title: String) { self.count = 3; self.title = title }
 var body: some View { Text(title) }
}
