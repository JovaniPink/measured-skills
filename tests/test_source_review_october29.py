"""Bind individual source decisions without weakening unchanged freshness policy."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SourceReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ledger = json.loads((ROOT / 'docs/audits/source-review-2026-10-29.json').read_text())
        raw = subprocess.check_output([
            'git', 'show', self.ledger['reviewed_revision'] + ':catalog/upstream-pins.json'], cwd=ROOT)
        self.assertEqual(hashlib.sha256(raw).hexdigest(), self.ledger['pins_before_sha256'])
        self.before = json.loads(raw)
        self.current = json.loads((ROOT / 'catalog/upstream-pins.json').read_text())

    def assert_transition(self, ledger: dict[str, Any], current: dict[str, Any]) -> None:
        expected = {r['source_url']: r for r in self.before['sources']}
        decisions = ledger['records'] + ledger['supplementary_records']
        self.assertEqual(32, len(decisions))
        self.assertEqual(32, len({r['source_url'] for r in decisions}))
        for report, records in [('initial_report', ledger['records']),
                                ('intermediate_report', ledger['supplementary_records'])]:
            observed = json.loads((ROOT / ledger[report]).read_text())['records']
            self.assertEqual({r['source_url'] for r in observed if r['result'] == 'changed'},
                             {r['source_url'] for r in records})
        for record in decisions:
            url = record['source_url']
            self.assertEqual(expected[url], record['before_pin'])
            self.assertEqual(url, record['after_pin']['source_url'])
            self.assertEqual(record['before_pin']['marker_kind'], record['after_pin']['marker_kind'])
            self.assertEqual(2, len(record['observations']))
            for observation in record['observations']:
                self.assertEqual(record['after_pin']['marker_kind'], observation['marker_kind'])
                self.assertEqual(record['after_pin']['marker_value'], observation['marker_value'])
                self.assertEqual(url, observation['final_url'])
                self.assertRegex(observation['raw_sha256'], r'^[0-9a-f]{64}$')
            expected[url] = record['after_pin']
        self.assertEqual(expected, {r['source_url']: r for r in current['sources']})
        self.assertEqual(len(expected), len(current['sources']))
        self.assertEqual({k: v for k, v in self.before.items() if k != 'sources'},
                         {k: v for k, v in current.items() if k != 'sources'})
        final = json.loads((ROOT / ledger['final_report']).read_text())
        self.assertEqual('pass', final['result'])
        self.assertEqual(set(expected), {r['source_url'] for r in final['records']})
        for result in final['records']:
            pin = expected[result['source_url']]
            marker = pin['marker_kind'] + ':' + pin['marker_value']
            self.assertEqual((marker, marker, 'pass'),
                             (result['expected_marker'], result['observed_marker'], result['result']))

    def test_reviewed_transitions_preserve_other_sources_and_policy(self) -> None:
        self.assert_transition(self.ledger, self.current)
        self.assertEqual(self.ledger['pins_after_sha256'],
                         hashlib.sha256((ROOT / 'catalog/upstream-pins.json').read_bytes()).hexdigest())

    def test_unreviewed_changes_and_weakened_bindings_fail(self) -> None:
        for mutation in ('unreviewed', 'review_age', 'method', 'url', 'missing', 'disagreement'):
            with self.subTest(mutation=mutation):
                ledger, current = deepcopy(self.ledger), deepcopy(self.current)
                if mutation == 'unreviewed':
                    reviewed = {r['source_url'] for r in ledger['records'] + ledger['supplementary_records']}
                    next(r for r in current['sources'] if r['source_url'] not in reviewed)['marker_value'] = 'tampered'
                elif mutation == 'review_age':
                    current['max_review_age_days'] += 1
                elif mutation == 'method':
                    ledger['records'][0]['after_pin']['marker_kind'] = 'last-modified'
                elif mutation == 'url':
                    ledger['records'][0]['after_pin']['source_url'] = 'https://example.invalid/'
                elif mutation == 'missing':
                    ledger['records'].pop()
                else:
                    ledger['records'][0]['observations'][1]['marker_value'] = 'different'
                with self.assertRaises(AssertionError):
                    self.assert_transition(ledger, current)


if __name__ == '__main__':
    unittest.main()
