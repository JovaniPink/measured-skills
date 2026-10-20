import SwiftUI
struct FixtureSettings: Equatable { var compact = false }
extension EnvironmentValues { @Entry var fixtureSettings = FixtureSettings() }
