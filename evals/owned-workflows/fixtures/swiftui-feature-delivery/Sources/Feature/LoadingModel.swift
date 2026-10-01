import Foundation
@MainActor final class LoadingModel {
    var result = ""
    func load(_ fetch: @escaping () async throws -> String) {
        Task { result = (try? await fetch()) ?? "" }
    }
}
