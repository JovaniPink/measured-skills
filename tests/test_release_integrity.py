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
        for mutation in ('valid', 'modified', 'missing', 'extra', 'duplicate', 'unsafe'):
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


if __name__ == '__main__':
    unittest.main()
