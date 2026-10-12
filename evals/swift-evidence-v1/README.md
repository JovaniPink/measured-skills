# Original Swift evidence corpus v1

These synthetic examples are primary-source experiments, not imported skill rules.
The manifest declares compiler outcomes; `observed-2026-10-12.json` records one
observed source snapshot. Raw logs stay outside distributable skill payloads.

```sh
python3 scripts/swift_evidence.py compile --developer-dir /Applications/Xcode.app/Contents/Developer --output /tmp/new-compile-receipt
python3 scripts/swift_evidence.py inventory --developer-dir /Applications/Xcode.app/Contents/Developer --output /tmp/new-sdk-receipt
python3 scripts/run_swift_runtime.py --developer-dir /Applications/Xcode.app/Contents/Developer --destination CALLER_OWNED_BOOTED_SIMULATOR_UUID --output /tmp/new-runtime-receipt
```

The runtime command explicitly compiles, ad-hoc signs and installs only the
synthetic fixture on the supplied booted simulator. It does not create, erase,
reset or select devices, change global Xcode selection, or install dependencies.
Use a disposable destination you own. Its sole stale result file is removed before
launch; previous external evidence directories are never overwritten. Exit 0 is
passed, 1 is a failed assertion, and 2 is blocked infrastructure or missing SDK.
Inspect the receipt, not just process status. Builds and timeouts retain logs.

The lexical inventory covers public Swift declarations carrying direct iOS or
anyAppleOS availability in requested modules. Architecture variants are retained;
Objective-C declarations, inherited availability and conditional compilation need
separate analysis. Do not call the inventory every deprecated Apple API.

The initial nine runtime checks cover retained reference state, deliberate identity reset,
equal binding writes, programmatic changes, explicit draft save/cancel, a constrained
short/wide view and one uninterrupted animation. They do not test provider behavior,
physical resizing, folding, accessibility, lazy row cost, caching, interrupted
motion or app-specific persistence. Expand with a separately identified workload.

A `@State` default plus the tested initializer assignment compiled successfully;
the original expected-error hypothesis was corrected after execution. One malformed
layout probe was repaired before the final compile run. Retain such failed attempts
rather than retroactively calling the first run successful.

The [runtime extension](observed-runtime-extension-2026-10-12.json) reruns those
cases and adds six assertions: one-shot observation of read versus unread stored
properties, nested struct invalidation, a child reading an injected observable
model, selected-item sheet presentation and dismissal retaining the parent draft.
All 15 passed on the recorded iOS 27.0 simulator. The counter is deliberately
non-observable instrumentation; its five prior body evaluations are not a universal
SwiftUI baseline. Twenty writes to the unread field produced no additional child
body evaluations during the measured interval. This is dependency evidence, not
Instruments, physical performance or a ban on environment injection.

The earlier nine-case receipt remains unchanged. The extension source and hash
identify the newer fixture. Programmatic sheet dismissal does not qualify keyboard
obstruction, gesture dismissal or assistive-technology behavior.

The [resource package](resource-package/README.md) separately executes real package
lookup, interpolation, pluralization and missing-resource cases on macOS. Its
receipt does not qualify iOS framework packaging or String Catalog extraction.

The [String Catalog fixture](string-catalog/README.md) checks installed lightweight
extraction, manual-key retention, symbol generation/typechecking and localized
build products. Its limitations differ from both the compile and package runs.
