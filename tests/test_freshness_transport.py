"""HTTP content coding must not hide changes or manufacture document drift."""
from __future__ import annotations

from datetime import date
import gzip
import hashlib
import io
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import check_upstream_freshness as freshness  # noqa: E402


class Response(io.BytesIO):
    def __init__(self, payload: bytes, encoding: str | None) -> None:
        super().__init__(payload)
        self.headers = {'ETag': '"site-build"'}
        if encoding is not None:
            self.headers['Content-Encoding'] = encoding


class FreshnessTransportTests(unittest.TestCase):
    def marker(self, payload: bytes, encoding: str | None, kind: str = 'content-sha256') -> tuple[str, str]:
        with patch('check_upstream_freshness.urllib.request.urlopen', return_value=Response(payload, encoding)):
            return freshness._fetch_marker('https://antigravity.google/docs/skills.md', kind)

    def test_gzip_and_identity_bind_the_same_complete_document(self) -> None:
        body = b'# Source\r\nKeep permission checks.\n\n'
        expected = ('content-sha256', hashlib.sha256(body).hexdigest())
        for encoding, payload in ((None, body), ('identity', body), ('gzip', gzip.compress(body, mtime=1)),
                                  ('GZip', gzip.compress(body, mtime=2))):
            with self.subTest(encoding=encoding):
                self.assertEqual(expected, self.marker(payload, encoding))

    def test_decoded_body_changes_and_trailing_bytes_change_the_hash(self) -> None:
        original = b'# Source\nKeep permission checks.\n'
        for changed in (original.replace(b'Keep', b'Remove'), original + b'\n', original + b'new section\n'):
            with self.subTest(changed=changed):
                self.assertNotEqual(self.marker(gzip.compress(original), 'gzip'),
                                    self.marker(gzip.compress(changed), 'gzip'))
        joined = gzip.compress(original) + gzip.compress(b'additional member\n')
        self.assertEqual(('content-sha256', hashlib.sha256(original + b'additional member\n').hexdigest()),
                         self.marker(joined, 'gzip'))

    def test_corrupt_or_unsupported_content_coding_fails_closed(self) -> None:
        for payload, encoding in ((b'not gzip', 'gzip'), (gzip.compress(b'body')[:-3], 'gzip'),
                                  (b'body', 'br'), (b'body', 'gzip, br')):
            with self.subTest(encoding=encoding):
                with self.assertRaises((ValueError, OSError, EOFError)):
                    self.marker(payload, encoding)

    def test_existing_normalization_receives_decoded_bytes_only(self) -> None:
        body = b'<main>Keep every requirement.</main>\n'
        self.assertEqual(self.marker(body, None, 'normalized-content-sha256'),
                         self.marker(gzip.compress(body), 'gzip', 'normalized-content-sha256'))

    def test_unlabeled_bytes_are_not_sniffed_or_rewritten(self) -> None:
        payload = gzip.compress(b'body')
        self.assertEqual(('content-sha256', hashlib.sha256(payload).hexdigest()), self.marker(payload, None))

    def test_online_report_keeps_changes_and_decoding_failures_blocking(self) -> None:
        url = 'https://antigravity.google/docs/skills.md'
        body = b'# Source\nPreserve authority.\n'
        pins = {'reviewed_on': '2026-10-26', 'max_review_age_days': 90,
                'sources': [{'source_url': url, 'marker_kind': 'content-sha256',
                             'marker_value': hashlib.sha256(body).hexdigest()}]}
        for payload, expected in ((gzip.compress(body), 'pass'),
                                  (gzip.compress(body + b'changed'), 'changed'),
                                  (b'not gzip', 'blocked')):
            with self.subTest(expected=expected), \
                    patch.object(freshness, '_load', return_value=pins), \
                    patch.object(freshness, 'source_urls', return_value=[url]), \
                    patch('check_upstream_freshness.urllib.request.urlopen',
                          return_value=Response(payload, 'gzip')):
                errors, report = freshness.check(online=True, today=date(2026, 10, 26))
                self.assertEqual(expected != 'pass', bool(errors))
                self.assertEqual('pass' if expected == 'pass' else 'fail', report['result'])
                records = report['records']
                assert isinstance(records, list)
                self.assertEqual(expected, records[0]['result'])
