"""Evidence must not confuse a broken compiler environment with an expected error."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from swift_evidence import classify, load_cases, scan_interface


class SwiftEvidenceTests(unittest.TestCase):
    def test_manifest_explicitly_selects_codegen_for_conformance_diagnostics(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "probe.swift").write_text("import SwiftUI\n")
            row = {"id": "compile-probe", "source": "probe.swift", "expect": "success",
                   "diagnostics": [], "target": "17.6", "language": "5", "minimum_sdk": "27.0",
                   "authority": "https://developer.apple.com/documentation/swiftui/", "phase": "object"}
            manifest = root / "cases.json"
            manifest.write_text(json.dumps({"format_version": 1, "cases": [row]}))
            self.assertEqual("object", load_cases(manifest)[0]["phase"])
            row["phase"] = "execute"
            manifest.write_text(json.dumps({"format_version": 1, "cases": [row]}))
            with self.assertRaisesRegex(ValueError, "phase"):
                load_cases(manifest)

    def test_expected_error_requires_the_named_diagnostic(self) -> None:
        self.assertEqual("passed", classify("error", ["only available in iOS 18"], 1,
                                          "error: 'Tab' is only available in iOS 18.0 or newer"))
        self.assertEqual("failed", classify("error", ["only available in iOS 18"], 1,
                                          "error: unrelated syntax failure"))
        self.assertEqual("failed", classify("error", ["only available"], 0, ""))

    def test_infrastructure_failure_never_counts_as_expected_error(self) -> None:
        for diagnostic in ["sandbox-exec: sandbox_apply: Operation not permitted",
                           "external macro implementation type could not be found",
                           "unable to find utility swiftc", "SDK does not contain libarclite"]:
            self.assertEqual("blocked", classify("error", [], 1, diagnostic))

    def test_success_and_warning_are_distinct(self) -> None:
        self.assertEqual("passed", classify("success", [], 0, ""))
        self.assertEqual("failed", classify("success", [], 0, "warning: regression"))
        self.assertEqual("failed", classify("warning", ["closure"], 0, ""))
        self.assertEqual("passed", classify("warning", ["closure"], 0, "warning: closure may invalidate"))
        self.assertEqual("failed", classify("warning", ["closure"], 1, "error: closure"))

    def test_availability_is_scoped_to_the_next_declaration(self) -> None:
        source = '''@available(iOS, introduced: 13.0, deprecated: 100000.0)
@available(macOS 10.15, *)
public func oldColor(_ color: Color) -> some View

public func currentColor() -> some View
@available(iOS 27.0, *)
public struct NewControl {
  public init()
}
'''
        rows = scan_interface(source)
        self.assertEqual(2, len(rows))
        self.assertEqual("oldColor", rows[0]["symbol"])
        self.assertTrue(rows[0]["soft_deprecated"])
        self.assertEqual("NewControl", rows[1]["symbol"])
        self.assertFalse(rows[1]["soft_deprecated"])

    def test_multiline_availability_and_platform_filter(self) -> None:
        source = '''@available(iOS,
 introduced: 17.0, deprecated: 100000.0)
public var oldValue: Int { get }
@available(macOS 27.0, *)
public func desktopOnly()
@available(anyAppleOS 27.0, *)
public func sharedValue()
'''
        self.assertEqual(["oldValue", "sharedValue"], [r["symbol"] for r in scan_interface(source)])

    def test_manifest_rejects_traversal_duplicate_ids_and_bad_expectations(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "probe.swift").write_text("import SwiftUI\n")
            row = {"id": "example", "source": "probe.swift", "expect": "success", "diagnostics": [],
                   "target": "17.6", "language": "5", "minimum_sdk": "27.0",
                   "authority": "https://developer.apple.com/documentation/swiftui"}
            manifest = root / "cases.json"
            manifest.write_text(json.dumps({"format_version": 1, "cases": [row]}))
            self.assertEqual(1, len(load_cases(manifest)))
            for changes in [{"source": "../outside.swift"}, {"expect": "maybe"}, {"language": "99"}]:
                manifest.write_text(json.dumps({"format_version": 1, "cases": [row | changes]}))
                with self.assertRaises(ValueError):
                    load_cases(manifest)
            manifest.write_text(json.dumps({"format_version": 1, "cases": [row, row]}))
            with self.assertRaises(ValueError):
                load_cases(manifest)


if __name__ == "__main__":
    unittest.main()
