"""Notice retention for independently usable skill distributions."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_distributions as builder  # noqa: E402
import export_selected  # noqa: E402
import validate_catalog as validator  # noqa: E402
from cataloglib import read_skill_metadata  # noqa: E402


class DistributionLicensingTests(unittest.TestCase):
    def test_generated_skills_and_packs_retain_the_complete_notice(self) -> None:
        notice = (ROOT / 'LICENSE').read_bytes()
        with tempfile.TemporaryDirectory() as raw:
            groups = builder.build(Path(raw) / 'plugins')
            for group in groups:
                for pack in group.values():
                    with self.subTest(pack=pack):
                        self.assertTrue((pack / 'LICENSE').is_file())
                        self.assertEqual(notice, (pack / 'LICENSE').read_bytes())
                        for skill in (pack / 'skills').iterdir():
                            self.assertTrue((skill / 'LICENSE').is_file())
                            self.assertEqual(notice, (skill / 'LICENSE').read_bytes())

    def test_selected_exports_retain_notice_and_bind_its_hash(self) -> None:
        notice = (ROOT / 'LICENSE').read_bytes()
        for client in ('codex', 'claude', 'antigravity'):
            with self.subTest(client=client), tempfile.TemporaryDirectory() as raw:
                output = Path(raw).resolve() / 'skills'
                export_selected.export(output, client, ['claim-verification'])
                self.assertTrue((output / 'claim-verification/LICENSE').is_file())
                self.assertEqual(notice, (output / 'claim-verification/LICENSE').read_bytes())
                receipt = json.loads((output / 'export-manifest.json').read_text())
                self.assertEqual(hashlib.sha256(notice).hexdigest(), receipt['files']['claim-verification/LICENSE'])

    def test_scoped_disposition_binds_inventory_without_accepting_it(self) -> None:
        import subprocess
        audit = json.loads((ROOT / 'docs/audits/scoped-expression-disposition-2026-10-20.json').read_text())
        self.assertEqual('proposed', audit['status'])
        repair = audit['notice_repair_checkpoint']
        subprocess.run(['git', 'merge-base', '--is-ancestor', repair['source_commit'], 'HEAD'], cwd=ROOT, check=True)
        self.assertEqual(hashlib.sha256(subprocess.check_output(['git', 'show', repair['source_commit'] + ':LICENSE'], cwd=ROOT)).hexdigest(), repair['license_sha256'])
        self.assertEqual((33, 244, 87), (repair['generated_pack_notices'], repair['generated_skill_notices'], repair['upload_archives']))

        self.assertEqual({'status': 'pending', 'accepted_by': None, 'accepted_on': None, 'accepted_revision': None}, audit['maintainer_decision'])
        profile = next(r for r in json.loads((ROOT / 'catalog/profiles.json').read_text())['profiles'] if r['id'] == 'daily-engineering-experimental')
        selected = set(profile['skills']) | {'claim-verification', 'cross-stack-quality-gates', 'prelaunch-readiness', 'publish-change-safely'}
        self.assertEqual(14, len(selected))
        self.assertEqual(selected, {r['skill'] for r in audit['skills']})
        all_skills = {r['skill'] for r in json.loads((ROOT / 'provenance/catalog.json').read_text())['entries']}
        self.assertEqual(all_skills - selected, set(audit['outside_scope']))
        self.assertEqual(73, len(audit['outside_scope']))
        expected = {'LICENSE', 'provenance/catalog.json'}
        for name in selected:
            expected.update(subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', audit['reviewed_source'], '--', 'skills/' + name], cwd=ROOT).decode().splitlines())
        self.assertEqual(expected, set(audit['inventory']))
        for path, value in audit['inventory'].items():
            payload = subprocess.check_output(['git', 'show', audit['reviewed_source'] + ':' + path], cwd=ROOT)
            self.assertEqual(hashlib.sha256(payload).hexdigest(), value)
            if path == 'LICENSE' or path.startswith('skills/'):
                self.assertEqual(payload, (ROOT / path).read_bytes())
        encoded = (json.dumps(audit['inventory'], sort_keys=True, separators=(',', ':')) + '\n').encode()
        self.assertEqual(hashlib.sha256(encoded).hexdigest(), audit['inventory_sha256'])
        previous = {r['skill']: r for r in json.loads(subprocess.check_output(['git', 'show', audit['reviewed_source'] + ':provenance/catalog.json'], cwd=ROOT))['entries']}
        current = {r['skill']: r for r in json.loads((ROOT / 'provenance/catalog.json').read_text())['entries']}
        self.assertEqual(5, len(audit['provenance_note_corrections']))
        for correction in audit['provenance_note_corrections']:
            name = correction['skill']
            self.assertIn(name, selected)
            self.assertEqual(previous[name]['upstream_license'], correction['previous_upstream_license'])
            self.assertEqual(current[name]['upstream_license'], correction['corrected_upstream_license'])
            self.assertEqual(previous[name]['local_changes'], correction['previous_local_changes'])
            self.assertEqual(current[name]['local_changes'], correction['corrected_local_changes'])
            for key in set(previous[name]) - {'upstream_license', 'local_changes'}:
                self.assertEqual(previous[name][key], current[name][key])
        self.assertIn('universal non-infringement', audit['excluded_claims'])
        self.assertEqual('not_established', next(r['status'] for r in audit['controls'] if r['id'] == 'human-contribution'))

    def test_archive_validation_rejects_coordinated_notice_loss(self) -> None:
        skill = 'claim-verification'
        metadata = read_skill_metadata(ROOT / 'skills' / skill)
        source = ROOT / 'plugins/claude' / metadata['plugin'] / 'skills' / skill
        for replacement in (None, b'MIT metadata without the owned notice.\n'):
            with self.subTest(replacement=replacement), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                shutil.copyfile(ROOT / 'LICENSE', root / 'LICENSE')
                shutil.copytree(ROOT / 'skills' / skill, root / 'skills' / skill)
                target = root / 'plugins/claude' / metadata['plugin'] / 'skills' / skill
                shutil.copytree(source, target)
                if replacement is None:
                    (target / 'LICENSE').unlink(missing_ok=True)
                else:
                    (target / 'LICENSE').write_bytes(replacement)
                packages = root / 'dist/claude-ai'
                packages.mkdir(parents=True)
                archive_path = packages / (skill + '-0.18.0.zip')
                with zipfile.ZipFile(archive_path, 'w') as archive:
                    for item in target.rglob('*'):
                        if item.is_file():
                            archive.writestr(skill + '/' + item.relative_to(target).as_posix(), item.read_bytes())
                (packages / 'SHA256SUMS').write_text(hashlib.sha256(archive_path.read_bytes()).hexdigest() + '  ' + archive_path.name + '\n')
                errors: list[str] = []
                with patch.object(validator, 'ROOT', root), patch.object(validator, 'SKILLS', (skill,)):
                    validator.validate_packages(errors)
                self.assertTrue(any('license notice' in error.lower() for error in errors), errors)
