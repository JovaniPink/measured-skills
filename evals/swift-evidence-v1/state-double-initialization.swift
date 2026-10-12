import SwiftUI
struct DoubleInitialization: View {
 @State private var value = 1
 init(value: Int) { self.value = value }
 var body: some View { Text(value, format: .number) }
}
