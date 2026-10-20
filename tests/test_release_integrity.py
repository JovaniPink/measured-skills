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
from cataloglib import VERSION, read_skill_metadata  # noqa: E402


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
                shutil.copyfile(ROOT / 'LICENSE', root / 'LICENSE')
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
        current = json.loads((ROOT / 'tests/fixtures/upstream-pins-before-readiness-followup.json').read_text())['snapshot']
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
        entries = {r['skill']: r for r in json.loads(subprocess.check_output(['git', 'show', audit['source_revision'] + ':provenance/catalog.json'], cwd=ROOT))['entries']}
        self.assertEqual(set(entries), {r['skill'] for r in audit['skills']})
        disputed = []
        for record in audit['skills']:
            skill = record['skill']
            self.assertEqual(entries[skill]['implementation_method'], record['current_declared_method'])
            payload = subprocess.check_output(['git', 'show', audit['source_revision'] + ':skills/' + skill + '/SKILL.md'], cwd=ROOT)
            self.assertEqual(hashlib.sha256(payload).hexdigest(), record['current_entrypoint_sha256'])
            if record['historical_adaptation_declaration']:
                disputed.append(skill)
                relabel = record['relabel_review']
                bodies = [subprocess.check_output(['git', 'show', rev + ':skills/' + skill + '/SKILL.md'], cwd=ROOT).split(b'---', 2)[2]
                          for rev in (relabel['parent_revision'], relabel['revision'])]
                self.assertEqual(bodies[0], bodies[1])
                self.assertEqual(hashlib.sha256(bodies[0]).hexdigest(), relabel['before_body_sha256'])
                self.assertEqual(relabel['before_body_sha256'], relabel['after_body_sha256'])
        self.assertEqual(['claim-verification', 'cross-stack-quality-gates', 'prelaunch-readiness', 'publish-change-safely'], disputed)
        self.assertTrue(audit['retained_record_findings']['missing_evidence'])

    def test_owned_origin_schema_accepts_valid_paths_and_rejects_unsafe_paths(self) -> None:
        from schema_validation import validate_instance
        document = json.loads((ROOT / 'provenance/catalog.json').read_text())
        schema = json.loads((ROOT / 'provenance/schema.json').read_text())
        self.assertEqual([], validate_instance(document, schema))
        for path in ('../outside', 'skills/claim-verification/SKILLXmd', 'skills/claim-verification/SKILL\\Xmd'):
            mutated = copy.deepcopy(document)
            entry = next(r for r in mutated['entries'] if 'owned_origin' in r)
            entry['owned_origin']['entrypoint'] = path
            self.assertTrue(validate_instance(mutated, schema), path)

    def test_owned_origin_corrections_preserve_history_and_remain_unqualified(self) -> None:
        audit = json.loads((ROOT / 'docs/audits/owned-origin-corrections-2026-10-20.json').read_text())
        entries = {r['skill']: r for r in json.loads((ROOT / 'provenance/catalog.json').read_text())['entries']}
        self.assertEqual('not_accepted', audit['release_acceptance'])
        self.assertEqual(4, len(audit['changes']))
        import subprocess
        historical = json.loads(subprocess.check_output(['git', 'show', audit['reviewed_source'] + ':provenance/catalog.json'], cwd=ROOT))
        self.assertEqual(audit['remaining_clean_room_declarations'],
                         sum(r['implementation_method'] == 'clean-room' for r in historical['entries']) - len(audit['changes']))
        for change in audit['changes']:
            skill = change['skill']
            entry = entries[skill]
            self.assertEqual('adapted', entry['implementation_method'])
            self.assertEqual(change['owned_origin'], entry['owned_origin'])
            self.assertEqual(entry['owned_origin']['revision'], entry['pinned_revision'])
            payload = (ROOT / 'skills' / skill / 'SKILL.md').read_bytes()
            self.assertEqual(hashlib.sha256(payload).hexdigest(), change['corrected_entrypoint_sha256'])
            self.assertEqual('adapted', read_skill_metadata(ROOT / 'skills' / skill)['provenance'])
            errors: list[str] = []
            validator._validate_owned_origin(entry, errors)
            self.assertEqual([], errors)

    def test_remaining_clean_room_review_is_complete_and_changes_only_labels(self) -> None:
        import subprocess
        audit = json.loads((ROOT / 'docs/audits/clean-room-declaration-review-2026-10-20.json').read_text())
        revision = audit['reviewed_source']
        correction_revision = '82d3ab5f1de27a32aa1bb698b72fe29d66e75c18'
        subprocess.run(['git', 'merge-base', '--is-ancestor', correction_revision, 'HEAD'], cwd=ROOT, check=True)
        before = {r['skill']: r for r in json.loads(subprocess.check_output(
            ['git', 'show', revision + ':provenance/catalog.json'], cwd=ROOT))['entries']}
        after = {r['skill']: r for r in json.loads(subprocess.check_output(
            ['git', 'show', correction_revision + ':provenance/catalog.json'], cwd=ROOT))['entries']}
        expected = {name for name, entry in before.items() if entry['implementation_method'] == 'clean-room'}
        self.assertEqual(40, len(expected))
        self.assertEqual(expected, {r['skill'] for r in audit['changes']})
        self.assertEqual(40, len(audit['changes']))
        self.assertEqual('not_accepted', audit['release_acceptance'])
        for record in audit['changes']:
            skill = record['skill']
            with self.subTest(skill=skill):
                self.assertEqual('requires_correction', record['decision'])
                self.assertEqual('needs_evidence', record['qualification'])
                self.assertEqual('original', after[skill]['implementation_method'])
                self.assertEqual('original', read_skill_metadata(ROOT / 'skills' / skill)['provenance'])
                entrypoint = 'skills/' + skill + '/SKILL.md'
                previous = subprocess.check_output(['git', 'show', revision + ':' + entrypoint], cwd=ROOT)
                # This audit proves its historical metadata-only correction.
                # The full expression packet separately binds today's reviewed delta.
                current = subprocess.check_output(['git', 'show', correction_revision + ':' + entrypoint], cwd=ROOT)
                self.assertEqual(previous.replace(b'  provenance: "clean-room"', b'  provenance: "original"'), current)
                self.assertEqual(hashlib.sha256(current).hexdigest(), record['corrected_entrypoint_sha256'])
                self.assertEqual(hashlib.sha256(previous.split(b'---', 2)[2]).hexdigest(), record['reviewed_body_sha256'])
                expected_paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', revision, 'skills/' + skill], cwd=ROOT).decode().splitlines()
                self.assertEqual(set(expected_paths), set(record['reviewed_files']))
                for path, value in record['reviewed_files'].items():
                    self.assertTrue(path.startswith('skills/' + skill + '/'))
                    blob = subprocess.check_output(['git', 'show', revision + ':' + path], cwd=ROOT)
                    self.assertEqual(hashlib.sha256(blob).hexdigest(), value)
                self.assertEqual(before[skill]['upstream_license'], record['previous_license_statement'])
                self.assertEqual(after[skill]['upstream_license'], record['corrected_license_statement'])
                self.assertIn('not independently established', record['corrected_license_statement'])
                creation = record['creation_revision']
                subprocess.run(['git', 'merge-base', '--is-ancestor', creation, revision], cwd=ROOT, check=True)
                creation_paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', creation, 'skills/' + skill], cwd=ROOT).decode().splitlines()
                self.assertEqual(set(creation_paths), set(record['creation_files']))
                for path, value in record['creation_files'].items():
                    self.assertTrue(path.startswith('skills/' + skill + '/'))
                    blob = subprocess.check_output(['git', 'show', creation + ':' + path], cwd=ROOT)
                    self.assertEqual(hashlib.sha256(blob).hexdigest(), value)
                initial = subprocess.check_output(['git', 'show', creation + ':' + entrypoint], cwd=ROOT)
                self.assertEqual(hashlib.sha256(initial).hexdigest(), record['creation_entrypoint_sha256'])
                self.assertEqual(hashlib.sha256(initial.split(b'---', 2)[2]).hexdigest(), record['creation_body_sha256'])
                for field in ('source_url', 'pinned_revision', 'reviewed_on', 'security_review'):
                    self.assertEqual(before[skill][field], after[skill][field])
        for skill in set(before) - expected:
            self.assertEqual(before[skill], after[skill])
        self.assertEqual({'original': 83, 'adapted': 4}, audit['summary']['current_declared_methods'])
        self.assertFalse(any(r['implementation_method'] == 'clean-room' for r in after.values()))

    def test_retained_authoring_evidence_does_not_invent_process_acceptance(self) -> None:
        audit = json.loads((ROOT / 'docs/audits/clean-room-declaration-review-2026-10-20.json').read_text())
        self.assertEqual(0, audit['summary']['supported_clean_room_processes'])
        self.assertEqual(0, audit['summary']['independent_qualifications'])
        self.assertEqual(40, sum(audit['summary']['batch_counts'].values()))
        for record in audit['changes']:
            self.assertTrue(record['missing_evidence'])
            self.assertTrue(record['authoring_events'])
            self.assertTrue(record['prior_exposure_events'])
            authored_at = audit['events'][record['authoring_events'][0]]['observed_at']
            for key in record['prior_exposure_events']:
                self.assertLess(audit['events'][key]['observed_at'], authored_at)
            for key in record['authoring_events'] + record['input_events'] + record['prior_exposure_events']:
                event = audit['events'][key]
                for field in ('input_sha256', 'output_sha256'):
                    self.assertRegex(event[field], r'^[0-9a-f]{64}$')
                self.assertTrue(event['scope'])
        self.assertEqual('mixed_authoring_input', audit['events']['event-5306']['kind'])

    def test_new_source_review_accounts_for_each_pin_change(self) -> None:
        import subprocess
        fixture = json.loads((ROOT / 'tests/fixtures/upstream-pins-before-readiness-followup.json').read_text())
        original = json.loads(subprocess.check_output(['git', 'show', fixture['source_commit'] + ':catalog/upstream-pins.json'], cwd=ROOT))
        self.assertEqual(original, fixture['snapshot'])
        current = json.loads((ROOT / 'catalog/upstream-pins.json').read_text())
        for field in ('reviewed_on', 'max_review_age_days'):
            self.assertEqual(original[field], current[field])
        before = {r['source_url']: r for r in original['sources']}
        actual = {r['source_url']: r for r in current['sources']}
        audit = json.loads((ROOT / 'docs/audits/source-hold-followup-2026-10-20.json').read_text())
        expected = before.copy()
        for decision in audit['decisions']:
            prior = expected.pop(decision['old_url'])
            self.assertEqual(f"{prior['marker_kind']}:{prior['marker_value']}", decision['previous_marker'])
            self.assertEqual(3, len(decision['sampled_markers']))
            self.assertTrue(decision['finding'])
            if decision['decision'] == 'retain_inconsistent_sample_hold':
                self.assertGreater(len(set(decision['sampled_markers'])), 1)
                expected[decision['old_url']] = prior
            else:
                self.assertEqual(1, len(set(decision['sampled_markers'])))
                kind, value = decision['sampled_markers'][0].split(':', 1)
                url = decision['current_url']
                expected[url] = {'source_url': url, 'marker_kind': kind, 'marker_value': value}
        self.assertEqual(expected, actual)
        self.assertEqual(audit['active_sources'], len(actual))
        checkpoint = json.loads((ROOT / 'docs/audits/source-hold-followup-checkpoint-2026-10-20.json').read_text())
        self.assertEqual('pass', checkpoint['result'])
        self.assertEqual(set(actual), {r['source_url'] for r in checkpoint['records']})
        self.assertEqual(hashlib.sha256((ROOT / 'catalog/upstream-pins.json').read_bytes()).hexdigest(),
                         audit['reviewed_pin_inventory_sha256'])
        for record in checkpoint['records']:
            self.assertEqual('pass', record['result'])
            pin = actual[record['source_url']]
            self.assertEqual(f"{pin['marker_kind']}:{pin['marker_value']}", record['expected_marker'])
            self.assertEqual(record['expected_marker'], record['observed_marker'])

    def test_owned_origin_rejects_an_existing_nonancestor_commit(self) -> None:
        import subprocess
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / 'skills/claim-verification/SKILL.md'
            target.parent.mkdir(parents=True)
            target.write_text('Synthetic owned-origin fixture.\n')
            (root / 'LICENSE').write_bytes((ROOT / 'LICENSE').read_bytes())
            def git(*args: str) -> bytes:
                return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.DEVNULL)
            git('init', '-q')
            git('add', '.')
            git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                '-c', 'core.hooksPath=/dev/null', '-c', 'commit.gpgsign=false', 'commit', '-qm', 'source')
            revision = git('rev-parse', 'HEAD').decode().strip()
            git('checkout', '--orphan', 'other-history')
            git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                '-c', 'core.hooksPath=/dev/null', '-c', 'commit.gpgsign=false', 'commit', '-qm', 'unrelated')
            git('cat-file', '-e', revision + '^{commit}')
            entry: dict[str, object] = {'skill': 'claim-verification', 'implementation_method': 'adapted',
                                       'pinned_revision': revision, 'owned_origin': {
                'revision': revision, 'entrypoint': 'skills/claim-verification/SKILL.md', 'license': 'MIT',
                'entrypoint_sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
                'license_sha256': hashlib.sha256((root / 'LICENSE').read_bytes()).hexdigest()}}
            errors: list[str] = []
            with patch.object(validator, 'ROOT', root):
                validator._validate_owned_origin(entry, errors)
            self.assertTrue(any('owned origin is unavailable' in e for e in errors), errors)

    def test_owned_adaptation_requires_verified_ancestor_and_license(self) -> None:
        import subprocess
        revision = '5593d89f8a9b2d30509244fb82d9c16666423151'
        entrypoint = 'skills/claim-verification/SKILL.md'
        payload = subprocess.check_output(['git', 'show', revision + ':' + entrypoint], cwd=ROOT)
        license_bytes = subprocess.check_output(['git', 'show', revision + ':LICENSE'], cwd=ROOT)
        original: dict[str, object] = {'skill': 'claim-verification', 'disposition': 'covered',
                    'implementation_method': 'adapted', 'pinned_revision': revision,
                    'owned_origin': {'revision': revision, 'entrypoint': entrypoint, 'license': 'MIT',
                                     'entrypoint_sha256': hashlib.sha256(payload).hexdigest(),
                                     'license_sha256': hashlib.sha256(license_bytes).hexdigest()}}
        for mutation in ('valid', 'missing', 'unknown_revision', 'content', 'license', 'path', 'pin', 'wrong_method'):
            with self.subTest(mutation=mutation):
                entry = copy.deepcopy(original)
                if mutation == 'missing':
                    entry.pop('owned_origin')
                elif mutation == 'unknown_revision':
                    origin = entry['owned_origin']
                    assert isinstance(origin, dict)
                    entry['pinned_revision'] = origin['revision'] = '0' * 40
                elif mutation == 'content':
                    origin = entry['owned_origin']
                    assert isinstance(origin, dict)
                    origin['entrypoint_sha256'] = '0' * 64
                elif mutation == 'license':
                    origin = entry['owned_origin']
                    assert isinstance(origin, dict)
                    origin['license_sha256'] = '0' * 64
                elif mutation == 'path':
                    origin = entry['owned_origin']
                    assert isinstance(origin, dict)
                    origin['entrypoint'] = '../outside'
                elif mutation == 'pin':
                    entry['pinned_revision'] = '0' * 40
                elif mutation == 'wrong_method':
                    entry['implementation_method'] = 'original'
                errors: list[str] = []
                with patch.object(validator, '_validate_json_schema', return_value={'entries': [entry]}), \
                        patch.object(validator, 'ALL_SKILLS', ('claim-verification',)), \
                        patch.object(validator, 'read_skill_metadata', return_value={'provenance': entry['implementation_method']}):
                    validator.validate_provenance(errors)
                self.assertEqual(mutation != 'valid', bool(errors), errors)

    def test_raw_repository_links_keep_the_same_boundary(self) -> None:
        import check_repository_independence as independence
        prefix = 'https://' + 'raw.githubusercontent.com/'
        asvs = prefix + 'OWASP/ASVS/master/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.json'
        self.assertEqual([], independence.scan_text('fixture.md', asvs))
        self.assertEqual([], independence.scan_text('fixture.md', prefix + 'JovaniPink/measured-skills/main/README.md'))
        self.assertTrue(independence.scan_text('fixture.md', prefix + 'unreviewed/skill-catalog/main/SKILL.md'))
        self.assertTrue(independence.scan_text('fixture.md', asvs + '?other=1'))
        self.assertEqual([], independence.scan_text('fixture.md', prefix + 'python/cpython/3.15/Doc/contents.rst'))
        self.assertTrue(independence.scan_text('fixture.md', prefix + 'python/cpython/3.15/Lib/unittest/__init__.py'))

    def test_primary_document_exceptions_are_exact(self) -> None:
        import check_repository_independence as independence
        prefix = 'https://' + 'raw.githubusercontent.com/'
        urls = [prefix + 'OWASP/ASVS/master/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.json',
                prefix + 'python/cpython/3.15/Doc/contents.rst',
                prefix + 'python/cpython/3.15/Doc/library/unittest.rst']
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'provenance').mkdir()
            for url in urls:
                wrong_owner = prefix + 'unreviewed/' + url.removeprefix(prefix).split('/', 1)[1]
                for candidate, allowed in [(url, True), (url + '?variant=other', False), (wrong_owner, False)]:
                    (root / 'provenance/catalog.json').write_text(json.dumps({'entries': [{'skill': 'fixture', 'source_url': candidate}]}))
                    with patch.object(independence, 'ROOT', root):
                        errors = independence.provenance_source_errors()
                    self.assertEqual(allowed, not errors)

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
