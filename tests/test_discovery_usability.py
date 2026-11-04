"""The chooser must be usable on a phone without losing any stated limit."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import discovery  # noqa: E402

# The last revision whose prompts predate the usability change.
BASELINE = '773e72f6f95c27030c4e91d5f65f8816b590e8cb'
FIRST_OPENING = ('In [REPOSITORY], inspect repository instructions, current branch, comparison [BASE_REVISION], '
                 'relevant staged/working/untracked changes, and [PLAN_FILE or none].')
DISCOVER = 'Discover the comparison revision and plan location; if absent, say so.'
# Each historical sentence that may differ, and exactly what replaced it.
REWRITES = {
    FIRST_OPENING: ['In [REPOSITORY], inspect repository instructions, the current branch, '
                    'relevant staged/working/untracked changes, and any saved plan.', DISCOVER],
    'In [REPOSITORY], inspect repository instructions and current branch, comparison [BASE_REVISION], '
    'relevant dirty/untracked files, and [PLAN_FILE or none].':
        ['In [REPOSITORY], inspect repository instructions, the current branch, '
         'relevant dirty/untracked files, and any saved plan.', DISCOVER],
    'In [REPOSITORY], inspect applicable instructions, current branch, comparison [BASE_REVISION or discover], '
    'relevant staged/working/untracked changes, and [PLAN_FILE or none].':
        ['In [REPOSITORY], inspect applicable instructions, the current branch, '
         'relevant staged/working/untracked changes, and any saved plan.', DISCOVER],
    'In [REPOSITORY], inspect repository instructions, branch, comparison [BASE_REVISION], '
    'relevant dirty files and [PLAN_FILE or none].':
        ['In [REPOSITORY], inspect repository instructions, the branch, relevant dirty files and any saved plan.',
         DISCOVER],
}
SUBSTRINGS = {
    'against [BASE_REVISION], including': 'against its discovered comparison revision, including',
    '[PLAN_FILE]': '[PLAN]',
}


def sentences(text: str) -> list[str]:
    return [s for s in re.split(r'(?<=\.)\s+', text.strip()) if s]


def registry() -> dict[str, Any]:
    data: dict[str, Any] = json.loads((ROOT / discovery.REGISTRY).read_text())
    return data


def prompts(data: dict[str, Any]) -> list[tuple[str, str, str, str]]:
    return [(r['id'], m['id'], c, p) for r in data['routes'] for m in r['modes'] for c, p in m['prompts'].items()]


class PromptWordingTests(unittest.TestCase):
    def test_no_prompt_asks_for_git_vocabulary(self) -> None:
        for route, mode, client, prompt in prompts(registry()):
            with self.subTest(route=route, mode=mode, client=client):
                self.assertNotIn('BASE_REVISION', prompt)
                self.assertNotIn('PLAN_FILE', prompt)
                self.assertTrue(prompt.isascii())

    def test_every_changed_sentence_is_an_expected_rewrite(self) -> None:
        old = json.loads(subprocess.check_output(['git', 'show', BASELINE + ':' + discovery.REGISTRY], cwd=ROOT))
        # Freeze the historical rewrite; later optional actions have separate tests.
        new = json.loads(subprocess.check_output(['git', 'show', '0a972d7b:' + discovery.REGISTRY], cwd=ROOT))
        self.assertEqual([p[:3] for p in prompts(old)], [p[:3] for p in prompts(new)])
        for (route, mode, client, before), (_, _, _, after) in zip(prompts(old), prompts(new), strict=True):
            expected: list[str] = []
            for sentence in sentences(before):
                command = re.match(r'[$/][a-z0-9-]+:[a-z0-9-]+ ', sentence)
                prefix = command.group(0) if command else ''
                sentence = sentence[len(prefix):]
                if sentence in REWRITES:
                    expected += [prefix + REWRITES[sentence][0], *REWRITES[sentence][1:]]
                    continue
                if prefix:
                    expected.append(prefix + sentence)
                    continue
                for old_text, new_text in SUBSTRINGS.items():
                    sentence = sentence.replace(old_text, new_text)
                expected.append(sentence)
            with self.subTest(route=route, mode=mode, client=client):
                self.assertEqual(expected, sentences(after))

    def test_every_request_is_single_spaced_sentences(self) -> None:
        # The site displays requests sentence by sentence and copies the original string,
        # so the two must be identical.
        for route, mode, client, prompt in prompts(registry()):
            with self.subTest(route=route, mode=mode, client=client):
                self.assertEqual(prompt, ' '.join(sentences(prompt)))

    def test_example_result_carries_no_hedge_prefix(self) -> None:
        for route in registry()['routes']:
            with self.subTest(route=route['id']):
                self.assertFalse(route['output_example'].startswith(('Fictional', 'Synthetic')))


class InputTests(unittest.TestCase):
    def test_each_route_declares_exactly_the_fields_its_requests_use(self) -> None:
        for route in registry()['routes']:
            used = {t for m in route['modes'] for p in m['prompts'].values() for t in re.findall(r'\[([^\]]+)\]', p)}
            tokens = [i['token'] for i in route['inputs']]
            with self.subTest(route=route['id']):
                self.assertEqual(len(tokens), len(set(tokens)))
                self.assertEqual(used, set(tokens))
                for field in route['inputs']:
                    self.assertTrue(field['label'].strip() and field['hint'].strip())
                    self.assertTrue((field['label'] + field['hint']).isascii())

    def test_registry_rejects_missing_unknown_and_blank_fields(self) -> None:
        known = {s['skill'] for s in json.loads((ROOT / 'catalog/skills.json').read_text())['skills']}
        self.assertEqual([], discovery.registry_errors(registry(), known))
        for mutation in ('missing', 'unknown', 'blank', 'duplicate'):
            with self.subTest(mutation=mutation):
                data = deepcopy(registry())
                inputs = data['routes'][0]['inputs']
                if mutation == 'missing':
                    inputs.pop()
                elif mutation == 'unknown':
                    inputs.append({'token': 'NOT_USED', 'label': 'x', 'hint': 'y'})
                elif mutation == 'blank':
                    inputs[0]['label'] = ' '
                else:
                    inputs.append(dict(inputs[0]))
                self.assertTrue(discovery.registry_errors(data, known))


    def test_registry_reports_malformed_actions_with_standing_limits(self) -> None:
        known = {s['skill'] for s in json.loads((ROOT / 'catalog/skills.json').read_text())['skills']}
        for field, value, message in (
            ('modes', None, 'missing action scope'),
            ('prompts', ['invalid'], 'invalid mode record'),
        ):
            with self.subTest(field=field):
                data = registry()
                route = data['routes'][0]
                record = route if field == 'modes' else route['modes'][0]
                record[field] = value
                self.assertIn(f"{route['id']}: {message}", discovery.registry_errors(data, known))


class LimitTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = registry()
        self.data = discovery.build_data('0' * 40, verify_source=False)

    def test_standing_limits_are_named_once_and_never_dropped_from_a_request(self) -> None:
        limits = self.registry['standard_limits']
        self.assertEqual(7, len(limits))
        for route in self.data['routes']:
            for mode in route['modes']:
                for style, texts in (('native', mode['prompts']), ('ordinary', mode['ordinary_prompts'])):
                    for client, full in texts.items():
                        part = mode['request_parts'][style][client]
                        with self.subTest(route=route['id'], mode=mode['id'], style=style, client=client):
                            shown = sentences(part['task']) + part['limits']
                            self.assertEqual(sorted(sentences(full)), sorted(shown))
                            self.assertTrue(set(part['limits']) <= set(limits))
                            self.assertFalse(set(sentences(part['task'])) & set(limits))
                            # Order is preserved so the copy stays the original request.
                            positions = [full.index(s) for s in part['limits']]
                            self.assertEqual(positions, sorted(positions))

    def test_every_prompt_still_contains_every_limit_it_had(self) -> None:
        old = json.loads(subprocess.check_output(['git', 'show', BASELINE + ':' + discovery.REGISTRY], cwd=ROOT))
        limits = set(self.registry['standard_limits'])
        current = {p[:3]: p[3] for p in prompts(self.registry)}
        for route, mode, client, before in prompts(old):
            after = current[(route, mode, client)]
            with self.subTest(route=route, mode=mode, client=client):
                self.assertEqual({s for s in sentences(before) if s in limits}, {s for s in sentences(after) if s in limits})

    def test_a_non_standard_sentence_is_never_hidden(self) -> None:
        part = discovery.request_parts('In [REPOSITORY], do it. Preserve unrelated work. Never push.', ['Preserve unrelated work.'])
        self.assertEqual(['Preserve unrelated work.'], part['limits'])
        self.assertEqual('In [REPOSITORY], do it. Never push.', part['task'])


class ActionTests(unittest.TestCase):
    def test_action_facts_come_from_catalog_data_not_prose(self) -> None:
        data = discovery.build_data('0' * 40, verify_source=False)
        skills = {s['id']: s for s in data['skills']}
        core = next(p['skills'] for p in data['profiles'] if p['id'] == 'finish-work-core')
        for route in data['routes']:
            for mode in route['modes']:
                action = mode['action']
                skill = skills[action['skill']]
                with self.subTest(route=route['id'], mode=mode['id']):
                    self.assertEqual(skill['pack'], action['pack'])
                    self.assertEqual(skill['invocation'], action['invocation'])
                    self.assertEqual(skill['id'] in core, action['in_core_profile'])
                    self.assertEqual(skill['availability'], action['availability'])
                    self.assertEqual(f"${skill['pack']}:{skill['id']}", action['command']['codex'])
                    self.assertEqual(f"/{skill['pack']}:{skill['id']}", action['command']['claude'])
                    self.assertEqual({'codex', 'claude'}, set(action['command']))

    def test_clients_have_short_labels_and_keep_their_caveat(self) -> None:
        data = registry()
        self.assertEqual({'codex', 'claude', 'antigravity', 'chatgpt', 'claude-web'}, set(data['clients']))
        self.assertEqual(set(data['clients']), set(data['client_notes']))
        for client, label in data['clients'].items():
            with self.subTest(client=client):
                self.assertLessEqual(len(label), 20)
                self.assertTrue(data['client_notes'][client].strip())


if __name__ == '__main__':
    unittest.main()
