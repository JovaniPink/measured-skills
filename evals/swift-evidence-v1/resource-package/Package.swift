// swift-tools-version: 6.4
import PackageDescription

let package = Package(
    name: "SyntheticResources", defaultLocalization: "en", platforms: [.macOS(.v14)],
    products: [.library(name: "ResourceFixture", targets: ["ResourceFixture"])],
    targets: [
        .target(name: "ResourceFixture", resources: [.process("Resources")]),
        .testTarget(name: "ResourceFixtureTests", dependencies: ["ResourceFixture"]),
    ]
)
