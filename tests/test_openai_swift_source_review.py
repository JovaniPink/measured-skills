"""Keep individual source decisions complete without rewriting prior evidence."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = '115b65085efa472584e9ae1be23b0f2737e68c9c'
REVIEWED_SOURCE = 'd67fcb70f64ebc36618ba27e080e02ec4845aaf1'
OPENAI = 'https://developers.openai.com/api/docs/guides/prompt-engineering'
SWIFT = 'https://www.swift.org/swift-evolution/'


class OpenAISwiftSourceReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ledger = json.loads((ROOT / 'docs/audits/openai-swift-source-review-2026-10-26.json').read_text())
        self.pins = json.loads((ROOT / 'catalog/upstream-pins.json').read_text())
        self.before = json.loads(subprocess.check_output(
            ['git', 'show', BASE + ':catalog/upstream-pins.json'], cwd=ROOT))

    def assert_transition(self, ledger: dict[str, Any], pins: dict[str, Any]) -> None:
        self.assertEqual(BASE, ledger['reviewed_revision'])
        path = ledger['prior_hold_receipt']
        payload = (ROOT / path).read_bytes()
        self.assertEqual(subprocess.check_output(['git', 'show', BASE + ':' + path], cwd=ROOT), payload)
        self.assertEqual(ledger['prior_hold_receipt_sha256'], hashlib.sha256(payload).hexdigest())
        held = {r['source_url'] for r in json.loads(payload)['records'] if r['result'] == 'changed'}
        self.assertEqual({OPENAI, SWIFT}, held)
        records = ledger['records']
        self.assertEqual(2, len(records))
        self.assertEqual({OPENAI: OPENAI + '.md', SWIFT: SWIFT},
                         {r['old_source_url']: r['source_url'] for r in records})
        expected = {r['source_url']: deepcopy(r) for r in self.before['sources']}
        for record in records:
            self.assertEqual(expected.pop(record['old_source_url']), record['before'])
            after = record['after']
            self.assertEqual(record['source_url'], after['source_url'])
            self.assertEqual('content-sha256', after['marker_kind'])
            self.assertEqual(3, len(record['observations']))
            for observation in record['observations']:
                self.assertEqual(record['source_url'], observation['requested_url'])
                self.assertEqual(record['source_url'], observation['final_url'])
                self.assertEqual(200, observation['status'])
                self.assertEqual(after['marker_value'], observation['decoded_sha256'])
            self.assertTrue(record['finding'])
            self.assertTrue(record['instruction_consequence'])
            self.assertTrue(record['affected_skills'])
            expected[record['source_url']] = after
        self.assertEqual(64, len(pins['sources']))
        self.assertEqual(expected, {r['source_url']: r for r in pins['sources']})
        self.assertEqual({k: v for k, v in self.before.items() if k != 'sources'},
                         {k: v for k, v in pins.items() if k != 'sources'})

    def test_exact_transition_and_authority_coverage(self) -> None:
        self.assert_transition(self.ledger, self.pins)
        before = json.loads(subprocess.check_output(['git', 'show', BASE + ':provenance/catalog.json'], cwd=ROOT))
        # This assertion concerns the source-review transition, not later authoring.
        # Current provenance bytes are bound by the post-acceptance delta tests.
        subprocess.run(['git', 'merge-base', '--is-ancestor', REVIEWED_SOURCE, 'HEAD'], cwd=ROOT, check=True)
        current = json.loads(subprocess.check_output(
            ['git', 'show', REVIEWED_SOURCE + ':provenance/catalog.json'], cwd=ROOT))
        for old, new in zip(before['entries'], current['entries'], strict=True):
            if old['skill'] == 'engineering-prompt-review':
                self.assertEqual(OPENAI, old['source_url'])
                self.assertEqual(OPENAI + '.md', new['source_url'])
                expected = deepcopy(old)
                expected['source_url'] = new['source_url']
                expected['reviewed_material'] = new['reviewed_material']
                self.assertEqual(expected, new)
            else:
                self.assertEqual(old, new)
        prompt = next(r for r in self.ledger['records'] if r['old_source_url'] == OPENAI)
        coverage = prompt['comparison']['coverage']
        self.assertTrue(set(coverage['html_headings']) <= set(coverage['markdown_headings']))
        self.assertEqual(prompt['before']['marker_value'], prompt['comparison']['old_body_sha256'])
        swift = next(r for r in self.ledger['records'] if r['source_url'] == SWIFT)
        self.assertFalse(swift['comparison']['old_body_available'])

    def test_unreviewed_changes_and_rewritten_evidence_fail(self) -> None:
        for mutation in ('unrelated', 'missing', 'observation', 'clock', 'prior_hash'):
            with self.subTest(mutation=mutation):
                ledger, pins = deepcopy(self.ledger), deepcopy(self.pins)
                if mutation == 'unrelated':
                    pins['sources'][0]['marker_value'] = 'unreviewed'
                elif mutation == 'missing':
                    ledger['records'].pop()
                elif mutation == 'observation':
                    ledger['records'][0]['observations'][0]['decoded_sha256'] = '0' * 64
                elif mutation == 'clock':
                    pins['reviewed_on'] = '2026-10-26'
                else:
                    ledger['prior_hold_receipt_sha256'] = '0' * 64
                with self.assertRaises(AssertionError):
                    self.assert_transition(ledger, pins)

    def test_closeout_binds_every_pin_and_retains_all_results(self) -> None:
        closeout = self.ledger['closeout']
        payload = (ROOT / closeout['path']).read_bytes()
        self.assertEqual(closeout['sha256'], hashlib.sha256(payload).hexdigest())
        self.assertEqual(closeout['pins_sha256'],
                         hashlib.sha256((ROOT / 'catalog/upstream-pins.json').read_bytes()).hexdigest())
        report = json.loads(payload)
        self.assertTrue(report['online'])
        self.assertEqual(64, len(report['records']))
        records = {r['source_url']: r for r in report['records']}
        self.assertEqual({r['source_url'] for r in self.pins['sources']}, set(records))
        for pin in self.pins['sources']:
            self.assertEqual(pin['marker_kind'] + ':' + pin['marker_value'],
                             records[pin['source_url']]['expected_marker'])
        failures = [r for r in report['records'] if r['result'] != 'pass']
        self.assertEqual(closeout['remaining_holds'], failures)
        self.assertEqual('fail' if failures else 'pass', report['result'])
        for url in (OPENAI + '.md', SWIFT):
            self.assertEqual('pass', records[url]['result'])
            self.assertEqual(records[url]['expected_marker'], records[url]['observed_marker'])
