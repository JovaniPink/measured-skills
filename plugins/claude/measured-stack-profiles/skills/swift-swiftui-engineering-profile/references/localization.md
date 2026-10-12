# Localized resources and accessible meaning

Authority: [String catalogs](https://developer.apple.com/documentation/xcode/localizing-and-varying-text-with-a-string-catalog). Reviewed 2026-10-12.

- Preserve the project's extraction workflow. Automatic extraction and intentional manual entries are both valid; converting every key to manual is not a requirement. [documented]
- Use localizable resources where a model carries user-facing copy. Test generated symbols and keys in the build that produces them, not only a standalone compiler probe. [documented]
- Test plural rules, interpolated values, translator context, locale-specific numbers/dates/measurements, and right-to-left ordering. Concatenated fragments can prevent translators from reordering a sentence. [documented]
- The bundle macro compiles with Xcode 27.0 at an iOS 17.6 deployment target. That does not prove it finds resources in a particular Swift package or framework. Preserve a working Bundle.module contract until resource lookup tests demonstrate equivalence. [verified: compile; resource behavior unverified]
- Pseudolocalization exposes expansion and layout problems; it is not reviewed translation. Verify missing-key fallback and package resources using a second locale. [unverified: runtime]
- Accessible labels, values, hints, and control names are user-facing content too. Keep labels meaningful when visual text is hidden, and verify reading order rather than relying on identifiers. [documented]
