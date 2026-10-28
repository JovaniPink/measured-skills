"""Bindings and limits of the proposed full canonical expression review."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import unittest
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACKET = 'docs/audits/catalog-expression-disposition-2026-10-20.json'


def git(*arguments: str) -> bytes:
    return subprocess.check_output(['git', *arguments], cwd=ROOT)


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def accepted_payload(path: str) -> bytes:
    """Keep the frozen review bound to the payload the maintainer accepted."""
    record = json.loads((ROOT / 'docs/audits/originality-acceptance-0.18.0.json').read_text())
    return git('show', record['accepted_revision'] + ':' + path)


class ExpressionDispositionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.audit: dict[str, Any] = json.loads((ROOT / PACKET).read_text())

    def test_full_inventory_and_correction_bytes_match(self) -> None:
        audit = self.audit
        source = audit['reviewed_source']
        git('merge-base', '--is-ancestor', source, 'HEAD')
        canonical = set(git('ls-tree', '-r', '--name-only', source, '--', 'skills').decode().splitlines())
        expected = canonical | {'LICENSE', 'provenance/catalog.json'}
        self.assertEqual(expected, set(audit['inventory']))
        self.assertEqual(expected, set(audit['result_inventory']))
        for path in sorted(expected):
            with self.subTest(path=path):
                self.assertEqual(digest(git('show', source + ':' + path)), audit['inventory'][path])
                self.assertEqual(digest(accepted_payload(path)), audit['result_inventory'][path])
        for key in ('inventory', 'result_inventory'):
            encoded = (json.dumps(audit[key], sort_keys=True, separators=(',', ':')) + '\n').encode()
            self.assertEqual(digest(encoded), audit[key + '_sha256'])
        modified = {p for p in expected if audit['inventory'][p] != audit['result_inventory'][p]}
        repairs = audit['canonical_text_corrections']
        self.assertEqual({'provenance/catalog.json'} | {r['path'] for r in repairs}, modified)
        for repair in repairs:
            before = git('show', source + ':' + repair['path'])
            after = accepted_payload(repair['path'])
            self.assertEqual(digest(before), repair['previous_sha256'])
            self.assertEqual(digest(after), repair['corrected_sha256'])
            self.assertEqual(before.decode().replace(repair['previous_text'], repair['corrected_text']), after.decode())

    def test_all_skills_have_owned_history_and_explicit_review_limits(self) -> None:
        audit = self.audit
        entries = {r['skill']: r for r in json.loads(accepted_payload('provenance/catalog.json'))['entries']}
        records = audit['skills']
        self.assertEqual(len(entries), len(records))
        self.assertEqual(set(entries), {r['skill'] for r in records})
        self.assertEqual([], audit['outside_scope'])
        self.assertEqual(73, sum(r['review_kind'] == 'additional_73' for r in records))
        self.assertEqual(14, sum(r['review_kind'] == 'prior_14_revalidated' for r in records))
        self.assertTrue(audit['excluded_assets'])
        prior = audit['prior_packet']
        self.assertEqual(digest((ROOT / prior['path']).read_bytes()), prior['sha256'])
        old = {r['skill']: r for r in json.loads((ROOT / prior['path']).read_text())['skills']}
        for record in records:
            with self.subTest(skill=record['skill']):
                name = record['skill']
                creation = record['creation_revision']
                git('merge-base', '--is-ancestor', creation, audit['reviewed_source'])
                notice = git('show', creation + ':LICENSE')
                self.assertEqual(digest(notice), record['creation_license_sha256'])
                self.assertIn(b'Copyright (c) 2026 Jovani Pink', notice)
                paths = git('ls-tree', '-r', '--name-only', creation, '--', 'skills/' + name).decode().splitlines()
                self.assertEqual(set(paths), set(record['creation_files']))
                for path in paths:
                    self.assertEqual(digest(git('show', creation + ':' + path)), record['creation_files'][path])
                self.assertEqual(entries[name]['implementation_method'], record['declared_method'])
                self.assertTrue(record['expression_finding'])
                self.assertTrue(record['license_limit'])
                self.assertEqual('technical_review_complete_maintainer_decision_pending', record['qualification'])
                for key in ('reviewed_files', 'result_files'):
                    selected = {p: h for p, h in audit['inventory' if key == 'reviewed_files' else 'result_inventory'].items() if p.startswith('skills/' + name + '/')}
                    self.assertEqual(selected, record[key])
                if name in old:
                    self.assertTrue(record['prior_canonical_bytes_unchanged'])
                    self.assertEqual(old[name]['reviewed_files'], record['reviewed_files'])
                    self.assertEqual(record['reviewed_files'], record['result_files'])
        self.assertEqual('proposed', audit['status'])
        decision = audit['maintainer_decision']
        self.assertEqual('pending', decision['status'])
        for field in ('accepted_by', 'accepted_on', 'accepted_revision', 'accepted_inventory_sha256'):
            self.assertIsNone(decision[field])
        controls = {r['id']: r for r in audit['controls']}
        self.assertEqual('not_established', controls['human-contribution']['status'])
        self.assertEqual('not_accepted', controls['historical-corpus-gate']['status'])

    def test_note_corrections_preserve_methods_pins_and_historical_receipts(self) -> None:
        audit = self.audit
        before = {r['skill']: r for r in json.loads(git('show', audit['reviewed_source'] + ':provenance/catalog.json'))['entries']}
        after = {r['skill']: r for r in json.loads(accepted_payload('provenance/catalog.json'))['entries']}
        corrections = audit['provenance_note_corrections']
        self.assertEqual(38, len(corrections))
        self.assertEqual(9, sum('wholly jovani-authored' in r['previous_local_changes'].lower() for r in corrections))
        self.assertEqual(6, len(audit['canonical_text_corrections']))
        self.assertEqual({n for n in before if before[n] != after[n]}, {r['skill'] for r in corrections})
        for record in corrections:
            name = record['skill']
            for field in ('upstream_license', 'local_changes'):
                self.assertEqual(before[name][field], record['previous_' + field])
                self.assertEqual(after[name][field], record['corrected_' + field])
            for field in set(before[name]) - {'upstream_license', 'local_changes'}:
                self.assertEqual(before[name][field], after[name][field])
        self.assertFalse(any('wholly Jovani-authored' in r['local_changes'] or 'Wholly Jovani-authored' in r['local_changes'] for r in after.values()))
        for path in (
            'docs/audits/originality-history-review-2026-10-20.json',
            'docs/audits/owned-origin-corrections-2026-10-20.json',
            'docs/audits/clean-room-declaration-review-2026-10-20.json',
            'docs/audits/scoped-expression-disposition-2026-10-20.json',
            'catalog/upstream-pins.json',
        ):
            accepted = json.loads((ROOT / 'docs/audits/originality-acceptance-0.18.0.json').read_text())
            historical = git('show', accepted['accepted_revision'] + ':' + path)
            self.assertEqual(git('show', audit['reviewed_source'] + ':' + path), historical)
            if path != 'catalog/upstream-pins.json':
                self.assertEqual(historical, (ROOT / path).read_bytes())

    def test_new_skills_are_separate_from_accepted_history(self) -> None:
        historical = {r['skill'] for r in self.audit['skills']}
        current = {r['skill']: r for r in json.loads((ROOT / 'provenance/catalog.json').read_text())['entries']}
        mapping = {r['old_id']: r['new_id'] for r in json.loads((ROOT / 'catalog/migrations/0.18-to-0.19.json').read_text())['entries']}
        additions = set(current) - {mapping[n] for n in historical}
        self.assertEqual({'review-engineering-prompt', 'choose-workflow', 'design-web-motion'}, additions)
        delta = json.loads((ROOT / 'docs/audits/post-acceptance-delta-2026-10-20.json').read_text())
        self.assertFalse(delta['new_maintainer_acceptance'])
        for name in additions:
            self.assertEqual('original', current[name]['implementation_method'])
            for path in (ROOT / 'skills' / name).rglob('*'):
                if path.is_file():
                    record = delta['changes'][path.relative_to(ROOT).as_posix()]
                    self.assertIsNone(record['before_sha256'])
                    self.assertEqual(digest(path.read_bytes()), record['after_sha256'])
                    self.assertTrue(record['expression_and_license_review'])

    def test_historical_inventory_tampering_still_fails(self) -> None:
        self.audit['skills'].pop()
        with self.assertRaises(AssertionError):
            self.test_all_skills_have_owned_history_and_explicit_review_limits()
