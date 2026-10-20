import SwiftUI
struct MotionProbe: View {
 var body: some View { Text("Motion").environment(\.accessibilityReduceMotion, true) }
}
