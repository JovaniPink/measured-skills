"""Regression tests for validator, scanner, manifest, and fixture-gate behavior.

Each test would fail on the code it replaced. Secret-like strings are built by
concatenation so the boundary scanner does not flag this file.
"""

from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import build_release_manifest  # noqa: E402
import check_public_boundary  # noqa: E402
import validate_catalog  # noqa: E402
from cataloglib import VERSION  # noqa: E402
from check_upstream_freshness import check as check_upstream_freshness  # noqa: E402
from evaluate_gate_fixtures import is_mutating_command  # noqa: E402

SHA = "a" * 40


class ActionPinTests(unittest.TestCase):
    def test_step_that_starts_with_a_name_is_checked(self) -> None:
        text = "steps:\n  - name: Check out\n    uses: actions/checkout@v4\n"
        errors = validate_catalog.immutable_action_reference_errors(text, "w.yml")
        self.assertEqual(1, len(errors))
        self.assertIn("40-character commit SHA", errors[0])

    def test_job_level_reusable_workflow_is_checked(self) -> None:
        text = "jobs:\n  call:\n    uses: octo/repo/.github/workflows/x.yml@main\n"
        self.assertEqual(1, len(validate_catalog.immutable_action_reference_errors(text, "w.yml")))

    def test_quoted_references_are_judged_by_their_revision(self) -> None:
        pinned = f'steps:\n  - name: ok\n    uses: "actions/checkout@{SHA}"\n'
        mutable = "steps:\n  - uses: 'actions/checkout@v4'\n"
        self.assertEqual([], validate_catalog.immutable_action_reference_errors(pinned, "w.yml"))
        self.assertEqual(1, len(validate_catalog.immutable_action_reference_errors(mutable, "w.yml")))

    def test_comments_local_actions_and_images_are_ignored(self) -> None:
        text = (
            "# uses: actions/checkout@v4\n"
            "steps:\n  - uses: ./local-action\n  - uses: docker://alpine:3\n"
        )
        self.assertEqual([], validate_catalog.immutable_action_reference_errors(text, "w.yml"))

    def check(self, text: str) -> list[str]:
        return validate_catalog.immutable_action_reference_errors(text, "w.yml")

    def test_uses_text_inside_a_literal_block_is_not_a_step(self) -> None:
        text = (
            "steps:\n"
            "  - run: |\n"
            "      cat > generated.yml <<'EOF'\n"
            "      jobs:\n"
            "        build:\n"
            "          uses: owner/action@v4\n"
            "      - uses: owner/other@v1\n"
            "      EOF\n"
        )
        self.assertEqual([], self.check(text))

    def test_uses_text_inside_folded_and_nested_blocks_is_ignored(self) -> None:
        folded = "steps:\n  - name: note\n    run: >-\n      uses: owner/action@v4\n"
        nested = (
            f"steps:\n  - uses: actions/github-script@{SHA}\n    with:\n"
            "      script: |  # inline comment\n        uses: owner/action@v4\n\n        uses: owner/more@v2\n"
        )
        self.assertEqual([], self.check(folded))
        self.assertEqual([], self.check(nested))

    def test_a_mutable_reference_after_a_block_is_still_flagged(self) -> None:
        text = "steps:\n  - run: |\n      echo hi\n\n  - uses: actions/checkout@v4\n"
        self.assertEqual(1, len(self.check(text)))

    def test_a_pinned_reference_after_a_block_still_passes(self) -> None:
        text = f"steps:\n  - run: |\n      echo hi\n  - uses: actions/checkout@{SHA}\n"
        self.assertEqual([], self.check(text))

    def test_a_single_line_run_is_not_a_block(self) -> None:
        text = "steps:\n  - name: a\n    run: echo hi\n    uses: actions/checkout@v4\n"
        self.assertEqual(1, len(self.check(text)))


