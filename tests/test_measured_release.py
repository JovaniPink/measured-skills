from __future__ import annotations

import sys
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from cataloglib import CATALOG_NAME, ROOT, SKILLS, directory_hashes, skills_by_plugin  # noqa: E402


class MeasuredReleaseTests(unittest.TestCase):
    def test_release_identity_and_historical_evidence(self) -> None:
        root = Path(__file__).resolve().parents[1]
        mappings = json.loads((root / "catalog" / "plugin-migrations.json").read_text())
        targets = [target for values in mappings["plugins"].values() for target in values]
        self.assertEqual(set(skills_by_plugin()) - {"measured-swift-workflows", "measured-nextjs-workflows"}, set(targets))
        self.assertEqual(len(targets), len(set(targets)))
        for source in (root / "skills").glob("*/SKILL.md"):
            self.assertNotIn('author: "Jovani', source.read_text())
            self.assertNotIn('plugin: "jovanipink-', source.read_text())
        ledger = json.loads((root / "catalog" / "evidence.json").read_text())
        for record in ledger["skills"]:
            for observation in record.get("historical_observations", []):
                matrix = json.loads((root / observation["record_file"]).read_text())
                original = next(r for r in matrix["records"] if r["case_id"] == observation["case_id"])
                for key in ("client_version", "surface", "observed_at", "catalog_version"):
                    self.assertEqual(original[key], observation[key])
                self.assertEqual("none", record["behavioral_evidence"]["status"])

    def test_export_rejects_missing_references_before_writing(self) -> None:
        from export_selected import export

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / "skills" / "test-strategy"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("[missing](references/missing.md)")
            with patch("export_selected.ROOT", root), self.assertRaises(ValueError):
                export(root / "output", "codex", ["test-strategy"])
            self.assertFalse((root / "output").exists())

    def test_pack_partition(self) -> None:
        packs = skills_by_plugin()
        self.assertEqual("measured-skills", CATALOG_NAME)
        self.assertEqual(11, len(packs))
        self.assertEqual(86, len(SKILLS))
        self.assertEqual(86, len({s for skills in packs.values() for s in skills}))
        self.assertEqual(5, len(packs["measured-engineering-build"]))
        self.assertEqual(11, len(packs["measured-engineering-review"]))
        self.assertEqual(9, len(packs["measured-engineering-delivery"]))

    def test_antigravity_manifests_use_documented_fields_only(self) -> None:
        for plugin in skills_by_plugin():
            manifest = ROOT / "plugins" / "antigravity" / plugin / "plugin.json"
            data = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual({"name", "description"}, set(data), plugin)

    def test_selected_exports(self) -> None:
        from export_selected import export

        for client in ("codex", "claude", "antigravity"):
            with tempfile.TemporaryDirectory() as tmp:
                first, second = Path(tmp) / "first", Path(tmp) / "second"
                export(first, client, ["test-strategy", "cross-stack-quality-gates"])
                export(second, client, ["cross-stack-quality-gates", "test-strategy"])
                self.assertEqual(directory_hashes(first), directory_hashes(second))
                with self.assertRaises(ValueError):
                    export(first, client, ["test-strategy"])
                with self.assertRaises(ValueError):
                    export(Path(tmp) / "unknown", client, ["unknown"])
                with self.assertRaises(ValueError):
                    export(Path(tmp) / "duplicate", client, ["test-strategy", "test-strategy"])
                with self.assertRaises(ValueError):
                    export(Path(tmp) / "explicit", client, ["publish-change-safely"])
                self.assertTrue((first / "cross-stack-quality-gates" / "references").is_dir())
                if client == "codex":
                    text = (first / "test-strategy" / "agents" / "openai.yaml").read_text()
                    self.assertIn("$test-strategy", text)
                    self.assertNotIn("$measured-", text)
                else:
                    self.assertFalse((first / "test-strategy" / "agents").exists())
