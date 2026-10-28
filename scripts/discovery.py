"""Deterministic, local-only discovery and one-to-one migration contracts."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import subprocess
from pathlib import Path
from typing import Any

import canonical_deltas

from cataloglib import ROOT, VERSION, read_skill_metadata

MIGRATION = 'catalog/migrations/0.18-to-0.19.json'
REGISTRY = 'catalog/workflows.json'
EXPORT = 'dist/discovery/catalog.json'
GENERATED_INDEX = 'skills/choose-workflow/references/workflow-index.md'


def encoded(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=True) + '\n').encode()


def sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def git(root: Path, *args: str) -> bytes:
    result = subprocess.run(['git', *args], cwd=root, capture_output=True, check=False)
    if result.returncode:
        raise ValueError('source revision is unavailable: ' + result.stderr.decode(errors='replace').strip())
    return result.stdout


def migration_errors(root: Path = ROOT, document: dict[str, Any] | None = None) -> list[str]:
    data = document if document is not None else json.loads((root / MIGRATION).read_text())
    errors: list[str] = []
    revision = data.get('source_revision', '')
    if not isinstance(revision, str) or re.fullmatch('[0-9a-f]{40}', revision) is None:
        return ['migration requires exact historical source revision']
    try:
        git(root, 'merge-base', '--is-ancestor', revision, 'HEAD')
        old = {r['skill']: r for r in json.loads(git(root, 'show', revision + ':catalog/skills.json'))['skills']}
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        return [str(error)]
    rows = data.get('entries', [])
    if not isinstance(rows, list) or not all(isinstance(r, dict) for r in rows):
        return ['migration entries must be records']
    if any(not isinstance(r.get(k), str) for r in rows for k in ('old_id', 'new_id')):
        return ['migration identifiers must be strings']
    before = [r.get('old_id') for r in rows]
    after = [r.get('new_id') for r in rows]
    if len(before) != len(set(before)) or len(after) != len(set(after)):
        errors.append('migration identifiers must be unique')
    if set(before) != set(old):
        errors.append('migration must preserve the entire historical inventory')
    current = {r['skill']: r for r in json.loads((root / 'catalog/skills.json').read_text())['skills']}
    additions = data.get('additions', [])
    if not isinstance(additions, list) or any(not isinstance(v, str) for v in additions) or len(additions) != len(set(additions)):
        return errors + ['migration additions must be unique strings']
    if set(after) & set(additions):
        errors.append('migration additions overlap existing capabilities')
    if set(after) | set(additions) != set(current):
        errors.append('migration destinations and additions must equal the current inventory')
    if data.get('installed_aliases') is not False:
        errors.append('historical names must not create installed alias skills')
    for row in rows:
        name, target = row.get('old_id'), row.get('new_id')
        if name not in old or target not in current:
            continue
        for key in ('invocation', 'risk_class'):
            if row.get(key) != old[name][key] or row.get(key) != current[target][key]:
                errors.append(f'{name}: migration must preserve authority ({key})')
        if row.get('old_pack') != old[name]['plugin'] or row.get('new_pack') != current[target]['plugin']:
            errors.append(f'{name}: incorrect pack mapping')
        if (root / 'skills' / str(name)).exists():
            errors.append(f'{name}: obsolete installed alias remains')
    return errors


def obsolete_message(names: list[str], root: Path = ROOT) -> str:
    data = json.loads((root / MIGRATION).read_text())
    replacements = {r['old_id']: r['new_id'] for r in data['entries']}
    changed = [f'{name} -> {replacements[name]}' for name in names if name in replacements]
    return 'Obsolete 0.18 identifier; use ' + ', '.join(changed) + '. See docs/migration-0.19.md.' if changed else ''


def registry_errors(data: dict[str, Any], known: set[str]) -> list[str]:
    errors: list[str] = []
    if data.get('format_version') != 1 or data.get('catalog_version') != VERSION:
        errors.append('workflow registry version mismatch')
    routes = data.get('routes', [])
    if not isinstance(routes, list) or not routes:
        return errors + ['workflow routes are missing']
    ids: set[str] = set()
    client_records = data.get('clients', {})
    if not isinstance(client_records, dict) or set(client_records) != {'codex', 'claude', 'antigravity', 'chatgpt', 'claude-web'}:
        return errors + ['workflow clients are missing or invalid']
    clients = set(client_records)
    for row in routes:
        if not isinstance(row, dict):
            errors.append('invalid workflow record')
            continue
        identity = row.get('id', '')
        if not isinstance(identity, str) or re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*', identity) is None or identity in ids:
            errors.append('invalid or duplicate workflow identity')
        if not isinstance(identity, str):
            continue
        ids.add(identity)
        for field in ('label', 'why', 'output_example'):
            if not isinstance(row.get(field), str) or not row[field].strip():
                errors.append(f'{identity}: missing {field}')
        for field in ('steps', 'required_inputs', 'search_phrases', 'optional_skills'):
            if not isinstance(row.get(field), list) or not all(isinstance(v, str) for v in row[field]):
                errors.append(f'{identity}: invalid {field}')
        optional = row.get('optional_skills', [])
        if not isinstance(row.get('primary_skill'), str) or row['primary_skill'] not in known or not isinstance(optional, list) or any(not isinstance(v, str) or v not in known for v in optional):
            errors.append(f'{identity}: unknown skill selection')
        modes = row.get('modes', [])
        if not isinstance(modes, list) or not modes:
            errors.append(f'{identity}: missing action scope')
            continue
        mode_ids: set[str] = set()
        for mode in modes:
            if not isinstance(mode, dict) or not isinstance(mode.get('id'), str) or not isinstance(mode.get('prompts'), dict):
                errors.append(f'{identity}: invalid mode record')
                continue
            if mode.get('id') in mode_ids or mode.get('id') not in {'assess', 'repair', 'maintain', 'prepare'}:
                errors.append(f'{identity}: invalid or duplicate mode')
            mode_ids.add(mode['id'])
            if set(mode.get('prompts', {})) != clients or not mode.get('scope'):
                errors.append(f'{identity}: incomplete client prompts or scope')
            command_skill = mode.get('command_skill')
            if command_skill is not None and (not isinstance(command_skill, str) or command_skill not in known):
                errors.append(f'{identity}: unknown native command skill')
            for prompt in mode.get('prompts', {}).values():
                if not isinstance(prompt, str) or '[REPOSITORY]' not in prompt or not prompt.isascii():
                    errors.append(f'{identity}: invalid portable prompt')
    if data.get('default_route') not in ids:
        errors.append('default workflow is missing')
    stacks = data.get('stack_options', {})
    if not isinstance(stacks, dict) or any(not isinstance(v, dict) for v in stacks.values()):
        return errors + ['invalid stack options']
    for option in stacks.values():
        if option.get('skill') is not None and (not isinstance(option['skill'], str) or option['skill'] not in known):
            errors.append('unknown optional stack')
    return errors


def input_hashes(root: Path = ROOT) -> dict[str, str]:
    paths = [REGISTRY, MIGRATION, canonical_deltas.RECORD, 'scripts/canonical_deltas.py', 'catalog/skills.json', 'catalog/profiles.json', 'catalog/evidence.json',
             'catalog/compatibility.json', 'scripts/discovery.py', 'scripts/discovery-ui.js', 'scripts/cataloglib.py']
    paths += [p.relative_to(root).as_posix() for p in sorted((root / 'skills').rglob('*'))
              if p.is_file() and p.relative_to(root).as_posix() != GENERATED_INDEX]
    return {p: sha((root / p).read_bytes()) for p in sorted(paths)}


def build_data(revision: str, root: Path = ROOT, verify_source: bool = True) -> dict[str, Any]:
    registry = json.loads((root / REGISTRY).read_text())
    catalog = json.loads((root / 'catalog/skills.json').read_text())['skills']
    errors = canonical_deltas.check(root) + migration_errors(root) + registry_errors(registry, {r['skill'] for r in catalog})
    if errors:
        raise ValueError('\n'.join(errors))
    if re.fullmatch('[0-9a-f]{40}', revision) is None:
        raise ValueError('discovery source must be a full commit')
    inputs = input_hashes(root)
    if verify_source:
        git(root, 'merge-base', '--is-ancestor', revision, 'HEAD')
        for path, digest in inputs.items():
            if sha(git(root, 'show', revision + ':' + path)) != digest:
                raise ValueError(f'discovery input drift from pinned source: {path}')
    migration = json.loads((root / MIGRATION).read_text())
    aliases = {r['new_id']: r['old_id'] for r in migration['entries']}
    skills = []
    for row in catalog:
        name = row['skill']
        meta = read_skill_metadata(root / 'skills' / name)
        interface = (root / 'skills' / name / 'agents/openai.yaml').read_text()
        match = re.search(r'^  display_name: "(.+)"$', interface, re.M)
        available = {c: 'packaged' for c in ('codex', 'claude', 'chatgpt', 'claude-web')}
        if meta['invocation'] == 'explicit':
            available['claude-web'] = 'archive prepared; upload held pending invocation control'
            available['chatgpt'] = 'archive prepared; receiving-surface control unverified'
        available['antigravity'] = 'excluded: explicit-only control unverified' if meta['invocation'] == 'explicit' else 'packaged'
        skills.append(dict(id=name, label=match[1] if match else name, pack=meta['plugin'],
                           description=meta['description'], invocation=meta['invocation'], risk_class=meta['risk_class'],
                           historical_names=[aliases[name]] if name in aliases else [], availability=available,
                           client_evidence='not_observed_for_0.19', evidence_reference='docs/client-candidate-v0.19.0.md'))
    return dict(**registry, source_revision=revision, input_files=inputs, skills=skills,
                migration=migration, profiles=json.loads((root / 'catalog/profiles.json').read_text())['profiles'])


def markdown(data: dict[str, Any], bundled: bool = False) -> str:
    lines = ['# Find your next workflow', '', 'Generated from one shared workflow registry. 0.19.0 preview, not released.', '',
             'Start with **Finish existing work**. Choose a task and action scope; then use the prompt for your client.', '',
             'Selection is not execution. Check the installed version and entry first. If missing, use ordinary task wording and report that no skill loaded.', '',
             'Codex: select the matching installed entry; duplicate names require source checks. Claude Code: one leading command is portable across interfaces. Antigravity: ordinary requests preserve all explicit-only exclusions.', '',
             'Web accounts require their own uploaded source and loading checks; local installation does not establish web availability.', '',
             'A stack is optional. Add its guidance only after repository discovery. Packs distribute skills; finish-work-core is the focused nine-skill selection.', '']
    lines += ['## Contents', ''] + ['- [' + r['label'] + '](#' + re.sub(r'[^a-z0-9 -]', '', r['label'].lower()).replace(' ', '-') + ')' for r in data['routes']] + ['- [Catalog and historical names](#catalog-and-historical-names)', '']
    for route in data['routes']:
        lines += ['## ' + route['label'], '', f"Start here: `{route['primary_skill']}`. {route['why']}", '',
                  'Provide: ' + ', '.join(route['required_inputs']) + '.', '',
                  'Steps: ' + ' -> '.join(route['steps']) + '.', '',
                  'Synthetic result: ' + route['output_example'], '',
                  'Optional specialists: ' + ', '.join(route['optional_skills']) + '.', '']
        for mode in route['modes']:
            lines += ['### ' + mode['label'], '', 'Finish line: ' + mode['scope'], '']
            if mode.get('command_skill'):
                entry = next(s for s in data['skills'] if s['id'] == mode['command_skill'])
                lines += [f"Native entry when installed: Codex `${entry['pack']}:{entry['id']}`; Claude Code `/{entry['pack']}:{entry['id']}`. Invocation: {entry['invocation']}. Antigravity and web prompts use ordinary requests; no excluded entry is implied.", '']
            for client, label in data['clients'].items():
                if bundled and client != 'antigravity':
                    continue
                lines += [label, '', '```text', mode['prompts'][client], '```', '']
    lines += ['## Catalog and historical names', '', '| Skill | Former name | Invocation |', '| --- | --- | --- |']
    for skill in data['skills']:
        lines += [f"| {skill['label']} (`{skill['id']}`) | {', '.join(skill['historical_names']) or 'New'} | {skill['invocation']} |"]
    lines += ['', 'Package availability, invocation policy, and observed behavior are separate. All 0.19 installed-client behavior remains unobserved. Historical names are lookup terms, never extra installed copies.', '']
    if not bundled:
        lines += ['Source revision: `' + data['source_revision'] + '`. File hashes: `catalog.json` alongside this guide.', '']
    return '\n'.join(lines)


def reader_guide(data: dict[str, Any]) -> str:
    lines = ['# Complete skill catalog', '', 'Generated from canonical metadata. Start with [the task chooser](start.md).', '',
             f"This preview contains {len(data['skills'])} portable agent skills. Packs are distribution units, not recommended activation sets.", '']
    for pack in sorted({s['pack'] for s in data['skills']}):
        lines += ['## ' + pack, '']
        for s in (s for s in data['skills'] if s['pack'] == pack):
            lines += ['### ' + s['label'], '', f"[`{s['id']}`](../skills/{s['id']}/SKILL.md)", '', s['description'], '',
                      'Invocation: ' + s['invocation'] + '. Risk class: ' + s['risk_class'] + '.', '',
                      'Historical name: ' + (', '.join(s['historical_names']) or 'new in 0.19') + '.', '']
    return '\n'.join(lines)


def offline_html(data: dict[str, Any], root: Path = ROOT) -> str:
    e = html.escape
    cards = []
    for r in data['routes']:
        modes = ''.join('<details><summary>' + e(m['label']) + '</summary><p>' + e(m['scope']) + '</p>' +
                        ''.join('<h4>' + e(data['clients'][c]) + '</h4><pre tabindex="0">' + e(p) + '</pre>' for c, p in m['prompts'].items()) + '</details>' for m in r['modes'])
        cards.append('<article id="' + e(r['id']) + '"><h2>' + e(r['label']) + '</h2><p>' + e(r['why']) + '</p><p>Start here: ' + e(r['primary_skill']) + '</p><p>Provide: ' + e(', '.join(r['required_inputs'])) + '</p><p>Synthetic output: ' + e(r['output_example']) + '</p>' + modes + '</article>')
    nav = ''.join('<a href="#' + e(r['id']) + '">' + e(r['label']) + '</a> ' for r in data['routes'][:7])
    catalog = ''.join('<li><strong>' + e(s['label']) + '</strong>: ' + e(s['id']) + ' (formerly ' + e(', '.join(s['historical_names']) or 'new') + '). ' + e(s['description']) + ' Invocation: ' + e(s['invocation']) + '.</li>' for s in data['skills'])
    payload = json.dumps(data, ensure_ascii=True).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    script = (root / 'scripts/discovery-ui.js').read_text()
    document: str = '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; script-src \'unsafe-inline\'; style-src \'unsafe-inline\'; connect-src \'none\'; base-uri \'none\'; form-action \'none\'"><title>Find your next workflow - Measured Skills</title><style>body{font:1.1rem/1.65 system-ui;margin:auto;padding:2rem;max-width:68rem;color:#172c27;background:#faf8f3}a{color:#125d48}nav{display:flex;gap:1rem;flex-wrap:wrap}article{border-top:1px solid #b6c9c0;margin-top:2rem}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit;background:#e9eee9;padding:1rem}input,select,button{font:inherit;max-width:100%;padding:.5rem;margin:.4rem}summary,button{cursor:pointer}:focus-visible{outline:3px solid #14694f;outline-offset:3px}h1,h2{line-height:1.2}li{margin:.7rem 0}[hidden]{display:none}</style><main><h1>Finish the next piece of work</h1><p>Measured Skills 0.19.0 preview. Nothing executes when you choose a route. No login, network calls, saved search text or installation.</p><p>Available source: ' + e(data['available_version']) + '. Installed names may differ; verify source and loading before using a command.</p><nav aria-label="Tasks">' + nav + '</nav><section id="interactive" hidden></section><section aria-label="Finish-work sequence"><h2>A small, complete repair</h2><p>Recover -> Plan -> Repair -> Check -> Review -> Verify. Findings return to Repair; blocked work stays visible.</p></section><section aria-label="Evidence ladder"><h2>What each result tells you</h2><ol><li>Source inspection: what the code says.</li><li>Local checks: what ran in this checkout.</li><li>Client behavior: what this installed client actually loaded and did.</li><li>Remote CI: what the host checked at its recorded revision.</li><li>Deployed behavior: what was observed in the receiving environment.</li></ol><p>No rung automatically establishes the next.</p></section><section id="static-guide">' + ''.join(cards) + '</section><details id="catalog"><summary>Browse all ' + str(len(data['skills'])) + ' skills</summary><ul>' + catalog + '</ul></details><p>Source revision: ' + e(data['source_revision']) + '. All 0.19 client behavior is unobserved.</p></main><script type="application/json" id="catalog-data">' + payload + '</script><script>' + script + '</script></html>\n'
    return document


def generated_files(data: dict[str, Any], root: Path = ROOT) -> dict[str, bytes]:
    files = {EXPORT: encoded(data), 'dist/discovery/guide.md': markdown(data).encode(),
             'dist/discovery/index.html': offline_html(data, root).encode(), GENERATED_INDEX: markdown(data, bundled=True).encode(),
             'docs/skill-catalog-reader-guide.md': reader_guide(data).encode()}
    files['dist/discovery/hashes.json'] = encoded({p: sha(v) for p, v in files.items()})
    return files


def check(root: Path = ROOT) -> list[str]:
    try:
        previous = json.loads((root / EXPORT).read_text())
        data = build_data(previous['source_revision'], root)
        return [f'discovery output drift: {p}' for p, value in generated_files(data, root).items()
                if not (root / p).is_file() or (root / p).read_bytes() != value]
    except (OSError, ValueError, KeyError, TypeError) as error:
        return [f'discovery: {error}']


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-revision')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.check:
        errors = check()
        print('\n'.join(errors) if errors else 'Discovery exports match their committed sources.')
        return int(bool(errors))
    if not args.source_revision:
        parser.error('--source-revision is required for generation')
    data = build_data(args.source_revision)
    for path, payload in generated_files(data).items():
        target = ROOT / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
    print('Discovery exports generated; nothing installed or published.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
