import SwiftUI
struct EmptyScreen: View {
    let retry: () -> Void
    var body: some View { Image(systemName: "arrow.clockwise").onTapGesture(perform: retry) }
}
