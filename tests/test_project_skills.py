"""Projection boundaries with real disposable Git source pins."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from project_skills import project


class ProjectSkillsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / "source"
        self.app = self.root / "app"
        self.source.mkdir()
        self.app.mkdir()
        subprocess.run(["git", "init", "-q", str(self.source)], check=True)
        subprocess.run(["git", "-C", str(self.source), "config", "user.name", "Fixture"], check=True)
        subprocess.run(["git", "-C", str(self.source), "config", "user.email", "fixture@example.invalid"], check=True)
        for skill, invocation in (("read-check", "implicit"), ("deliver-check", "explicit")):
            target = self.source / "skills" / skill
            (target / "agents").mkdir(parents=True)
            (target / "references").mkdir()
            (target / "SKILL.md").write_text(f'---\nname: {skill}\ndescription: Synthetic fixture\nmetadata:\n  version: "0.18.0"\n  invocation: "{invocation}"\n  risk_class: "{"read-only" if invocation == "implicit" else "bounded-execution"}"\n---\n\n# Fixture\n[Checks](references/check.md)\n')
            (target / "references/check.md").write_text("Synthetic check.\n")
            (target / "agents/openai.yaml").write_text(f'interface:\n  default_prompt: "Use ${skill}."\n' + ('policy:\n  allow_implicit_invocation: false\n' if invocation == "explicit" else ''))
        (self.source / "catalog").mkdir()
        (self.source / "catalog/revocations.json").write_text('{"entries": []}\n')
        self.commit()
        (self.app / "docs/skills").mkdir(parents=True)
        (self.app / "docs/skills/contract.md").write_text("# Contract\nSynthetic read/write owner.\n")
        self.manifest = {"format_version": 1, "source_commit": self.sha, "prefix": "fixture", "contract": "docs/skills/contract.md", "skills": ["read-check", "deliver-check"], "codex_version": "0.154.0"}
        self.save()

    def commit(self) -> None:
        subprocess.run(["git", "-C", str(self.source), "add", "."], check=True)
        subprocess.run(["git", "-C", str(self.source), "commit", "-qm", "fixture"], check=True)
        self.sha = subprocess.check_output(["git", "-C", str(self.source), "rev-parse", "HEAD"], text=True).strip()

    def save(self) -> None:
        (self.app / "docs/skills/project.json").write_text(json.dumps(self.manifest))

    def test_layout_controls_and_reproducibility(self) -> None:
        self.assertEqual([], project(self.source, self.app, False))
        self.assertEqual([], project(self.source, self.app, True))
        self.assertFalse((self.app / ".agents/skills/fixture-deliver-check").exists())
        self.assertIn("allow_implicit_invocation: false", (self.app / ".codex/skills/fixture-deliver-check/agents/openai.yaml").read_text())
        self.assertIn("disable-model-invocation: true", (self.app / ".claude/skills/fixture-deliver-check/SKILL.md").read_text())
        self.assertTrue((self.app / ".agents/skills/fixture-read-check/references/project-contract.md").exists())

    def test_one_to_zero_to_one_preserves_unowned_files(self) -> None:
        self.manifest["skills"] = ["read-check"]
        self.save()
        project(self.source, self.app, False)
        unrelated = self.app / ".agents/skills/unowned/SKILL.md"
        unrelated.parent.mkdir()
        unrelated.write_text("owned by someone else")
        self.manifest["skills"] = []
        self.save()
        project(self.source, self.app, False)
        self.assertFalse((self.app / ".agents/skills/fixture-read-check").exists())
        self.assertTrue(unrelated.exists())
        self.manifest["skills"] = ["read-check"]
        self.save()
        project(self.source, self.app, False)
        self.assertEqual([], project(self.source, self.app, True))

    def test_revocation_removes_previously_owned_projection(self) -> None:
        project(self.source, self.app, False)
        (self.source / "catalog/revocations.json").write_text('{"entries": [{"skill": "deliver-check"}]}')
        self.commit()
        self.manifest["source_commit"] = self.sha
        self.save()
        project(self.source, self.app, False)
        self.assertFalse((self.app / ".codex/skills/fixture-deliver-check").exists())

    def test_identical_metadata_different_bytes_and_missing_extra(self) -> None:
        project(self.source, self.app, False)
        p = self.app / ".agents/skills/fixture-read-check/references/check.md"
        info = p.stat()
        p.write_bytes(b"X" * info.st_size)
        os.utime(p, ns=(info.st_atime_ns, info.st_mtime_ns))
        self.assertTrue(project(self.source, self.app, True))
        with self.assertRaises(ValueError):
            project(self.source, self.app, False)
        p.unlink()
        self.assertTrue(project(self.source, self.app, True))
        project(self.source, self.app, False)
        (p.parent / "unowned.md").write_text("extra")
        with self.assertRaises(ValueError):
            project(self.source, self.app, False)

    def test_traversal_symlink_and_collision_fail_before_mutation(self) -> None:
        for field, value in (("prefix", "../escape"), ("contract", "../contract.md"), ("source_commit", "main"), ("codex_version", "0.155.0"), ("skills", ["../escape"])):
            original = self.manifest[field]
            self.manifest[field] = value
            self.save()
            with self.assertRaises(ValueError):
                project(self.source, self.app, False)
            self.manifest[field] = original
        self.save()
        (self.app / ".agents").symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(ValueError):
            project(self.source, self.app, False)
        (self.app / ".agents").unlink()
        collision = self.app / ".agents/skills/fixture-read-check/SKILL.md"
        collision.parent.mkdir(parents=True)
        collision.write_text("unowned")
        with self.assertRaises(ValueError):
            project(self.source, self.app, False)
        self.assertEqual("unowned", collision.read_text())
        self.assertFalse((self.app / ".codex").exists())

    def test_stale_contract_and_source_pin(self) -> None:
        project(self.source, self.app, False)
        (self.app / "docs/skills/contract.md").write_text("changed contract")
        self.assertTrue(project(self.source, self.app, True))
        self.manifest["source_commit"] = "0" * 40
        self.save()
        with self.assertRaises(ValueError):
            project(self.source, self.app, True)

    def test_partial_write_rolls_back(self) -> None:
        project(self.source, self.app, False)
        before = {p.relative_to(self.app): p.read_bytes() for p in self.app.rglob("*") if p.is_file()}
        (self.app / "docs/skills/contract.md").write_text("changed")
        replace = os.replace
        calls = 0

        def fail_once(source: object, target: object) -> None:
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("synthetic interruption")
            replace(source, target)  # type: ignore[arg-type]

        with patch("project_skills.os.replace", fail_once), self.assertRaises(OSError):
            project(self.source, self.app, False)
        for relative, payload in before.items():
            if relative.as_posix() != "docs/skills/contract.md":
                self.assertEqual(payload, (self.app / relative).read_bytes())

class PrimaryAuthorityTests(unittest.TestCase):
    def test_framework_publishers_allowed_without_skill_repository_exception(self) -> None:
        from check_repository_independence import PRIMARY_AUTHORITY_HOSTS, scan_text
        for host in ("developer.apple.com", "nextjs.org", "react.dev"):
            self.assertIn(host, PRIMARY_AUTHORITY_HOSTS)
        self.assertTrue(scan_text("skills/example/references/check.md", "https://github.com/unknown/skill-catalog"))

class FrozenWorkflowCasesTests(unittest.TestCase):
    def test_frozen_cases_have_semantic_contracts(self) -> None:
        from schema_validation import validate_instance
        root = Path(__file__).resolve().parents[1]
        schema = json.loads((root / "evals/qualification-case-schema-v1.json").read_text())
        cases = sorted((root / "evals/owned-workflows/cases").glob("*.json"))
        self.assertEqual(49, len(cases))
        for path in cases:
            value = json.loads(path.read_text())
            self.assertEqual([], validate_instance(value, schema), path.name)
            self.assertTrue(any(item["kind"] == "semantic" and item["mandatory"] for item in value["obligations"]))
