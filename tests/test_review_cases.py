"""Deterministic integrity checks for the review casebook."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CASEBOOK_DIR = ROOT / 'docs' / 'review-cases'


class ReviewCasebookTests(unittest.TestCase):
    def test_casebook_files_exist_and_are_ascii(self) -> None:
        expected = {
            'README.md',
            'captured-review-case-2026-11-19.md',
            'disconfirmation-and-failure-cases.md',
            'preserved-corrections.md',
        }
        actual = {p.name for p in CASEBOOK_DIR.glob('*.md')}
        self.assertEqual(expected, actual)
        for path in sorted(CASEBOOK_DIR.glob('*.md')):
            text = path.read_text(encoding='utf-8')
            self.assertTrue(text.isascii(), f'Non-ASCII characters in {path.name}')

    def test_captured_review_pins_real_ancestors_and_five_dimensions(self) -> None:
        text = (CASEBOOK_DIR / 'captured-review-case-2026-11-19.md').read_text(encoding='utf-8')
        self.assertIn('Captured read-only code review', text)
        self.assertIn('Distinct from synthetic', text)
        shas = sorted(set(re.findall(r'\b[0-9a-f]{40}\b', text)))
        self.assertGreaterEqual(len(shas), 2, 'Expected base and head 40-char SHAs')
        for sha in shas:
            result = subprocess.run(
                ['git', 'merge-base', '--is-ancestor', sha, 'HEAD'],
                cwd=ROOT,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, f'Pinned SHA is not an ancestor of HEAD: {sha}')
        for dimension in (
            'Investigation coverage',
            'Claim assessment',
            'Disposition',
            'Verification',
            'Completion',
        ):
            self.assertIn(dimension, text)
        for marker in ('`supported`', '`cleared`', '`unresolved`', '`blocked`'):
            self.assertIn(marker, text)

    def test_synthetic_casebook_is_labeled_explicitly(self) -> None:
        text = (CASEBOOK_DIR / 'disconfirmation-and-failure-cases.md').read_text(encoding='utf-8')
        self.assertIn('Synthetic and reconstructed teaching cases', text)
        self.assertIn('competing explanation', text.lower())
        self.assertIn('review-nextjs-cache-auth', text)


if __name__ == '__main__':
    unittest.main()
