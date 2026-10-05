"""Tests for the rule that every skill reference file is linked from its SKILL.md."""

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import validate_catalog  # noqa: E402

SKILL = "claim-verification"
REFERENCE = "references/continuity-example.md"


class ReferenceLinkTests(unittest.TestCase):
    def check(self, mutate: object = None) -> list[str]:
        """Copy a real skill into a temporary folder, optionally change it, and run the rule."""

        with tempfile.TemporaryDirectory() as raw:
            skill_dir = Path(raw) / "skills" / SKILL
            shutil.copytree(REPO / "skills" / SKILL, skill_dir)
            if callable(mutate):
                mutate(skill_dir)
            return validate_catalog.unlinked_reference_errors(SKILL, skill_dir)

    def test_a_skill_that_links_its_reference_passes(self) -> None:
        self.assertEqual([], self.check())

    def test_an_unlinked_reference_is_reported_by_path(self) -> None:
        def add(skill_dir: Path) -> None:
            (skill_dir / "references" / "extra.md").write_text("# Extra\n", encoding="utf-8")

        errors = self.check(add)
        self.assertEqual(
            [f"skills/{SKILL}/references/extra.md: reference is not linked from SKILL.md"], errors
        )

    def test_removing_the_link_from_skill_md_is_reported(self) -> None:
        def unlink(skill_dir: Path) -> None:
            path = skill_dir / "SKILL.md"
            text = path.read_text(encoding="utf-8")
            self.assertIn(f"]({REFERENCE})", text)
            path.write_text(text.replace(f"]({REFERENCE})", "](#top)"), encoding="utf-8")

        errors = self.check(unlink)
        self.assertEqual(1, len(errors))
        self.assertIn("continuity-example.md", errors[0])

    def test_dot_prefix_and_anchor_still_count_as_linked(self) -> None:
        def reword(skill_dir: Path) -> None:
            path = skill_dir / "SKILL.md"
            text = path.read_text(encoding="utf-8")
            path.write_text(
                text.replace(f"]({REFERENCE})", f"](./{REFERENCE}#example)"), encoding="utf-8"
            )

        self.assertEqual([], self.check(reword))

    def test_nested_reference_files_must_be_linked_too(self) -> None:
        def add(skill_dir: Path) -> None:
            nested = skill_dir / "references" / "deeper"
            nested.mkdir()
            (nested / "note.md").write_text("# Note\n", encoding="utf-8")

        errors = self.check(add)
        self.assertEqual(1, len(errors))
        self.assertIn("references/deeper/note.md", errors[0])

        def add_and_link(skill_dir: Path) -> None:
            add(skill_dir)
            path = skill_dir / "SKILL.md"
            path.write_text(
                path.read_text(encoding="utf-8") + "\nRead [the note](references/deeper/note.md).\n",
                encoding="utf-8",
            )

        self.assertEqual([], self.check(add_and_link))

    def test_a_skill_without_references_has_nothing_to_report(self) -> None:
        def remove(skill_dir: Path) -> None:
            shutil.rmtree(skill_dir / "references")

        self.assertEqual([], self.check(remove))

    def test_every_reference_in_the_catalog_is_linked(self) -> None:
        errors: list[str] = []
        validate_catalog.validate_reference_links(errors)
        self.assertEqual([], errors)

    def test_the_agentic_security_review_links_its_threat_domains(self) -> None:
        text = (REPO / "skills" / "agentic-system-security-review" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("](references/agentic-threat-domains.md)", text)


if __name__ == "__main__":
    unittest.main()
