"""The extension preserves frozen cases and distinguishes plans from results."""
from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SwiftAdoptionCasesTests(unittest.TestCase):
    def test_inventory_and_unqualified_results(self) -> None:
        data = json.loads((ROOT / "evals/swift-adoption-v1/cases.json").read_text())
        self.assertEqual(data["format_version"], 1)
        self.assertEqual(data["historical_case_count"], 49)
        self.assertEqual(data["context_turns"], [1, 8, 20])
        self.assertEqual(data["repetitions"], 3)
        self.assertEqual(set(data["conditions"]), {"baseline", "candidate"})
        rows = data["cases"]
        self.assertEqual(len(rows), len({row["id"] for row in rows}))
        self.assertEqual({row["category"] for row in rows}, {"positive", "near_miss", "safety"})
        for row in rows:
            self.assertEqual(set(row), {"id", "category", "prompt", "obligations", "result"})
            self.assertEqual(row["result"], "not_run")
            self.assertGreaterEqual(len(row["obligations"]), 2)
            self.assertTrue(all(isinstance(value, str) and value.strip() for value in row["obligations"]))
        self.assertTrue({"old-target", "missing-sdk", "upload-claim", "binding-draft", "environment",
                         "read-only", "persistence", "missing-runtime", "localization", "performance",
                         "new-platform", "motion"} <= {row["id"] for row in rows})
