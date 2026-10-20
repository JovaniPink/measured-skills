# String Catalog toolchain fixture

Original synthetic inputs check selected installed-tool behavior. The
[receipt](../observed-string-catalog-2026-10-12.json) records five passing assertions:
automatic keys were extracted, verbatim text was excluded, a manual key survived
sync, its generated symbol typechecked for iOS 17.6 in Swift 5 mode, and English
and French build products were emitted.

Reproduce from the repository root, using a new output directory:

```sh
(
  export DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer
  loc_probe=$(mktemp -d)
  mkdir "$loc_probe/extracted" "$loc_probe/symbols" "$loc_probe/compiled"
  xcrun xcstringstool extract --SwiftUI --modern-localizable-strings evals/swift-evidence-v1/string-catalog/Extraction.swift --output-directory "$loc_probe/extracted"
  cp evals/swift-evidence-v1/string-catalog/Localizable.xcstrings "$loc_probe/Localizable.xcstrings"
  xcrun xcstringstool sync "$loc_probe/Localizable.xcstrings" --stringsdata "$loc_probe/extracted/Extraction-swift.stringsdata"
  xcrun xcstringstool generate-symbols "$loc_probe/Localizable.xcstrings" --output-directory "$loc_probe/symbols" --language swift
  xcrun xcstringstool compile "$loc_probe/Localizable.xcstrings" --output-directory "$loc_probe/compiled"
  xcrun swiftc -typecheck -sdk "$(xcrun --sdk iphonesimulator --show-sdk-path)" -target arm64-apple-ios17.6-simulator -swift-version 5 evals/swift-evidence-v1/string-catalog/Symbol.swift "$loc_probe/symbols/GeneratedStringSymbols_Localizable.swift"
)
```

Inspect the resulting catalog: keys `Inventory`, `Available items`, and
`library.empty` must exist; `Synthetic diagnostic` must not. The manual key must
retain `extractionState: manual`. Inspect both compiled localization directories.
Command success alone does not prove these assertions.

The first experiment used a named `Manual` table; its symbols were correctly
namespaced and default-table extraction did not populate it. The corrected
`Localizable` fixture uses the unscoped `.libraryEmpty` symbol. Keep that distinction
when an app has multiple tables. Automatic extraction is not a reason to mark
every entry manual.

This lightweight extractor does not invoke the full Xcode compilation pipeline
and cannot always infer interpolation format specifiers. The separate resource
package verifies runtime interpolation/plural examples. Neither fixture qualifies
native localized UI, accessibility, framework/extension lookup or old-OS runtime.