class SecretPatternTests(unittest.TestCase):
    @staticmethod
    def findings(text: str) -> str:
        patterns = check_public_boundary._patterns(None)
        return "\n".join(check_public_boundary._scan_text("fixture", text, patterns))

    def test_common_credential_shapes_are_detected(self) -> None:
        samples = {
            "Anthropic API key": "s" + "k-ant-" + "api03-" + "A" * 24,
            "prefixed OpenAI-style key": "s" + "k-proj-" + "B" * 30,
            "GitHub fine-grained token": "github" + "_pat_" + "C" * 30,
            "Slack token": "xo" + "xb-" + "1234567890-abcdef",
            "Google API key": "AI" + "za" + "D" * 35,
        }
        for label, secret in samples.items():
            with self.subTest(label=label):
                self.assertIn(label, self.findings(f"value = {secret}\n"))

    def test_ordinary_hyphenated_words_are_not_flagged(self) -> None:
        text = "A risk-adjusted-performance-metrics-for-everyone note and task-specific-review-workflow-notes.\n"
        self.assertEqual("", self.findings(text))


class NonUtf8Tests(unittest.TestCase):
    def test_unreadable_text_file_is_reported_not_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "notes.md"
            path.write_bytes(b"\xff\xfe\x00 not utf-8")
            errors = check_public_boundary.scan(paths=[path], include_packages=False)
        self.assertEqual(1, len(errors))
        self.assertIn("not valid UTF-8", errors[0])

    def test_archives_are_left_to_the_archive_scan(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "skill.zip"
            path.write_bytes(b"\xff\xfe\x00 binary")
            self.assertEqual([], check_public_boundary.scan(paths=[path], include_packages=False))


class SkillValidationTests(unittest.TestCase):
    SKILL = "claim-verification"

    def validate(self, mutate: object = None, base: tuple[str, ...] = ()) -> list[str]:
        """Copy a real skill into a temporary root, optionally change it, and validate it."""

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw).resolve().joinpath(*base, "repo")
            skill_dir = root / "skills" / self.SKILL
            shutil.copytree(REPO / "skills" / self.SKILL, skill_dir)
            if callable(mutate):
                mutate(skill_dir)
            errors: list[str] = []
            with mock.patch.object(validate_catalog, "ROOT", root):
                validate_catalog.validate_skill_directory(self.SKILL, skill_dir, errors)
            return errors

    @staticmethod
    def append(text: str) -> object:
        def run(skill_dir: Path) -> None:
            path = skill_dir / "SKILL.md"
            path.write_text(path.read_text(encoding="utf-8") + text, encoding="utf-8")

        return run

    def test_unchanged_real_skill_has_no_errors(self) -> None:
        self.assertEqual([], self.validate())

    def test_a_checkout_under_a_folder_named_like_a_forbidden_directory_is_fine(self) -> None:
        self.assertEqual([], self.validate(base=("scripts", "commands")))

    def test_placeholders_are_rejected(self) -> None:
        for marker in ("TODO", "TBD"):
            with self.subTest(marker=marker):
                errors = self.validate(self.append(f"\n{marker}: finish this\n"))
                self.assertTrue(any("unresolved placeholder" in error for error in errors), errors)

    def test_wrong_version_is_rejected(self) -> None:
        def change(skill_dir: Path) -> None:
            path = skill_dir / "SKILL.md"
            path.write_text(
                path.read_text(encoding="utf-8").replace(f'version: "{VERSION}"', 'version: "0.0.1"'),
                encoding="utf-8",
            )

        errors = self.validate(change)
        self.assertTrue(any("version must be" in error for error in errors), errors)

    def test_overlong_description_is_rejected(self) -> None:
        def change(skill_dir: Path) -> None:
            path = skill_dir / "SKILL.md"
            lines = path.read_text(encoding="utf-8").split("\n")
            index = next(i for i, line in enumerate(lines) if line.startswith("description:"))
            lines[index] = "description: " + "x" * 1100
            path.write_text("\n".join(lines), encoding="utf-8")

        errors = self.validate(change)
        self.assertTrue(any("1 to 1024 characters" in error for error in errors), errors)

    def test_symlinks_are_rejected(self) -> None:
        def change(skill_dir: Path) -> None:
            try:
                os.symlink(skill_dir / "SKILL.md", skill_dir / "references" / "alias.md")
            except OSError:
                self.skipTest("symlinks are unavailable on this system")

        errors = self.validate(change)
        self.assertTrue(any("symlinks are not allowed" in error for error in errors), errors)

    def test_forbidden_directories_inside_a_skill_are_rejected(self) -> None:
        def change(skill_dir: Path) -> None:
            (skill_dir / "hooks").mkdir()
            (skill_dir / "hooks" / "run.md").write_text("not allowed\n", encoding="utf-8")

        errors = self.validate(change)
        self.assertTrue(any("forbidden skill directories" in error for error in errors), errors)


