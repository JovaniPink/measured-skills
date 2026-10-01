import Foundation
@MainActor final class Streaming {
    var text = ""
    var work: Task<Void, Never>?
    func start(_ stream: AsyncStream<String>) {
        work?.cancel()
        text = ""
        work = Task { for await chunk in stream { text += chunk } }
    }
}
