#!/usr/bin/env python3
"""Offline integrity checker, materializer, structural linter, and summary reporter for review-comparison-v1.

This script never executes model calls, client subprocesses, or network requests.
Structural receipt linting checks schema, hashes, evidence links, and 5-dimension
state invariants only; it never claims to verify finding truth or review quality.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / 'evals' / 'review-comparison-v1'
MANIFEST = KIT / 'study.json'

ARMS = ('ordinary_baseline', 'structured_request', 'structured_plus_skills')
COVERAGE_VALUES = frozenset({'examined', 'skipped', 'blocked', 'excluded'})
CLAIM_VALUES = frozenset({'supported', 'cleared', 'unresolved'})
DISPOSITION_VALUES = frozenset({'accept', 'reject', 'defer', 'clarify', 'already addressed', 'pending'})
COMPLETION_VALUES = frozenset({'complete', 'complete_with_gaps', 'budget_exhausted', 'blocked'})
ADJUDICATION_STATUSES = frozenset({'adjudicated', 'disputed', 'pending'})
RUN_STATUSES = frozenset({'completed', 'blocked', 'failed'})


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def canonical_json_bytes(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True) + '\n').encode('ascii')


def load_manifest(path: Path = MANIFEST) -> dict[str, Any]:
    return json.loads(path.read_text(encoding='utf-8'))  # type: ignore[no-any-return]


def load_case(case_id: str, kit: Path = KIT) -> dict[str, Any]:
    case_path = kit / 'cases' / f'{case_id}.json'
    return json.loads(case_path.read_text(encoding='utf-8'))  # type: ignore[no-any-return]


def materialized_payload(case_data: dict[str, Any]) -> dict[str, Any]:
    """Return only the client-visible snapshot; strip oracle and disconfirmation notes."""
    return {
        'id': case_data['id'],
        'requirement': case_data['requirement'],
        'diff': case_data['diff'],
        'head_files': case_data['head_files'],
    }


def workspace_hash(case_data: dict[str, Any]) -> str:
    return sha256_bytes(canonical_json_bytes(materialized_payload(case_data)))


def check_kit(kit: Path = KIT) -> list[str]:
    """Deterministically verify study manifest, case schemas, hashes, and ASCII bounds."""
    errors: list[str] = []
    manifest_path = kit / 'study.json'
    if not manifest_path.is_file():
        return [f'missing review-comparison manifest: {manifest_path}']
    raw_manifest = manifest_path.read_text(encoding='utf-8')
    if not raw_manifest.isascii():
        errors.append('review-comparison manifest must be ASCII')
    manifest: dict[str, Any] = json.loads(raw_manifest)
    if manifest.get('format_version') != 1:
        errors.append('review-comparison format_version must be 1')
    if manifest.get('study_id') != 'review-comparison-2026-11-v1':
        errors.append('unexpected review-comparison study_id')
    if manifest.get('execution_authorized') is not False:
        errors.append('review-comparison execution_authorized must remain false in committed manifest')
    if tuple(manifest.get('arms', [])) != ARMS:
        errors.append('review-comparison arms must match ordinary_baseline, structured_request, structured_plus_skills')
    prompts = manifest.get('arm_prompts', {})
    if not isinstance(prompts, dict) or set(prompts) != set(ARMS):
        errors.append('review-comparison arm_prompts must cover every arm')
    else:
        for arm, text in prompts.items():
            if not isinstance(text, str) or not text.strip() or not text.isascii():
                errors.append(f'review-comparison arm_prompt invalid: {arm}')
    cases = manifest.get('cases', [])
    if not isinstance(cases, list) or len(cases) < 6:
        return errors + ['review-comparison manifest must declare at least 6 cases']
    seen_ids: set[str] = set()
    declared_files: set[str] = set()
    for entry in cases:
        if not isinstance(entry, dict):
            errors.append('review-comparison case entry must be an object')
            continue
        cid = entry.get('id')
        if not isinstance(cid, str) or not cid:
            errors.append('review-comparison case missing id')
            continue
        if cid in seen_ids:
            errors.append(f'duplicate review-comparison case id: {cid}')
            continue
        seen_ids.add(cid)
        case_path = kit / 'cases' / f'{cid}.json'
        declared_files.add(case_path.name)
        if not case_path.is_file():
            errors.append(f'missing review-comparison case file: {case_path.name}')
            continue
        raw_case = case_path.read_bytes()
        if not raw_case.decode('utf-8').isascii():
            errors.append(f'non-ASCII review-comparison case: {cid}')
        if sha256_bytes(raw_case) != entry.get('case_sha256'):
            errors.append(f'case_sha256 drift for {cid}')
        case_data: dict[str, Any] = json.loads(raw_case.decode('utf-8'))
        for field in ('id', 'category', 'requirement', 'diff', 'head_files', 'oracle', 'disconfirmation_notes'):
            if field not in case_data:
                errors.append(f'{cid}: missing required field {field}')
        if case_data.get('id') != cid:
            errors.append(f'{cid}: case id mismatch')
        head_files = case_data.get('head_files')
        if not isinstance(head_files, dict) or not head_files:
            errors.append(f'{cid}: head_files must be a non-empty mapping')
        else:
            for rel_path, content in head_files.items():
                if not isinstance(rel_path, str) or rel_path.startswith('/') or '..' in Path(rel_path).parts:
                    errors.append(f'{cid}: unsafe head_files path {rel_path}')
                if not isinstance(content, str):
                    errors.append(f'{cid}: head_files content must be string for {rel_path}')
            if workspace_hash(case_data) != entry.get('workspace_sha256'):
                errors.append(f'workspace_sha256 drift for {cid}')
        oracle = case_data.get('oracle')
        if not isinstance(oracle, dict) or not isinstance(oracle.get('has_planted_defect'), bool):
            errors.append(f'{cid}: oracle.has_planted_defect must be boolean')
    cases_dir = kit / 'cases'
    if cases_dir.is_dir():
        on_disk = {p.name for p in cases_dir.glob('*.json')}
        extra = sorted(on_disk - declared_files)
        for name in extra:
            errors.append(f'undeclared review-comparison case file: {name}')
    return errors


def materialize_case(case_id: str, out_dir: Path, kit: Path = KIT) -> str:
    """Write only the client-visible fixture files (no oracle or disconfirmation notes)."""
    manifest = load_manifest(kit / 'study.json')
    known = {entry['id'] for entry in manifest['cases']}
    if case_id not in known:
        raise ValueError(f'unknown case id: {case_id}')
    if out_dir.exists() and any(out_dir.iterdir()):
        raise ValueError(f'output directory must be empty or nonexistent: {out_dir}')
    case_data = load_case(case_id, kit)
    out_dir.mkdir(parents=True, exist_ok=True)
    for rel_path, content in case_data['head_files'].items():
        if rel_path.startswith('/') or '..' in Path(rel_path).parts:
            raise ValueError(f'unsafe relative path: {rel_path}')
        target = out_dir / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding='utf-8')
    (out_dir / 'REQUIREMENT.md').write_text(case_data['requirement'].rstrip() + '\n', encoding='utf-8')
    (out_dir / 'CHANGE.diff').write_text(case_data['diff'].rstrip() + '\n', encoding='utf-8')
    return workspace_hash(case_data)


def lint_receipts(receipts: list[dict[str, Any]], kit: Path = KIT) -> list[str]:
    """Structural completeness lint ONLY. Never establishes finding truth or quality."""
    if not isinstance(receipts, list) or not receipts:
        return ['receipts must be a non-empty JSON list']
    manifest = load_manifest(kit / 'study.json')
    case_index = {entry['id']: entry for entry in manifest['cases']}
    errors: list[str] = []
    seen_cells: set[tuple[str, str, int]] = set()
    synthetic_flags: set[bool] = set()
    for idx, rec in enumerate(receipts):
        prefix = f'receipt[{idx}]'
        if not isinstance(rec, dict):
            errors.append(f'{prefix}: must be a JSON object')
            continue
        if rec.get('study_id') != manifest['study_id']:
            errors.append(f'{prefix}: study_id mismatch')
        cid = rec.get('case_id')
        arm = rec.get('arm')
        rep = rec.get('repetition', 1)
        if not isinstance(cid, str) or cid not in case_index:
            errors.append(f'{prefix}: unknown case_id {cid!r}')
            continue
        if arm not in ARMS:
            errors.append(f'{prefix}: invalid arm {arm!r}')
        if not isinstance(rep, int) or rep < 1:
            errors.append(f'{prefix}: repetition must be positive integer')
        else:
            cell = (cid, str(arm), rep)
            if cell in seen_cells:
                errors.append(f'{prefix}: duplicate cell {cell}')
            seen_cells.add(cell)
        if rec.get('workspace_sha256') != case_index[cid]['workspace_sha256']:
            errors.append(f'{prefix}: workspace_sha256 mismatch for {cid}')
        is_synthetic = rec.get('synthetic')
        if not isinstance(is_synthetic, bool):
            errors.append(f'{prefix}: boolean synthetic flag is required')
        else:
            synthetic_flags.add(is_synthetic)
        if rec.get('run_status') not in RUN_STATUSES:
            errors.append(f'{prefix}: invalid run_status')
        if not isinstance(rec.get('skill_loaded'), bool):
            errors.append(f'{prefix}: boolean skill_loaded attestation is required')
        elif arm in ('ordinary_baseline', 'structured_request') and rec['skill_loaded'] is True:
            errors.append(f'{prefix}: contaminated no-skill arm {arm} reported skill_loaded=true')
        for metric in ('elapsed_seconds', 'turns', 'input_tokens', 'output_tokens', 'reported_cost_usd'):
            val = rec.get(metric)
            if not isinstance(val, (int, float)) or isinstance(val, bool) or val < 0:
                errors.append(f'{prefix}: non-negative numeric {metric} is required')
        items = rec.get('items')
        if not isinstance(items, list):
            errors.append(f'{prefix}: items list is required')
            continue
        for j, item in enumerate(items):
            iprefix = f'{prefix}.items[{j}]'
            if not isinstance(item, dict):
                errors.append(f'{iprefix}: must be object')
                continue
            cov = item.get('investigation_coverage')
            claim = item.get('claim_assessment')
            disp = item.get('disposition')
            comp = item.get('completion')
            if cov not in COVERAGE_VALUES:
                errors.append(f'{iprefix}: invalid investigation_coverage {cov!r}')
            if claim not in CLAIM_VALUES:
                errors.append(f'{iprefix}: invalid claim_assessment {claim!r}')
            if disp not in DISPOSITION_VALUES:
                errors.append(f'{iprefix}: invalid disposition {disp!r}')
            if comp not in COMPLETION_VALUES:
                errors.append(f'{iprefix}: invalid completion {comp!r}')
            # Core invariant from BugHunter closure audit: skipped/blocked/excluded can never become cleared.
            if cov in ('skipped', 'blocked', 'excluded') and claim == 'cleared':
                errors.append(
                    f'{iprefix}: non-examined coverage ({cov}) cannot be recorded as claim_assessment=cleared'
                )
            evidence = item.get('evidence_refs')
            if claim in ('supported', 'cleared') and (
                not isinstance(evidence, list) or not evidence or not all(isinstance(e, str) and e.strip() for e in evidence)
            ):
                errors.append(f'{iprefix}: {claim} assessment requires non-empty evidence_refs')
            if not isinstance(item.get('verification'), str) or not item['verification'].strip():
                errors.append(f'{iprefix}: verification summary string is required')
    if len(synthetic_flags) > 1:
        errors.append('receipts cannot mix synthetic and observed records')
    return errors


def summarize_receipts(receipts: list[dict[str, Any]], kit: Path = KIT) -> dict[str, Any]:
    """Summarize adjudicated receipts across the six preserved tradeoff measures."""
    lint_errors = lint_receipts(receipts, kit)
    if lint_errors:
        raise ValueError('structural lint failed: ' + '; '.join(lint_errors))
    summary: dict[str, Any] = {
        'synthetic': receipts[0]['synthetic'],
        'note': (
            'Synthetic test summary only; not observed model evidence.'
            if receipts[0]['synthetic']
            else 'Observed adjudicated summary; counts, effort, cost, and gaps remain separate.'
        ),
        'arms': {},
    }
    for arm in ARMS:
        rows = [r for r in receipts if r['arm'] == arm]
        adjudicated = [
            r for r in rows
            if isinstance(r.get('adjudication'), dict) and r['adjudication'].get('status') == 'adjudicated'
        ]
        disputed = [
            r for r in rows
            if isinstance(r.get('adjudication'), dict) and r['adjudication'].get('status') == 'disputed'
        ]
        pending = len(rows) - len(adjudicated) - len(disputed)
        valid_findings = sum(int(r['adjudication']['valid_material_findings']) for r in adjudicated)
        false_positives = sum(int(r['adjudication']['false_positives']) for r in adjudicated)
        missed_defects = sum(int(r['adjudication']['missed_known_defects']) for r in adjudicated)
        human_minutes = round(sum(float(r['adjudication']['human_verification_minutes']) for r in adjudicated), 2)
        scope_violations = sum(int(r['adjudication']['scope_violations']) for r in adjudicated)
        uncertainty_preserved = sum(
            1 for r in adjudicated if bool(r['adjudication'].get('uncertainty_reported_accurately'))
        )
        summary['arms'][arm] = {
            'runs_total': len(rows),
            'runs_completed': sum(1 for r in rows if r['run_status'] == 'completed'),
            'runs_blocked': sum(1 for r in rows if r['run_status'] == 'blocked'),
            'runs_failed': sum(1 for r in rows if r['run_status'] == 'failed'),
            'skill_loaded_count': sum(1 for r in rows if r['skill_loaded']),
            'adjudicated_count': len(adjudicated),
            'disputed_count': len(disputed),
            'pending_adjudication_count': pending,
            'valid_material_findings': valid_findings,
            'false_positives_and_unsupported_severity': false_positives,
            'missed_known_defects': missed_defects,
            'human_verification_minutes': human_minutes,
            'uncertainty_reported_accurately_count': uncertainty_preserved,
            'scope_violations': scope_violations,
            'total_elapsed_seconds': round(sum(float(r['elapsed_seconds']) for r in rows), 2),
            'total_turns': sum(int(r['turns']) for r in rows),
            'total_reported_cost_usd': round(sum(float(r['reported_cost_usd']) for r in rows), 4),
        }
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--check', action='store_true', help='Verify manifest and case fixture hashes')
    group.add_argument('--materialize', nargs=2, metavar=('CASE_ID', 'OUT_DIR'), help='Write client-visible case snapshot')
    group.add_argument('--lint-receipts', metavar='RECEIPTS_JSON', help='Structural completeness lint only')
    group.add_argument('--summarize', metavar='RECEIPTS_JSON', help='Summarize adjudicated receipts')
    args = parser.parse_args()
    if args.check:
        errors = check_kit()
        if errors:
            print('\n'.join(f'ERROR: {e}' for e in errors), file=sys.stderr)
            return 1
        print('Review comparison kit manifest and fixture hashes passed.')
        return 0
    if args.materialize:
        digest = materialize_case(args.materialize[0], Path(args.materialize[1]))
        print(f'Materialized client-visible snapshot (oracle omitted); workspace_sha256={digest}')
        return 0
    if args.lint_receipts:
        receipts = json.loads(Path(args.lint_receipts).read_text(encoding='utf-8'))
        errors = lint_receipts(receipts)
        if errors:
            print('\n'.join(f'ERROR: {e}' for e in errors), file=sys.stderr)
            return 1
        print('Structural completeness check passed; this check does not verify finding truth or review quality.')
        return 0
    receipts = json.loads(Path(args.summarize).read_text(encoding='utf-8'))
    print(json.dumps(summarize_receipts(receipts), indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
