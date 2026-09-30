from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_distributions as distributions  # noqa: E402
from cataloglib import EXPLICIT_SKILLS, skills_by_plugin  # noqa: E402
from sync_private_overlay import sync  # noqa: E402


class RemovalRegressions(unittest.TestCase):
    def test_overlay_one_zero_one(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary).resolve() / "repo"
            shutil.copytree(ROOT / "examples" / "private-overlay", repo)
            source = repo / ".agent-skills" / "skills"
            backup = Path(temporary) / "backup"
            shutil.copytree(source, backup)
            self.assertEqual([], sync(repo, check_only=False))
            for path in source.iterdir():
                shutil.rmtree(path)
            self.assertEqual([], sync(repo, check_only=False))
            for client in (".agents", ".claude"):
                self.assertEqual([], list((repo / client / "skills").iterdir()))
            self.assertEqual([], sync(repo, check_only=True))
            shutil.copytree(backup, source, dirs_exist_ok=True)
            self.assertEqual([], sync(repo, check_only=False))
            self.assertEqual([], sync(repo, check_only=True))

    def test_revoked_pack_and_entire_catalog_are_removed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            distributions.build(output)
            groups = skills_by_plugin()
            removed = next(iter(groups))
            with patch.object(distributions, "skills_by_plugin", return_value={name: skills for name, skills in groups.items() if name != removed}):
                distributions.build(output)
            for client in ("codex", "claude", "antigravity"):
                self.assertFalse((output / client / removed).exists())
            with patch.object(distributions, "skills_by_plugin", return_value={}):
                distributions.build(output)
                distributions.build(output)
            for client in ("codex", "claude", "antigravity"):
                self.assertEqual([], list((output / client).iterdir()))

    def test_antigravity_tracked_packs_omit_explicit_workflows(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            distributions.build(Path(temporary))
            entries = list((Path(temporary) / "antigravity").glob("*/skills/*"))
            self.assertFalse(set(EXPLICIT_SKILLS) & {path.name for path in entries})

    def test_unowned_directory_is_preserved_and_generation_refuses(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            unknown = output / "claude" / "unowned"
            unknown.mkdir(parents=True)
            (unknown / "keep").write_text("evidence")
            with self.assertRaises(ValueError):
                distributions.build(output)
            self.assertEqual("evidence", (unknown / "keep").read_text())

    def test_symlinked_client_root_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "output"
            output.mkdir()
            outside = Path(temporary) / "outside"
            outside.mkdir()
            (output / "codex").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                distributions.build(output)
            self.assertEqual([], list(outside.iterdir()))

    def test_symlinked_output_root_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            outside = root / "outside"
            outside.mkdir()
            output = root / "output"
            output.symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                distributions.build(output)
            self.assertEqual([], list(outside.iterdir()))
