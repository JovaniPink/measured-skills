"""Bind deliberate canonical edits to the preserved naming-only checkpoint."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any

BASELINE = '62af7d15431c9b3e653523888cd574b7319d7171'
RECORD = 'docs/audits/workflow-depth-2026-10-28.json'


def digest(value: bytes | None) -> str | None:
    return hashlib.sha256(value).hexdigest() if value is not None else None


def validate(before: dict[str, bytes], after: dict[str, bytes], record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if record.get('format_version') != 1 or record.get('baseline_revision') != BASELINE:
        errors.append('canonical delta must retain the exact identity-migration checkpoint')
    if record.get('new_maintainer_acceptance') is not False:
        errors.append('technical delta does not extend maintainer acceptance')
    rows = record.get('changes')
    if not isinstance(rows, dict):
        return errors + ['canonical changes must be path-keyed records']
    changed = {p for p in before.keys() | after.keys() if before.get(p) != after.get(p)}
    if set(rows) != changed:
        errors.append('canonical delta inventory differs from actual added, removed, or changed files')
    for path, row in rows.items():
        if path not in changed or not isinstance(row, dict):
            errors.append(f'{path}: unexpected or invalid canonical delta')
            continue
        if row.get('before_sha256') != digest(before.get(path)) or row.get('after_sha256') != digest(after.get(path)):
            errors.append(f'{path}: canonical delta hash mismatch')
        if not isinstance(row.get('review_reason'), str) or not row['review_reason'].strip():
            errors.append(f'{path}: missing technical review rationale')
    return errors


def check(root: Path) -> list[str]:
    # The derived chooser index is covered by discovery regeneration, not hand-authored deltas.
    excluded = 'skills/choose-workflow/references/workflow-index.md'
    def git(*args: str) -> bytes:
        return subprocess.run(['git', *args], cwd=root, check=True, capture_output=True).stdout
    try:
        git('merge-base', '--is-ancestor', BASELINE, 'HEAD')
        paths = git('ls-tree', '-r', '--name-only', BASELINE, '--', 'skills').decode().splitlines()
        before = {p: git('show', BASELINE + ':' + p) for p in paths if p != excluded}
        after = {p.relative_to(root).as_posix(): p.read_bytes() for p in (root / 'skills').rglob('*')
                 if p.is_file() and p.relative_to(root).as_posix() != excluded}
        record = json.loads((root / RECORD).read_text())
        if not isinstance(record, dict):
            return ['canonical delta must be an object']
        return validate(before, after, record)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        return [f'canonical delta unavailable: {error}']
