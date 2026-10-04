#!/usr/bin/env python3
"""Scan all publishable repository content for public-boundary violations."""

from __future__ import annotations

import re
import subprocess
import zipfile
from pathlib import Path
from typing import Iterable

from cataloglib import ROOT


EXACT_TOKEN_PATTERNS = (
    re.compile(r"```.*?```", re.DOTALL),
    re.compile(r"`[^`\n]+`"),
    re.compile(r"\[[^\]\n]+\]\(https?://[^)\s]+\)"),
    re.compile(r"https?://[^\s<>]+"),
    re.compile(r"(?<![A-Za-z0-9])(?:[A-Za-z0-9._-]+/)+[A-Za-z0-9._-]+"),
    re.compile(r"(?<![A-Za-z0-9])--[A-Za-z0-9][A-Za-z0-9-]*"),
)


def _patterns(denylist_path: Path | None = None) -> list[tuple[str, re.Pattern[str]]]:
    # Split sensitive-looking literals so the scanner can inspect its own source.
    patterns = [
        ("absolute macOS user path", re.compile("/" + "Users/[^/\\s]+/")),
        ("absolute Linux user path", re.compile("/" + "home/[^/\\s]+/")),
        ("private SSH remote", re.compile("git" + r"@[A-Za-z0-9_.-]+:")),
        ("work-repository path", re.compile("src/" + "work/", re.IGNORECASE)),
        ("GitHub token", re.compile("gh" + r"[pousr]_[A-Za-z0-9]{20,}")),
        ("OpenAI-style secret", re.compile("s" + r"k-[A-Za-z0-9]{20,}")),
        ("AWS access key", re.compile("AK" + r"IA[0-9A-Z]{16}")),
        ("Anthropic API key", re.compile("(?<![A-Za-z0-9])s" + r"k-ant-[A-Za-z0-9_-]{20,}")),
        ("prefixed OpenAI-style key", re.compile("(?<![A-Za-z0-9])s" + r"k-(?:proj|svcacct|admin)-[A-Za-z0-9_-]{20,}")),
        ("GitHub fine-grained token", re.compile("github" + r"_pat_[A-Za-z0-9_]{22,}")),
        ("Slack token", re.compile("xo" + r"x[abeoprs]-[A-Za-z0-9-]{10,}")),
        ("Google API key", re.compile("AI" + r"za[0-9A-Za-z_-]{35}")),
        ("private key block", re.compile("BEGIN " + r"(?:RSA |EC |OPENSSH )?PRIVATE KEY")),
        ("unsupported universal validation claim", re.compile(r"all (?:clients|validators|surfaces) (?:pass|passed|are supported)", re.IGNORECASE)),
        ("ASCII control character", re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]")),
        ("non-ASCII character", re.compile(r"[^\x00-\x7F]")),
        (
            "non-US English spelling",
            re.compile(
                r"\b(?:"
                + "|".join(
                    (
                        "author" + "ised",
                        "author" + "ise",
                        "author" + "ising",
                        "author" + "isation",
                        "unauthor" + "ised",
                        "behav" + "iour",
                        "behav" + "iours",
                        "behav" + "ioural",
                        "col" + "our",
                        "col" + "ours",
                        "col" + "oured",
                        "col" + "ouring",
                        "optim" + "ise",
                        "optim" + "ised",
                        "optim" + "ising",
                        "optim" + "isation",
                        "organi" + "sation",
                        "organi" + "sations",
                        "organi" + "se",
                        "organi" + "sed",
                        "organi" + "sing",
                        "lic" + "ence",
                        "lic" + "ences",
                        "lic" + "enced",
                        "unlic" + "enced",
                        "cen" + "tre",
                        "cen" + "tres",
                        "cen" + "tred",
                        "cen" + "tring",
                        "cata" + "logue",
                        "cata" + "logues",
                        "ana" + "lyse",
                        "ana" + "lysed",
                        "ana" + "lysing",
                        "def" + "ence",
                        "arte" + "fact",
                        "arte" + "facts",
                        "ful" + "fil",
                        "ful" + "filled",
                        "ful" + "filling",
                        "model" + "ling",
                        "model" + "led",
                        "model" + "ler",
                        "pro" + "gramme",
                        "pro" + "grammes",
                        "serial" + "ise",
                        "serial" + "ised",
                        "serial" + "ising",
                        "initial" + "ise",
                        "initial" + "ised",
                        "initial" + "ising",
                        "recog" + "nise",
                        "recog" + "nised",
                        "recog" + "nising",
                        "travel" + "ling",
                        "travel" + "led",
                        "travel" + "ler",
                        "cancel" + "led",
                        "cancel" + "ling",
                        "la" + "bour",
                        "fa" + "vour",
                        "fa" + "vours",
                        "fa" + "voured",
                        "fa" + "vouring",
                        "fa" + "vourite",
                        "fa" + "vourites",
                        "gr" + "ey",
                        "among" + "st",
                        "whil" + "st",
                        "priorit" + "ise",
                        "priorit" + "ised",
                        "priorit" + "ising",
                        "special" + "ise",
                        "special" + "ised",
                        "special" + "ising",
                        "summar" + "ise",
                        "summar" + "ised",
                        "summar" + "ising",
                        "custom" + "ise",
                        "custom" + "ised",
                        "custom" + "ising",
                        "judge" + "ment",
                        "label" + "led",
                        "label" + "ling",
                        "focus" + "sed",
                        "focus" + "sing",
                        "pract" + "ise",
                        "pract" + "ised",
                        "pract" + "ising",
                        "ma" + "ths",
                        "che" + "que",
                        "acknowledge" + "ment",
                    )
                )
                + r")\b",
                re.IGNORECASE,
            ),
        ),
    ]
    selected_denylist = denylist_path or ROOT / ".local-boundary-denylist"
    if selected_denylist.is_file():
        for line in selected_denylist.read_text(encoding="utf-8").splitlines():
            value = line.strip()
            if value and not value.startswith("#"):
                patterns.append(("local denylist", re.compile(re.escape(value), re.IGNORECASE)))
    return patterns


