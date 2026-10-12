import SwiftUI
struct AdaptiveView: View {
 var body: some View {
  if #available(iOS 26, *) { Text("Content").safeAreaBar(edge: .bottom) { Button("Continue") {} } }
  else { Text("Content").safeAreaInset(edge: .bottom) { Button("Continue") {} } }
 }
}
