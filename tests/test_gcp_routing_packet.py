from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import export_selected  # noqa: E402


class GcpRoutingPacketTests(unittest.TestCase):
    def test_standalone_exports_preserve_required_reference_bytes_and_controls(self) -> None:
        name = 'gcp-data-engineering-profile'
        source = ROOT / 'skills' / name
        canonical = (source / 'SKILL.md').read_bytes()
        for client in ('codex', 'claude', 'antigravity'):
            with self.subTest(client=client), tempfile.TemporaryDirectory() as raw:
                output = Path(raw).resolve() / 'stage with spaces'
                export_selected.export(output, client, [name])
                self.assertEqual(canonical, (output / name / 'SKILL.md').read_bytes())
                for reference in (source / 'references').glob('*.md'):
                    exported = output / name / 'references' / reference.name
                    self.assertEqual(reference.read_bytes(), exported.read_bytes())
                manifest = json.loads((output / 'export-manifest.json').read_text())
                for relative, digest in manifest['files'].items():
                    self.assertEqual(digest, hashlib.sha256((output / relative).read_bytes()).hexdigest())
                frontmatter = yaml.safe_load(canonical.decode().split('---')[1])
                self.assertEqual('implicit', frontmatter['metadata']['invocation'])
                self.assertEqual('read-only', frontmatter['metadata']['risk_class'])
                self.assertNotIn('disable-model-invocation', frontmatter)
                self.assertNotIn('allowed-tools', frontmatter)
                if client == 'codex':
                    self.assertEqual((source / 'agents/openai.yaml').read_bytes(),
                                     (output / name / 'agents/openai.yaml').read_bytes())
                    native = yaml.safe_load((output / name / 'agents/openai.yaml').read_text())
                    self.assertTrue(native['policy']['allow_implicit_invocation'])
                else:
                    self.assertFalse((output / name / 'agents').exists())

    def test_prepared_controls_bind_unchanged_payloads_and_current_source(self) -> None:
        packet = json.loads((ROOT / 'docs/audits/gcp-routing-retest-preparation-2026-10-26.json').read_text())
        original = json.loads((ROOT / 'docs/audits/claude-retest-preparation-2026-10-26.json').read_text())
        implicit = {row['source_case']: row for row in original['rows']
                    if row['selection_mode'] == 'implicit'}
        self.assertEqual('prepared_not_run', packet['status'])
        self.assertEqual(0, packet['requests_executed'])
        self.assertEqual(len(packet['rows']), packet['case_session_ceiling'])
        self.assertEqual(len(packet['continuity_followups']), packet['followup_ceiling'])
        for row in packet['rows']:
            with self.subTest(order=row['order']):
                self.assertEqual('not_run', row['execution'])
                self.assertEqual(implicit[row['source_case']]['prompt'], row['task_prompt'])
                self.assertEqual(row['task_prompt_sha256'],
                                 hashlib.sha256(row['task_prompt'].encode()).hexdigest())
                self.assertFalse(row['task_prompt'].startswith('/'))
                if row['selection_mode'] == 'native_command_control':
                    self.assertEqual('/measured-daily-pilot:' + row['expected_skill'], row['native_command'])
                else:
                    self.assertIsNone(row['native_command'])
        for current, old in zip(packet['continuity_followups'], original['continuity_followups'], strict=True):
            self.assertEqual(4, current['after_row'])
            self.assertEqual(old['prompt'], current['prompt'])
            self.assertEqual(current['prompt_sha256'], hashlib.sha256(current['prompt'].encode()).hexdigest())
        for relative, digest in packet['canonical_gcp_files'].items():
            self.assertEqual(digest, hashlib.sha256((ROOT / relative).read_bytes()).hexdigest())


if __name__ == '__main__':
    unittest.main()
