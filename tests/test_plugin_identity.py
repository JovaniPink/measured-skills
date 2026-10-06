"""Check original shared branding in generated Claude plugins."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_distributions as distributions  # noqa: E402


class PluginIdentityTests(unittest.TestCase):
    def test_each_claude_pack_has_the_canonical_icon(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            _, plugins, _ = distributions.build(Path(temporary))
            canonical = (ROOT / ".claude-plugin" / "icon.svg").read_bytes()
            for plugin in plugins.values():
                manifest = json.loads((plugin / ".claude-plugin/plugin.json").read_text())
                self.assertEqual("./.claude-plugin/icon.svg", manifest["icon"])
                self.assertEqual(canonical, (plugin / ".claude-plugin/icon.svg").read_bytes())

    def test_missing_icon_fails_before_replacing_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "output"
            output.mkdir()
            sentinel = output / "keep.txt"
            sentinel.write_text("keep")
            with patch.object(distributions, "PLUGIN_ICON", root / "missing.svg"):
                with self.assertRaises(ValueError):
                    distributions.build(output)
            self.assertEqual("keep", sentinel.read_text())

    def test_symlinked_icon_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            real = root / "real.svg"
            real.write_text("<svg/>")
            link = root / "link.svg"
            link.symlink_to(real)
            with patch.object(distributions, "PLUGIN_ICON", link):
                with self.assertRaises(ValueError):
                    distributions.build(root / "output")
