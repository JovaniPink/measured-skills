"""Bind the November 2 source decisions without weakening freshness policy or ancestry."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any
import unittest

ROOT = Path(__file__).resolve().parents[1]
LEDGER = 'docs/audits/source-review-2026-11-02.json'
OCTOBER29_AFTER_PINS = '4687ea079c759618c452a5e871c698a2ba29fb21d440d1fa087fcb354d78f709'


def git(*args: str) -> bytes:
    return subprocess.check_output(['git', *args], cwd=ROOT)


class SourceReviewNovemberTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ledger = json.loads((ROOT / LEDGER).read_text())
        raw = git('show', self.ledger['reviewed_revision'] + ':catalog/upstream-pins.json')
        self.assertEqual(hashlib.sha256(raw).hexdigest(), self.ledger['pins_before_sha256'])
        self.before = json.loads(raw)
        self.current = json.loads((ROOT / 'catalog/upstream-pins.json').read_text())

    def assert_transition(self, ledger: dict[str, Any], current: dict[str, Any]) -> None:
        expected = {r['source_url']: r for r in self.before['sources']}
        records = ledger['records']
        self.assertEqual(27, len(records))
        self.assertEqual(27, len({r['source_url'] for r in records}))
        initial = json.loads((ROOT / ledger['initial_report']).read_text())['records']
        self.assertEqual({r['source_url'] for r in initial if r['result'] == 'changed'},
                         {r['source_url'] for r in records})
        changes = {c['from']: c for c in ledger['source_url_changes']}
        moved = set()
        for record in records:
            url = record['source_url']
            after = record['after_pin']
            self.assertEqual(expected[url], record['before_pin'])
            self.assertEqual(2, len(record['observations']))
            for observation in record['observations']:
                self.assertEqual(after['marker_kind'], observation['marker_kind'])
                self.assertEqual(after['marker_value'], observation['marker_value'])
                self.assertEqual(after['source_url'], observation['final_url'])
                self.assertRegex(observation['raw_sha256'], r'^[0-9a-f]{64}$')
            if after['source_url'] == url:
                self.assertEqual(record['before_pin']['marker_kind'], after['marker_kind'])
                self.assertEqual('repin-after-review', record['decision'])
            else:
                self.assertIn(url, changes)
                change = changes[url]
                moved.add(url)
                self.assertEqual('rebind-official-markdown', record['decision'])
                self.assertEqual(change['to'], after['source_url'])
                self.assertEqual(url + '.md.txt', after['source_url'])
                self.assertEqual('content-sha256', after['marker_kind'])
                self.assertEqual(record['before_pin']['marker_kind'], change['marker_kind_from'])
                self.assertEqual(after['marker_kind'], change['marker_kind_to'])
                del expected[url]
            expected[after['source_url']] = after
        self.assertEqual(set(changes), moved)
        self.assertEqual(2, len(moved))
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

    def test_ancestry_and_freshness_checker_are_preserved(self) -> None:
        self.assertEqual(OCTOBER29_AFTER_PINS, self.ledger['pins_before_sha256'])
        git('merge-base', '--is-ancestor', self.ledger['reviewed_revision'], 'HEAD')
        old = git('show', self.ledger['reviewed_revision'] + ':scripts/check_upstream_freshness.py')
        self.assertEqual(old, (ROOT / 'scripts/check_upstream_freshness.py').read_bytes())
        for name in ('reviewed_on', 'max_review_age_days'):
            self.assertEqual(self.before[name], self.current[name])

    def test_google_representation_changes_reach_the_review_catalog(self) -> None:
        reviews = json.loads((ROOT / 'catalog/upstream-reviews.json').read_text())['reviews']
        urls = {r['url'] for r in reviews}
        for change in self.ledger['source_url_changes']:
            self.assertIn(change['to'], urls)
            self.assertNotIn(change['from'], urls)
            self.assertIn('Re-reviewed 2026-11-02', next(r for r in reviews if r['url'] == change['to'])['finding'])

    def test_unreviewed_changes_and_weakened_bindings_fail(self) -> None:
        for mutation in ('unreviewed', 'review_age', 'method', 'url', 'missing', 'disagreement', 'extra_move'):
            with self.subTest(mutation=mutation):
                ledger, current = deepcopy(self.ledger), deepcopy(self.current)
                if mutation == 'unreviewed':
                    reviewed = {r['source_url'] for r in ledger['records']}
                    moved = {r['after_pin']['source_url'] for r in ledger['records']}
                    next(r for r in current['sources']
                         if r['source_url'] not in reviewed | moved)['marker_value'] = 'tampered'
                elif mutation == 'review_age':
                    current['max_review_age_days'] += 1
                elif mutation == 'method':
                    ledger['records'][0]['after_pin']['marker_kind'] = 'last-modified'
                elif mutation == 'url':
                    ledger['records'][0]['after_pin']['source_url'] = 'https://example.invalid/'
                elif mutation == 'missing':
                    ledger['records'].pop()
                elif mutation == 'extra_move':
                    ledger['source_url_changes'].pop()
                else:
                    ledger['records'][0]['observations'][1]['marker_value'] = 'different'
                with self.assertRaises(AssertionError):
                    self.assert_transition(ledger, current)


if __name__ == '__main__':
    unittest.main()
