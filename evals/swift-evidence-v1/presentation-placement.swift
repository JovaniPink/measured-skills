import SwiftUI
struct SheetView: View {
 @State private var shown = false
 var body: some View { Button("Show") { shown = true }.sheet(isPresented: $shown) { Text("Sheet").presentationPlacement(.trailing) } }
}
