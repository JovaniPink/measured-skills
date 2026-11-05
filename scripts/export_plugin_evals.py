#!/usr/bin/env python3
"""Prepare one arm of the native Claude plugin eval suite; never run a client."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shlex
import subprocess
from typing import Any

from cataloglib import ROOT, VERSION, read_skill_metadata
from export_selected import check_destination
from export_trigger_evals import skill_pattern

SUITE = ROOT / 'evals/plugin-eval'
PACKS = Path('plugins/claude')
ROUTING_TOOLS = ['Skill', 'Read', 'Glob', 'Grep']
SUITE_PLUGIN = 'measured-eval-suite'
OUTPUT_TOKEN = '<OUTPUT>'


def sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def git(checkout: Path, *args: str) -> str:
    run = subprocess.run(['git', '-C', str(checkout), *args], capture_output=True, check=False)
    if run.returncode:
        raise ValueError(run.stderr.decode(errors='replace').strip() or 'Git inspection failed')
    return run.stdout.decode()


def load_arms(suite: Path = SUITE) -> dict[str, Any]:
    document: dict[str, Any] = load_json(suite / 'arms.json')
    if document.get('format_version') != 1 or document.get('status') != 'prepared_not_run':
        raise ValueError('unsupported arm definition')
    return document


def find_arm(document: dict[str, Any], arm_id: str) -> dict[str, Any]:
    arms: list[dict[str, Any]] = document['arms']
    for arm in arms:
        if arm['id'] == arm_id:
            return arm
    raise ValueError(f'unknown arm: {arm_id}')


def yaml_list(values: list[str]) -> str:
    return '[' + ', '.join(json.dumps(value) for value in values) + ']'


def frontmatter(fields: list[tuple[str, str]]) -> str:
    return '---\n' + ''.join(f'{key}: {value}\n' for key, value in fields) + '---\n'


def case_prompt(name: str, tags: list[str], arm: dict[str, Any], document: dict[str, Any],
                packs: list[str], tools: list[str], prompt: str) -> bytes:
    fields = [
        ('name', json.dumps(name)),
        ('tags', yaml_list(tags)),
        ('plugins', yaml_list([f'../../packs/{pack}' for pack in packs])),
        ('runs', str(arm['runs'])),
        ('model', json.dumps(document['model'])),
        ('max_turns', str(arm['max_turns'])),
        ('timeout_seconds', str(arm['timeout_seconds'])),
        ('allowed_tools', yaml_list(tools)),
    ]
    return (frontmatter(fields) + '\n' + prompt + '\n').encode('utf-8')


def tool_grader(tool: str, pattern: str | None, forbid: bool) -> bytes:
    fields = [('type', 'tool_used'), ('tool', tool)]
    if pattern is not None:
        fields.append(('input_match', json.dumps(pattern)))
    if forbid:
        fields += [('min', '0'), ('max', '0'), ('arm', 'both')]
    return frontmatter(fields).encode('utf-8')


def other_skill_pattern(name: str) -> str:
    # Match any skill value except the expected skill, with or without a namespace.
    return r'"skill"\s*:\s*"(?!(?:[\w-]+:)?' + re.escape(name) + r'")'


def routing_selection(source: Path, document: dict[str, Any]) -> dict[str, list[tuple[str, dict[str, str]]]]:
    """Group cases the way the exploration sampled them, so runs stay comparable."""
    skills = load_json(source / 'evals/cases.json')['skills']
    profiles = load_json(source / 'catalog/profiles.json')['profiles']
    core = next(row['skills'] for row in profiles if row['id'] == document['core_profile'])
    groups: dict[str, list[tuple[str, dict[str, str]]]] = {
        'core-positive': [], 'core-near-miss': [],
        'specialist-positive': [], 'specialist-near-miss': [],
    }
    for skill in skills:
        if skill['invocation'] != 'implicit':
            continue
        name = skill['skill']
        if name in core:
            groups['core-positive'] += [(name, case) for case in skill['positive']]
            groups['core-near-miss'] += [(name, case) for case in skill['near_miss']]
        else:
            groups['specialist-positive'].append((name, skill['positive'][0]))
            groups['specialist-near-miss'].append((name, skill['near_miss'][0]))
    return groups


def routing_cases(source: Path, arm: dict[str, Any], document: dict[str, Any],
                  packs: list[str]) -> dict[str, bytes]:
    groups = routing_selection(source, document)
    files: dict[str, bytes] = {}
    for group in arm['selection']:
        family, kind = group.split('-', 1)
        for skill, case in groups[group]:
            base = f"evals/{case['id']}/"
            tags = ['routing', family, kind, skill]
            files[base + 'prompt.md'] = case_prompt(case['id'], tags, arm, document, packs,
                                                    ROUTING_TOOLS, case['prompt'])
            if kind == 'positive':
                files[base + 'graders/expected-skill-called.md'] = tool_grader('Skill', skill_pattern(skill), False)
                files[base + 'graders/no-other-skill-called.md'] = tool_grader('Skill', other_skill_pattern(skill), True)
            else:
                files[base + 'graders/own-skill-not-called.md'] = tool_grader('Skill', skill_pattern(skill), True)
                files[base + 'graders/no-skill-called.md'] = tool_grader('Skill', None, True)
    return files


def assess_prompt(source: Path, settings: dict[str, Any]) -> str:
    routes = load_json(source / 'catalog/workflows.json')['routes']
    route = next(row for row in routes if row['id'] == settings['route'])
    mode = next(row for row in route['modes'] if row['id'] == settings['mode'])
    prompt: str = mode['prompts'][settings['prompt_surface']]
    for placeholder, value in settings['replacements'].items():
        prompt = prompt.replace(placeholder, value)
    if '[' in prompt or ']' in prompt:
        raise ValueError('assess prompt kept an unresolved placeholder')
    return prompt


def forced_skill(source: Path, settings: dict[str, Any]) -> tuple[str, str]:
    """Return the slash command and a heading only the loaded skill body carries."""
    name = settings['forced_skill']
    metadata = read_skill_metadata(source / 'skills' / name)
    path = source / PACKS / metadata['plugin'] / 'skills' / name / 'SKILL.md'
    body = path.read_text(encoding='utf-8').split('---', 2)[2]
    match = re.search(r'^# (.+)$', body, re.M)
    if match is None or match.group(1) in metadata['description']:
        raise ValueError('skill body needs a heading that its description does not contain')
    return f"/{metadata['plugin']}:{name}", match.group(0)


def skill_indicators(settings: dict[str, Any], body_heading: str) -> dict[str, bytes]:
    """Record both load paths: slash commands load the body without a Skill call."""
    called = [('type', 'tool_used'), ('tool', 'Skill'),
              ('input_match', json.dumps(skill_pattern(settings['forced_skill']))), ('arm', 'with-only')]
    seen = [('type', 'regex'), ('target', 'trace'),
            ('pattern', json.dumps(re.escape(body_heading))), ('arm', 'with-only')]
    return {'skill-tool-called.md': frontmatter(called).encode('utf-8'),
            'skill-body-seen.md': frontmatter(seen).encode('utf-8')}


def behavior_cases(source: Path, suite: Path, arm: dict[str, Any], document: dict[str, Any],
                   packs: list[str]) -> dict[str, bytes]:
    settings = document['behavior']
    command, body_heading = forced_skill(source, settings)
    prompts = {'long': assess_prompt(source, settings), 'short': settings['short_prompt']}
    tools = ROUTING_TOOLS + settings['bash_grants']
    scaffold = (suite / settings['fixture']).read_bytes()
    graders = {path.name: path.read_bytes() for path in sorted((suite / 'graders').glob('*.md'))}
    graders.update(skill_indicators(settings, body_heading))
    files: dict[str, bytes] = {}
    for selected in arm['selection']:
        length, _, forced = selected.partition('-')
        prompt = f'{command} {prompts[length]}' if forced else prompts[length]
        name = 'behavior-' + selected
        base = f'evals/{name}/'
        tags = ['behavior', length] + (['forced'] if forced else [])
        files[base + 'prompt.md'] = case_prompt(name, tags, arm, document, packs, tools, prompt)
        files[base + 'case.yaml'] = (f'schema_version: "1.1"\nname: {json.dumps(name)}\n'
                                     'context:\n  scaffold_script: scaffold.sh\n').encode('utf-8')
        files[base + 'scaffold.sh'] = scaffold
        for grader, payload in graders.items():
            files[base + 'graders/' + grader] = payload
    return files


def pack_files(source: Path) -> tuple[list[str], dict[str, bytes]]:
    """Copy the tracked generated packs, which is what the exploration loaded."""
    files: dict[str, bytes] = {}
    packs: set[str] = set()
    for relative in sorted(filter(None, git(source, 'ls-files', '-z', PACKS.as_posix()).split('\0'))):
        path = source / relative
        if path.is_symlink() or not path.is_file():
            raise ValueError('pack files must be regular files')
        inner = Path(relative).relative_to(PACKS)
        packs.add(inner.parts[0])
        files['packs/' + inner.as_posix()] = path.read_bytes()
    if not packs:
        raise ValueError('source has no generated Claude packs')
    return sorted(packs), files


def run_command(arm: dict[str, Any], document: dict[str, Any], output: str) -> str:
    environment = {'CLAUDE_CODE_EFFORT_LEVEL': document['effort'], 'DISABLE_AUTOUPDATER': '1', **arm['environment']}
    words = ['claude', 'plugin', 'eval', output, '--ablation', arm['ablation'], '--threshold', '0',
             '--max-cost-usd', f"{arm['max_cost_usd']:.2f}", '--concurrency', str(arm['concurrency']),
             '--no-publish', '--trust-plugin', '--output-dir', output + '/results',
             '--disallow-tools', *document['withheld_tools']]
    if arm['kind'] == 'behavior':
        words += ['--scaffold', '--judge-model', document['judge_model'],
                  '--allow-tools', *document['behavior']['bash_grants']]
    return ' '.join([f'{key}={value}' for key, value in sorted(environment.items())] + [shlex.join(words)])


def render(arm_id: str, source: Path = ROOT, suite: Path = SUITE) -> dict[str, bytes]:
    """Return the suite as bytes. The result depends only on the two input trees."""
    document = load_arms(suite)
    arm = find_arm(document, arm_id)
    packs, files = pack_files(source)
    if arm['kind'] == 'routing':
        cases = routing_cases(source, arm, document, packs)
    else:
        cases = behavior_cases(source, suite, arm, document, packs)
    count = len({path.split('/')[1] for path in cases})
    if count != arm['expected_cases']:
        raise ValueError(f"{arm_id}: expected {arm['expected_cases']} cases, found {count}")
    files.update(cases)
    files['.claude-plugin/plugin.json'] = (json.dumps({
        'name': SUITE_PLUGIN,
        'version': VERSION,
        'description': 'Temporary evaluation suite. It holds no observed results.',
    }, indent=2) + '\n').encode('utf-8')
    return files


def receipt(files: dict[str, bytes], arm_id: str, source_commit: str, suite_commit: str,
            suite: Path = SUITE) -> bytes:
    document = load_arms(suite)
    arm = find_arm(document, arm_id)
    return (json.dumps({
        'format_version': 1,
        'status': 'prepared_not_run',
        'arm': arm_id,
        'source_commit': source_commit,
        'suite_commit': suite_commit,
        'model': document['model'],
        'cases': arm['expected_cases'],
        'runs_per_case': arm['runs'],
        'max_cost_usd': arm['max_cost_usd'],
        'command': run_command(arm, document, OUTPUT_TOKEN),
        'files': {path: sha(payload) for path, payload in sorted(files.items())},
    }, indent=2, sort_keys=True) + '\n').encode('utf-8')


def require_clean(checkout: Path) -> str:
    if git(checkout, 'status', '--porcelain'):
        raise ValueError('export requires clean committed checkouts')
    return git(checkout, 'rev-parse', 'HEAD').strip()


def export(arm_id: str, output: Path, source: Path = ROOT, suite: Path = SUITE) -> str:
    check_destination(output)
    source = source.resolve()
    suite_root = Path(git(suite, 'rev-parse', '--show-toplevel').strip()).resolve()
    if any(output.resolve().is_relative_to(checkout) for checkout in (source, suite_root)):
        raise ValueError('evaluation output must be outside the source checkout')
    source_commit = require_clean(source)
    suite_commit = require_clean(suite_root)
    files = render(arm_id, source, suite)
    files['receipt.json'] = receipt(files, arm_id, source_commit, suite_commit, suite)
    output.mkdir()
    for relative, payload in sorted(files.items()):
        path = output / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
    document = load_arms(suite)
    return run_command(find_arm(document, arm_id), document, str(output.absolute()))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--arm', required=True)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--source', type=Path, default=ROOT,
                        help='clean checkout that supplies cases, catalog, and generated packs')
    args = parser.parse_args()
    try:
        command = export(args.arm, args.output, args.source)
    except (ValueError, OSError) as error:
        parser.error(str(error))
    print('Prepared without running a client. A run costs money and needs its own approval:')
    print(command)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
