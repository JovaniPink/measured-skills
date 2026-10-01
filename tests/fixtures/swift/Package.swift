// swift-tools-version: 6.2
import PackageDescription

let package = Package(
    name: "PortableGateFixture",
    products: [.library(name: "ConcurrencyFixture", targets: ["ConcurrencyFixture"])],
    targets: [
        .target(name: "ConcurrencyFixture"),
        .testTarget(name: "ConcurrencyFixtureTests", dependencies: ["ConcurrencyFixture"])
    ]
)
