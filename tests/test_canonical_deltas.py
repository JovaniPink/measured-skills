"""Intentional content edits cannot erase the preserved naming-only checkpoint."""
from __future__ import annotations

import copy
import sys
from pathlib import Path
import unittest
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import canonical_deltas  # noqa: E402


class CanonicalDeltaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.before = {'skills/example/SKILL.md': b'original'}
        self.after = {'skills/example/SKILL.md': b'revised', 'skills/example/references/new.md': b'new'}
        self.record: dict[str, Any] = {
            'format_version': 1,
            'baseline_revision': canonical_deltas.BASELINE,
            'new_maintainer_acceptance': False,
            'changes': {p: {'before_sha256': canonical_deltas.digest(self.before.get(p)),
                            'after_sha256': canonical_deltas.digest(self.after.get(p)),
                            'review_reason': 'Reviewed bounded contract improvement.'}
                        for p in self.after},
        }

    def test_exact_reviewed_changes_pass(self) -> None:
        self.assertEqual([], canonical_deltas.validate(self.before, self.after, self.record))

    def test_unrecorded_added_removed_and_modified_files_fail(self) -> None:
        for current in ({}, {**self.after, 'skills/example/extra.md': b'extra'},
                        {**self.after, 'skills/example/SKILL.md': b'unreviewed'}):
            with self.subTest(current=current):
                self.assertTrue(canonical_deltas.validate(self.before, current, self.record))

    def test_baseline_tampering_and_stale_review_fail(self) -> None:
        self.assertTrue(canonical_deltas.validate({'skills/example/SKILL.md': b'tampered'}, self.after, self.record))
        for field, value in (('baseline_revision', 'a' * 40), ('new_maintainer_acceptance', True), ('changes', [])):
            bad = copy.deepcopy(self.record)
            bad[field] = value
            self.assertTrue(canonical_deltas.validate(self.before, self.after, bad))
        bad = copy.deepcopy(self.record)
        bad['changes']['skills/example/SKILL.md']['review_reason'] = ''
        self.assertTrue(canonical_deltas.validate(self.before, self.after, bad))

    def test_redundant_and_unsafe_records_fail(self) -> None:
        for path in ('../outside', 'skills/example/unchanged.md'):
            bad = copy.deepcopy(self.record)
            bad['changes'][path] = next(iter(self.record['changes'].values()))
            self.assertTrue(canonical_deltas.validate(self.before, self.after, bad))


if __name__ == '__main__':
    unittest.main()
