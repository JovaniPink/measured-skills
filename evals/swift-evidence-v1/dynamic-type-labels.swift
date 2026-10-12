import SwiftUI
struct AccessibleProbe: View {
 @Environment(\.dynamicTypeSize) private var size
 @Environment(\.accessibilityReduceMotion) private var reduceMotion
 @Environment(\.accessibilityDifferentiateWithoutColor) private var differentiate
 @ScaledMetric private var symbolSize = 20.0
 var body: some View {
  Button("Add entry", systemImage: "plus") {}
   .labelStyle(.iconOnly)
   .accessibilityInputLabels(["Add entry", "New entry"])
   .overlay { if differentiate { Image(systemName: "checkmark") } }
   .animation(reduceMotion ? nil : .default, value: size)
 }
}
