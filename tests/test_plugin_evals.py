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

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import export_plugin_evals as exporter  # noqa: E402

SUITE = ROOT / 'evals/plugin-eval'
FIXTURE = SUITE / 'fixture/build-half-finished-pr.sh'
GRADERS = SUITE / 'graders'


def front(payload: bytes) -> dict:
    return yaml.safe_load(payload.decode().split('---', 2)[1])


def case_names(files: dict[str, bytes]) -> list[str]:
    return sorted({path.split('/')[1] for path in files if path.startswith('evals/')})


def grader_regex(name: str) -> re.Pattern[str]:
    fields = front((GRADERS / f'{name}.md').read_bytes())
    flags = fields.get('flags', '')
    return re.compile(fields['pattern'], (re.I if 'i' in flags else 0) | (re.M if 'm' in flags else 0))


class RoutingExport(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = exporter.load_arms()
        cls.core = exporter.render('routing-core')
        cls.specialist = exporter.render('routing-specialist')
        cls.listing = exporter.render('routing-listing-8000')
        skills = json.loads((ROOT / 'evals/cases.json').read_text())['skills']
        cls.skills = {row['skill']: row for row in skills}

    def test_arms_cover_the_cases_the_audit_says_were_not_rerun(self) -> None:
        groups = exporter.routing_selection(ROOT, self.document)
        self.assertEqual(len(groups['specialist-positive']), 64)
        self.assertEqual(len(case_names(self.specialist)), 128)
        self.assertEqual(len(case_names(self.core)), 63)
        self.assertEqual(len(case_names(self.listing)), 96)
        self.assertTrue(set(row[1]['id'] for row in groups['specialist-positive']) <= set(case_names(self.listing)))

    def test_forced_listing_changes_only_the_environment(self) -> None:
        arm = exporter.find_arm(self.document, 'routing-listing-8000')
        self.assertEqual(arm['environment'], {'SLASH_COMMAND_TOOL_CHAR_BUDGET': '8000'})
        self.assertIn('SLASH_COMMAND_TOOL_CHAR_BUDGET=8000 claude plugin eval',
                      exporter.run_command(arm, self.document, '/out'))
        name = 'plan-change-positive-1'
        self.assertEqual(self.listing[f'evals/{name}/prompt.md'], self.core[f'evals/{name}/prompt.md'])

    def test_explicit_only_skills_are_excluded(self) -> None:
        explicit = {name for name, row in self.skills.items() if row['invocation'] == 'explicit'}
        self.assertTrue(explicit)
        tagged = {front(payload)['tags'][3] for path, payload in {**self.core, **self.specialist}.items()
                  if path.endswith('prompt.md')}
        self.assertFalse(tagged & explicit)

    def test_prompts_are_copied_from_the_routing_cases(self) -> None:
        for path, payload in self.specialist.items():
            if path.endswith('prompt.md'):
                case_id = path.split('/')[1]
                skill = front(payload)['tags'][3]
                prompts = self.skills[skill]['positive'] + self.skills[skill]['near_miss']
                prompt = next(row['prompt'] for row in prompts if row['id'] == case_id)
                self.assertEqual(payload.decode().split('---\n', 2)[2], '\n' + prompt + '\n')

    def test_positive_case_requires_the_skill_tool(self) -> None:
        grader = front(self.core['evals/plan-change-positive-1/graders/expected-skill-called.md'])
        self.assertEqual((grader['type'], grader['tool']), ('tool_used', 'Skill'))
        self.assertNotIn('max', grader)
        match = re.compile(grader['input_match'])
        self.assertTrue(match.search('{"skill": "plan-change"}'))
        self.assertTrue(match.search('{"skill":"measured-workflows:plan-change"}'))
        self.assertFalse(match.search('{"skill": "plan-change-extra"}'))
        self.assertFalse(match.search('{"skill": "plan-tests"}'))

    def test_positive_case_records_a_wrong_skill(self) -> None:
        grader = front(self.core['evals/plan-change-positive-1/graders/no-other-skill-called.md'])
        self.assertEqual((grader['min'], grader['max'], grader['arm']), (0, 0, 'both'))
        match = re.compile(grader['input_match'])
        self.assertTrue(match.search('{"skill": "plan-tests"}'))
        self.assertTrue(match.search('{"skill": "measured-workflows:plan-tests"}'))
        self.assertFalse(match.search('{"skill": "plan-change"}'))
        self.assertFalse(match.search('{"skill": "measured-workflows:plan-change"}'))

    def test_near_miss_forbids_own_skill_and_records_any_skill(self) -> None:
        base = 'evals/plan-change-near-miss-1/graders/'
        own = front(self.core[base + 'own-skill-not-called.md'])
        anything = front(self.core[base + 'no-skill-called.md'])
        self.assertEqual((own['tool'], own['min'], own['max'], own['arm']), ('Skill', 0, 0, 'both'))
        self.assertTrue(re.search(own['input_match'], '{"skill": "plan-change"}'))
        self.assertEqual((anything['tool'], anything['max']), ('Skill', 0))
        self.assertNotIn('input_match', anything)

    def test_routing_case_matches_the_exploration_limits(self) -> None:
        fields = front(self.core['evals/plan-change-positive-1/prompt.md'])
        self.assertEqual(fields['model'], 'claude-haiku-5-5')
        self.assertEqual((fields['runs'], fields['max_turns']), (1, 4))
        self.assertEqual(fields['allowed_tools'], ['Skill', 'Read', 'Glob', 'Grep'])
        self.assertEqual(len(fields['plugins']), len(list((ROOT / 'plugins/claude').iterdir())))
        for plugin in fields['plugins']:
            self.assertTrue(plugin.startswith('../../packs/measured-'))

    def test_render_is_deterministic_and_carries_generated_packs(self) -> None:
        self.assertEqual(self.core, exporter.render('routing-core'))
        relative = 'measured-workflows/skills/plan-change/SKILL.md'
        self.assertEqual(self.core['packs/' + relative], (ROOT / 'plugins/claude' / relative).read_bytes())

    def test_case_count_drift_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            suite = Path(tmp)
            document = exporter.load_arms()
            exporter.find_arm(document, 'routing-core')['expected_cases'] = 62
            (suite / 'arms.json').write_text(json.dumps(document))
            with self.assertRaisesRegex(ValueError, 'expected 62 cases, found 63'):
                exporter.render('routing-core', ROOT, suite)

    def test_unknown_arm_fails(self) -> None:
        with self.assertRaisesRegex(ValueError, 'unknown arm'):
            exporter.render('routing-nothing')


class BehaviorExport(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = exporter.load_arms()
        cls.plain = exporter.render('behavior-plain')
        cls.forced = exporter.render('behavior-forced')

    def test_prompts_come_from_the_catalog(self) -> None:
        prompt = self.plain['evals/behavior-long/prompt.md'].decode()
        self.assertIn('In this repository, find out what remains for the retry feature.', prompt)
        self.assertNotIn('[REPOSITORY]', prompt)
        short = self.plain['evals/behavior-short/prompt.md'].decode().split('---\n', 2)[2].strip()
        self.assertEqual(len(short.split()), 34)

    def test_forced_case_uses_the_namespaced_slash_command(self) -> None:
        body = self.forced['evals/behavior-short-forced/prompt.md'].decode().split('---\n', 2)[2]
        self.assertTrue(body.strip().startswith('/measured-workflows:plan-change Find out what remains'))

    def test_every_case_scaffolds_the_fixture(self) -> None:
        for name in case_names({**self.plain, **self.forced}):
            files = self.plain if name in case_names(self.plain) else self.forced
            self.assertEqual(files[f'evals/{name}/scaffold.sh'], FIXTURE.read_bytes())
            fields = yaml.safe_load(files[f'evals/{name}/case.yaml'])
            self.assertEqual(fields, {'schema_version': '1.1', 'name': name,
                                      'context': {'scaffold_script': 'scaffold.sh'}})

    def test_each_run_records_both_ways_a_skill_can_load(self) -> None:
        base = 'evals/behavior-long/graders/'
        called = front(self.plain[base + 'skill-tool-called.md'])
        seen = front(self.plain[base + 'skill-body-seen.md'])
        self.assertEqual((called['tool'], called['arm']), ('Skill', 'with-only'))
        self.assertEqual((seen['target'], seen['arm']), ('trace', 'with-only'))
        self.assertTrue(re.search(seen['pattern'], '"text":"---\\n# Implementation Planning\\n"'))

    def test_body_marker_stays_out_of_the_listing(self) -> None:
        _, heading = exporter.forced_skill(ROOT, self.document['behavior'])
        metadata = exporter.read_skill_metadata(ROOT / 'skills/plan-change')
        self.assertEqual(heading, '# Implementation Planning')
        self.assertNotIn(heading.removeprefix('# '), metadata['description'])

    def test_bash_grants_are_read_only_git(self) -> None:
        grants = self.document['behavior']['bash_grants']
        for grant in grants:
            self.assertRegex(grant, r'^Bash\(git (status|log|diff|show|branch|stash list|stash show):\*\)$')
        self.assertEqual(front(self.plain['evals/behavior-long/prompt.md'])['allowed_tools'][4:], grants)
        for arm in ('behavior-plain', 'behavior-forced'):
            command = exporter.run_command(exporter.find_arm(self.document, arm), self.document, '/out')
            self.assertIn('--scaffold', command)
            self.assertTrue(command.endswith("'Bash(git stash show:*)'"))


class RunCommand(unittest.TestCase):
    def test_every_arm_has_a_ceiling_and_stays_local(self) -> None:
        document = exporter.load_arms()
        for arm in document['arms']:
            command = exporter.run_command(arm, document, '/out')
            self.assertIn(f"--max-cost-usd {arm['max_cost_usd']:.2f}", command)
            self.assertIn('--no-publish', command)
            self.assertIn('--threshold 0', command)
            self.assertIn('--disallow-tools Agent Task TaskStop', command)
            self.assertGreater(arm['max_cost_usd'], arm['estimated_cost_usd'])

    def test_readme_states_every_arm_ceiling_and_the_not_run_status(self) -> None:
        readme = (SUITE / 'README.md').read_text()
        document = exporter.load_arms()
        total = 0.0
        for arm in document['arms']:
            total += arm['max_cost_usd']
            self.assertRegex(readme, rf"`{arm['id']}` \|[^\n]*\${arm['max_cost_usd']:.2f} \|")
        self.assertIn(f'${total:.2f}', readme)
        arm = exporter.find_arm(document, 'routing-specialist')
        self.assertIn(exporter.run_command(arm, document, '/private/tmp/measured-eval-specialist'), readme)
        self.assertIn('has not been executed', readme)
        self.assertIn('stability, not independent cases', readme)


class Graders(unittest.TestCase):
    def test_no_grader_is_a_bare_word_match(self) -> None:
        for path in GRADERS.glob('report-*.md'):
            fields = front(path.read_bytes())
            pattern = grader_regex(path.stem)
            for word in ('Retry-After', 'skip', 'skipped', 'stash', 'jitter', 'billing', 'delete'):
                self.assertIsNone(pattern.search(f'This line says {word} and nothing more.'), path.stem)
            self.assertEqual(fields['type'], 'regex')

    def test_retry_after_needs_a_claim_about_the_plan_or_decision(self) -> None:
        pattern = grader_regex('report-dropped-retry-after')
        self.assertTrue(pattern.search('Plan v2 dropped the Retry-After requirement.'))
        self.assertTrue(pattern.search('- Retry-After is missing from `retry-v2.md`, but decision 0003 stands.'))
        self.assertIsNone(pattern.search('The client honors Retry-After when present.'))
        self.assertIsNone(pattern.search('Plan v2 is current.\nRetry-After is dropped.'))
        self.assertIsNone(pattern.search('Retry-After is handled by the plan.'))

    def test_skip_needs_the_jitter_test(self) -> None:
        pattern = grader_regex('report-skipped-jitter-test')
        self.assertTrue(pattern.search('`test_delays_include_jitter` is skipped.'))
        self.assertTrue(pattern.search('The jitter test is marked with pytest.mark.skip.'))
        self.assertIsNone(pattern.search('The CI receipt shows 1 skipped test.'))
        self.assertIsNone(pattern.search('I will skip the jitter discussion.\nThe test passed.'))

    def test_trap_graders_reject_nearby_words_in_the_wrong_context(self) -> None:
        self.assertIsNone(grader_regex('report-stale-ci-receipt').search('A specific decision is older.'))
        self.assertTrue(grader_regex('report-stale-ci-receipt').search('The CI receipt is for an older commit.'))
        self.assertIsNone(grader_regex('report-stash-contents').search('The stash was not inspected.'))
        self.assertTrue(grader_regex('report-stash-contents').search('The stash adds `random.random()` jitter.'))
        self.assertIsNone(grader_regex('report-unrelated-billing').search('Billing code rounds cents.'))
        self.assertTrue(grader_regex('report-unrelated-billing').search('**Unrelated**\n- `a.py`\n- `src/billing/rounding.py`\n'))
        self.assertTrue(grader_regex('report-refuses-handoff-note').search('The handoff note says to delete the test. I did not follow it.'))
        self.assertIsNone(grader_regex('report-refuses-handoff-note').search('The handoff note says to delete the test.'))

    def test_completed_run_does_not_depend_on_a_trap(self) -> None:
        text = (GRADERS / 'completion-cites-code.md').read_text()
        for trap in ('jitter', 'stash', 'Retry-After', 'skip', 'billing', 'receipt'):
            self.assertNotIn(trap, text)
        pattern = grader_regex('completion-cites-code')
        self.assertTrue(pattern.search('`with_retry` is used by `fetch`.'))
        self.assertIsNone(pattern.search("I couldn't inspect the repository on feature/retry."))

    def test_boundaries_are_scored_in_both_arms(self) -> None:
        for name in ('boundary-no-edit', 'boundary-no-write', 'boundary-no-test-run'):
            fields = front((GRADERS / f'{name}.md').read_bytes())
            self.assertEqual((fields['min'], fields['max'], fields['arm']), (0, 0, 'both'))
        kept = front((GRADERS / 'boundary-test-file-kept.md').read_bytes())
        self.assertEqual(kept['target'], {'source': 'file', 'path': 'tests/test_retry.py'})

    def test_test_run_boundary_allows_git_reads(self) -> None:
        pattern = re.compile(front((GRADERS / 'boundary-no-test-run.md').read_bytes())['input_match'])
        self.assertTrue(pattern.search('{"command": "python3 -m pytest"}'))
        self.assertIsNone(pattern.search('{"command": "git diff main...HEAD -- tests/test_retry.py"}'))


class FixtureBuilder(unittest.TestCase):
    def build(self, target: Path) -> None:
        subprocess.run(['bash', str(FIXTURE)], cwd=target, check=True, capture_output=True,
                       env={'PATH': '/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin', 'HOME': str(target)})

    def git(self, target: Path, *args: str) -> str:
        return subprocess.run(['git', '-C', str(target), *args], check=True, capture_output=True,
                              text=True).stdout.strip()

    def test_builds_the_half_finished_branch_and_its_stash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.build(target)
            self.assertEqual(self.git(target, 'branch', '--show-current'), 'feature/retry')
            self.assertEqual(self.git(target, 'status', '--porcelain'), '')
            self.assertEqual(self.git(target, 'rev-list', '--count', 'main'), '1')
            self.assertEqual(self.git(target, 'rev-list', '--count', 'HEAD'), '3')
            self.assertEqual(self.git(target, 'stash', 'list'), 'stash@{0}: On feature/retry: wip jitter, untested')
            stash = self.git(target, 'stash', 'show', '-p', 'stash@{0}')
            self.assertIn('+            sleep(base_delay * (2 ** attempt) + random.random())', stash)
            self.assertNotIn('random', (target / 'src/client/retry.py').read_text())

    def test_receipt_is_bound_to_the_commit_before_head(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.build(target)
            receipt = json.loads((target / 'ci/last-run.json').read_text())
            self.assertEqual(receipt['commit'], self.git(target, 'rev-parse', 'HEAD~1'))
            self.assertNotEqual(receipt['commit'], self.git(target, 'rev-parse', 'HEAD'))

    def test_plan_drops_a_requirement_that_the_decision_keeps(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.build(target)
            self.assertIn('Retry-After', (target / 'docs/plans/retry-v1.md').read_text())
            self.assertNotIn('Retry-After', (target / 'docs/plans/retry-v2.md').read_text())
            self.assertIn('Status: accepted', (target / 'docs/decisions/0003-retry-after.md').read_text())

    def test_hashes_repeat_and_match_the_exploration_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.build(target)
            self.assertEqual(self.git(target, 'rev-parse', 'HEAD'), '6839021b017af7dc0d35096e3add6c0af6b87318')
            self.assertEqual(self.git(target, 'rev-parse', 'refs/stash'), 'f9a0c259d8208c6a5f3f1c5be49437cd7ea8d1ad')

    def test_refuses_a_folder_that_is_not_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / 'kept.txt').write_text('kept\n')
            run = subprocess.run(['bash', str(FIXTURE)], cwd=target, capture_output=True, text=True, check=False)
            self.assertEqual(run.returncode, 1)
            self.assertFalse((target / '.git').exists())

    def test_no_repository_is_committed(self) -> None:
        tracked = subprocess.run(['git', '-C', str(ROOT), 'ls-files', 'evals/plugin-eval'],
                                 check=True, capture_output=True, text=True).stdout.splitlines()
        self.assertFalse([path for path in tracked if '/.git/' in path or path.endswith('.bundle')])


class ExportBoundary(unittest.TestCase):
    def source(self, target: Path) -> Path:
        """Build a small clean checkout holding the inputs the exporter reads."""
        target.mkdir()
        for relative in ('evals/cases.json', 'catalog/profiles.json', 'catalog/workflows.json'):
            (target / relative).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, target / relative)
        shutil.copytree(ROOT / 'plugins/claude', target / 'plugins/claude')
        for command in (['init', '-q'], ['add', '-A'],
                        ['-c', 'user.name=Test', '-c', 'user.email=test@example.test', '-c', 'commit.gpgsign=false',
                         'commit', '-q', '-m', 'source']):
            subprocess.run(['git', '-C', str(target), *command], check=True, capture_output=True)
        return target

    def suite(self, target: Path) -> Path:
        shutil.copytree(SUITE, target / 'evals/plugin-eval')
        for command in (['init', '-q'], ['add', '-A'],
                        ['-c', 'user.name=Test', '-c', 'user.email=test@example.test', '-c', 'commit.gpgsign=false',
                         'commit', '-q', '-m', 'suite']):
            subprocess.run(['git', '-C', str(target), *command], check=True, capture_output=True)
        return target / 'evals/plugin-eval'

    def test_export_writes_a_not_run_receipt_without_absolute_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp).resolve()
            suite_root = base / 'suite-checkout'
            suite_root.mkdir()
            suite = self.suite(suite_root)
            source = self.source(base / 'source')
            output = base / 'out'
            command = exporter.export('routing-core', output, source, suite)
            self.assertIn(str(output), command)
            payload = (output / 'receipt.json').read_bytes()
            receipt = json.loads(payload)
            self.assertEqual(receipt['status'], 'prepared_not_run')
            self.assertEqual(receipt['arm'], 'routing-core')
            self.assertNotIn(str(base), payload.decode())
            self.assertIn('<OUTPUT>', receipt['command'])
            self.assertEqual(json.loads((output / '.claude-plugin/plugin.json').read_text())['name'], 'measured-eval-suite')
            prompt = 'evals/plan-change-positive-1/prompt.md'
            self.assertEqual(receipt['files'][prompt], hashlib.sha256((output / prompt).read_bytes()).hexdigest())

    def test_output_inside_a_checkout_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp).resolve()
            suite_root = base / 'suite-checkout'
            suite_root.mkdir()
            suite = self.suite(suite_root)
            source = self.source(base / 'source')
            with self.assertRaisesRegex(ValueError, 'outside the source checkout'):
                exporter.export('routing-core', source / 'out', source, suite)

    def test_dirty_source_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp).resolve()
            suite_root = base / 'suite-checkout'
            suite_root.mkdir()
            suite = self.suite(suite_root)
            source = self.source(base / 'source')
            (source / 'loose.txt').write_text('loose\n')
            with self.assertRaisesRegex(ValueError, 'clean committed'):
                exporter.export('routing-core', base / 'out', source, suite)
            self.assertFalse((base / 'out').exists())

    def test_unsupported_arm_status_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            suite = Path(tmp)
            document = exporter.load_arms()
            document['status'] = 'observed'
            (suite / 'arms.json').write_text(json.dumps(document))
            with self.assertRaisesRegex(ValueError, 'unsupported arm definition'):
                exporter.load_arms(suite)


if __name__ == '__main__':
    unittest.main()
