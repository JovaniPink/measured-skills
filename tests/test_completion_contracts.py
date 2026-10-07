from __future__ import annotations
import unittest
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("plan-execution", "swiftui-feature-delivery", "nextjs-feature-delivery")


class CompletionContracts(unittest.TestCase):
    def test_scenario_coverage_and_declared_dispositions(self) -> None:
        document = json.loads(
            (ROOT / "evals/completion-contract-scenarios.json").read_text()
        )
        self.assertEqual("prepared_not_run", document["status"])
        self.assertIn("No grading of agent behavior occurred", document["purpose"])
        expected = {
            f"{skill}-{suffix}": (skill, disposition, complete)
            for skill in SKILLS
            for suffix, disposition, complete in (
                ("blocked", "blocked", False),
                ("missing-validation", "partial", False),
                ("completed", "complete", True),
                ("no-op", "not_needed", True),
            )
            if suffix != "no-op" or skill != "plan-execution"
        }
        scenarios = document["scenarios"]
        self.assertEqual(len(expected), len(scenarios))
        self.assertEqual(set(expected), {item["id"] for item in scenarios})
        for item in scenarios:
            with self.subTest(scenario=item["id"]):
                self.assertEqual(
                    {
                        "id",
                        "skill",
                        "evidence",
                        "expected",
                        "disposition",
                        "requested_work_complete",
                    },
                    set(item),
                )
                self.assertEqual(
                    expected[item["id"]],
                    (
                        item["skill"],
                        item["disposition"],
                        item["requested_work_complete"],
                    ),
                )
                self.assertIs(type(item["requested_work_complete"]), bool)
                self.assertTrue(item["evidence"].strip())
                self.assertTrue(item["expected"].strip())

    def test_required_validation_cannot_be_unavailable_and_complete(self) -> None:
        for name in SKILLS:
            text = (ROOT / "skills" / name / "SKILL.md").read_text()
            with self.subTest(skill=name):
                self.assertNotIn("pass or are reported as unavailable", text)
                self.assertNotIn("passed or is reported as unavailable", text)
                self.assertIn("required checks pass", text)

    def test_blocked_work_is_explicitly_unfinished(self) -> None:
        for name in SKILLS:
            text = (ROOT / "skills" / name / "SKILL.md").read_text()
            with self.subTest(skill=name):
                self.assertIn("Blocked and partial work remain unfinished", text)
                self.assertNotIn("or when the result is Not Needed or Blocked", text)

    def test_noop_requires_evidence(self) -> None:
        for name in ("swiftui-feature-delivery", "nextjs-feature-delivery"):
            self.assertIn(
                "Not Needed requires evidence",
                (ROOT / "skills" / name / "SKILL.md").read_text(),
            )
