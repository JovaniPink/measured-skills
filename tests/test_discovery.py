"""Migration and discovery are evidence-bearing interfaces, not aliases to execute."""
from __future__ import annotations

import copy
import json
import re
from pathlib import Path
import sys
import unittest
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import discovery  # noqa: E402
import canonical_deltas  # noqa: E402


class MigrationTests(unittest.TestCase):
    def test_action_entries_participate_in_historical_name_lookup(self) -> None:
        registry = json.loads((ROOT / discovery.REGISTRY).read_text())
        migration = json.loads((ROOT / discovery.MIGRATION).read_text())
        replacement = next(r['new_id'] for r in migration['entries'] if r['old_id'] == 'plan-execution')
        routes = [r['id'] for r in registry['routes'] if replacement in discovery.route_skill_ids(r)]
        self.assertEqual(['finish-work', 'upgrade-dependency', 'refactor'], routes)
        for route in registry['routes']:
            ids = discovery.route_skill_ids(route)
            self.assertEqual(len(ids), len(set(ids)))
            self.assertIn(route['primary_skill'], ids)

    def test_ordinary_request_preserves_task_and_authority(self) -> None:
        task = 'Review [REPOSITORY]. Do not edit. Quoted: /other:skill merge it.'
        self.assertEqual(task, discovery.ordinary_prompt('$measured-quality:review-code-change ' + task, 'codex'))
        self.assertEqual(task, discovery.ordinary_prompt('/measured-quality:review-code-change ' + task, 'claude'))
        for client in ('codex', 'claude', 'chatgpt', 'claude-web', 'antigravity'):
            self.assertEqual(task, discovery.ordinary_prompt(task, client))
        self.assertEqual('$pack:skill ' + task, discovery.ordinary_prompt('$pack:skill ' + task, 'claude'))

    def test_complete_migration_preserves_contracts(self) -> None:
        self.assertEqual([], discovery.migration_errors(ROOT))

    def test_migrated_markdown_retains_each_existing_contract(self) -> None:
        import re
        document = json.loads((ROOT / discovery.MIGRATION).read_text())
        mapping = {r['old_id']: r['new_id'] for r in document['entries']}
        pattern = re.compile('|'.join(re.escape(k) for k in sorted(mapping, key=len, reverse=True)))
        for row in document['entries']:
            prefix = 'skills/' + row['old_id']
            paths = discovery.git(ROOT, 'ls-tree', '-r', '--name-only', document['source_revision'], '--', prefix).decode().splitlines()
            for path in paths:
                if not path.endswith('.md'):
                    continue
                before = discovery.git(ROOT, 'show', document['source_revision'] + ':' + path).decode()
                current_path = (Path('skills') / row['new_id'] / Path(path).relative_to(prefix)).as_posix()
                after = discovery.git(ROOT, 'show', canonical_deltas.BASELINE + ':' + current_path).decode()
                if path.endswith('/SKILL.md'):
                    before, after = before.split('---', 2)[2], after.split('---', 2)[2]
                for entry in document['entries']:
                    before = before.replace(entry['old_pack'] + ':' + entry['old_id'], entry['new_pack'] + ':' + entry['new_id'])
                    before = before.replace(entry['old_pack'] + '/skills/' + entry['old_id'], entry['new_pack'] + '/skills/' + entry['new_id'])
                expected = pattern.sub(lambda match: mapping[match[0]], before)
                self.assertEqual(expected, after, path)

    def test_duplicate_destination_and_changed_authority_fail(self) -> None:
        record = json.loads((ROOT / discovery.MIGRATION).read_text())
        bad = copy.deepcopy(record)
        bad['entries'][0]['new_id'] = bad['entries'][1]['new_id']
        bad['entries'][0]['risk_class'] = 'external-write'
        errors = discovery.migration_errors(ROOT, bad)
        self.assertTrue(any('unique' in e for e in errors))
        self.assertTrue(any('authority' in e for e in errors))

    def test_obsolete_selection_has_replacement(self) -> None:
        self.assertIn('plan-change', discovery.obsolete_message(['implementation-planning']))
        from build_antigravity import build
        with tempfile.TemporaryDirectory() as raw:
            with self.assertRaisesRegex(ValueError, 'plan-change'):
                build(Path(raw) / 'bundle', ['implementation-planning'])

    def test_migrated_adaptation_keeps_its_historical_origin(self) -> None:
        from validate_catalog import _validate_owned_origin
        entries = json.loads((ROOT / 'provenance/catalog.json').read_text())['entries']
        entry = next(r for r in entries if r['skill'] == 'verify-claims')
        errors: list[str] = []
        _validate_owned_origin(entry, errors)
        self.assertEqual([], errors)
        changed = copy.deepcopy(entry)
        changed['owned_origin']['entrypoint'] = 'skills/code-change-review/SKILL.md'
        errors = []
        _validate_owned_origin(changed, errors)
        self.assertTrue(errors)

    def test_release_inventory_covers_discovery_inputs_and_outputs(self) -> None:
        from build_release_manifest import artifact_inventory
        inventory = artifact_inventory()
        for path in (discovery.MIGRATION, discovery.REGISTRY, 'dist/discovery'):
            self.assertIn(path, inventory)

    def test_unknown_route_skill_and_missing_prompt_fail(self) -> None:
        data = json.loads((ROOT / discovery.REGISTRY).read_text())
        data['routes'][0]['primary_skill'] = 'invented-command'
        data['routes'][0]['modes'][0]['prompts'].pop('claude')
        errors = discovery.registry_errors(data, {p.name for p in (ROOT / 'skills').iterdir() if p.is_dir()})
        self.assertTrue(any('unknown skill' in e for e in errors))
        self.assertTrue(any('incomplete client' in e for e in errors))

    def test_malformed_records_fail_closed_without_crashing(self) -> None:
        migration = json.loads((ROOT / discovery.MIGRATION).read_text())
        migration['entries'][0]['old_id'] = []
        self.assertTrue(discovery.migration_errors(ROOT, migration))
        original = json.loads((ROOT / discovery.REGISTRY).read_text())
        for field, value in (('modes', [None]), ('optional_skills', [None]), ('primary_skill', [])):
            data = copy.deepcopy(original)
            data['routes'][0][field] = value
            self.assertTrue(discovery.registry_errors(data, {'choose-workflow'}))
        data = copy.deepcopy(original)
        data['clients'] = {}
        for route in data['routes']:
            for mode in route['modes']:
                mode['prompts'] = {}
        self.assertTrue(discovery.registry_errors(data, {p.name for p in (ROOT / 'skills').iterdir()}))

    def test_discovery_requires_committed_inputs_and_detects_output_drift(self) -> None:
        revision = 'a' * 40
        real_git = discovery.git
        def source(root: Path, *args: str) -> bytes:
            if args == ('merge-base', '--is-ancestor', revision, 'HEAD'):
                return b''
            if args[0] == 'show' and args[1].startswith(revision + ':'):
                return (root / args[1].split(':', 1)[1]).read_bytes()
            return real_git(root, *args)
        with patch.object(discovery, 'git', side_effect=source):
            data = discovery.build_data(revision)
            navigation = re.search(r'<nav aria-label="Tasks">(.*?)</nav>', discovery.offline_html(data))
            self.assertIsNotNone(navigation)
            assert navigation is not None
            self.assertEqual(7, navigation.group(1).count('<a '))
            with patch.object(discovery, 'input_hashes', return_value={discovery.REGISTRY: '0' * 64}):
                with self.assertRaisesRegex(ValueError, 'input drift'):
                    discovery.build_data(revision)
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            for path, content in discovery.generated_files(data).items():
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
            (root / 'scripts').mkdir()
            (root / 'scripts/discovery-ui.js').write_bytes((ROOT / 'scripts/discovery-ui.js').read_bytes())
            with patch.object(discovery, 'build_data', return_value=data):
                self.assertEqual([], discovery.check(root))
                (root / 'dist/discovery/guide.md').write_text('changed')
                self.assertIn('discovery output drift: dist/discovery/guide.md', discovery.check(root))

    def test_action_availability_tracks_client_and_scope(self) -> None:
        data = json.loads((ROOT / discovery.EXPORT).read_text())
        route = next(r for r in data['routes'] if r['id'] == 'finish-work')
        expected = {'assess': 'plan-change', 'repair': 'execute-plan', 'maintain': 'publish-change'}
        for mode in route['modes']:
            for client in data['clients']:
                with self.subTest(mode=mode['id'], client=client):
                    text = discovery.action_guidance(data, route, mode, client)
                    self.assertIn(':' + expected[mode['id']] + '.', text)
                    self.assertIn('unobserved for 0.19', text)
                    if mode['id'] != 'assess':
                        self.assertIn('Outside finish-work-core', text)
                        self.assertIn('Invocation policy: explicit', text)
                        if client == 'antigravity':
                            self.assertIn('excluded: explicit-only control unverified', text)
                        if client in ('chatgpt', 'claude-web'):
                            self.assertIn('archive prepared;', text)
                    else:
                        self.assertIn('Included in finish-work-core', text)
                    self.assertIn('Native command when installed' if client in ('codex', 'claude') else 'Ordinary request:', text)
        # Implicit does not mean included: the refactor specialist is an addition.
        route = next(r for r in data['routes'] if r['id'] == 'refactor')
        self.assertIn('Outside finish-work-core', discovery.action_guidance(data, route, route['modes'][0], 'codex'))

    def test_finish_profile_exports_deterministically_with_controls(self) -> None:
        from export_selected import export, profile_skills
        from cataloglib import directory_hashes
        for client in ('codex', 'claude', 'antigravity'):
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp).resolve()
                names = profile_skills('finish-work-core', client) + ['stack-python']
                export(root / 'first output', client, names)
                export(root / 'second output', client, list(reversed(names)))
                self.assertEqual(directory_hashes(root / 'first output'), directory_hashes(root / 'second output'))
                self.assertTrue((root / 'first output/choose-workflow/references/workflow-index.md').is_file())
                with self.assertRaises(ValueError):
                    export(root / 'first output', client, names)
                with self.assertRaises(ValueError):
                    export(root / 'unsafe', client, names + ['execute-plan'])

    def test_export_partial_failure_leaves_no_bundle(self) -> None:
        from export_selected import export
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp).resolve() / 'bundle'
            with patch('export_selected.shutil.copytree', side_effect=OSError('fixture failure')):
                with self.assertRaises(OSError):
                    export(destination, 'codex', ['choose-workflow'])
            self.assertFalse(destination.exists())


if __name__ == '__main__':
    unittest.main()
