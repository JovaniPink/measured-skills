#!/usr/bin/env python3
"""Check provenance review age and optionally compare pinned upstream bytes."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.request
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

from cataloglib import ROOT, VERSION


NORMALIZED_HTML_HOSTS = frozenset(
    {
        "airc.nist.gov",
        "developers.googleblog.com",
        "genai.owasp.org",
        "learn.chatgpt.com",
        "trailhead.salesforce.com",
        "www.drupal.org",
    }
)
TRAILING_WHITESPACE_NORMALIZED_URLS = frozenset(
    {"https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/"}
)
# Streamed pages whose markup changes per request while their readable text does not.
# Each entry is a reviewed exception; the marker hashes visible text only.
VISIBLE_TEXT_URLS = frozenset(
    {"https://owasp.org/www-project-application-security-verification-standard/"}
)
NON_VISIBLE_TAGS = frozenset({"noscript", "script", "style", "svg", "template"})


class _VisibleText(HTMLParser):
    """Collect text that a reader would see, skipping scripts, styles, and templates."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in NON_VISIBLE_TAGS:
            self.depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in NON_VISIBLE_TAGS and self.depth:
            self.depth -= 1

    def handle_data(self, data: str) -> None:
        if not self.depth:
            self.parts.append(data)


def _visible_text_sha256(payload: bytes) -> str:
    """Hash the readable text of a page, ignoring markup and script chunk order."""

    parser = _VisibleText()
    parser.feed(payload.decode("utf-8"))
    parser.close()
    text = " ".join(" ".join(parser.parts).split())
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _normalized_content(payload: bytes) -> str:
    """Remove known per-request HTML values while preserving authority content."""

    text = payload.decode("utf-8")
    substitutions = (
        (
            r'(<meta name="csrf-token" content=")[^"]*(" />)',
            r'\1[volatile]\2',
        ),
        (
            r'"queueTime":\d+,"applicationTime":\d+',
            '"queueTime":0,"applicationTime":0',
        ),
        (
            r"(<meta content=')[^']+(' name='ua:temp_visitor_id'>)",
            r"\1[volatile]\2",
        ),
        (
            r'(name="form_build_id" value=")[^"]+(")',
            r'\1[volatile]\2',
        ),
        (
            r'(view-dom-id-)[A-Fa-f0-9]{32}',
            r'\1[volatile]',
        ),
        (
            r'("theme_token":")[^"]+(")',
            r'\1[volatile]\2',
        ),
        (
            r'(nonce=")[^"]+(")',
            r'\1[volatile]\2',
        ),
        (
            r'<script nonce="\[volatile\]">\(function\(\)\{.*?/cdn-cgi/challenge-platform/.*?</script>',
            "",
        ),
        (
            r'<script[^>]*src="https://static\.cloudflareinsights\.com/beacon\.min\.js/[^"]+"[^>]*></script>',
            "",
        ),
        (
            # WordPress batcache timing comment, in its freshly generated or cached form.
            r"<!--\s*(?:generated \d+ seconds ago\s+)?generated in [\d.]+ seconds\s+"
            r"(?:served from batcache in [\d.]+ seconds\s+expires in \d+ seconds"
            r"|\d+ bytes batcached for \d+ seconds)\s*-->",
            "",
        ),
    )
    for pattern, replacement in substitutions:
        text = re.sub(pattern, replacement, text)
    return text


def _normalized_content_sha256(payload: bytes, strip_trailing: bool = False) -> str:
    """Hash authority content after removing known per-request HTML values."""

    content = _normalized_content(payload)
    if strip_trailing:
        content = content.rstrip()
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected object: {path}")
    return value


def _fetch_marker(url: str, preferred_kind: str | None = None) -> tuple[str, str]:
    request = urllib.request.Request(url, headers={"User-Agent": "JovaniPink-skills-freshness/0.8"})
    with urllib.request.urlopen(request, timeout=30) as response:
        etag = response.headers.get("ETag")
        last_modified = response.headers.get("Last-Modified")
        host = (urlparse(url).hostname or "").casefold()
        if url in VISIBLE_TEXT_URLS and preferred_kind in (None, "visible-text-sha256"):
            return "visible-text-sha256", _visible_text_sha256(response.read())
        if preferred_kind == "visible-text-sha256":
            raise ValueError(f"visible-text-sha256 is not allowed for {url}")
        if preferred_kind == "normalized-content-sha256":
            return "normalized-content-sha256", _normalized_content_sha256(
                response.read(), strip_trailing=url in TRAILING_WHITESPACE_NORMALIZED_URLS
            )
        if preferred_kind == "content-sha256":
            return "content-sha256", hashlib.sha256(response.read()).hexdigest()
        if preferred_kind == "etag" and etag and not etag.startswith("W/"):
            return "etag", etag
        if preferred_kind == "last-modified" and last_modified:
            return "last-modified", last_modified
        if preferred_kind is not None:
            return "content-sha256", hashlib.sha256(response.read()).hexdigest()
        if host in NORMALIZED_HTML_HOSTS:
            return "normalized-content-sha256", _normalized_content_sha256(
                response.read(), strip_trailing=url in TRAILING_WHITESPACE_NORMALIZED_URLS
            )
        if etag and not etag.startswith("W/"):
            return "etag", etag
        if last_modified:
            return "last-modified", last_modified
        return "content-sha256", hashlib.sha256(response.read()).hexdigest()


