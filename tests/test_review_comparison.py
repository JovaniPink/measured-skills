"""Unit tests for the compact 3-arm review comparison kit and offline linter."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from typing import Any
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import review_comparison as rc  # noqa: E402


def sample_receipt(
    *,
    case_id: str = 'rc-01-missing-tenant-scope',
    arm: str = 'structured_request',
    synthetic: bool = True,
    skill_loaded: bool = False,
    coverage: str = 'examined',
    claim: str = 'supported',
    adjudication_status: str = 'adjudicated',
) -> dict[str, Any]:
    manifest = rc.load_manifest()
    entry = next(c for c in manifest['cases'] if c['id'] == case_id)
    return {
        'study_id': manifest['study_id'],
        'case_id': case_id,
        'arm': arm,
        'repetition': 1,
        'workspace_sha256': entry['workspace_sha256'],
        'synthetic': synthetic,
        'run_status': 'completed',
        'skill_loaded': skill_loaded,
        'elapsed_seconds': 12.5,
        'turns': 3,
        'input_tokens': 1200,
        'output_tokens': 350,
        'reported_cost_usd': 0.015,
        'items': [
            {
                'id': 'F-1',
                'investigation_coverage': coverage,
                'claim_assessment': claim,
                'disposition': 'pending',
                'verification': 'Static inspection of app/handlers.py and app/store.py',
                'completion': 'complete',
                'evidence_refs': ['app/handlers.py:2', 'app/store.py:5'],
            }
        ],
        'adjudication': {
            'status': adjudication_status,
            'valid_material_findings': 1 if claim == 'supported' else 0,
            'false_positives': 0,
            'missed_known_defects': 0,
            'human_verification_minutes': 2.5,
            'uncertainty_reported_accurately': True,
            'scope_violations': 0,
        },
    }


class ReviewComparisonTests(unittest.TestCase):
    def test_committed_kit_passes_integrity_check(self) -> None:
        self.assertEqual([], rc.check_kit())

    def test_tampered_case_hash_fails_check(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            kit = Path(tmp) / 'kit'
            shutil.copytree(rc.KIT, kit)
            case_file = kit / 'cases' / 'rc-01-missing-tenant-scope.json'
            case_file.write_text(case_file.read_text(encoding='utf-8') + '\n', encoding='utf-8')
            errors = rc.check_kit(kit)
            self.assertTrue(any('case_sha256 drift' in e for e in errors))

    def test_materialized_workspace_excludes_oracle_and_disconfirmation_notes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'rc-02'
            digest = rc.materialize_case('rc-02-auth-enforced-below', out)
            manifest = rc.load_manifest()
            expected = next(c['workspace_sha256'] for c in manifest['cases'] if c['id'] == 'rc-02-auth-enforced-below')
            self.assertEqual(expected, digest)
            self.assertTrue((out / 'REQUIREMENT.md').is_file())
            self.assertTrue((out / 'CHANGE.diff').is_file())
            self.assertTrue((out / 'app' / 'repo.py').is_file())
            combined = '\n'.join(p.read_text(encoding='utf-8') for p in out.rglob('*') if p.is_file())
            self.assertNotIn('has_planted_defect', combined)
            self.assertNotIn('disconfirmation_notes', combined)

    def test_linter_rejects_skipped_or_blocked_marked_as_cleared(self) -> None:
        bad_skipped = sample_receipt(coverage='skipped', claim='cleared')
        bad_blocked = sample_receipt(coverage='blocked', claim='cleared')
        for bad in (bad_skipped, bad_blocked):
            errors = rc.lint_receipts([bad])
            self.assertTrue(any('cannot be recorded as claim_assessment=cleared' in e for e in errors))

    def test_linter_rejects_contaminated_baseline_and_mixed_synthetic_flags(self) -> None:
        contaminated = sample_receipt(arm='ordinary_baseline', skill_loaded=True)
        self.assertTrue(any('contaminated no-skill arm' in e for e in rc.lint_receipts([contaminated])))
        mixed = [
            sample_receipt(case_id='rc-01-missing-tenant-scope', synthetic=True),
            sample_receipt(case_id='rc-02-auth-enforced-below', synthetic=False),
        ]
        self.assertTrue(any('cannot mix synthetic and observed' in e for e in rc.lint_receipts(mixed)))

    def test_cli_lint_message_explicitly_disclaims_semantic_verification(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'receipts.json'
            path.write_text(json.dumps([sample_receipt()]), encoding='utf-8')
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts' / 'review_comparison.py'), '--lint-receipts', str(path)],
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertIn('does not verify finding truth or review quality', result.stdout)

    def test_summary_preserves_failed_activation_disputed_rows_and_tradeoffs(self) -> None:
        r_base = sample_receipt(arm='ordinary_baseline', skill_loaded=False)
        r_struct = sample_receipt(arm='structured_request', skill_loaded=False)
        r_skill_unloaded = sample_receipt(
            case_id='rc-01-missing-tenant-scope',
            arm='structured_plus_skills',
            skill_loaded=False,
        )
        r_skill_disputed = copy.deepcopy(
            sample_receipt(
                case_id='rc-08-missing-store-contract',
                arm='structured_plus_skills',
                skill_loaded=True,
                coverage='blocked',
                claim='unresolved',
                adjudication_status='disputed',
            )
        )
        r_skill_disputed['items'][0]['evidence_refs'] = []
        summary = rc.summarize_receipts([r_base, r_struct, r_skill_unloaded, r_skill_disputed])
        self.assertTrue(summary['synthetic'])
        skill_arm = summary['arms']['structured_plus_skills']
        self.assertEqual(2, skill_arm['runs_total'])
        self.assertEqual(1, skill_arm['skill_loaded_count'])
        self.assertEqual(1, skill_arm['adjudicated_count'])
        self.assertEqual(1, skill_arm['disputed_count'])

    def test_linter_requires_complete_adjudicated_grades(self) -> None:
        missing = sample_receipt()
        del missing['adjudication']['valid_material_findings']
        errors = rc.lint_receipts([missing])
        self.assertTrue(any('adjudication.valid_material_findings' in e for e in errors), errors)
        with self.assertRaises(ValueError):
            rc.summarize_receipts([missing])

    def test_linter_rejects_negative_or_mistyped_adjudication_values(self) -> None:
        cases = {
            'false_positives': -1,
            'scope_violations': 1.5,
            'missed_known_defects': True,
            'human_verification_minutes': -2.0,
            'uncertainty_reported_accurately': 'false',
        }
        for field, value in cases.items():
            receipt = sample_receipt()
            receipt['adjudication'][field] = value
            errors = rc.lint_receipts([receipt])
            self.assertTrue(any(f'adjudication.{field}' in e for e in errors), (field, errors))
        infinite = sample_receipt()
        infinite['adjudication']['human_verification_minutes'] = float('inf')
        self.assertTrue(any('human_verification_minutes' in e for e in rc.lint_receipts([infinite])))

    def test_linter_rejects_unknown_adjudication_status_or_shape(self) -> None:
        unknown = sample_receipt(adjudication_status='graded')
        self.assertTrue(any('adjudication.status' in e for e in rc.lint_receipts([unknown])))
        not_object = sample_receipt()
        not_object['adjudication'] = 'adjudicated'
        self.assertTrue(any('adjudication must be' in e for e in rc.lint_receipts([not_object])))

    def test_pending_and_disputed_records_need_no_grades(self) -> None:
        absent = sample_receipt(arm='ordinary_baseline')
        del absent['adjudication']
        pending = sample_receipt(arm='structured_request', adjudication_status='pending')
        disputed = sample_receipt(arm='structured_plus_skills', adjudication_status='disputed')
        for record in (pending, disputed):
            for field in rc.ADJUDICATION_COUNT_FIELDS + ('human_verification_minutes', 'uncertainty_reported_accurately'):
                del record['adjudication'][field]
        self.assertEqual([], rc.lint_receipts([absent, pending, disputed]))
        summary = rc.summarize_receipts([absent, pending, disputed])
        self.assertEqual(1, summary['arms']['ordinary_baseline']['pending_adjudication_count'])
        self.assertEqual(1, summary['arms']['structured_request']['pending_adjudication_count'])
        self.assertEqual(1, summary['arms']['structured_plus_skills']['disputed_count'])

    def test_false_uncertainty_flag_is_not_counted(self) -> None:
        receipt = sample_receipt()
        receipt['adjudication']['uncertainty_reported_accurately'] = False
        summary = rc.summarize_receipts([receipt])
        self.assertEqual(0, summary['arms']['structured_request']['uncertainty_reported_accurately_count'])

    def test_summary_keeps_token_usage_separate_from_cost(self) -> None:
        first = sample_receipt(case_id='rc-01-missing-tenant-scope')
        second = sample_receipt(case_id='rc-02-auth-enforced-below')
        second['input_tokens'] = 800
        second['output_tokens'] = 150
        arm = rc.summarize_receipts([first, second])['arms']['structured_request']
        self.assertEqual(2000, arm['total_input_tokens'])
        self.assertEqual(500, arm['total_output_tokens'])
        self.assertEqual(0.03, arm['total_reported_cost_usd'])

    def test_linter_requires_integer_token_and_turn_counts(self) -> None:
        for metric in ('input_tokens', 'output_tokens', 'turns'):
            receipt = sample_receipt()
            receipt[metric] = 12.5
            self.assertTrue(any(metric in e for e in rc.lint_receipts([receipt])), metric)

    def test_cleared_retry_case_runs_under_its_stated_sqlite_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'rc-03'
            rc.materialize_case('rc-03-idempotent-retry', out)
            script = (
                'import sqlite3, sys\n'
                'sys.path.insert(0, sys.argv[1])\n'
                'from app.exports import create_export\n'
                'conn = sqlite3.connect(":memory:")\n'
                'conn.executescript(open(sys.argv[1] + "/app/schema.sql").read())\n'
                'first = create_export(conn, "t1", "r1", "{}")\n'
                'retry = create_export(conn, "t1", "r1", "{}")\n'
                'rows = conn.execute("SELECT COUNT(*) FROM exports").fetchone()[0]\n'
                'print(first is not None, retry is None, rows)\n'
            )
            result = subprocess.run(
                [sys.executable, '-I', '-c', script, str(out)],
                capture_output=True,
                text=True,
                check=True,
            )
            # One row survives the retry; the conflicting retry returns no row,
            # which is the open question the case preserves.
            self.assertEqual('True True 1', result.stdout.strip())


if __name__ == '__main__':
    unittest.main()
