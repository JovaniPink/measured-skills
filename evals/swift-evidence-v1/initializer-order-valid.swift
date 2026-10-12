import SwiftUI
struct Editor: View {
 let title: String
 @State private var count: Int
 init(_ title: String) { self.title = title; self.count = 3 }
 var body: some View { Text("\(title): \(count)") }
}