def _publishable_paths(root: Path) -> list[Path]:
    """Return tracked and non-ignored files, falling back to a filesystem walk."""

    try:
        result = subprocess.run(
            ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
            cwd=root,
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return sorted(
            path
            for path in root.rglob("*")
            if path.is_file() and ".git" not in path.relative_to(root).parts
        )
    return sorted(root / item.decode("utf-8") for item in result.stdout.split(b"\0") if item)


def _scan_text(
    label: str,
    text: str,
    patterns: Iterable[tuple[str, re.Pattern[str]]],
) -> list[str]:
    errors: list[str] = []
    for finding, pattern in patterns:
        selected_text = _mask_exact_tokens(text) if finding == "non-US English spelling" else text
        for match in pattern.finditer(selected_text):
            line = text.count("\n", 0, match.start()) + 1
            errors.append(f"{label}:{line}: {finding}")
    return errors


def _mask_exact_tokens(text: str) -> str:
    """Blank exact-token contexts while preserving offsets and line numbers."""

    masked = text
    for pattern in EXACT_TOKEN_PATTERNS:
        masked = pattern.sub(lambda match: re.sub(r"[^\n]", " ", match.group(0)), masked)
    return masked


# Archives are scanned member by member in _scan_archives.
BINARY_SUFFIXES = {".zip"}


def _scan_file(path: Path, label: str, patterns: list[tuple[str, re.Pattern[str]]]) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return []
    except UnicodeDecodeError:
        if path.suffix.lower() in BINARY_SUFFIXES:
            return []
        return [f"{label}: not valid UTF-8 text, so the boundary scan cannot read it"]
    return _scan_text(label, text, patterns)


def _scan_archives(patterns: list[tuple[str, re.Pattern[str]]]) -> list[str]:
    errors: list[str] = []
    package_root = ROOT / "dist" / "claude-ai"
    if not package_root.is_dir():
        return errors
    for archive_path in sorted(package_root.glob("*.zip")):
        try:
            with zipfile.ZipFile(archive_path) as archive:
                for member in sorted(archive.namelist()):
                    label = f"{archive_path.relative_to(ROOT)}!{member}"
                    try:
                        text = archive.read(member).decode("utf-8")
                    except KeyError:
                        continue
                    except UnicodeDecodeError:
                        errors.append(f"{label}: not valid UTF-8 text, so the boundary scan cannot read it")
                        continue
                    errors.extend(_scan_text(label, text, patterns))
        except (OSError, zipfile.BadZipFile) as error:
            errors.append(f"{archive_path.relative_to(ROOT)}: invalid ZIP: {error}")
    return errors


def scan(
    paths: Iterable[Path] | None = None,
    denylist_path: Path | None = None,
    include_packages: bool = True,
) -> list[str]:
    patterns = _patterns(denylist_path)
    errors: list[str] = []
    selected_paths = list(paths) if paths is not None else _publishable_paths(ROOT)
    for path in sorted(selected_paths):
        try:
            relative = path.relative_to(ROOT)
            label = relative.as_posix()
        except ValueError:
            label = path.as_posix()
        errors.extend(_scan_file(path, label, patterns))
    if include_packages and paths is None:
        errors.extend(_scan_archives(patterns))
    return errors


def main() -> int:
    errors = scan()
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("Public/private boundary scan passed for all publishable files and packages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
