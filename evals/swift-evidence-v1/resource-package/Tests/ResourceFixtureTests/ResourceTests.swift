import Foundation
import Testing
@testable import ResourceFixture

struct ResourceTests {
    @Test func macroFindsPackageResources() throws {
        #expect(ResourceFixture.macroBundle.bundleURL == ResourceFixture.moduleBundle.bundleURL)
        let macroURL = try #require(ResourceFixture.macroBundle.url(forResource: "payload", withExtension: "json"))
        let moduleURL = try #require(ResourceFixture.moduleBundle.url(forResource: "payload", withExtension: "json"))
        #expect(try Data(contentsOf: macroURL) == Data(contentsOf: moduleURL))
        let payload = try JSONDecoder().decode(Payload.self, from: Data(contentsOf: macroURL))
        #expect(payload.fixture == "synthetic-resource-v1")
        #expect(payload.count == 3)
    }

    @Test(arguments: [("en", "Hello, River"), ("fr", "Bonjour, River")])
    func interpolation(language: String, expected: String) throws {
        let bundle = try ResourceFixture.localizedBundle(language)
        let format = bundle.localizedString(forKey: "greeting", value: nil, table: nil)
        #expect(String(format: format, locale: Locale(identifier: language), "River") == expected)
    }

    @Test(arguments: [("en", 1, "1 item"), ("en", 2, "2 items"),
                      ("fr", 1, "1 element"), ("fr", 2, "2 elements")])
    func pluralization(language: String, count: Int, expected: String) throws {
        let bundle = try ResourceFixture.localizedBundle(language)
        let format = bundle.localizedString(forKey: "item_count", value: nil, table: nil)
        #expect(String.localizedStringWithFormat(format, count) == expected)
    }

    @Test func missingResourceRemainsMissing() throws {
        #expect(ResourceFixture.macroBundle.url(forResource: "not-present", withExtension: "json") == nil)
        let bundle = try ResourceFixture.localizedBundle("en")
        #expect(bundle.localizedString(forKey: "missing", value: "Explicit fallback", table: nil) == "Explicit fallback")
        #expect(throws: ResourceFixture.ResourceError.self) { try ResourceFixture.localizedBundle("zz") }
    }
}

private struct Payload: Decodable { let fixture: String; let count: Int }
