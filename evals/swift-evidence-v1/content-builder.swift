import SwiftUI
struct BuilderView: View {
 @ContentBuilder var content: some View { Text("First"); Text("Second") }
 var body: some View { VStack { content } }
}
