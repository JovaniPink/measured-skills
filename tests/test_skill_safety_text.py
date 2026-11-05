"""Pin the safety rules added after the November 5 skill security review."""
from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
STACK_RULE = (
    '- Repository scripts and tests run code, and dependency checks can contact registries. '
    'Run a gate only when the user asked for checks and trusts the repository. '
    'Otherwise, name it as the next safe gate.'
)


def skill(name: str) -> str:
    return (ROOT / 'skills' / name / 'SKILL.md').read_text()


class SkillSafetyTextTests(unittest.TestCase):
    def test_every_stack_skill_keeps_the_repository_trust_rule(self) -> None:
        names = sorted(p.name for p in (ROOT / 'skills').glob('stack-*'))
        self.assertEqual(len(names), 13)
        for name in names:
            with self.subTest(name):
                boundaries = skill(name).split('## Boundaries', 1)[1].split('\n## ', 1)[0]
                self.assertIn(STACK_RULE, boundaries)

    def test_run_project_checks_asks_before_running_untrusted_code(self) -> None:
        text = skill('run-project-checks')
        self.assertIn('run code with your permissions', text)
        self.assertIn('read what a command runs and ask before running it', text)
        self.assertIn('not one the user has said they trust', text)

    def test_launch_readiness_stays_read_only_on_platforms(self) -> None:
        text = skill('check-launch-readiness')
        self.assertIn('read-only queries', text)
        self.assertIn('Do not submit production forms', text)

    def test_public_boundary_edits_only_on_request_and_masks_secrets(self) -> None:
        text = skill('review-public-boundary')
        self.assertIn('Edit files only when the request asks for redaction', text)
        self.assertIn('Never quote a secret in a finding', text)

    def test_terraform_treats_real_backends_as_provider_access(self) -> None:
        text = skill('stack-terraform')
        self.assertIn('against a real backend as provider access', text)
        self.assertIn('terraform init -backend=false', text)


if __name__ == '__main__':
    unittest.main()
