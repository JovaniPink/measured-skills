"""HTTP content coding must not hide changes or manufacture document drift."""
from __future__ import annotations

from datetime import date
import gzip
import hashlib
import io
import json
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
    def test_owasp_initiative_taxonomy_order_preserves_content_changes(self) -> None:
        url = 'https://genai.owasp.org/wp-json/wp/v2/pages/50812'
        markup = ('<div data-elementor-type="loop-item" data-elementor-id="42" '
                  'class="widget category-b category-a tag-y tag-x">Resource</div>')

        def marker(body: str, address: str = url) -> tuple[str, str]:
            payload = json.dumps({'content': {'rendered': body}}).encode()
            with patch('check_upstream_freshness.urllib.request.urlopen', return_value=Response(payload, None)):
                return freshness._fetch_marker(address, 'normalized-content-sha256')

        reordered = markup.replace('category-b category-a', 'category-a category-b')
        self.assertEqual(marker(markup), marker(reordered))
        for original, mutation in [('category-a', 'category-c'), ('tag-x', 'tag-z'), ('Resource', 'Resource link')]:
            self.assertNotEqual(marker(markup), marker(markup.replace(original, mutation)))
        other_page = url.replace('50812', '123')
        self.assertNotEqual(marker(markup, other_page), marker(reordered, other_page))

    def test_owasp_audience_and_team_order_preserves_links_labels_and_other_markup(self) -> None:
        url = 'https://genai.owasp.org/wp-json/wp/v2/pages/50812'
        item = ('<a href="https://genai.owasp.org/learning_persona/{}/" '
                'class="elementor-post-info__terms-list-item">{}</a>')
        first, second = item.format('alpha', 'Alpha'), item.format('beta', 'Beta')
        wrapper = '<span class="elementor-post-info__terms-list">\n\t{}\t</span>'
        card = '<div data-elementor-type="loop-item" data-elementor-id="42" class="team_area-a team_area-b">'

        def marker(markup: str, address: str = url) -> str:
            body = json.dumps({'content': {'rendered': markup}}).replace('/', r'\/').encode()
            return freshness._normalized_marker(address, body)

        original = card + wrapper.format(first + ', ' + second) + '</div>'
        reorder = card.replace('team_area-a team_area-b', 'team_area-b team_area-a')
        reordered = reorder + wrapper.format(second + ', ' + first) + '</div>'
        self.assertEqual(marker(original), marker(reordered))
        for old, new in [('team_area-a', 'team_area-c'), ('/alpha/', '/gamma/'), ('Alpha', 'Gamma'),
                         (second, first), (', ' + second, '')]:
            self.assertNotEqual(marker(original), marker(original.replace(old, new)))
        self.assertNotEqual(marker(first + ', ' + second), marker(second + ', ' + first))
        other = url.replace('50812', '123')
        self.assertNotEqual(marker(original, other), marker(reordered, other))

    def marker(self, payload: bytes, encoding: str | None, kind: str = 'content-sha256') -> tuple[str, str]:
        with patch('check_upstream_freshness.urllib.request.urlopen', return_value=Response(payload, encoding)):
            return freshness._fetch_marker('https://antigravity.google/docs/skills.md', kind)

    def test_swift_landing_fingerprint_tracks_body_despite_deployment_etags(self) -> None:
        url = 'https://docs.swift.org/latest/documentation/'
        def fetch(body: bytes, etag: str) -> tuple[str, str]:
            response = Response(body, None)
            response.headers['ETag'] = etag
            with patch('check_upstream_freshness.urllib.request.urlopen', return_value=response):
                return freshness._fetch_marker(url)
        marker = fetch(b'Swift index', '"one"')
        self.assertEqual(('content-sha256', hashlib.sha256(b'Swift index').hexdigest()), marker)
        self.assertEqual(marker, fetch(b'Swift index', '"two"'))
        self.assertNotEqual(marker, fetch(b'Changed index', '"one"'))

    def test_signal_fingerprint_preserves_document_and_telemetry_script_identity(self) -> None:
        url = 'https://opentelemetry.io/docs/concepts/signals/'
        body = (b'<p>Traces</p><script async id="netlify-rum-container" src="/.netlify/scripts/rum" '
                b'data-netlify-deploy-context="production" data-netlify-cwv-token="abc.def.ghi"></script>')
        def fetch(payload: bytes, address: str = url) -> tuple[str, str]:
            with patch('check_upstream_freshness.urllib.request.urlopen', return_value=Response(payload, None)):
                return freshness._fetch_marker(address)
        marker = fetch(body)
        self.assertEqual('normalized-content-sha256', marker[0])
        changed_token = body.replace(b'abc.def.ghi', b'abc.new.sig')
        self.assertEqual(marker, fetch(changed_token))
        for old, new in [(b'Traces', b'Metrics'), (b'/rum"', b'/other"'), (b'production', b'preview'),
                         (b'netlify-rum-container', b'other'), (b'abc.def.ghi', b'unrecognized')]:
            self.assertNotEqual(marker, fetch(body.replace(old, new)))
        other_url = url + 'traces/'
        self.assertNotEqual(freshness._normalized_marker(other_url, body),
                            freshness._normalized_marker(other_url, changed_token))

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
