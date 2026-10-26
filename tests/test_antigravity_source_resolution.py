"""Bind each official representation replacement to its retained source hold."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = '13c3e4e36c82782c17b197fdeb1159b3d388d6d0'
REPLACEMENTS = {
    'https://antigravity.google/docs/cli/headless/': 'https://antigravity.google/docs/cli/headless.md',
    'https://antigravity.google/docs/skills/': 'https://antigravity.google/docs/skills.md',
    'https://www.antigravity.google/docs/plugins?tab=cli': 'https://antigravity.google/docs/plugins.md',
    'https://www.antigravity.google/docs/sdk/overview': 'https://antigravity.google/docs/sdk/overview.md',
}


class AntigravitySourceResolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ledger = json.loads((ROOT / 'docs/audits/antigravity-source-resolution-2026-10-26.json').read_text())
        self.pins = json.loads((ROOT / 'catalog/upstream-pins.json').read_text())
        self.before = json.loads(subprocess.check_output(
            ['git', 'show', BASE + ':catalog/upstream-pins.json'], cwd=ROOT))

    def assert_transition(self, ledger: dict[str, Any], pins: dict[str, Any]) -> None:
        self.assertEqual(BASE, ledger['reviewed_revision'])
        path = ledger['prior_hold_receipt']
        receipt = (ROOT / path).read_bytes()
        self.assertEqual(subprocess.check_output(['git', 'show', BASE + ':' + path], cwd=ROOT), receipt)
        self.assertEqual(hashlib.sha256(receipt).hexdigest(), ledger['prior_hold_receipt_sha256'])
        held = {r['source_url'] for r in json.loads(receipt)['records'] if r['result'] == 'changed'}
        self.assertEqual(set(REPLACEMENTS), held)
        records = ledger['records']
        self.assertEqual(4, len(records))
        self.assertEqual(REPLACEMENTS, {r['old_source_url']: r['source_url'] for r in records})
        expected = {r['source_url']: deepcopy(r) for r in self.before['sources']}
        for record in records:
            old, new = record['old_source_url'], record['source_url']
            self.assertEqual(expected.pop(old), record['before'])
            self.assertEqual('replace_html_with_official_markdown', record['decision'])
            after = record['after']
            self.assertEqual(new, after['source_url'])
            self.assertEqual('content-sha256', after['marker_kind'])
            observations = record['observations']
            self.assertEqual(3, len(observations))
            self.assertEqual({after['marker_value']}, {o['decoded_sha256'] for o in observations})
            for observation in observations:
                self.assertEqual(new, observation['requested_url'])
                self.assertEqual(new, observation['final_url'])
                self.assertEqual(200, observation['status'])
                self.assertEqual('text/markdown', observation['content_type'])
                self.assertIn(observation['content_encoding'], ('identity', 'gzip'))
                self.assertGreater(observation['decoded_bytes'], 1000)
                self.assertRegex(observation['raw_sha256'], r'^[a-f0-9]{64}$')
                if observation['content_encoding'] == 'identity':
                    self.assertEqual(observation['raw_sha256'], observation['decoded_sha256'])
            self.assertTrue(record['affected_skills'])
            self.assertTrue(record['finding'])
            self.assertTrue(record['instruction_consequence'])
            coverage = record['representation_review']
            self.assertEqual(coverage['html_document_headings'], coverage['markdown_document_headings'])
            self.assertEqual(coverage['document_heading_count'], len(coverage['markdown_document_headings']))
            expected[new] = after
        self.assertEqual(64, len(pins['sources']))
        self.assertEqual(expected, {r['source_url']: r for r in pins['sources']})
        self.assertEqual({k: v for k, v in self.before.items() if k != 'sources'},
                         {k: v for k, v in pins.items() if k != 'sources'})

    def test_only_four_reviewed_representations_replace_the_retained_holds(self) -> None:
        self.assert_transition(self.ledger, self.pins)
        reviews = json.loads((ROOT / 'catalog/upstream-reviews.json').read_text())['reviews']
        urls = {r['url'] for r in reviews}
        self.assertFalse(set(REPLACEMENTS) & urls)
        self.assertTrue(set(REPLACEMENTS.values()) <= urls)

    def test_unreviewed_change_missing_decision_and_divergent_bytes_are_rejected(self) -> None:
        for mutation in ('unrelated', 'missing', 'divergent', 'clock'):
            with self.subTest(mutation=mutation):
                ledger, pins = deepcopy(self.ledger), deepcopy(self.pins)
                if mutation == 'unrelated':
                    pins['sources'][0]['marker_value'] = 'unreviewed'
                elif mutation == 'missing':
                    ledger['records'].pop()
                elif mutation == 'divergent':
                    ledger['records'][0]['observations'][0]['decoded_sha256'] = '0' * 64
                else:
                    pins['reviewed_on'] = '2026-10-26'
                with self.assertRaises(AssertionError):
                    self.assert_transition(ledger, pins)

    def test_transport_evidence_retains_both_wire_forms_and_one_document(self) -> None:
        observations = self.ledger['transport_review']['observations']
        self.assertEqual(6, len(observations))
        self.assertEqual({'identity', 'gzip'}, {o['content_encoding'] for o in observations})
        self.assertEqual(2, len({o['raw_sha256'] for o in observations}))
        self.assertEqual(1, len({o['decoded_sha256'] for o in observations}))
        sdk = next(r for r in self.ledger['records'] if r['source_url'].endswith('/sdk/overview.md'))
        self.assertEqual({sdk['after']['marker_value']}, {o['decoded_sha256'] for o in observations})

    def test_closeout_binds_all_current_pins_and_preserves_remaining_holds(self) -> None:
        closeout = self.ledger['closeout']
        payload = (ROOT / closeout['path']).read_bytes()
        self.assertEqual(closeout['sha256'], hashlib.sha256(payload).hexdigest())
        self.assertEqual(closeout['pins_sha256'],
                         hashlib.sha256((ROOT / 'catalog/upstream-pins.json').read_bytes()).hexdigest())
        report = json.loads(payload)
        self.assertTrue(report['online'])
        self.assertEqual('fail', report['result'])
        records = {r['source_url']: r for r in report['records']}
        self.assertEqual(64, len(report['records']))
        self.assertEqual({r['source_url'] for r in self.pins['sources']}, set(records))
        for pin in self.pins['sources']:
            self.assertEqual(pin['marker_kind'] + ':' + pin['marker_value'],
                             records[pin['source_url']]['expected_marker'])
        for url in REPLACEMENTS.values():
            self.assertEqual('pass', records[url]['result'])
            self.assertEqual(records[url]['expected_marker'], records[url]['observed_marker'])
        held = [r for r in report['records'] if r['result'] != 'pass']
        self.assertEqual(closeout['remaining_holds'], held)
        self.assertEqual({'https://developers.openai.com/api/docs/guides/prompt-engineering',
                          'https://www.swift.org/swift-evolution/'}, {r['source_url'] for r in held})
        self.assertTrue(all(r['result'] == 'changed' for r in held))
        self.assertEqual({'pass': 62, 'changed': 2}, closeout['counts'])
