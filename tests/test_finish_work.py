"""Finish-work selection and narrowly reviewed prompt authorities."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import check_repository_independence as independence  # noqa: E402
import export_selected  # noqa: E402
from cataloglib import EXPLICIT_SKILLS, directory_hashes  # noqa: E402

PROMPT_SOURCES = (
    'https://developers.openai.com/api/docs/guides/prompt-engineering',
    'https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md',
)


class FinishWorkTests(unittest.TestCase):
    def test_prompt_authority_allowances_are_exact(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'provenance').mkdir()
            for source in PROMPT_SOURCES:
                for url, valid in ((source, True), (source + '?unreviewed=1', False),
                                   (source.rsplit('/', 1)[0] + '/unreviewed', False)):
                    with self.subTest(url=url):
                        (root / 'provenance/catalog.json').write_text(json.dumps({'entries': [
                            {'skill': 'engineering-prompt-review', 'source_url': url}]}))
                        with patch.object(independence, 'ROOT', root):
                            self.assertEqual(not valid, bool(independence.provenance_source_errors()))

    def test_finish_profile_exports_are_deterministic_and_implicit(self) -> None:
        for client in ('codex', 'claude', 'antigravity'):
            with self.subTest(client=client), tempfile.TemporaryDirectory() as temporary:
                names = export_selected.profile_skills('finish-existing-work-experimental', client)
                self.assertEqual(14, len(names))
                self.assertIn('engineering-prompt-review', names)
                self.assertFalse(set(names) & EXPLICIT_SKILLS)
                first, second = Path(temporary).resolve() / 'first', Path(temporary).resolve() / 'second'
                export_selected.export(first, client, names)
                export_selected.export(second, client, names)
                self.assertEqual(directory_hashes(first), directory_hashes(second))
                prompt = (first / 'engineering-prompt-review/SKILL.md').read_text()
                self.assertIn('name: engineering-prompt-review', prompt)
                if client == 'codex':
                    self.assertIn('allow_implicit_invocation: true',
                                  (first / 'engineering-prompt-review/agents/openai.yaml').read_text())
                if client == 'claude':
                    self.assertNotIn('disable-model-invocation: true', prompt)
                with self.assertRaises(ValueError):
                    export_selected.export(first, client, names)
                with self.assertRaises(ValueError):
                    export_selected.export(Path(temporary).resolve() / 'excluded', client, names + ['plan-execution'])

    def test_prompt_cases_preserve_unrun_status_and_case_classes(self) -> None:
        records = json.loads((ROOT / 'evals/cases.json').read_text())['skills']
        record = next(r for r in records if r['skill'] == 'engineering-prompt-review')
        self.assertEqual([5, 4, 6], [len(record[k]) for k in ('positive', 'near_miss', 'safety')])
        self.assertEqual('blocked', record['baseline_comparison']['status'])
        self.assertIn('Not run:', record['baseline_comparison']['note'])
        prompts = [r['prompt'] for r in record['positive']]
        self.assertTrue(all('engineering-prompt-review' not in p for p in prompts))
