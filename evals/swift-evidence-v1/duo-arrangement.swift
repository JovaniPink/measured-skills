import SwiftUI
struct FoldingView: View { var body: some View { ArrangementView { Text("First"); Text("Second") }.arrangementViewStyle(.split) } }
