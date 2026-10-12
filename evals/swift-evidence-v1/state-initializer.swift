import SwiftUI
struct InitialValueView: View {
 @State private var count: Int
 init(value: Int) { _count = State(initialValue: value) }
 var body: some View { Text(count, format: .number) }
}
