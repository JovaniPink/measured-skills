# Synthetic package resources

This dependency-free package tests actual resource lookup with the selected Swift
6.4 toolchain. Resources are original synthetic JSON, strings and plural rules.
It does not contain application content, user data or network clients.

```sh
DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer xcrun swift test --package-path evals/swift-evidence-v1/resource-package --scratch-path /tmp/new-resource-build
```

The [observed receipt](../observed-resources-2026-10-12.json) records source hashes,
toolchain, destination, test outcome and limits. Four Swift Testing tests passed,
including two interpolation cases and four plural cases. The same package resource
bytes were found through `#bundle` and `Bundle.module`. Missing files, localization
and keys retain explicit failure/fallback behavior.

This is macOS package evidence. iOS framework and extension lookup, automatic
extraction, generated String Catalog symbols, wider plural/language coverage and
user-facing localized layouts remain separate checks. Do not replace an existing
application bundle contract based on this one fixture alone.
