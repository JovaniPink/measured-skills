"""Shared, standard-library-only helpers for the portable skill catalog."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import TypedDict


ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.17.1"
CATALOG_NAME = "measured-skills"
PLUGIN_CATEGORY = "Developer Tools"

class PluginSpec(TypedDict):
    """Typed metadata used to generate both client plugin manifests."""

    display_name: str
    description: str
    short_description: str
    keywords: list[str]


PLUGIN_SPECS: dict[str, PluginSpec] = {
    "measured-skills": {
        "display_name": "Measured Skills",
        "description": "Portable evidence, diagnosis, quality, publication, and skill-security workflows.",
        "short_description": "Evidence-oriented workflows for Codex",
        "keywords": ["skills", "research", "diagnosis", "quality", "security"],
    },
    "measured-engineering-build": {
        "display_name": "Measured Engineering Build",
        "description": "Frame outcomes, design interfaces, plan vertical slices, and test behavior.",
        "short_description": "Design and build cohesive software",
        "keywords": ["skills", "engineering", "architecture", "testing"],
    },
    "measured-engineering-review": {
        "display_name": "Measured Engineering Review",
        "description": "Review correctness, compatibility, security, operations, and test quality.",
        "short_description": "Risk-focused engineering review",
        "keywords": ["skills", "review", "security", "quality"],
    },
    "measured-engineering-delivery": {
        "display_name": "Measured Engineering Delivery",
        "description": "Coordinate bounded execution, isolated work, review handoffs, and delivery evidence.",
        "short_description": "Bounded execution and delivery workflows",
        "keywords": ["skills", "delivery", "git", "execution"],
    },
    "measured-stack-profiles": {
        "display_name": "Measured Stack Profiles",
        "description": "Optional language and infrastructure engineering profiles.",
        "short_description": "Stack-specific engineering guidance for Codex",
        "keywords": ["skills", "engineering", "languages", "infrastructure"],
    },
    "measured-operations": {
        "display_name": "Measured Operations",
        "description": "Portable requirements, decision, measurement, adoption, and incident workflows.",
        "short_description": "Operating and decision workflows for Codex",
        "keywords": ["skills", "operations", "decisions", "measurement"],
    },
    "measured-reasoning": {
        "display_name": "Measured Reasoning",
        "description": "Portable alignment, explanation, impact, writing, evidence, and skill-authoring workflows.",
        "short_description": "Reasoning and communication workflows for Codex",
        "keywords": ["skills", "reasoning", "writing", "architecture", "evidence"],
    },
    "measured-ai-systems": {
        "display_name": "Measured AI Systems",
        "description": "Optional AI evaluation, context reliability, and source-to-output conformance workflows.",
        "short_description": "AI reliability workflows for Codex",
        "keywords": ["skills", "ai", "evaluation", "context", "conformance"],
    },
    "measured-agent-platforms": {
        "display_name": "Measured Agent Platforms",
        "description": "Human-facing agent architecture, security, tooling, context, protocol, retrieval, and Google ADK workflows.",
        "short_description": "Agent platform engineering workflows for Codex",
        "keywords": ["skills", "agents", "adk", "security", "retrieval"],
    },
}


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
