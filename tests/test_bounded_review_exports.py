"""Exercise standalone protocol delivery without running agents or installing skills."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import shutil
import tempfile
import unittest
import zipfile
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_distributions  # noqa: E402
import export_selected  # noqa: E402
import package_claude_ai  # noqa: E402
from cataloglib import EXPLICIT_SKILLS, read_skill_metadata  # noqa: E402

REFERENCES = {
    'code-change-review': 'bounded-review.md',
    'publish-change-safely': 'pr-maintenance.md',
}


class BoundedReviewExports(unittest.TestCase):
    def test_selected_review_includes_protocol_and_hash_receipt_on_each_client(self) -> None:
        for client in ('codex', 'claude', 'antigravity'):
            with self.subTest(client=client), tempfile.TemporaryDirectory() as temporary:
                output = Path(temporary).resolve() / 'review with spaces'
                export_selected.export(output, client, ['code-change-review'])
                relative = 'code-change-review/references/bounded-review.md'
                self.assertEqual((ROOT / 'skills' / relative).read_bytes(),
                                 (output / relative).read_bytes())
                receipt = json.loads((output / 'export-manifest.json').read_text())
                self.assertIn(relative, receipt['files'])
                self.assertEqual('not_installed', receipt['installation'])
                self.assertEqual('not_observed', receipt['behavior'])
                with self.assertRaises(ValueError):
                    export_selected.export(Path(temporary).resolve() / 'excluded', client,
                                           ['publish-change-safely'])

    def test_generated_packages_and_archives_keep_references_and_controls(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            build_distributions.build(root / 'plugins')
            shutil.copytree(ROOT / 'skills', root / 'skills')
            # Package the temporary Claude projection, not the tracked output.
            with patch.object(package_claude_ai, 'ROOT', root):
                archives = package_claude_ai.package(root / 'archives')
            self.assertEqual(len(list((ROOT / 'skills').glob('*/SKILL.md'))), len(archives))
            for skill, reference in REFERENCES.items():
                metadata = read_skill_metadata(ROOT / 'skills' / skill)
                plugin = metadata['plugin']
                expected = (ROOT / 'skills' / skill / 'references' / reference).read_bytes()
                explicit = metadata['invocation'] == 'explicit'
                for client in ('codex', 'claude', 'antigravity'):
                    target = root / 'plugins' / client / plugin / 'skills' / skill
                    if client == 'antigravity' and explicit:
                        self.assertFalse(target.exists())
                        continue
                    self.assertEqual(expected, (target / 'references' / reference).read_bytes())
                    body = (target / 'SKILL.md').read_text()
                    self.assertIn(f'(references/{reference})', body)
                    if client == 'codex':
                        policy = yaml.safe_load((target / 'agents/openai.yaml').read_text())
                        self.assertEqual(not explicit, policy['policy']['allow_implicit_invocation'])
                    if client == 'claude':
                        self.assertEqual(explicit, 'disable-model-invocation: true' in body)
                archive = root / 'archives' / f'{skill}-0.18.0.zip'
                with zipfile.ZipFile(archive) as bundle:
                    self.assertEqual(expected, bundle.read(f'{skill}/references/{reference}'))
                    body = bundle.read(f'{skill}/SKILL.md').decode()
                    self.assertEqual(explicit, 'disable-model-invocation: true' in body)
            self.assertEqual(17, len(EXPLICIT_SKILLS))
            exported = {p.parent.name for p in (root / 'plugins/antigravity').glob('*/skills/*/SKILL.md')}
            self.assertFalse(exported & EXPLICIT_SKILLS)
