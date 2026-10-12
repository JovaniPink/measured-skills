import Foundation

public enum ResourceFixture {
    public static var macroBundle: Bundle { #bundle }
    public static var moduleBundle: Bundle { .module }

    public static func localizedBundle(_ language: String) throws -> Bundle {
        guard let url = macroBundle.url(forResource: language, withExtension: "lproj"),
              let bundle = Bundle(url: url) else { throw ResourceError.missingLanguage }
        return bundle
    }

    enum ResourceError: Error { case missingLanguage }
}
