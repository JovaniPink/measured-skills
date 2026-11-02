"""Shared, standard-library-only helpers for the portable skill catalog."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import TypedDict


ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.19.0"
CATALOG_NAME = "measured-skills"
PLUGIN_CATEGORY = "Developer Tools"

class PluginSpec(TypedDict):
    """Typed metadata used to generate both client plugin manifests."""

    display_name: str
    description: str
    short_description: str
    keywords: list[str]


PLUGIN_SPECS: dict[str, PluginSpec] = {'measured-workflows': {'display_name': 'Measured Workflows', 'description': 'Find a route, understand the work, plan, repair, and deliver within authority.', 'short_description': 'Workflows for focused engineering work', 'keywords': ['skills', 'workflows', 'engineering']}, 'measured-quality': {'display_name': 'Measured Quality', 'description': 'Check behavior, evidence, compatibility, security, and operational boundaries.', 'short_description': 'Quality for focused engineering work', 'keywords': ['skills', 'quality', 'engineering']}, 'measured-stacks': {'display_name': 'Measured Stacks', 'description': 'Apply language and platform guidance after discovering the project.', 'short_description': 'Stacks for focused engineering work', 'keywords': ['skills', 'stacks', 'engineering']}, 'measured-operations': {'display_name': 'Measured Operations', 'description': 'Clarify requirements, decisions, adoption, measurement, and incident learning.', 'short_description': 'Operations for focused engineering work', 'keywords': ['skills', 'operations', 'engineering']}}

def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    marker = "\n---\n"
    end = text.find(marker, 4)
    if end < 0:
        raise ValueError("SKILL.md has no closing frontmatter delimiter")
    return text[4:end], text[end + len(marker) :]


def _scalar(frontmatter: str, key: str) -> str:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", frontmatter)
    if not match:
        raise ValueError(f"missing frontmatter key: {key}")
    value = match.group(1).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value


def _metadata_scalar(frontmatter: str, key: str) -> str:
    match = re.search(rf"(?m)^\s{{2}}{re.escape(key)}:\s*(.+?)\s*$", frontmatter)
    if not match:
        raise ValueError(f"missing metadata key: {key}")
    value = match.group(1).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value


def read_skill_metadata(skill_dir: Path) -> dict[str, str]:
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    frontmatter, _ = split_frontmatter(text)
    result = {
        "name": _scalar(frontmatter, "name"),
        "description": _scalar(frontmatter, "description"),
        "license": _scalar(frontmatter, "license"),
        "author": _metadata_scalar(frontmatter, "author"),
        "version": _metadata_scalar(frontmatter, "version"),
        "plugin": _metadata_scalar(frontmatter, "plugin"),
        "invocation": _metadata_scalar(frontmatter, "invocation"),
        "provenance": _metadata_scalar(frontmatter, "provenance"),
        "risk_class": _metadata_scalar(frontmatter, "risk_class"),
    }
    result["claude_explicit"] = "true" if re.search(
        r"(?m)^disable-model-invocation:\s*true\s*$", frontmatter
    ) else "false"
    return result


def skill_names() -> tuple[str, ...]:
    root = ROOT / "skills"
    if not root.is_dir():
        return ()
    return tuple(sorted(path.name for path in root.iterdir() if path.is_dir()))


def revoked_skill_names(path: Path | None = None) -> frozenset[str]:
    registry = path or ROOT / "catalog" / "revocations.json"
    if not registry.is_file():
        return frozenset()
    value = json.loads(registry.read_text(encoding="utf-8"))
    entries = value.get("entries", []) if isinstance(value, dict) else []
    return frozenset(
        entry["skill"] for entry in entries
        if isinstance(entry, dict) and isinstance(entry.get("skill"), str)
    )


def filter_revoked(skills: tuple[str, ...], revoked: frozenset[str]) -> tuple[str, ...]:
    return tuple(skill for skill in skills if skill not in revoked)


def skills_by_plugin() -> dict[str, tuple[str, ...]]:
    grouped: dict[str, list[str]] = {}
    for skill in SKILLS:
        plugin = read_skill_metadata(ROOT / "skills" / skill)["plugin"]
        grouped.setdefault(plugin, []).append(skill)
    return {plugin: tuple(skills) for plugin, skills in sorted(grouped.items())}


def discovery_estimate(skills: list[str], client: str) -> int:
    """Count a reproducible native-layout listing, not an observed client prompt."""
    total = 0
    for skill in skills:
        metadata = read_skill_metadata(ROOT / "skills" / skill)
        path = f"plugins/{client}/{metadata['plugin']}/skills/{skill}/SKILL.md"
        total += len(f"{skill}\t{path}\t{metadata['description']}\n")
    return total


ALL_SKILLS = skill_names()
SKILLS = filter_revoked(ALL_SKILLS, revoked_skill_names())
EXPLICIT_SKILLS = frozenset(
    skill for skill in SKILLS if read_skill_metadata(ROOT / "skills" / skill)["invocation"] == "explicit"
)
PLUGIN_NAME = CATALOG_NAME


def add_claude_explicit_control(text: str) -> str:
    frontmatter, body = split_frontmatter(text)
    if re.search(r"(?m)^disable-model-invocation:", frontmatter):
        raise ValueError("canonical frontmatter must not contain Claude-native controls")
    return f"---\n{frontmatter}\ndisable-model-invocation: true\n---\n{body}"


def directory_hashes(path: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    if not path.is_dir():
        return hashes
    for item in sorted(path.rglob("*")):
        if item.is_file():
            relative = item.relative_to(path).as_posix()
            hashes[relative] = hashlib.sha256(item.read_bytes()).hexdigest()
    return hashes


def license_notice(root: Path) -> bytes:
    """Read the owned notice that must travel with standalone distributions."""
    path = root / "LICENSE"
    if path.is_symlink() or not path.is_file() or path.stat().st_mode & 0o111:
        raise ValueError("license notice must be a regular non-executable file")
    payload = path.read_bytes()
    if not payload.startswith(b"MIT License\n") or b"Copyright (c)" not in payload:
        raise ValueError("canonical MIT license notice is missing")
    return payload
