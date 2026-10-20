import SwiftUI
struct LayoutView: View {
 @Environment(\.horizontalSizeClass) private var horizontal
 var body: some View { ViewThatFits { HStack { Text(horizontal == .regular ? "Wide" : "Narrow"); Button("Continue") {} }; ScrollView { VStack { Text("Content"); Button("Continue") {} } } }
}
}
