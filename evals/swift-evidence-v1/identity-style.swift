import SwiftUI
struct HighlightView: View {
 @State private var highlighted = false
 var body: some View { TextField("Value", text: .constant("Draft")).background(highlighted ? AnyShapeStyle(.thinMaterial) : AnyShapeStyle(.clear)) }
}
