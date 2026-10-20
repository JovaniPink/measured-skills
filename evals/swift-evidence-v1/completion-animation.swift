import SwiftUI
struct AnimatedView: View {
 @State private var expanded = false
 @State private var finished = false
 var body: some View { Button("Animate") { withAnimation { expanded.toggle() } completion: { finished = true } } }
}
