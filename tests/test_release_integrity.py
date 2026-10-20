"""Mutation-sensitive checks for current release inventory and archive content."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
import warnings
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import validate_catalog as validator  # noqa: E402
from cataloglib import VERSION  # noqa: E402


class ReleaseIntegrityTests(unittest.TestCase):
    def test_manifest_rejects_inventory_mutations(self) -> None:
        original = json.loads((ROOT / 'releases' / VERSION / 'manifest.json').read_text())
        for mutation in ('missing', 'extra', 'duplicate', 'kind', 'unsafe'):
            with self.subTest(mutation=mutation):
                document = copy.deepcopy(original)
                if mutation == 'missing':
                    document['artifacts'].pop()
                elif mutation == 'extra':
                    document['artifacts'].append({'kind': 'file', 'path': 'README.md', 'sha256': '0' * 64})
                elif mutation == 'duplicate':
                    document['artifacts'].append(document['artifacts'][0].copy())
                elif mutation == 'kind':
                    document['artifacts'][0]['kind'] = 'zip'
                else:
                    document['artifacts'][0]['path'] = '../outside'
                errors: list[str] = []
                with patch.object(validator, '_validate_json_schema', return_value=document):
                    validator.validate_release_manifest(errors)
                self.assertTrue(any('artifact inventory' in e for e in errors), errors)

    def test_rehashed_archive_rejects_content_mutations(self) -> None:
        skill = 'claim-verification'
        source = next((ROOT / 'plugins' / 'claude').glob('*/skills/' + skill))
        expected = {f'{skill}/{p.relative_to(source).as_posix()}': p.read_bytes()
                    for p in source.rglob('*') if p.is_file()}
        for mutation in ('valid', 'modified', 'missing', 'extra', 'duplicate', 'unsafe', 'executable', 'symlink'):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                shutil.copytree(ROOT / 'skills' / skill, root / 'skills' / skill)
                target = root / 'plugins' / 'claude' / source.parents[1].name / 'skills' / skill
                shutil.copytree(source, target)
                package_dir = root / 'dist' / 'claude-ai'
                package_dir.mkdir(parents=True)
                archive_path = package_dir / f'{skill}-{VERSION}.zip'
                members = list(expected.items())
                if mutation == 'modified':
                    members[0] = (members[0][0], b'not canonical\n')
                elif mutation == 'missing':
                    members.pop()
                elif mutation == 'extra':
                    members.append((f'{skill}/extra.md', b'extra\n'))
                elif mutation == 'duplicate':
                    members.append(members[0])
                elif mutation == 'unsafe':
                    members.append((f'{skill}/../escape', b'escape\n'))
                with warnings.catch_warnings(), zipfile.ZipFile(archive_path, 'w') as archive:
                    warnings.simplefilter('ignore', UserWarning)
                    for name, payload in members:
                        if mutation in ('executable', 'symlink'):
                            info = zipfile.ZipInfo(name)
                            info.create_system = 3
                            info.external_attr = (0o100755 if mutation == 'executable' else 0o120644) << 16
                            archive.writestr(info, payload)
                        else:
                            archive.writestr(name, payload)
                digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
                (package_dir / 'SHA256SUMS').write_text(f'{digest}  {archive_path.name}\n')
                errors: list[str] = []
                with patch.object(validator, 'ROOT', root), patch.object(validator, 'SKILLS', (skill,)):
                    validator.validate_packages(errors)
                if mutation == 'valid':
                    self.assertEqual([], errors)
                else:
                    self.assertTrue(errors, mutation)

    def test_malformed_manifest_inventory_reports_errors_without_crashing(self) -> None:
        document = {"catalog_version": VERSION, "artifacts": [{"path": [], "kind": "file", "sha256": "0" * 64}]}
        errors: list[str] = []
        with patch.object(validator, '_validate_json_schema', return_value=document):
            validator.validate_release_manifest(errors)
        self.assertTrue(any('artifact inventory' in e for e in errors))

    def test_cli_smoke_contract_preserves_cases_and_request_ceiling(self) -> None:
        suite_path = ROOT / 'evals/daily-engineering/cases.json'
        suite = json.loads(suite_path.read_text())
        contract = json.loads((ROOT / 'evals/daily-engineering/cli-smoke-2026-10-20.json').read_text())
        self.assertEqual(hashlib.sha256(suite_path.read_bytes()).hexdigest(), contract['source_suite_sha256'])
        cases = {case['id']: case for case in suite['cases']}
        self.assertEqual(6, len(contract['cases']))
        self.assertEqual(6, contract['case_session_ceiling_per_client'])
        self.assertEqual(2, contract['continuity_followup_ceiling_per_client'])
        self.assertEqual(2, len(contract['continuity_followups']))
        for case in contract['cases']:
            self.assertEqual(cases[case['id']], case)
            encoded = (json.dumps(case, sort_keys=True, separators=(',', ':')) + '\n').encode()
            self.assertEqual(hashlib.sha256(encoded).hexdigest(), contract['case_hashes'][case['id']])

    def test_october20_pins_change_only_for_reviewed_stable_decisions(self) -> None:
        fixture = json.loads((ROOT / 'tests/fixtures/upstream-pins-before-october20.json').read_text())
        import subprocess
        original = json.loads(subprocess.check_output(['git', 'show', fixture['source_commit'] + ':catalog/upstream-pins.json'], cwd=ROOT))
        self.assertEqual(original, fixture['snapshot'])
        current = json.loads((ROOT / 'tests/fixtures/upstream-pins-before-pr72-followup.json').read_text())['snapshot']
        self.assertEqual(fixture['snapshot']['reviewed_on'], current['reviewed_on'])
        previous = {r['source_url']: r for r in fixture['snapshot']['sources']}
        actual = {r['source_url']: r for r in current['sources']}
        ledger = json.loads((ROOT / 'docs/audits/source-review-2026-10-20.json').read_text())
        reviews = ledger['records'] + ledger['additional_reviews']
        approved = {r['source_url']: r for r in reviews if r['decision'] == 'repin_reviewed_current_content'}
        self.assertEqual(35, len(approved))
        self.assertEqual(set(previous), set(actual))
        for url, pin in actual.items():
            if url in approved:
                record = approved[url]
                self.assertTrue(record['finding'])
                self.assertEqual(1, len(set(record['resampled_markers'])))
                self.assertEqual(f"{pin['marker_kind']}:{pin['marker_value']}", record['resampled_markers'][0])
            else:
                self.assertEqual(previous[url], pin)

    def test_followup_source_decisions_account_for_every_pin_change(self) -> None:
        import subprocess
        fixture = json.loads((ROOT / 'tests/fixtures/upstream-pins-before-pr72-followup.json').read_text())
        original = json.loads(subprocess.check_output(['git', 'show', fixture['source_commit'] + ':catalog/upstream-pins.json'], cwd=ROOT))
        self.assertEqual(original, fixture['snapshot'])
        current = json.loads((ROOT / 'catalog/upstream-pins.json').read_text())
        self.assertEqual(original['reviewed_on'], current['reviewed_on'])
        previous = {r['source_url']: r for r in original['sources']}
        actual = {r['source_url']: r for r in current['sources']}
        ledger = json.loads((ROOT / 'docs/audits/pr72-source-hold-repairs-2026-10-20.json').read_text())
        remaining = previous.copy()
        for decision in ledger['decisions']:
            old = decision['old_url']
            new = decision['current_url']
            prior = remaining.pop(old)
            self.assertEqual(f"{prior['marker_kind']}:{prior['marker_value']}", decision['expected_marker'])
            self.assertTrue(decision['finding'])
            action = decision['decision']
            if action == 'retire_obsolete_duplicate':
                self.assertNotIn(old, actual)
                self.assertIn(new, actual)
            elif action == 'retain_hold_inconsistent_samples':
                self.assertEqual(prior, actual[old])
                self.assertGreater(len(set(decision['resampled_markers'])), 1)
            else:
                self.assertEqual(3, len(decision['resampled_markers']))
                self.assertEqual({decision['reviewed_marker']}, set(decision['resampled_markers']))
                pin = actual[new]
                self.assertEqual(f"{pin['marker_kind']}:{pin['marker_value']}", decision['reviewed_marker'])
                if new != old:
                    self.assertNotIn(old, actual)
        for url, pin in remaining.items():
            self.assertEqual(pin, actual[url])
        self.assertEqual(ledger['current_active_sources'], len(actual))
        closeout = json.loads((ROOT / 'docs/audits/pr72-source-closeout-2026-10-20.json').read_text())
        self.assertEqual(set(actual), {r['source_url'] for r in closeout['records']})
        self.assertEqual(set(ledger['remaining_holds']),
                         {r['source_url'] for r in closeout['records'] if r['result'] != 'pass'})
        for record in closeout['records']:
            pin = actual[record['source_url']]
            self.assertEqual(f"{pin['marker_kind']}:{pin['marker_value']}", record['expected_marker'])
        self.assertEqual(set(previous) | {r['current_url'] for r in ledger['decisions']},
                         set(actual) | {r['old_url'] for r in ledger['decisions']})

    def test_originality_review_binds_owned_history_without_inventing_acceptance(self) -> None:
        import subprocess
        audit = json.loads((ROOT / 'docs/audits/originality-history-review-2026-10-20.json').read_text())
        entries = {r['skill']: r for r in json.loads((ROOT / 'provenance/catalog.json').read_text())['entries']}
        self.assertEqual(set(entries), {r['skill'] for r in audit['skills']})
        disputed = []
        for record in audit['skills']:
            skill = record['skill']
            self.assertEqual(entries[skill]['implementation_method'], record['current_declared_method'])
            payload = (ROOT / 'skills' / skill / 'SKILL.md').read_bytes()
            self.assertEqual(hashlib.sha256(payload).hexdigest(), record['current_entrypoint_sha256'])
            if record['historical_adaptation_declaration']:
                disputed.append(skill)
                relabel = record['relabel_review']
                bodies = [subprocess.check_output(['git', 'show', rev + ':skills/' + skill + '/SKILL.md'], cwd=ROOT).split(b'---', 2)[2]
                          for rev in (relabel['parent_revision'], relabel['revision'])]
                self.assertEqual(bodies[0], bodies[1])
                self.assertEqual(hashlib.sha256(bodies[0]).hexdigest(), relabel['before_body_sha256'])
                self.assertEqual(relabel['before_body_sha256'], relabel['after_body_sha256'])
                self.assertIn('Release acceptance remains held', entries[skill]['local_changes'])
        self.assertEqual(['claim-verification', 'cross-stack-quality-gates', 'prelaunch-readiness', 'publish-change-safely'], disputed)
        self.assertTrue(audit['retained_record_findings']['missing_evidence'])

    def test_official_swift_data_host_is_allowed_but_lookalikes_are_not(self) -> None:
        import check_repository_independence as independence
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'provenance').mkdir()
            for host, allowed in [('docs.swift.org', True), ('docs.swift.org.invalid', False)]:
                (root / 'provenance/catalog.json').write_text(json.dumps({'entries': [{'skill': 'fixture', 'source_url': f'https://{host}/latest/data/documentation.json'}]}))
                with patch.object(independence, 'ROOT', root):
                    errors = independence.provenance_source_errors()
                self.assertEqual(allowed, not errors)


if __name__ == '__main__':
    unittest.main()
