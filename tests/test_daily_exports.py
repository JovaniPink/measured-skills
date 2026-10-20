from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import export_selected  # noqa: E402
import export_trigger_evals  # noqa: E402


class DailyExports(unittest.TestCase):
    def test_reviewed_data_authorities_are_explicitly_allowed(self) -> None:
        from check_repository_independence import PRIMARY_AUTHORITY_HOSTS
        for host in ('docs.cloud.google.com', 'docs.getdbt.com', 'airflow.apache.org', 'spark.apache.org'):
            self.assertIn(host, PRIMARY_AUTHORITY_HOSTS)
        self.assertNotIn('unreviewed.example', PRIMARY_AUTHORITY_HOSTS)

    def test_inlined_matrices_preserve_every_original_row(self) -> None:
        matrices = {'agent-context-state-memory-design': ['| Field | Question |',
                                               '| --- | --- |',
                                               '| Class | Is this instruction, request context, event '
                                               'history, scoped state, memory, retrieval, tool output, or '
                                               'artifact? |',
                                               '| Subject | Which user, tenant, case, agent, or system '
                                               'does it concern? |',
                                               '| Authority | What store or decision owner can establish '
                                               'or change it? |',
                                               '| Provenance | Where did it come from, and can that origin '
                                               'be verified? |',
                                               '| Writer | Which authenticated principal may create or '
                                               'update it? |',
                                               '| Reader | Which principal may observe it, and for what '
                                               'purpose? |',
                                               '| Time | When was it effective, observed, recorded, and '
                                               'last checked? |',
                                               '| Retention | How long does it remain, and what rule '
                                               'governs deletion? |',
                                               '| Conflict | What happens when sources disagree? |',
                                               '| Revocation | How is it made ineligible and removed from '
                                               'future context? |',
                                               '| Isolation | Which request, session, user, tenant, and '
                                               'evaluation boundaries apply? |'],
         'agent-protocol-interoperability-review': ['| Boundary | Questions |',
                                                    '| --- | --- |',
                                                    '| Version | Which specification and implementation '
                                                    'versions are in use? |',
                                                    '| Normative source | Which versioned schema is '
                                                    'authoritative, and which rendered or generated '
                                                    'artifacts are only projections? |',
                                                    '| Discovery | Who publishes capabilities, how is the '
                                                    'record signed or authenticated, and how are caches '
                                                    'refreshed or revoked? |',
                                                    '| Binding | Do each advertised transport and protocol '
                                                    'binding preserve operations, results, errors, and '
                                                    'authentication? |',
                                                    '| Identity | Which user, service, agent, and tenant '
                                                    'identities cross the boundary? |',
                                                    '| Authority | What is delegated, for how long, and '
                                                    'how is scope enforced? Does an authorization-required '
                                                    'state remain only a request until an external '
                                                    'decision grants a defined scope? |',
                                                    '| Schema | How are inputs, outputs, extensions, and '
                                                    'content types validated? |',
                                                    '| Lifecycle | How are tasks, requests, streams, '
                                                    'artifacts, cancellation, and completion represented? '
                                                    '|',
                                                    '| Failure | What happens on timeout, retry, '
                                                    'duplication, partial delivery, or version mismatch? |',
                                                    '| Security | Can untrusted content influence tools, '
                                                    'URLs, credentials, rendering, or another agent? |',
                                                    '| Revocation | How are credentials, capabilities, '
                                                    'tasks, and compromised endpoints disabled? |'],
         'agent-tool-action-boundary-review': ['| Field | Required evidence |',
                                               '| --- | --- |',
                                               '| Tool | Registered name, version, owner, and '
                                               'implementation |',
                                               '| Caller | Agent identity and authenticated product '
                                               'principal |',
                                               '| Arguments | Schema, validation, allowlists, ownership '
                                               'checks, and limits |',
                                               '| Data | Input and output classifications and tenant '
                                               'boundary |',
                                               '| Network | Allowed destination, redirect policy, DNS and '
                                               'address controls |',
                                               '| Effect | Read, compute, draft, external write, '
                                               'destructive, financial, publication, deployment, or trust '
                                               'decision |',
                                               '| Approval | Approver, exact bound arguments, expiration, '
                                               'and durable record |',
                                               '| Replay | Idempotency key, duplicate handling, retry, and '
                                               'cancellation |',
                                               '| Recovery | Rollback, compensation, partial failure, and '
                                               'emergency stop |',
                                               '| Evidence | Request, decision, execution, and readback '
                                               'audit records |'],
         'agentic-system-security-review': ['| Domain | Evidence and tests |',
                                            '| --- | --- |',
                                            '| Instructions | Priority rules, direct and indirect '
                                            'injection, conflict, and untrusted-content labeling |',
                                            '| Identity | User, tenant, agent, service, delegation, '
                                            'credential, and approval binding |',
                                            '| Tools | Registration, schema, least privilege, effects, '
                                            'network, replay, and audit |',
                                            '| Context and memory | Scope, provenance, freshness, '
                                            'poisoning, retention, deletion, and isolation |',
                                            '| Retrieval | Corpus authority, ACL filtering, poisoning, '
                                            'injection, and evidence support |',
                                            '| Delegation and protocols | Ownership, capability claims, '
                                            'trust zones, cancellation, and reconciliation |',
                                            '| Supply chain | Skills, prompts, plugins, models, '
                                            'dependencies, build provenance, and revocation |',
                                            '| Output | Escaping, active content, sensitive data, '
                                            'downstream execution, and user interpretation |',
                                            '| Resources | Cost, tokens, storage, network, retries, '
                                            'concurrency, and emergency limits |',
                                            '| Operations | Monitoring, incidents, audit evidence, '
                                            'revocation, rollback, and emergency stop |'],
         'context-reliability-review': ['| Status | Meaning |',
                                        '| --- | --- |',
                                        '| `RELIABLE` | Current evidence supports the assertion within its '
                                        'authority and permission scope. |',
                                        '| `QUALIFIED` | The assertion is usable only with an explicit '
                                        'limitation or narrower scope. |',
                                        '| `STALE` | Its freshness rule is violated or currentness cannot '
                                        'be established. |',
                                        '| `CONFLICTED` | Relevant sources disagree and no ratified '
                                        'resolution rule settles the conflict. |',
                                        '| `REVOKED` | An authorized event invalidated the assertion for '
                                        'the reviewed use. |',
                                        '| `UNVERIFIED` | The source, authority, or supporting evidence '
                                        'cannot be established. |'],
         'retrieval-grounding-quality-review': ['| Stage | Questions |',
                                                '| --- | --- |',
                                                '| Source | Is the source authorized, licensed, current, '
                                                'versioned, and eligible for this user and purpose? |',
                                                '| Ingestion | Were content, metadata, authority, time, '
                                                'access control, and deletion status preserved? |',
                                                '| Embedding | Can stored or exposed vectors reveal '
                                                'protected source content through inversion, '
                                                'reconstruction, or similarity access? |',
                                                '| Query | Does the case represent a real need, boundary, '
                                                'conflict, no-answer state, or attack? |',
                                                '| Retrieval | Were relevant sources found, ranked, '
                                                'filtered, and returned within limits? |',
                                                '| Claim | Is each material claim directly or partially '
                                                'supported, contradicted, or unsupported? |',
                                                '| Citation | Does the cited source support the nearby '
                                                'claim with correct date, unit, and context? |',
                                                '| Safety | Can document text, metadata, or a tool result '
                                                'change instructions, cross a tenant boundary, or trigger '
                                                'a tool? |',
                                                '| Behavior | Does retrieval preserve the intended '
                                                'correctness, relevance, safety, tone, and usefulness of '
                                                'the application? |',
                                                '| Recovery | Can the system abstain, ask, disclose '
                                                'conflict, correct a result, and revoke bad content? |']}
        for skill, rows in matrices.items():
            text = (ROOT / 'skills' / skill / 'SKILL.md').read_text()
            for row in rows:
                self.assertIn(row, text, skill)

    def test_profile_resolves_exact_members_and_rejects_unknown(self) -> None:
        names = export_selected.profile_skills('daily-engineering-experimental', 'codex')
        self.assertEqual(12, len(names))
        self.assertIn('gcp-data-engineering-profile', names)
        with self.assertRaisesRegex(ValueError, 'unknown profile'):
            export_selected.profile_skills('missing', 'codex')

    def test_cli_selection_is_mutually_exclusive(self) -> None:
        run = subprocess.run([sys.executable, str(ROOT / 'scripts/export_selected.py'), '--output', 'unused', '--client', 'codex', '--skill', 'claim-verification', '--profile', 'daily-engineering-experimental'], capture_output=True, text=True)
        self.assertNotEqual(0, run.returncode)
        self.assertIn('not allowed with argument', run.stderr)

    def test_selected_export_rejects_symlink_parent_before_writing(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw).resolve()
            (base / 'real').mkdir()
            (base / 'link').symlink_to(base / 'real', target_is_directory=True)
            with self.assertRaisesRegex(ValueError, 'symlink'):
                export_selected.export(base / 'link' / 'out', 'codex', ['claim-verification'])
            self.assertFalse((base / 'real' / 'out').exists())

    def fixture(self, base: Path) -> Path:
        source = base / 'source'
        source.mkdir()
        for relative in ('catalog/profiles.json', 'catalog/revocations.json', 'evals/daily-engineering/cases.json'):
            target = source / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)
        for name in export_selected.profile_skills('daily-engineering-experimental', 'codex'):
            shutil.copytree(ROOT / 'skills' / name, source / 'skills' / name)
        subprocess.run(['git', 'init', '-q', str(source)], check=True)
        subprocess.run(['git', '-C', str(source), 'add', '.'], check=True)
        subprocess.run(['git', '-C', str(source), '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'Synthetic fixture'], check=True)
        return source

    def test_reproducible_export_preserves_source_and_case_hashes(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw).resolve()
            source = self.fixture(base)
            a, b = base / 'a', base / 'b'
            export_trigger_evals.export(a, source=source)
            export_trigger_evals.export(b, source=source)
            def files(root: Path) -> dict[str, bytes]:
                return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob('*') if p.is_file()}
            self.assertEqual(files(a), files(b))
            receipt = json.loads((a / 'receipt.json').read_text())
            self.assertEqual('prepared_not_run', receipt['status'])
            plugin = json.loads((a / 'claude/.claude-plugin/plugin.json').read_text())
            self.assertEqual('Measured Studios', plugin['author']['name'])
            self.assertEqual(30, len(receipt['case_hashes']))
            self.assertEqual(12, len(receipt['skills']))
            for relative, digest in receipt['source_files'].items():
                self.assertEqual(hashlib.sha256((source / relative).read_bytes()).hexdigest(), digest)
            for relative, digest in receipt['files'].items():
                self.assertEqual(hashlib.sha256((a / relative).read_bytes()).hexdigest(), digest)
            for case in json.loads((source / export_trigger_evals.SUITE).read_text())['cases']:
                payload = (json.dumps(case, indent=2, sort_keys=True) + '\n').encode()
                self.assertEqual(hashlib.sha256(payload).hexdigest(), receipt['case_hashes'][case['id']])
            self.assertEqual(subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip(), receipt['source_commit'])
            cases = json.loads((a / 'codex/cases.json').read_text())['cases']
            self.assertEqual(24, sum(c['kind'] == 'positive' for c in cases))
            positive = next(c for c in cases if c['expected_skills'])
            grader = a / 'claude/evals' / positive['id'] / 'graders' / ('expect-' + positive['expected_skills'][0] + '.md')
            text = grader.read_text()
            self.assertIn('input_match:', text)
            pattern = export_trigger_evals.skill_pattern(positive['expected_skills'][0])
            self.assertIsNotNone(re.search(pattern, json.dumps({'skill': 'measured-daily-eval:' + positive['expected_skills'][0]})))
            self.assertIsNone(re.search(pattern, json.dumps({'skill': 'wrong-skill'})))
            negative = next(c for c in cases if c['kind'] == 'near_miss')
            negative_text = next((a / 'claude/evals' / negative['id'] / 'graders').glob('forbid-*.md')).read_text()
            self.assertIn('min: 0\nmax: 0', negative_text)
            self.assertNotIn('agents/openai.yaml', '\n'.join(files(a / 'claude')))
            with self.assertRaisesRegex(ValueError, 'new'):
                export_trigger_evals.export(a, source=source)

    def test_explicit_and_revoked_source_selections_are_rejected(self) -> None:
        for mode in ('explicit', 'revoked'):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as raw:
                base = Path(raw).resolve()
                source = self.fixture(base)
                if mode == 'explicit':
                    p = source / 'skills/claim-verification/SKILL.md'
                    p.write_text(p.read_text().replace('invocation: "implicit"', 'invocation: "explicit"'))
                else:
                    p = source / 'catalog/revocations.json'
                    value = json.loads(p.read_text())
                    value['entries'].append({'skill': 'claim-verification', 'revoked_on': '2026-10-20', 'reason': 'Synthetic revocation', 'replacement': 'none', 'security_immediate': True})
                    p.write_text(json.dumps(value))
                subprocess.run(['git', '-C', str(source), 'add', '.'], check=True)
                subprocess.run(['git', '-C', str(source), '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'Change policy'], check=True)
                with self.assertRaisesRegex(ValueError, 'explicit-only|revoked'):
                    export_trigger_evals.export(base / 'out', source=source)
                self.assertFalse((base / 'out').exists())

    def test_dirty_source_is_rejected_before_output(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw).resolve()
            source = self.fixture(base)
            (source / 'untracked.txt').write_text('uncommitted')
            with self.assertRaisesRegex(ValueError, 'clean'):
                export_trigger_evals.export(base / 'output', source=source)
            self.assertFalse((base / 'output').exists())

    def test_unknown_selection_and_path_traversal_are_rejected(self) -> None:
        document = json.loads((ROOT / 'evals/daily-engineering/cases.json').read_text())
        names = export_selected.profile_skills('daily-engineering-experimental', 'codex')
        document['cases'][0]['expected_skills'] = ['missing']
        with self.assertRaisesRegex(ValueError, 'selection'):
            export_trigger_evals.validate_suite(document, names)
        document = json.loads((ROOT / 'evals/daily-engineering/cases.json').read_text())
        document['cases'][0]['id'] = '../escape'
        with self.assertRaisesRegex(ValueError, 'case id'):
            export_trigger_evals.validate_suite(document, names)

    def test_invalid_suite_and_write_failure_leave_no_export(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw).resolve()
            source = self.fixture(base)
            with patch.object(export_trigger_evals, 'validate_suite', side_effect=ValueError('invalid suite')):
                with self.assertRaisesRegex(ValueError, 'invalid suite'):
                    export_trigger_evals.export(base / 'out', source=source)
            self.assertFalse((base / 'out').exists())
            with patch.object(export_trigger_evals, 'write_files', side_effect=OSError('disk full')):
                with self.assertRaisesRegex(OSError, 'disk full'):
                    export_trigger_evals.export(base / 'out', source=source)
            self.assertFalse((base / 'out').exists())


if __name__ == '__main__':
    unittest.main()
