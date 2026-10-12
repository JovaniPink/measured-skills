import SwiftUI
@Observable @MainActor final class Draft { var value = ""; var writes = 0
 var binding: Binding<String> { Binding(get: { self.value }, set: { self.value = $0; self.writes += 1 }) }
}
