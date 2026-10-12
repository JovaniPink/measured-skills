import SwiftUI
struct ToolbarView: View { var body: some View { Text("Fixture").toolbar { ToolbarItem { Button("Action") {} }.hidden() } } }
