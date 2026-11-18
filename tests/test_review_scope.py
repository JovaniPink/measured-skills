"""Review explanation is an optional action, not another execution scope."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import discovery  # noqa: E402


class ReviewScopeTests(unittest.TestCase):
    def test_all_review_requests_bind_uncommitted_content_only_for_working_tree_scope(self) -> None:
        registry = json.loads((ROOT / discovery.REGISTRY).read_text())
        route = next(r for r in registry['routes'] if r['id'] == 'review')
        self.assertIn('working-tree scope only when requested', route['required_inputs'])
        self.assertIn('Confirm committed or working-tree scope', route['steps'])
        for mode in route['modes']:
            for client, prompt in mode['prompts'].items():
                with self.subTest(mode=mode['id'], client=client):
                    self.assertIn('only when the requested scope includes the working tree', prompt)
                    self.assertNotIn('including relevant staged, unstaged and untracked content hashes', prompt)
                    self.assertNotIn('the current branch, relevant dirty/untracked files', prompt)
                    self.assertIn('Pin PR base and head when available.', prompt)
                    self.assertIn('For a pasted diff, review the supplied snapshot and report unavailable context.', prompt)

    def test_registry_accepts_explanation_only_on_review_route(self) -> None:
        data = json.loads((ROOT / discovery.REGISTRY).read_text())
        known = {s['skill'] for s in json.loads((ROOT / 'catalog/skills.json').read_text())['skills']}
        review = next(r for r in data['routes'] if r['id'] == 'review')
        mode = copy.deepcopy(review['modes'][0])
        mode['id'] = 'explain-scope'
        review['modes'] = [review['modes'][0], mode]
        self.assertEqual([], discovery.registry_errors(data, known))
        review['modes'].append(copy.deepcopy(mode))
        self.assertTrue(discovery.registry_errors(data, known))
        review['modes'].pop()
        review['id'] = 'unrelated-route'
        self.assertTrue(discovery.registry_errors(data, known))
        review['id'] = 'review'
        mode['id'] = 'execute-unbounded'
        self.assertTrue(discovery.registry_errors(data, known))

    def test_review_actions_preserve_client_identity_and_read_only_scope(self) -> None:
        current = json.loads((ROOT / discovery.REGISTRY).read_text())
        new = next(r for r in current['routes'] if r['id'] == 'review')
        self.assertEqual(['assess', 'explain-scope'], [m['id'] for m in new['modes']])
        self.assertEqual('Inspection and recommendations; no edits or external writes.', new['modes'][0]['scope'])
        for prompt in new['modes'][0]['prompts'].values():
            self.assertIn('Findings only: no edits, replies, approvals or publication.', prompt)
        data = discovery.build_data('0' * 40, verify_source=False)
        route = next(r for r in data['routes'] if r['id'] == 'review')
        for mode in route['modes']:
            for client in data['clients']:
                with self.subTest(mode=mode['id'], client=client):
                    self.assertEqual('review-code-change', mode['action']['skill'])
                    self.assertEqual('implicit', mode['action']['invocation'])
                    self.assertEqual(discovery.ordinary_prompt(mode['prompts'][client], client),
                                     mode['ordinary_prompts'][client])
                    self.assertIn(mode['ordinary_prompts'][client], discovery.markdown(data))
        self.assertIn('data-action-scope="explain-scope"', discovery.offline_html(data))


if __name__ == '__main__':
    unittest.main()
