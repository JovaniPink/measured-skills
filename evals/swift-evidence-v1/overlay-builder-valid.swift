import SwiftUI
struct OverlayProbe: View {
 var body: some View { Text("Fixture").overlay { Color.indigo.opacity(0.4).blendMode(.multiply) } }
}