class FreshnessTests(unittest.TestCase):
    @staticmethod
    def pins() -> tuple[date, int]:
        value = json.loads((REPO / "catalog" / "upstream-pins.json").read_text(encoding="utf-8"))
        return date.fromisoformat(value["reviewed_on"]), int(value["max_review_age_days"])

    def test_pins_pass_on_the_last_allowed_day(self) -> None:
        reviewed, maximum = self.pins()
        errors, report = check_upstream_freshness(online=False, today=reviewed + timedelta(days=maximum))
        self.assertEqual([], errors)
        self.assertEqual("pass", report["result"])

    def test_pins_fail_the_day_after_the_limit(self) -> None:
        reviewed, maximum = self.pins()
        errors, _ = check_upstream_freshness(online=False, today=reviewed + timedelta(days=maximum + 1))
        self.assertTrue(any("overdue" in error for error in errors), errors)


class ReleaseManifestTests(unittest.TestCase):
    def fake_git(self, head: str, status: str) -> object:
        def run(arguments: list[str]) -> str:
            if arguments[:1] == ["rev-parse"]:
                return head
            if arguments[:1] == ["status"]:
                return status
            return ""

        return run

    def test_commit_must_be_a_full_lowercase_sha(self) -> None:
        for value in ("abc123", "A" * 40, SHA[:-1]):
            with self.subTest(value=value), self.assertRaises(ValueError):
                build_release_manifest.build(value)

    def test_head_must_equal_the_source_commit(self) -> None:
        with mock.patch.object(build_release_manifest, "_git_text", self.fake_git("b" * 40, "")):
            with self.assertRaisesRegex(ValueError, "must equal the clean checkout HEAD"):
                build_release_manifest.build(SHA)

    def test_checkout_must_be_clean(self) -> None:
        with mock.patch.object(build_release_manifest, "_git_text", self.fake_git(SHA, " M file")):
            with self.assertRaisesRegex(ValueError, "clean checkout"):
                build_release_manifest.build(SHA)

    def test_output_is_deterministic_and_uses_the_given_date(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            first, second = Path(raw) / "one.json", Path(raw) / "two.json"
            with (
                mock.patch.object(build_release_manifest, "_require_clean_source_checkout"),
                mock.patch.object(build_release_manifest, "_require_tracked_source_artifact"),
            ):
                build_release_manifest.build(SHA, first, date(2026, 1, 2))
                build_release_manifest.build(SHA, second, date(2026, 1, 2))
            self.assertEqual(first.read_bytes(), second.read_bytes())
            document = json.loads(first.read_text(encoding="utf-8"))
        self.assertEqual("2026-01-02", document["created_on"])
        self.assertEqual(SHA, document["source_commit"])
        self.assertEqual(VERSION, document["catalog_version"])
        self.assertGreater(len(document["artifacts"]), 100)


class GateCommandTests(unittest.TestCase):
    def test_mutating_commands_are_flagged(self) -> None:
        for command in (
            "gofmt -w .",
            "prettier --write .",
            "go generate ./...",
            "go fmt ./...",
            "terraform fmt",
            "cargo fmt",
            "npm install",
            "pip install requests",
            "pip install -U requests",
            "terraform apply",
        ):
            with self.subTest(command=command):
                self.assertTrue(is_mutating_command(command))

    def test_read_only_gates_are_not_flagged(self) -> None:
        for command in (
            "go test ./...",
            "python -m compileall src",
            "swift test",
            "npm run lint",
            "npm test",
            "terraform fmt -check -recursive",
            "terraform validate",
            "gofmt -l .",
            "cargo fmt --check",
        ):
            with self.subTest(command=command):
                self.assertFalse(is_mutating_command(command))


if __name__ == "__main__":
    unittest.main()
