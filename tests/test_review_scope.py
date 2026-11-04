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

    def test_new_action_preserves_existing_requests_and_client_identity(self) -> None:
        import subprocess

        baseline = json.loads(subprocess.check_output(
            ['git', 'show', '0a972d7b:catalog/workflows.json'], cwd=ROOT))
        current = json.loads((ROOT / discovery.REGISTRY).read_text())
        old = next(r for r in baseline['routes'] if r['id'] == 'review')
        new = next(r for r in current['routes'] if r['id'] == 'review')
        self.assertEqual(old['modes'][0], new['modes'][0])
        self.assertEqual(['assess', 'explain-scope'], [m['id'] for m in new['modes']])
        data = discovery.build_data('0' * 40, verify_source=False)
        route = next(r for r in data['routes'] if r['id'] == 'review')
        mode = route['modes'][1]
        for client in data['clients']:
            self.assertEqual('review-code-change', mode['action']['skill'])
            self.assertEqual('implicit', mode['action']['invocation'])
            self.assertEqual(discovery.ordinary_prompt(mode['prompts'][client], client),
                             mode['ordinary_prompts'][client])
            self.assertIn(mode['ordinary_prompts'][client], discovery.markdown(data))
        self.assertIn('data-action-scope="explain-scope"', discovery.offline_html(data))


if __name__ == '__main__':
    unittest.main()
