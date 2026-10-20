import SwiftUI
struct TabProbe: View {
 var body: some View {
  if #available(iOS 18, *) { TabView { Tab("One", systemImage: "1.circle") { Text("One") } } }
  else { TabView { Text("One").tabItem { Label("One", systemImage: "1.circle") } } }
 }
}
