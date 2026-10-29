"""Check executable registry selections and standalone reference delivery."""
from __future__ import annotations
import json
from pathlib import Path
import re
import sys
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from export_selected import export  # noqa: E402
from cataloglib import read_skill_metadata  # noqa: E402


class WorkflowDepthTests(unittest.TestCase):
    def test_native_modes_resolve_and_antigravity_excludes_explicit_commands(self) -> None:
        data = json.loads((ROOT / 'catalog/workflows.json').read_text())
        self.assertEqual(15, len(data['routes']))
        for route in data['routes']:
            for mode in route['modes']:
                name = mode.get('command_skill', route['primary_skill'])
                meta = read_skill_metadata(ROOT / 'skills' / name)
                for client, marker in (('codex', '$'), ('claude', '/')):
                    self.assertTrue(mode['prompts'][client].startswith(marker + meta['plugin'] + ':' + name + ' '))
                if meta['invocation'] == 'explicit':
                    self.assertNotIn(name, mode['prompts']['antigravity'])
        for identity in ('diagnose-data-query', 'review-data-replay'):
            route = next(r for r in data['routes'] if r['id'] == identity)
            self.assertEqual(['assess'], [m['id'] for m in route['modes']])

    def test_new_references_survive_each_supported_standalone_export(self) -> None:
        names = ['explain-codebase', 'plan-change', 'verify-claims', 'design-module-interface',
                 'stack-postgresql-sql', 'stack-gcp-data', 'stack-swift-swiftui']
        for client in ('codex', 'claude', 'antigravity'):
            with tempfile.TemporaryDirectory() as raw:
                dest = Path(raw).resolve() / 'export with spaces'
                export(dest, client, names)
                for name in names:
                    for path in (ROOT / 'skills' / name / 'references').glob('*.md'):
                        self.assertEqual(path.read_bytes(), (dest / name / 'references' / path.name).read_bytes())
                    for relative in re.findall(r'\]\((references/[^)]+)\)', (dest / name / 'SKILL.md').read_text()):
                        self.assertTrue((dest / name / relative).is_file(), relative)

    def test_new_source_pins_extend_without_changing_existing_sources(self) -> None:
        before = json.loads(subprocess.check_output(
            ['git', 'show', '62af7d15431c9b3e653523888cd574b7319d7171:catalog/upstream-pins.json'], cwd=ROOT))
        # This assertion protects the historical five-source addition, not later reviewed repins.
        current = json.loads(subprocess.check_output(
            ['git', 'show', '3f3cbe34019f0edeaaf620631332c4b1a6d1e4b6:catalog/upstream-pins.json'], cwd=ROOT))
        added = json.loads((ROOT / 'docs/audits/workflow-depth-sources-2026-10-28.json').read_text())
        expected = {r['source_url']: r for r in before['sources']}
        self.assertEqual(5, len(added['sources']))
        for row in added['sources']:
            self.assertNotIn(row['url'], expected)
            self.assertEqual(2, row['identical_retrievals'])
            self.assertRegex(row['sha256'], r'^[0-9a-f]{64}$')
            expected[row['url']] = dict(source_url=row['url'], marker_kind='content-sha256', marker_value=row['sha256'])
        self.assertEqual(expected, {r['source_url']: r for r in current['sources']})
        self.assertEqual({k: v for k, v in before.items() if k != 'sources'},
                         {k: v for k, v in current.items() if k != 'sources'})

    def test_scenario_inventory_has_distinct_evidence_cases(self) -> None:
        data = json.loads((ROOT / 'evals/workflow-depth/cases.json').read_text())
        self.assertEqual('prepared_not_run', data['status'])
        self.assertEqual(24, len({r['id'] for r in data['cases']}))
        routes = {r['id'] for r in json.loads((ROOT / 'catalog/workflows.json').read_text())['routes']}
        for area in {r['area'] for r in data['cases']}:
            self.assertEqual({'useful', 'near-miss', 'safety'}, {r['kind'] for r in data['cases'] if r['area'] == area})
        for row in data['cases']:
            self.assertIn(row['candidate_route'], routes)
            self.assertEqual('prepared_not_run', row['status'])
            self.assertTrue(row['prompt'] and row['expected_output'] and row['forbidden_conclusions'])


if __name__ == '__main__':
    unittest.main()
