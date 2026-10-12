import SwiftUI
import Observation

// Synthetic fixtures only. Results describe this simulator run, not an app release.
@main
struct EvidenceApp: App {
    var body: some Scene { WindowGroup { EvidenceView() } }
}

@MainActor @Observable
final class RetainedToken { let value = UUID() }

struct ResultRow: Codable {
    let id: String
    let status: String
    let observed: String
}

@MainActor @Observable
final class Recorder {
    var identities: [Int: UUID] = [:]
    var sizes: [Int: CGSize] = [:]
    var rows: [ResultRow] = []
    var finished = false

    func check(_ id: String, _ condition: Bool, _ observed: String) {
        rows.append(ResultRow(id: id, status: condition ? "passed" : "failed", observed: observed))
    }

    func waitFor(_ predicate: () -> Bool) async -> Bool {
        for _ in 0..<100 {
            if predicate() { return true }
            try? await Task.sleep(for: .milliseconds(50))
        }
        return predicate()
    }

    func save() {
        finished = true
        do {
            let folder = URL.documentsDirectory
            let encoder = JSONEncoder()
            encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
            try encoder.encode(rows).write(to: folder.appending(path: "runtime-results.json"), options: .atomic)
        } catch {
            // The runner treats a missing result file as blocked, never passed.
            print("Evidence result write failed: \(error)")
        }
    }
}

struct TokenView: View {
    @State private var token = RetainedToken()
    let step: Int
    let recorder: Recorder
    var body: some View {
        Text("Retained identity")
            .foregroundStyle(step == 0 ? Color.primary : Color.secondary)
            .task(id: step) { recorder.identities[step] = token.value }
    }
}

struct EvidenceView: View {
    @State private var recorder = Recorder()
    @State private var step = 0
    @State private var identity = 0
    @State private var sizeStep = 0
    @State private var width: CGFloat = 240
    @State private var height: CGFloat = 160
    @State private var animated = false
    @State private var animationCompleted = false
    @State private var bindingValue = 1
    @State private var setterCalls = 0
    @State private var changeCalls = 0
    @State private var changedValues: [Int] = []
    @State private var draft = ""
    @State private var saved = "original"

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                Text("Synthetic SwiftUI evidence").font(.title)
                Text("No product data, purchases, network, or live services.")
                TokenView(step: step, recorder: recorder).id(identity)
                RoundedRectangle(cornerRadius: 12)
                    .fill(.blue.opacity(0.2))
                    .frame(width: width, height: height)
                    .onGeometryChange(for: CGSize.self) { $0.size } action: { size in
                        recorder.sizes[sizeStep] = size
                    }
                Text("Completion fixture").opacity(animated ? 0.5 : 1)
                ForEach(recorder.rows, id: \.id) { row in
                    Label(row.id + ": " + row.status, systemImage: row.status == "passed" ? "checkmark.circle" : "xmark.circle")
                }
                Text(recorder.finished ? "Finished" : "Running")
            }.padding()
        }
        .onChange(of: bindingValue) { _, value in
            changeCalls += 1
            changedValues.append(value)
        }
        .task { await run() }
    }

    private func run() async {
        let initialReady = await recorder.waitFor { recorder.identities[0] != nil && recorder.sizes[0] != nil }
        step = 1
        let styleReady = await recorder.waitFor { recorder.identities[1] != nil }
        recorder.check("state-styling-retains-reference", initialReady && styleReady && recorder.identities[0] == recorder.identities[1], "Identity recorded before and after conditional foreground style.")
        identity = 1
        step = 2
        let resetReady = await recorder.waitFor { recorder.identities[2] != nil }
        recorder.check("state-explicit-identity-recreates", resetReady && recorder.identities[1] != recorder.identities[2], "Changing explicit identity created a different retained reference.")

        let binding = Binding(get: { bindingValue }, set: { value in setterCalls += 1; bindingValue = value })
        binding.wrappedValue = 1
        binding.wrappedValue = 1
        // Equal writes synchronously invoke the setter. No changed-value event is expected.
        recorder.check("binding-equal-writes-call-setter", setterCalls == 2, "Setter count after two equal writes: \(setterCalls).")
        binding.wrappedValue = 2
        let editObserved = await recorder.waitFor { changedValues.contains(2) }
        bindingValue = 3
        let programmaticObserved = await recorder.waitFor { changedValues.contains(3) }
        recorder.check("binding-programmatic-change-bypasses-setter", editObserved && programmaticObserved && setterCalls == 3 && changeCalls == 2, "Setter calls \(setterCalls); onChange calls \(changeCalls); values \(changedValues).")

        draft = "not yet saved"
        recorder.check("draft-edit-does-not-save", saved == "original", "Draft mutation kept the saved value intact.")
        draft = saved
        recorder.check("draft-cancel", draft == "original" && saved == "original", "Cancel restored the draft from saved state.")
        draft = "committed"
        saved = draft
        recorder.check("draft-explicit-save", saved == "committed", "Only the explicit Save operation copied the draft.")

        sizeStep = 1
        width = 320
        height = 100
        let wideReady = await recorder.waitFor { recorder.sizes[1] != nil }
        recorder.check("geometry-short-wide", wideReady && recorder.sizes[1] == CGSize(width: 320, height: 100), "Observed constrained fixture geometry, not a physical folding display.")

        withAnimation(.linear(duration: 0.1), completionCriteria: .removed) {
            animated = true
        } completion: {
            animationCompleted = true
        }
        let completed = await recorder.waitFor { animationCompleted }
        recorder.check("animation-completion-delivered", completed, "One uninterrupted animation delivered its completion; interruption and Reduce Motion remain separate cases.")
        recorder.save()
    }
}
