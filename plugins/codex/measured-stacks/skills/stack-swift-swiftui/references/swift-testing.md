# Swift Testing

Evidence labels: [verified] means run with `swift test` on Xcode 27.0 (Swift 6.4, Testing library 2084) on 2026-09-22. [documented] means stated in the linked Apple documentation but not executed here. [unverified] means review judgment.

Authorities: [Swift Testing](https://developer.apple.com/documentation/testing), [Parallelization](https://developer.apple.com/documentation/testing/parallelization), and [Migrating a test from XCTest](https://developer.apple.com/documentation/testing/migratingfromxctest).

## Discovery

- Find which targets use `import Testing`, which use XCTest, and which use both. One source file can hold both kinds of tests. [documented]
- Find the command the repository uses: `swift test`, `xcodebuild test` with a scheme and destination, or a script. Report the exact filter and destination used.

## XCTest assertions inside Swift Testing

A test that is partly migrated can pass while its assertions fail. [verified]

- Interoperability mode decides what happens when an `XCTAssert` runs inside a Swift Testing test. [documented]
- The default depends on the toolchain and the package's `swift-tools-version`. Toolchains before Swift 6.4 use `none`, which ignores the assertion. A 6.4 toolchain with an older tools version uses `limited`, which reports it as a warning. Swift 6.4 with tools version 6.4 uses `complete`, which reports it as a failure. [documented]
- On the Swift 6.4 toolchain with tools version 6.2, `XCTAssertEqual(1, 2)` inside `@Test` produced a warning and the test passed. With `SWIFT_TESTING_XCTEST_INTEROP_MODE=complete`, the same test failed. [verified]
- A Swift Testing `#expect` inside an `XCTestCase` method failed that XCTest test. [verified]
- Treat any `XCTAssert` inside a `@Test` as a finding unless the gate runs in `complete` or `strict` mode. Replace it with `#expect` or `#require`. [unverified]

## Parallel by default

- Tests run in parallel, including tests inside one suite. [verified] XCTest runs a suite's tests one at a time by default. [documented]
- Tests that share global or static state become flaky under parallel runs. Add `.serialized` to the suite or remove the shared state. [documented]
- `.serialized` on a suite ran its tests one after another. [verified]
- `.serialized` on a parameterized test runs its cases one at a time. [documented]

## Suites and setup

- Each test function gets a fresh suite instance. Stored properties set in `init` act as per-test setup. [verified]
- A class or actor suite can use `deinit` for teardown. [documented]
- Free functions can be tests; a suite type is optional. [documented]

## Expectations

- `#expect` records a failure and keeps going. [verified]
- `try #require` stops the test on failure and unwraps optionals. [verified]
- `#expect(throws:)` checks the error type. [verified]
- `withKnownIssue` records an expected failure without failing the run. [verified]
- `confirmation(expectedCount:)` checks that a callback fired an exact number of times. Use it in place of `XCTestExpectation`. [verified]

## Parameterized tests

- `@Test(arguments:)` reports each argument as its own case. [verified]
- Tags and `.timeLimit(.minutes(n))` traits compile and run alongside other traits. [verified]

## Isolation

- Mark a test `@MainActor` when it calls main-actor code. It compiled and passed against a module with `MainActor` default isolation. [verified]
- A nonisolated test calling that module's API fails to compile. [verified]

## What to test first in this stack

- Every SwiftData `#Predicate` against a real container, because some bad predicates only fail at fetch time. See the SwiftData reference. [verified]
- Actor methods with an `await` between a check and a change. See the concurrency reference. [verified]
- HealthKit empty, denied, and limited states through a fake store. See the HealthKit reference. [unverified]

## Gaps to report

- In Xcode 27, UI automation APIs such as `XCUIApplication` live in the XCUIAutomation framework. [verified declaration] Confirm which runner executes UI and performance tests before reporting them as covered. [unverified]
- A green `swift test` on macOS says nothing about iOS simulator or device behavior. Report the platform that ran.
