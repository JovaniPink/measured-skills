"""Check prepared case budgets and frozen-source correspondence without inference."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any
import unittest


ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs/audits/gemini-flash-trial-preparation-2026-11-02.json"


def find_case(value: Any, identity: str) -> dict[str, Any] | None:
    if isinstance(value, dict):
        if value.get("id") == identity:
            return value
        children = list(value.values())
    elif isinstance(value, list):
        children = value
    else:
        return None
    for child in children:
        found = find_case(child, identity)
        if found is not None:
            return found
    return None


class TrialPreparationTests(unittest.TestCase):
    def test_selected_cases_fit_the_recorded_budget(self) -> None:
        record = json.loads(RECORD.read_text())
        rows = record["rows"]
        self.assertLessEqual(len(rows), record["case_session_ceiling"])
        self.assertEqual(list(range(1, len(rows) + 1)), [r["order"] for r in rows])
        self.assertEqual(len(rows), len({r["source_case"] for r in rows}))
        followups = record["continuity_followups"]
        self.assertLessEqual(len(followups), record["followup_ceiling"])
        for followup in followups:
            self.assertIn(followup["after_row"], [r["order"] for r in rows])

    def test_every_case_matches_its_own_frozen_source(self) -> None:
        record = json.loads(RECORD.read_text())
        for row in record["rows"] + record.get("deferred_rows", []):
            with self.subTest(case=row["source_case"]):
                source_file = row.get("source_file")
                self.assertIsInstance(source_file, str)
                self.assertTrue(source_file.startswith("evals/"))
                self.assertNotIn("..", Path(source_file).parts)
                source = subprocess.check_output(
                    ["git", "show", record["source_revision"] + ":" + source_file],
                    cwd=ROOT,
                )
                self.assertEqual(
                    record["frozen_sources"][source_file], hashlib.sha256(source).hexdigest()
                )
                original = find_case(json.loads(source), row["source_case"])
                self.assertIsNotNone(original)
                assert original is not None
                self.assertEqual(original["prompt"], row["prompt"])
                self.assertEqual(
                    hashlib.sha256(row["prompt"].encode()).hexdigest(), row["prompt_sha256"]
                )
                if "request_sha256" in row:
                    request = row["prompt"]
                    if row.get("context"):
                        request += "\n\n" + row["context"]
                    self.assertEqual(
                        hashlib.sha256(request.encode()).hexdigest(), row["request_sha256"]
                    )


if __name__ == "__main__":
    unittest.main()
