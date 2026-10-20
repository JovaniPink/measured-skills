#!/usr/bin/env python3
"""Export implicit skills to a new staging directory without installing anything."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

from build_distributions import _copy_claude_skill
from cataloglib import EXPLICIT_SKILLS, ROOT, SKILLS, VERSION, directory_hashes


def check_destination(output: Path) -> None:
    if ".." in output.parts:
        raise ValueError("output may not traverse parent directories")
    if output.exists() or output.is_symlink():
        raise ValueError("output must be a new staging directory")
    for parent in output.absolute().parents:
        if parent.is_symlink():
            raise ValueError("output parent may not be a symlink")
    if not output.parent.is_dir():
        raise ValueError("output parent must be an existing directory")


def profile_skills(profile: str, client: str, root: Path = ROOT) -> list[str]:
    surfaces = {"codex": "codex", "claude": "claude-code", "antigravity": "antigravity-cli"}
    if client not in surfaces:
        raise ValueError("unsupported client")
    document = json.loads((root / "catalog/profiles.json").read_text())
    records = [p for p in document["profiles"] if p["id"] == profile]
    if len(records) != 1:
        raise ValueError("unknown profile")
    record = records[0]
    if surfaces[client] not in record["target_surfaces"]:
        raise ValueError("profile does not target this client")
    names = record["skills"]
    if not isinstance(names, list) or not names or any(not isinstance(n, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", n) for n in names) or len(set(names)) != len(names):
        raise ValueError("invalid profile selection")
    return [str(name) for name in names]


def export(output: Path, client: str, selected: list[str]) -> None:
    if client not in {"codex", "claude", "antigravity"}:
        raise ValueError("client must be codex, claude, or antigravity")
    if not selected or len(selected) != len(set(selected)):
        raise ValueError("select at least one skill without duplicates")
    if set(selected) - set(SKILLS):
        raise ValueError("unknown or revoked skill")
    if set(selected) & EXPLICIT_SKILLS:
        raise ValueError("explicit-only skills require separately verified plugin activation")
    check_destination(output)
    for skill in selected:
        source = ROOT / "skills" / skill
        if not (source / "SKILL.md").is_file():
            raise ValueError("missing canonical skill")
        for item in source.rglob("*"):
            if item.is_symlink():
                raise ValueError("symlinks are not permitted in selected exports")
            if item.suffix == ".md":
                for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", item.read_text(encoding="utf-8")):
                    target = target.split("#", 1)[0].strip("<>")
                    if not target or "://" in target or target.startswith("mailto:"):
                        continue
                    resolved = (item.parent / target).resolve()
                    if not resolved.is_relative_to(source.resolve()) or not resolved.exists():
                        raise ValueError("missing or non-portable selected-skill reference")
    # Resolve the parent, but never follow an output symlink or replace old output.
    output = output.parent.resolve() / output.name
    output.mkdir(parents=True, exist_ok=False)
    for skill in sorted(selected):
        source = ROOT / "skills" / skill
        target = output / skill
        if client == "codex":
            shutil.copytree(source, target)
        else:
            _copy_claude_skill(source, target, explicit=False)
    manifest = {
        "catalog_version": VERSION,
        "client": client,
        "skills": sorted(selected),
        "files": directory_hashes(output),
        "installation": "not_installed",
        "behavior": "not_observed",
    }
    (output / "export-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--client", choices=("codex", "claude", "antigravity"), required=True)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--skill", action="append")
    selection.add_argument("--profile")
    args = parser.parse_args()
    try:
        selected = profile_skills(args.profile, args.client) if args.profile else args.skill
        export(args.output, args.client, selected)
    except ValueError as error:
        parser.error(str(error))
    print("Selected skills exported; no client configuration or installation changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
