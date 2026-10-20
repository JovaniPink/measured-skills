"""Scope and evidence bindings for the proposed originality decision."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import unittest
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACKET = 'docs/audits/originality-approval-2026-10-20.json'


def git(*args: str) -> bytes:
    return subprocess.check_output(['git', *args], cwd=ROOT)


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def inventory_digest(value: object) -> str:
    return digest((json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode())


class NoncanonicalDispositionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.audit: dict[str, Any] = json.loads((ROOT / PACKET).read_text())

    def test_full_input_and_corrected_payload_are_accounted_for(self) -> None:
        audit = self.audit
        source = audit['reviewed_source']
        git('merge-base', '--is-ancestor', source, 'HEAD')
        paths = git('ls-tree', '-r', '--name-only', source).decode().splitlines()
        self.assertEqual(set(paths), set(audit['inventory']))
        for path in paths:
            self.assertEqual(digest(git('show', source + ':' + path)), audit['inventory'][path], path)
        self.assertEqual(inventory_digest(audit['inventory']), audit['inventory_sha256'])
        result = dict(audit['inventory'])
        for path in audit['payload_exclusions']:
            result.pop(path, None)
        result.update(audit['corrections'])
        result.update(audit['new_payload_files'])
        self.assertEqual(inventory_digest(result), audit['result_inventory_sha256'])
        for path, expected in result.items():
            self.assertEqual(digest((ROOT / path).read_bytes()), expected, path)
        self.assertEqual(set(paths) - {p for p in paths if p.startswith('skills/')}, set(audit['noncanonical_classes']))
        known = set(result) | set(audit['payload_exclusions'])
        # Accepted decisions are separate envelopes, never retroactive edits to this proposal.
        current = set(git('ls-files').decode().splitlines())
        self.assertFalse(current - known, sorted(current - known))
        for record in audit['source_families']:
            git('merge-base', '--is-ancestor', record['creation_revision'], source)
            license_bytes = git('show', record['creation_revision'] + ':LICENSE')
            self.assertEqual(digest(license_bytes), record['license_sha256'])

    def test_icon_dependency_and_preserved_record_evidence_is_bound(self) -> None:
        audit = self.audit
        icon = audit['artwork']
        payload = (ROOT / icon['path']).read_bytes()
        self.assertEqual(digest(payload), icon['sha256'])
        self.assertEqual(payload, git('show', icon['creation_revision'] + ':' + icon['path']))
        self.assertEqual(11, len(icon['generated_copies']))
        for path in icon['generated_copies']:
            self.assertEqual(payload, (ROOT / path).read_bytes())
        self.assertEqual('not_executed_infrastructure_approval_failure', icon['retained_events'][0]['result'])
        self.assertTrue(any(r['result'] == 'retained_tool_reports_completion' for r in icon['retained_events']))
        for source, record in audit['preserved_packets'].items():
            self.assertEqual(digest((ROOT / source).read_bytes()), record)
        tools = json.loads((ROOT / 'provenance/ci-tools.json').read_text())['tools']
        receipts = {r['name']: r for r in audit['ci_dependencies']}
        self.assertEqual({r['name'] for r in tools}, set(receipts))
        for tool in tools:
            receipt = receipts[tool['name']]
            self.assertEqual(tool['version'], receipt['version'])
            self.assertEqual([tool['artifact_sha256']], [r['sha256'] for r in receipt['matched_artifacts']])
            self.assertFalse(receipt['bundled'])
        actions = json.loads((ROOT / 'provenance/ci-actions.json').read_text())['actions']
        action_receipts = {r['name']: r for r in audit['license_file_receipts']}
        for action in actions:
            self.assertEqual(action['pinned_revision'], action_receipts[action['name']]['pinned_revision'])
            self.assertEqual('MIT', action_receipts[action['name']]['license'])
        self.assertEqual('bounded_technical_review', audit['review_depth']['claim'])
        self.assertFalse(audit['review_depth']['every_line_independently_compared'])

    def test_proposed_policy_decision_is_explicit_and_unaccepted(self) -> None:
        audit = self.audit
        self.assertEqual('proposed', audit['status'])
        self.assertEqual('pending', audit['maintainer_decision']['status'])
        self.assertIsNone(audit['maintainer_decision']['accepted_by'])
        self.assertIsNone(audit['maintainer_decision']['accepted_revision'])
        self.assertEqual('requires_explicit_maintainer_approval', audit['policy_replacement']['status'])
        self.assertEqual('retain_until_accepted', audit['originality_hold'])
        self.assertTrue(audit['decision_text'])
        gaps = {r['id']: r for r in audit['remaining_gaps']}
        self.assertEqual('not_established', gaps['exclusive-human-contribution']['status'])
        self.assertEqual('not_performed', gaps['outside-corpus-comparison']['status'])
        self.assertEqual('not_observed', gaps['independent-human-review']['status'])
        self.assertTrue(all(r['proposed_disposition'] for r in gaps.values()))
        self.assertIn('release', audit['excluded_authorizations'])
        self.assertIn('paid evaluations', audit['excluded_authorizations'])
        self.assertNotIn('acceptance', audit['implementation_actions'])
