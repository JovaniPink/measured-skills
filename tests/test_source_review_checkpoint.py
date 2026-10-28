"""Require individually observed pin changes without weakening historical evidence."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = '56aa6a9fb8462875edd05984d162acc3fc140eee'
CHECKPOINT = '13c3e4e36c82782c17b197fdeb1159b3d388d6d0'
FULL_BODY_BINDINGS = {
    'https://git-scm.com/docs/git-worktree': 'last-modified',
    'https://adk-labs.github.io/adk-docs/': 'etag',
    'https://adk-labs.github.io/adk-docs/safety/': 'etag',
}


class SourceReviewCheckpointTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ledger = json.loads((ROOT / 'docs/audits/source-review-2026-10-26.json').read_text())
        # Later representation changes must not rewrite this retained four-hold checkpoint.
        self.current_bytes = subprocess.check_output(
            ['git', 'show', CHECKPOINT + ':catalog/upstream-pins.json'], cwd=ROOT)
        self.current = json.loads(self.current_bytes)
        self.before = json.loads(subprocess.check_output(
            ['git', 'show', BASE + ':catalog/upstream-pins.json'], cwd=ROOT))

    def assert_reviewed_transition(self, ledger: dict[str, Any], current: dict[str, Any]) -> None:
        self.assertEqual(BASE, ledger['reviewed_revision'])
        initial_bytes = (ROOT / ledger['initial_report']).read_bytes()
        self.assertEqual(ledger['initial_report_sha256'], hashlib.sha256(initial_bytes).hexdigest())
        initial = json.loads(initial_bytes)
        changed = {r['source_url']: r for r in initial['records'] if r['result'] == 'changed'}
        records = ledger['records']
        self.assertEqual(33, len(changed))
        self.assertEqual(len(changed), len(records))
        self.assertEqual(set(changed), {r['source_url'] for r in records})
        expected = {r['source_url']: deepcopy(r) for r in self.before['sources']}
        for record in records:
            url = record['source_url']
            prior = expected[url]
            self.assertEqual(prior['marker_kind'] + ':' + prior['marker_value'], record['expected_marker'])
            self.assertEqual(changed[url]['expected_marker'], record['expected_marker'])
            self.assertEqual(changed[url]['observed_marker'], record['observed_marker'])
            if url in FULL_BODY_BINDINGS:
                self.assertEqual(FULL_BODY_BINDINGS[url], prior['marker_kind'])
                self.assertEqual('content-sha256', record['marker_kind'])
                self.assertTrue(record['marker_change_reason'])
            else:
                self.assertEqual(prior['marker_kind'], record['marker_kind'])
            observations = record['observations']
            self.assertEqual(3, len(observations))
            self.assertEqual(1, len({o['preferred_marker'] for o in observations}))
            self.assertEqual(record['raw_body_variants'], len({o['raw_sha256'] for o in observations}))
            for observation in observations:
                self.assertEqual(url, observation['final_url'])
                self.assertRegex(observation['raw_sha256'], r'^[a-f0-9]{64}$')
                self.assertTrue(observation['observed_at'])
            self.assertTrue(record['affected_skills'])
            self.assertTrue(record['finding'])
            self.assertTrue(record['instruction_consequence'])
            if record['decision'] == 'hold_unstable_response':
                self.assertEqual(prior['marker_value'], record['marker_value'])
                self.assertTrue(record['closeout_finding'])
                self.assertGreater(len({o['preferred_marker'] for o in
                                        observations + record['closeout_observations']}), 1)
            else:
                self.assertEqual('repin_reviewed_current_content', record['decision'])
                final_observations = record.get('closeout_observations', observations)
                self.assertEqual(3, len(final_observations))
                if url in FULL_BODY_BINDINGS:
                    self.assertEqual({record['marker_value']},
                                     {o['raw_sha256'] for o in observations + final_observations})
                else:
                    self.assertEqual({record['marker_kind'] + ':' + record['marker_value']},
                                     {o['preferred_marker'] for o in final_observations})
                prior.update(marker_kind=record['marker_kind'], marker_value=record['marker_value'])
        self.assertEqual(29, sum(r['decision'] == 'repin_reviewed_current_content' for r in records))
        self.assertEqual(4, sum(r['decision'] == 'hold_unstable_response' for r in records))
        self.assertEqual(len(expected), len(current['sources']))
        self.assertEqual(expected, {r['source_url']: r for r in current['sources']})
        self.assertEqual({k: v for k, v in self.before.items() if k != 'sources'},
                         {k: v for k, v in current.items() if k != 'sources'})

    def test_exact_reviewed_transition(self) -> None:
        self.assert_reviewed_transition(self.ledger, self.current)

    def test_unrecorded_pin_change_is_rejected(self) -> None:
        changed = deepcopy(self.current)
        changed['sources'][0]['marker_value'] = 'unreviewed'
        with self.assertRaises(AssertionError):
            self.assert_reviewed_transition(self.ledger, changed)

    def test_missing_or_divergent_observation_is_rejected(self) -> None:
        for mutation in ('missing', 'divergent', 'historical'):
            with self.subTest(mutation=mutation):
                ledger = deepcopy(self.ledger)
                if mutation == 'missing':
                    ledger['records'].pop()
                elif mutation == 'divergent':
                    ledger['records'][0]['observations'][1]['preferred_marker'] = 'etag:unreviewed'
                else:
                    ledger['records'][0]['expected_marker'] = 'etag:rewritten-history'
                with self.assertRaises(AssertionError):
                    self.assert_reviewed_transition(ledger, self.current)

    def test_closeout_covers_exact_final_pins_and_retained_holds(self) -> None:
        ledger = self.ledger
        payload = (ROOT / ledger['closeout_report']).read_bytes()
        self.assertEqual(ledger['closeout_report_sha256'], hashlib.sha256(payload).hexdigest())
        self.assertEqual(ledger['closeout_pins_sha256'],
                         hashlib.sha256(self.current_bytes).hexdigest())
        report = json.loads(payload)
        self.assertTrue(report['online'])
        self.assertEqual('fail', report['result'])
        self.assertEqual(64, len(report['records']))
        pins = {r['source_url']: r['marker_kind'] + ':' + r['marker_value'] for r in self.current['sources']}
        self.assertEqual(pins, {r['source_url']: r['expected_marker'] for r in report['records']})
        held = {r['source_url'] for r in ledger['records'] if r['decision'] == 'hold_unstable_response'}
        self.assertEqual(held, {r['source_url'] for r in report['records'] if r['result'] == 'changed'})
        self.assertEqual({'pass': 60, 'changed': 4, 'blocked': 0}, ledger['closeout_counts'])
        for result, count in ledger['closeout_counts'].items():
            self.assertEqual(count, sum(r['result'] == result for r in report['records']))