def source_urls() -> list[str]:
    catalog = _load(ROOT / "provenance" / "catalog.json")
    entries = catalog.get("entries", [])
    if not isinstance(entries, list):
        raise ValueError("provenance catalog entries must be an array")
    urls: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        source_url = entry.get("source_url")
        if isinstance(source_url, str):
            urls.add(source_url)
    reviews = _load(ROOT / "catalog" / "upstream-reviews.json")
    review_records = reviews.get("reviews", [])
    if not isinstance(review_records, list):
        raise ValueError("upstream review records must be an array")
    for review in review_records:
        if not isinstance(review, dict):
            continue
        review_url = review.get("url")
        if isinstance(review_url, str):
            urls.add(review_url)
    return sorted(urls)


def refresh_pins(output: Path | None = None) -> Path:
    sources: list[dict[str, str]] = []
    for url in source_urls():
        try:
            marker_kind, marker_value = _fetch_marker(url)
        except Exception as error:
            raise RuntimeError(f"cannot pin {url}: {type(error).__name__}: {error}") from error
        sources.append({"source_url": url, "marker_kind": marker_kind, "marker_value": marker_value})
    value = {
        "$schema": "./upstream-pins-schema.json",
        "catalog_version": VERSION,
        "reviewed_on": date.today().isoformat(),
        "max_review_age_days": 90,
        "sources": sources,
    }
    target = (output or ROOT / "catalog" / "upstream-pins.json").resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    return target


def check(online: bool = False, today: date | None = None) -> tuple[list[str], dict[str, object]]:
    today = today or date.today()
    pins = _load(ROOT / "catalog" / "upstream-pins.json")
    raw_sources = pins.get("sources", [])
    if not isinstance(raw_sources, list):
        raise ValueError("upstream pin sources must be an array")
    expected: dict[str, tuple[str, str]] = {}
    for item in raw_sources:
        if not isinstance(item, dict):
            continue
        source_url = item.get("source_url")
        marker_kind = item.get("marker_kind")
        marker_value = item.get("marker_value")
        if isinstance(source_url, str) and isinstance(marker_kind, str) and isinstance(marker_value, str):
            expected[source_url] = (marker_kind, marker_value)
    errors: list[str] = []
    urls = source_urls()
    missing = sorted(set(urls) - set(expected))
    extra = sorted(set(expected) - set(urls))
    if missing:
        errors.append(f"upstream pins missing provenance sources: {missing}")
    if extra:
        errors.append(f"upstream pins contain unused sources: {extra}")
    reviewed_on_value = pins.get("reviewed_on")
    maximum_value = pins.get("max_review_age_days")
    if not isinstance(reviewed_on_value, str):
        raise ValueError("upstream pin review date must be a string")
    if not isinstance(maximum_value, int) or isinstance(maximum_value, bool):
        raise ValueError("upstream pin maximum review age must be an integer")
    reviewed_on = date.fromisoformat(reviewed_on_value)
    maximum = maximum_value
    if (today - reviewed_on).days > maximum:
        errors.append(f"security re-review is overdue: pins reviewed {reviewed_on.isoformat()}, maximum age {maximum} days")
    records: list[dict[str, str]] = []
    if online:
        for url in urls:
            try:
                expected_marker = expected.get(url)
                preferred_kind = expected_marker[0] if expected_marker is not None else None
                observed_kind, observed_value = _fetch_marker(url, preferred_kind=preferred_kind)
                observed = f"{observed_kind}:{observed_value}"
                result = "pass" if expected_marker == (observed_kind, observed_value) else "changed"
                if result == "changed":
                    errors.append(f"upstream content changed: {url}")
            except Exception as error:
                observed = "unavailable"
                result = "blocked"
                errors.append(f"upstream check blocked for {url}: {type(error).__name__}: {error}")
            expected_text = "missing" if expected.get(url) is None else f"{expected[url][0]}:{expected[url][1]}"
            records.append({"source_url": url, "expected_marker": expected_text, "observed_marker": observed, "result": result})
    report = {
        "catalog_version": VERSION,
        "checked_on": today.isoformat(),
        "online": online,
        "result": "pass" if not errors else "fail",
        "records": records,
        "errors": errors,
    }
    return errors, report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--online", action="store_true")
    parser.add_argument("--refresh-pins", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.refresh_pins:
        target = refresh_pins(args.output)
        print(f"Wrote reviewed upstream pins to {target}")
        return 0
    errors, report = check(online=args.online)
    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("Upstream provenance freshness passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
