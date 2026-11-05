"""Bind two later source changes without replacing the initial review checkpoint."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any
import unittest

ROOT = Path(__file__).resolve().parents[1]
LEDGER = 'docs/audits/source-review-addendum-2026-11-02.json'
# The November 5 review moved the live pins; this checkpoint keeps the addendum's result.
CLOSEOUT_REVISION = 'f64991a9d6668f1a0b02de5e8e5666d90ce0e8e0'


class SourceReviewAddendumTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ledger = json.loads((ROOT / LEDGER).read_text())
        revision = self.ledger['reviewed_revision']
        subprocess.check_call(['git', 'merge-base', '--is-ancestor', revision, 'HEAD'], cwd=ROOT)
        raw = subprocess.check_output(['git', 'show', revision + ':catalog/upstream-pins.json'], cwd=ROOT)
        self.assertEqual(hashlib.sha256(raw).hexdigest(), self.ledger['pins_before_sha256'])
        self.before = json.loads(raw)
        self.closeout_bytes = subprocess.check_output(['git', 'show', CLOSEOUT_REVISION + ':catalog/upstream-pins.json'], cwd=ROOT)
        self.current = json.loads(self.closeout_bytes)

    def assert_transition(self, ledger: dict[str, Any], current: dict[str, Any]) -> None:
        expected = {r['source_url']: r for r in self.before['sources']}
        initial_bytes = (ROOT / ledger['initial_report']).read_bytes()
        self.assertEqual(ledger['initial_report_sha256'], hashlib.sha256(initial_bytes).hexdigest())
        changed = {r['source_url'] for r in json.loads(initial_bytes)['records'] if r['result'] == 'changed'}
        self.assertEqual(2, len(ledger['records']))
        self.assertEqual(2, len({r['source_url'] for r in ledger['records']}))
        self.assertEqual(changed, {r['source_url'] for r in ledger['records']})
        for record in ledger['records']:
            url = record['source_url']
            before, after = record['before_pin'], record['after_pin']
            self.assertEqual(expected[url], before)
            self.assertEqual(url, after['source_url'])
            self.assertEqual(before['marker_kind'], after['marker_kind'])
            self.assertEqual(2, len(record['observations']))
            for observation in record['observations']:
                self.assertEqual(url, observation['final_url'])
                self.assertEqual(after['marker_kind'], observation['marker_kind'])
                self.assertEqual(after['marker_value'], observation['marker_value'])
            expected[url] = after
        self.assertEqual({k: v for k, v in self.before.items() if k != 'sources'},
                         {k: v for k, v in current.items() if k != 'sources'})
        self.assertEqual(len(expected), len(current['sources']))
        self.assertEqual(expected, {r['source_url']: r for r in current['sources']})
        final_bytes = (ROOT / ledger['final_report']).read_bytes()
        self.assertEqual(ledger['final_report_sha256'], hashlib.sha256(final_bytes).hexdigest())
        final = json.loads(final_bytes)
        self.assertEqual('pass', final['result'])
        self.assertEqual(set(expected), {r['source_url'] for r in final['records']})
        for result in final['records']:
            pin = expected[result['source_url']]
            marker = pin['marker_kind'] + ':' + pin['marker_value']
            self.assertEqual((marker, marker, 'pass'),
                             (result['expected_marker'], result['observed_marker'], result['result']))

    def test_reviewed_addendum_binds_closeout_pins_and_preserves_checker(self) -> None:
        self.assert_transition(self.ledger, self.current)
        self.assertEqual(self.ledger['pins_after_sha256'], hashlib.sha256(self.closeout_bytes).hexdigest())
        old = subprocess.check_output(['git', 'show', self.ledger['reviewed_revision'] +
                                       ':scripts/check_upstream_freshness.py'], cwd=ROOT)
        self.assertEqual(old, (ROOT / 'scripts/check_upstream_freshness.py').read_bytes())

    def test_unreviewed_or_weakened_addendum_is_rejected(self) -> None:
        for mutation in ('extra_pin', 'age', 'date', 'url', 'method', 'missing', 'duplicate', 'observation'):
            with self.subTest(mutation=mutation):
                ledger, current = deepcopy(self.ledger), deepcopy(self.current)
                if mutation == 'extra_pin':
                    urls = {r['source_url'] for r in ledger['records']}
                    next(r for r in current['sources'] if r['source_url'] not in urls)['marker_value'] = 'tampered'
                elif mutation == 'age':
                    current['max_review_age_days'] += 1
                elif mutation == 'date':
                    current['reviewed_on'] = '2099-01-01'
                elif mutation == 'url':
                    ledger['records'][0]['after_pin']['source_url'] += '.md'
                elif mutation == 'method':
                    ledger['records'][0]['after_pin']['marker_kind'] = 'etag'
                elif mutation == 'missing':
                    ledger['records'].pop()
                elif mutation == 'duplicate':
                    ledger['records'][1] = deepcopy(ledger['records'][0])
                else:
                    ledger['records'][0]['observations'][1]['marker_value'] = 'disagreement'
                with self.assertRaises(AssertionError):
                    self.assert_transition(ledger, current)


if __name__ == '__main__':
    unittest.main()
