"""Validate the prepared case inventory, not agent behavior or client parity."""
from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class FollowThroughScenarios(unittest.TestCase):
    def test_six_modes_have_distinct_failure_and_counterexample_cases(self) -> None:
        packet = json.loads((ROOT / "evals/follow-through-scenarios.json").read_text())
        self.assertEqual(packet["status"], "prepared_not_run")
        self.assertIn("not grading of agent behavior", packet["purpose"])
        modes = {"completion", "context", "rejected-option", "tool-access",
                 "evidence-reuse", "review-handoff"}
        cases = packet["scenarios"]
        self.assertEqual(len(cases), 12)
        self.assertEqual({c["id"] for c in cases},
                         {f"{m}-{k}" for m in modes for k in ("failure", "counterexample")})
        self.assertEqual(len({c["prompt"] for c in cases}), 12)
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertTrue(case["expected"])
                self.assertTrue(case["forbidden"])
                self.assertFalse(set(case["expected"]) & set(case["forbidden"]))
                self.assertIs(type(case["requested_work_complete"]), bool)
                for skill in case["skills"]:
                    self.assertTrue((ROOT / "skills" / skill / "SKILL.md").is_file())
                self.assertNotIn("observed_result", case)


if __name__ == "__main__":
    unittest.main()
