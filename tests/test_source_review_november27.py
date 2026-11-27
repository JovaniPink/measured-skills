"""Bind the live pins to the individual November 27 reviews and their receipts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class NovemberSourceCloseoutTests(unittest.TestCase):
    def test_each_changed_pin_has_a_review_and_repeated_capture(self) -> None:
        ledger = json.loads((ROOT / 'docs/audits/source-review-2026-11-27.json').read_text())
        baseline = subprocess.check_output(
            ['git', 'show', ledger['reviewed_revision'] + ':catalog/upstream-pins.json'], cwd=ROOT)
        self.assertEqual(hashlib.sha256(baseline).hexdigest(), ledger['pins_before_sha256'])
        original = json.loads(baseline)
        expected = {r['source_url']: r for r in original['sources']}
        reports = {}
        for name in ('initial_report', 'intermediate_report', 'final_report'):
            raw = (ROOT / ledger[name]).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), ledger[name + '_sha256'])
            reports[name] = json.loads(raw)
        initial = reports['initial_report']['records']
        changed = {r['source_url'] for r in initial if r['result'] == 'changed'}
        self.assertEqual(47, len(changed))
        self.assertEqual(47, len(ledger['records']))
        self.assertEqual(changed, {r['source_url'] for r in ledger['records']})
        late = [r for r in reports['intermediate_report']['records'] if r['result'] != 'pass']
        self.assertEqual(['https://genai.owasp.org/wp-json/wp/v2/pages/50812'], [r['source_url'] for r in late])
        reviews = json.loads((ROOT / 'catalog/upstream-reviews.json').read_text())['reviews']
        affected = {r['url']: r['affected_skills'] for r in reviews}
        for record in ledger['records']:
            old, new = record['before_pin'], record['after_pin']
            self.assertEqual(expected.pop(record['source_url']), old)
            self.assertEqual(record['affected_skills'], affected[new['source_url']])
            self.assertTrue(record['finding'])
            self.assertGreaterEqual(len(record['observations']), 2)
            for obs in record['observations']:
                self.assertEqual((new['marker_kind'], new['marker_value']), (obs['marker_kind'], obs['marker_value']))
            expected[new['source_url']] = new
        current_bytes = (ROOT / 'catalog/upstream-pins.json').read_bytes()
        self.assertEqual(hashlib.sha256(current_bytes).hexdigest(), ledger['pins_after_sha256'])
        current = json.loads(current_bytes)
        self.assertEqual(original['reviewed_on'], current['reviewed_on'])
        self.assertEqual(original['max_review_age_days'], current['max_review_age_days'])
        self.assertEqual(expected, {r['source_url']: r for r in current['sources']})
        final = reports['final_report']
        self.assertEqual('pass', final['result'])
        self.assertEqual(69, len(final['records']))
        self.assertEqual(set(expected), {r['source_url'] for r in final['records']})
        for observation in final['records']:
            pin = expected[observation['source_url']]
            marker = pin['marker_kind'] + ':' + pin['marker_value']
            self.assertEqual((marker, marker, 'pass'),
                             (observation['expected_marker'], observation['observed_marker'], observation['result']))
