#!/usr/bin/env python3
"""Reject external implementation attribution from skill content."""

from __future__ import annotations

import re
import zipfile
from pathlib import Path

from cataloglib import ROOT


PROHIBITED = {
    "external implementation attribution": re.compile(
        r"\b(?:copied|adapted|derived) from (?:an? )?(?:external|third-party|upstream) skill\b",
        re.IGNORECASE,
    ),
    "external behavior attribution": re.compile(
        r"\bbased on (?:an? )?(?:external|third-party|upstream) skill(?: repository)?\b",
        re.IGNORECASE,
    ),
}


def _scan_text(label: str, text: str) -> list[str]:
    errors: list[str] = []
    for finding, pattern in PROHIBITED.items():
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            errors.append(f"{label}:{line}: {finding}")
    return errors


def _content_paths() -> list[Path]:
    roots = (ROOT / "skills", ROOT / "plugins" / "codex", ROOT / "plugins" / "claude", ROOT / "plugins" / "antigravity")
    return sorted(path for root in roots if root.is_dir() for path in root.rglob("*") if path.is_file())


def check(include_packages: bool = True) -> list[str]:
    errors: list[str] = []
    for path in _content_paths():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        errors.extend(_scan_text(path.relative_to(ROOT).as_posix(), text))
    if include_packages:
        for archive_path in sorted((ROOT / "dist" / "claude-ai").glob("*.zip")):
            with zipfile.ZipFile(archive_path) as archive:
                for member in archive.namelist():
                    try:
                        text = archive.read(member).decode("utf-8")
                    except UnicodeDecodeError:
                        continue
                    errors.extend(_scan_text(f"{archive_path.relative_to(ROOT)}!{member}", text))
    return errors


def main() -> int:
    errors = check()
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("Attribution-pattern scan passed for canonical, generated, and packaged skill content; this does not establish originality qualification.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
