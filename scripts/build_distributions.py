#!/usr/bin/env python3
"""Generate tracked Codex and Claude plugin distributions."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import TypedDict

from cataloglib import (
    CATALOG_NAME,
    PLUGIN_CATEGORY,
    PLUGIN_SPECS,
    ROOT,
    SKILLS,
    VERSION,
    add_claude_explicit_control,
    read_skill_metadata,
    skills_by_plugin,
)

PLUGIN_ICON = ROOT / ".claude-plugin" / "icon.svg"


class CodexMarketplaceSource(TypedDict):
    source: str
    path: str


class CodexMarketplacePolicy(TypedDict):
    installation: str
    authentication: str


class CodexMarketplacePlugin(TypedDict):
    name: str
    source: CodexMarketplaceSource
    policy: CodexMarketplacePolicy
    category: str


class CodexMarketplace(TypedDict):
    name: str
    interface: dict[str, str]
    plugins: list[CodexMarketplacePlugin]


class ClaudeMarketplacePlugin(TypedDict):
    name: str
    source: str
    description: str
    version: str


class ClaudeMarketplace(TypedDict):
    name: str
    description: str
    owner: dict[str, str]
    plugins: list[ClaudeMarketplacePlugin]


class AntigravityMarketplaceSource(TypedDict):
    source: str
    path: str


class AntigravityMarketplacePlugin(TypedDict):
    name: str
    source: AntigravityMarketplaceSource
    description: str
    version: str


class AntigravityMarketplace(TypedDict):
    name: str
    description: str
    owner: dict[str, str]
    plugins: list[AntigravityMarketplacePlugin]


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def marketplace_documents() -> tuple[CodexMarketplace, ClaudeMarketplace, AntigravityMarketplace]:
    """Return the client-native marketplace documents for tracked output."""

    codex: CodexMarketplace = {
        "name": CATALOG_NAME,
        "interface": {"displayName": "Measured Skills Catalog"},
        "plugins": [
            {
                "name": plugin,
                "source": {
                    "source": "local",
                    "path": f"./plugins/codex/{plugin}",
                },
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": PLUGIN_CATEGORY,
            }
            for plugin in skills_by_plugin()
        ],
    }
    claude: ClaudeMarketplace = {
        "name": CATALOG_NAME,
        "description": "Portable workflow skills for software, research, and operations.",
        "owner": {"name": "Measured Studios", "url": "https://measuredstudios.com"},
        "plugins": [
            {
                "name": plugin,
                "source": f"./plugins/claude/{plugin}",
                "description": PLUGIN_SPECS[plugin]["description"],
                "version": VERSION,
            }
            for plugin in skills_by_plugin()
        ],
    }
    antigravity: AntigravityMarketplace = {
        "name": CATALOG_NAME,
        "description": "Portable workflow skills for software, research, and operations.",
        "owner": {"name": "Measured Studios", "url": "https://measuredstudios.com"},
        "plugins": [
            {
                "name": plugin,
                "source": {
                    "source": "local",
                    "path": f"./plugins/antigravity/{plugin}",
                },
                "description": PLUGIN_SPECS[plugin]["description"],
                "version": VERSION,
            }
            for plugin in antigravity_groups()
        ],
    }
    return codex, claude, antigravity


def antigravity_groups() -> dict[str, list[str]]:
    groups = {plugin: [skill for skill in skills if read_skill_metadata(ROOT / "skills" / skill)["invocation"] != "explicit"] for plugin, skills in skills_by_plugin().items()}
    return {plugin: skills for plugin, skills in groups.items() if skills}


def _reset_directory(path: Path, allowed_parent: Path, allowed_names: set[str]) -> None:
    if path.is_symlink() or allowed_parent.is_symlink():
        raise ValueError(f"refusing symlinked distribution path: {path}")
    path = path.resolve()
    allowed_parent = allowed_parent.resolve()
    if path.parent != allowed_parent or path.name not in allowed_names:
        raise ValueError(f"refusing to reset unexpected distribution path: {path}")
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def _validate_generated_parent(parent: Path) -> None:
    if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
        raise ValueError(f"unsafe distribution parent: {parent}")
    if parent.exists():
        for child in parent.iterdir():
            if child.name not in PLUGIN_SPECS or child.is_symlink() or not child.is_dir():
                raise ValueError(f"unowned or unsafe distribution entry: {child}")


def _remove_obsolete(parent: Path, expected: set[str]) -> None:
    for child in parent.iterdir():
        if child.name not in expected:
            # The complete set of parents and children was validated before any reset.
            if child.is_symlink() or not child.is_dir() or child.name not in PLUGIN_SPECS:
                raise ValueError(f"unsafe obsolete distribution: {child}")
            shutil.rmtree(child)


def _copy_codex_skill(source: Path, target: Path, skill: str, plugin: str) -> None:
    shutil.copytree(source, target)
    interface_path = target / "agents" / "openai.yaml"
    interface = interface_path.read_text(encoding="utf-8")
    interface_path.write_text(
        interface.replace(f"${skill}", f"${plugin}:{skill}"),
        encoding="utf-8",
    )


def _copy_claude_skill(source: Path, target: Path, explicit: bool) -> None:
    target.mkdir(parents=True)
    for item in sorted(source.iterdir()):
        if item.name == "agents":
            continue
        destination = target / item.name
        if item.is_dir():
            shutil.copytree(item, destination)
        elif item.name == "SKILL.md" and explicit:
            destination.write_text(
                add_claude_explicit_control(item.read_text(encoding="utf-8")),
                encoding="utf-8",
            )
        else:
            shutil.copy2(item, destination)


def build(output_root: Path, write_marketplaces: bool = False) -> tuple[dict[str, Path], dict[str, Path], dict[str, Path]]:
    if PLUGIN_ICON.is_symlink() or not PLUGIN_ICON.is_file():
        raise ValueError("shared plugin icon must be a regular source file")
    icon = PLUGIN_ICON.read_bytes()
    for path in (output_root.absolute(), *output_root.absolute().parents):
        if path in (Path("/tmp"), Path("/var")) and path.resolve() == Path("/private") / path.name:
            continue
        if path.is_symlink():
            raise ValueError(f"refusing symlinked distribution root or ancestor: {path}")
    output_root = output_root.resolve()
    codex_parent = output_root / "codex"
    claude_parent = output_root / "claude"
    antigravity_parent = output_root / "antigravity"
    for parent in (codex_parent, claude_parent, antigravity_parent):
        _validate_generated_parent(parent)
    codex_parent.mkdir(parents=True, exist_ok=True)
    claude_parent.mkdir(parents=True, exist_ok=True)
    antigravity_parent.mkdir(parents=True, exist_ok=True)
    grouped = skills_by_plugin()
    allowed_names = set(grouped)
    codex_plugins = {plugin: codex_parent / plugin for plugin in grouped}
    claude_plugins = {plugin: claude_parent / plugin for plugin in grouped}
    agy_grouped = antigravity_groups()
    antigravity_plugins = {plugin: antigravity_parent / plugin for plugin in agy_grouped}
    _remove_obsolete(codex_parent, allowed_names)
    _remove_obsolete(claude_parent, allowed_names)
    _remove_obsolete(antigravity_parent, set(agy_grouped))
    for path in codex_plugins.values():
        _reset_directory(path, codex_parent, allowed_names)
    for path in claude_plugins.values():
        _reset_directory(path, claude_parent, allowed_names)
    for path in antigravity_plugins.values():
        _reset_directory(path, antigravity_parent, allowed_names)

    for plugin, skills in grouped.items():
        codex_plugin = codex_plugins[plugin]
        claude_plugin = claude_plugins[plugin]
        antigravity_plugin = antigravity_plugins.get(plugin)
        for skill in skills:
            source = ROOT / "skills" / skill
            metadata = read_skill_metadata(source)
            is_explicit = metadata["invocation"] == "explicit"
            _copy_codex_skill(source, codex_plugin / "skills" / skill, skill, plugin)
            _copy_claude_skill(source, claude_plugin / "skills" / skill, is_explicit)
            if not is_explicit and antigravity_plugin is not None:
                _copy_claude_skill(source, antigravity_plugin / "skills" / skill, False)

        spec = PLUGIN_SPECS[plugin]
        _write_json(
            codex_plugin / ".codex-plugin" / "plugin.json",
            {
                "name": plugin,
                "version": VERSION,
                "description": spec["description"],
                "author": {"name": "Measured Studios", "url": "https://measuredstudios.com"},
                "homepage": "https://measuredstudios.com/skills",
                "repository": "https://github.com/JovaniPink/measured-skills",
                "license": "MIT",
                "skills": "./skills/",
                "interface": {
                    "displayName": spec["display_name"],
                    "shortDescription": spec["short_description"],
                    "longDescription": spec["description"],
                    "developerName": "Measured Studios",
                    "category": PLUGIN_CATEGORY,
                    "capabilities": ["Skills"],
                    "defaultPrompt": [
                        f"Help me choose and use a {spec['display_name']} workflow skill."
                    ],
                },
            },
        )
        _write_json(
            claude_plugin / ".claude-plugin" / "plugin.json",
            {
                "name": plugin,
                "version": VERSION,
                "description": spec["description"],
                "author": {"name": "Measured Studios", "url": "https://measuredstudios.com"},
                "homepage": "https://measuredstudios.com/skills",
                "repository": "https://github.com/JovaniPink/measured-skills",
                "license": "MIT",
                "keywords": spec["keywords"],
                "icon": "./.claude-plugin/icon.svg",
            },
        )
        (claude_plugin / ".claude-plugin" / "icon.svg").write_bytes(icon)
        if antigravity_plugin is not None:
            _write_json(
                antigravity_plugin / "plugin.json",
                {"name": plugin, "description": spec["description"]},
            )

    if write_marketplaces:
        codex_marketplace, claude_marketplace, antigravity_marketplace = marketplace_documents()
        _write_json(ROOT / ".agents" / "plugins" / "marketplace.json", codex_marketplace)
        _write_json(ROOT / ".claude-plugin" / "marketplace.json", claude_marketplace)
        _write_json(ROOT / ".gemini" / "plugins" / "marketplace.json", antigravity_marketplace)
    return codex_plugins, claude_plugins, antigravity_plugins


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        type=Path,
        default=ROOT / "plugins",
        help="Parent containing codex/, claude/, and antigravity/ distribution directories.",
    )
    parser.add_argument(
        "--write-marketplaces",
        action="store_true",
        help="Also rewrite root marketplace files when the host permits it.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Compare tracked output with a temporary render without modifying the checkout.",
    )
    args = parser.parse_args()
    if args.check:
        if args.output_root != ROOT / "plugins" or args.write_marketplaces:
            parser.error("--check cannot be combined with output or write options")
        from check_generated import check

        errors = check()
        if errors:
            print("\n".join(f"ERROR: {error}" for error in errors))
            return 1
        print("Generated distributions and marketplaces match canonical sources.")
        return 0
    build(args.output_root, write_marketplaces=args.write_marketplaces)
    agy_count = sum(len(skills) for skills in antigravity_groups().values())
    print(f"Generated {len(SKILLS)} Codex skills, {len(SKILLS)} Claude skills, and {agy_count} Antigravity skills.")
    return 0



if __name__ == "__main__":
    raise SystemExit(main())
