#!/usr/bin/env python3
"""Prepare an offline Antigravity preview. Never install or activate it."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from cataloglib import EXPLICIT_SKILLS, ROOT, SKILLS, VERSION, add_claude_explicit_control, directory_hashes


def build(output: Path, selected: list[str] | None = None) -> Path:
    """Copy skills into a new Antigravity bundle with explicit controls applied."""
    included = sorted(set(SKILLS) - EXPLICIT_SKILLS) if selected is None else sorted(selected)
    if not included or len(included) != len(set(included)):
        raise ValueError("choose at least one skill without duplicate names")
    if set(included) - set(SKILLS):
        raise ValueError("selection contains an unknown skill")
    if set(included) & EXPLICIT_SKILLS:
        raise ValueError("explicit-only skills are held on Antigravity until invocation controls are verified")
    # Refuse existing paths, including dangling symlinks. Never reset evidence or settings.
    if output.exists() or output.is_symlink():
        raise FileExistsError(f"output already exists: {output}")
    output.mkdir(parents=True)
    plugin = output / "plugin"
    for skill in included:
        source = ROOT / "skills" / skill
        target = plugin / "skills" / skill
        target.mkdir(parents=True)
        explicit = skill in EXPLICIT_SKILLS
        for item in sorted(source.iterdir()):
            if item.name == "agents":
                continue
            if item.is_dir():
                shutil.copytree(item, target / item.name)
            elif item.name == "SKILL.md" and explicit:
                (target / item.name).write_text(
                    add_claude_explicit_control(item.read_text(encoding="utf-8")),
                    encoding="utf-8",
                )
            else:
                shutil.copy2(item, target / item.name)
    (plugin / "plugin.json").write_text(json.dumps({
        "name": "measured-antigravity-preview",
        "description": "Selected workflow skills for an Antigravity loading check.",
    }, indent=2) + "\n", encoding="utf-8")
    receipt = {
        "format_version": 1,
        "status": "preview",
        "source_catalog_version": VERSION,
        "client_loading": "not_observed",
        "supported_install_claim": False,
        "included_skills": included,
        "explicit_skills": sorted(set(included) & EXPLICIT_SKILLS),
        "excluded_skills": sorted(set(SKILLS) - set(included)),
        "exclusion_reason": "Explicit-only skills are held; other skills may be unselected.",
        "plugin_sha256": directory_hashes(plugin),
    }
    (output / "bundle.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="New review directory; must not exist.")
    parser.add_argument("--skill", action="append", help="Repeat to select skills; default includes all eligible skills.")
    args = parser.parse_args()
    try:
        target = build(args.output, args.skill)
    except (ValueError, OSError) as error:
        parser.exit(1, f"ERROR: {error}\n")
    print(f"Prepared preview at {target}. Client loading remains unverified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
