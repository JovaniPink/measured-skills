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

The nine runtime checks cover retained reference state, deliberate identity reset,
equal binding writes, programmatic changes, explicit draft save/cancel, a constrained
short/wide view and one uninterrupted animation. They do not test provider behavior,
physical resizing, folding, accessibility, lazy row cost, caching, interrupted
motion or app-specific persistence. Expand with a separately identified workload.

A `@State` default plus the tested initializer assignment compiled successfully;
the original expected-error hypothesis was corrected after execution. One malformed
layout probe was repaired before the final compile run. Retain such failed attempts
rather than retroactively calling the first run successful.
