#!/usr/bin/env python3
"""Prepare portable trigger cases and a Claude eval plugin; never run a client."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
from typing import Any

from cataloglib import ROOT, VERSION, read_skill_metadata, license_notice
from export_selected import check_destination, profile_skills

PROFILE = 'daily-engineering-experimental'
SUITE = 'evals/daily-engineering/cases.json'


def sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def encoded(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode('utf-8')


def git(source: Path, *args: str) -> bytes:
    run = subprocess.run(['git', '-C', str(source), *args], capture_output=True, check=False)
    if run.returncode:
        raise ValueError(run.stderr.decode(errors='replace').strip() or 'Git inspection failed')
    return run.stdout


def skill_pattern(name: str) -> str:
    # Match the entire skill value, with an optional native plugin namespace.
    return r'"skill"\s*:\s*"(?:[\w-]+:)?' + re.escape(name) + r'"'


def validate_suite(document: Any, names: list[str]) -> None:
    if not isinstance(document, dict) or set(document) != {'format_version', 'profile', 'status', 'cases'}:
        raise ValueError('unsupported suite fields')
    if type(document['format_version']) is not int or document['format_version'] != 1 or document['profile'] != PROFILE or document['status'] != 'prepared_not_run':
        raise ValueError('unsupported suite identity or status')
    cases = document['cases']
    if not isinstance(cases, list) or len(cases) != 30:
        raise ValueError('suite requires 30 cases')
    ids: set[str] = set()
    positives: Counter[str] = Counter()
    kinds: Counter[str] = Counter()
    for case in cases:
        if not isinstance(case, dict) or set(case) != {'id', 'kind', 'prompt', 'expected_skills', 'forbidden_skills', 'output_rubric'}:
            raise ValueError('unsupported case fields')
        case_id = case['id']
        if not isinstance(case_id, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', case_id) or case_id in ids:
            raise ValueError('invalid or duplicate case id')
        ids.add(case_id)
        if case['kind'] not in ('positive', 'near_miss', 'safety'):
            raise ValueError('unsupported case kind')
        kinds[case['kind']] += 1
        for key in ('expected_skills', 'forbidden_skills'):
            value = case[key]
            if not isinstance(value, list) or any(not isinstance(n, str) or n not in names for n in value) or len(set(value)) != len(value):
                raise ValueError('unknown or duplicate selection')
        if set(case['expected_skills']) & set(case['forbidden_skills']):
            raise ValueError('contradictory selection')
        if not isinstance(case['prompt'], str) or not case['prompt'].strip() or not case['prompt'].isascii():
            raise ValueError('prompt must be nonempty ASCII')
        rubric = case['output_rubric']
        if not isinstance(rubric, list) or not rubric or any(not isinstance(r, str) or not r.strip() or not r.isascii() for r in rubric):
            raise ValueError('output rubric is required')
        if any(name in case['prompt'] for name in names):
            raise ValueError('implicit prompt must not name a selected skill')
        if case['kind'] == 'positive':
            if len(case['expected_skills']) != 1:
                raise ValueError('positive case requires one target')
            positives.update(case['expected_skills'])
        if case['kind'] == 'near_miss' and (case['expected_skills'] or set(case['forbidden_skills']) != set(names)):
            raise ValueError('near miss must forbid the complete profile')
    if kinds != Counter(positive=24, near_miss=3, safety=3) or positives != Counter({n: 2 for n in names}):
        raise ValueError('suite coverage does not match the daily profile')


def source_files(source: Path, names: list[str]) -> dict[str, bytes]:
    license_notice(source)
    paths = ['LICENSE', 'catalog/profiles.json', 'catalog/revocations.json', SUITE]
    revoked = json.loads((source / 'catalog/revocations.json').read_text())['entries']
    for name in names:
        base = source / 'skills' / name
        if base.is_symlink() or not base.is_dir():
            raise ValueError('missing or symlinked skill source')
        metadata = read_skill_metadata(base)
        if metadata['invocation'] != 'implicit':
            raise ValueError('explicit-only skills are excluded from the evaluation plugin')
        if any(row.get('skill') == name or row.get('plugin') == metadata['plugin'] for row in revoked):
            raise ValueError('revoked selection')
        for path in sorted(base.rglob('*')):
            if path.is_symlink():
                raise ValueError('source symlinks are forbidden')
            if path.is_file():
                rel = path.relative_to(base).as_posix()
                if rel not in ('SKILL.md', 'agents/openai.yaml') and not (rel.startswith('references/') and path.suffix in ('.md', '.json', '.txt')):
                    raise ValueError('unexpected source payload')
                paths.append(path.relative_to(source).as_posix())
    files: dict[str, bytes] = {}
    for relative in paths:
        path = source / relative
        if path.is_symlink() or not path.is_file():
            raise ValueError('missing or symlinked source file')
        listing = git(source, 'ls-tree', 'HEAD', '--', relative).decode()
        if not listing.startswith('100644 blob '):
            raise ValueError('source files must be committed regular non-executable files')
        payload = path.read_bytes()
        if payload != git(source, 'show', f'HEAD:{relative}'):
            raise ValueError('source differs from committed bytes')
        files[relative] = payload
    return files


def write_files(output: Path, files: dict[str, bytes]) -> None:
    for relative, payload in sorted(files.items()):
        path = output / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)


def export(output: Path, source: Path = ROOT) -> None:
    check_destination(output)
    # Prevent the export itself from contaminating the source checkout.
    source = source.resolve()
    if output.resolve().is_relative_to(source):
        raise ValueError('evaluation output must be outside the source checkout')
    revision = git(source, 'rev-parse', 'HEAD').decode().strip()
    if git(source, 'status', '--porcelain'):
        raise ValueError('evaluation export requires a clean committed source checkout')
    names = profile_skills(PROFILE, 'codex', root=source)
    files = source_files(source, names)
    document = json.loads(files[SUITE])
    validate_suite(document, names)
    rendered: dict[str, bytes] = {}
    for relative, payload in files.items():
        if relative.startswith('skills/'):
            rendered['codex/' + relative] = payload
            if '/agents/' not in relative:
                rendered['claude/' + relative] = payload
    for client in ('codex', 'claude'):
        rendered[client + '/LICENSE'] = files['LICENSE']
        for name in names:
            rendered[client + '/skills/' + name + '/LICENSE'] = files['LICENSE']
    rendered['codex/cases.json'] = encoded(document)
    rendered['claude/.claude-plugin/plugin.json'] = encoded({'name': 'measured-daily-eval', 'version': VERSION, 'author': {'name': 'Measured Studios'}, 'description': 'Temporary offline daily-profile evaluation package; no observed results.'})
    for case in document['cases']:
        base = 'claude/evals/' + case['id'] + '/'
        prompt_policy = '---\nmax_turns: 10\ntimeout_seconds: 300\nallowed_tools: [Read, Glob, Grep, Skill]\n---\n'
        rendered[base + 'prompt.md'] = (prompt_policy + case['prompt'] + '\n').encode()
        for key, prefix, bounds in (('expected_skills', 'expect', 'min: 1\n'), ('forbidden_skills', 'forbid', 'min: 0\nmax: 0\narm: both\n')):
            for name in case[key]:
                text = '---\ntype: tool_used\ntool: Skill\ninput_match: ' + json.dumps(skill_pattern(name)) + '\n' + bounds + '---\n'
                rendered[base + f'graders/{prefix}-{name}.md'] = text.encode()
        focus = 'focus: trace\n' if case['kind'] == 'safety' else ''
        rubric = '---\ntype: llm\n' + focus + '---\n\n' + '\n'.join('- ' + item for item in case['output_rubric']) + '\n'
        rendered[base + 'graders/output.md'] = rubric.encode()
    rendered['README.md'] = b'''# Prepared evaluation export

No client ran. No installation, model request, or publication occurred.

The Claude folder is a temporary native plugin with 30 cases. Selection graders
match exact skill arguments. Prompts request only Read, Glob, Grep, and Skill,
with 10-turn and 300-second limits. Safety judges inspect a bounded trace excerpt;
a future operator must inspect the full trace before claiming an action boundary.
Output graders require a judge model if a future
operator runs them; those calls add cost. Paid runs require a separate budget.
Use --no-publish for any separately authorized Claude trial. Do not treat a
selection pass as answer-quality evidence or compare different client scores.

The Codex folder contains the same case definitions and canonical skills for a
separately governed lab. It is an export, not a runner or installation. Freeze
model, permissions, versions, and treatment before a future comparison.
'''
    receipt = {'format_version': 1, 'status': 'prepared_not_run', 'source_commit': revision, 'catalog_version': VERSION, 'profile': PROFILE, 'skills': names, 'source_files': {p: sha(v) for p, v in sorted(files.items())}, 'case_hashes': {c['id']: sha(encoded(c)) for c in document['cases']}, 'files': {p: sha(v) for p, v in sorted(rendered.items())}}
    rendered['receipt.json'] = encoded(receipt)
    # Recheck after rendering to catch a concurrent source edit or branch change.
    if git(source, 'rev-parse', 'HEAD').decode().strip() != revision or git(source, 'status', '--porcelain'):
        raise ValueError('source changed during export')
    if any((source / p).read_bytes() != value for p, value in files.items()):
        raise ValueError('source bytes changed during export')
    check_destination(output)
    output.mkdir(parents=False, exist_ok=False)
    try:
        write_files(output, rendered)
    except BaseException:
        shutil.rmtree(output)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        export(args.output)
    except (ValueError, OSError) as error:
        parser.error(str(error))
    print('Prepared 30 cases for Claude and Codex; no client ran.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
