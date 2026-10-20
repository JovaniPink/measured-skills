import SwiftUI
final class FixtureStore {}
extension EnvironmentValues { @Entry var fixtureStore = FixtureStore() }
