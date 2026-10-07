from __future__ import annotations
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("plan-execution", "swiftui-feature-delivery", "nextjs-feature-delivery")


class CompletionContracts(unittest.TestCase):
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
