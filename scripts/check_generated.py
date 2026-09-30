#!/usr/bin/env python3
"""Fail when tracked plugin trees drift from canonical sources."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from build_distributions import antigravity_groups, build, marketplace_documents
from cataloglib import ROOT, directory_hashes, skills_by_plugin


def check() -> list[str]:
    errors: list[str] = []
    with tempfile.TemporaryDirectory(prefix="measured-skills-") as temporary:
        output_root = Path(temporary) / "plugins"
        build(output_root, write_marketplaces=False)
        for client in ("codex", "claude", "antigravity"):
            client_root = ROOT / "plugins" / client
            if not client_root.is_dir():
                errors.append(f"{client}: missing client plugins directory")
                continue
            actual_plugins = {path.name for path in client_root.iterdir() if path.is_dir()}
            expected_plugins = antigravity_groups() if client == "antigravity" else skills_by_plugin()
            if actual_plugins != set(expected_plugins):
                errors.append(f"{client}: unexpected or missing plugin directories")
            for plugin in expected_plugins:
                expected_hashes = directory_hashes(output_root / client / plugin)
                actual_hashes = directory_hashes(ROOT / "plugins" / client / plugin)
                missing = sorted(set(expected_hashes) - set(actual_hashes))
                extra = sorted(set(actual_hashes) - set(expected_hashes))
                changed = sorted(
                    relative_path
                    for relative_path in set(expected_hashes) & set(actual_hashes)
                    if expected_hashes[relative_path] != actual_hashes[relative_path]
                )
                for relative_path in missing:
                    errors.append(f"{client}/{plugin} generated file missing: {relative_path}")
                for relative_path in extra:
                    errors.append(f"{client}/{plugin} generated file unexpected: {relative_path}")
                for relative_path in changed:
                    errors.append(f"{client}/{plugin} generated file drifted: {relative_path}")

        codex_marketplace, claude_marketplace, antigravity_marketplace = marketplace_documents()
        expected_marketplaces = (
            (ROOT / ".agents" / "plugins" / "marketplace.json", codex_marketplace),
            (ROOT / ".claude-plugin" / "marketplace.json", claude_marketplace),
            (ROOT / ".gemini" / "plugins" / "marketplace.json", antigravity_marketplace),
        )
        for marketplace_path, expected in expected_marketplaces:
            rendered = json.dumps(expected, indent=2, sort_keys=False) + "\n"
            if not marketplace_path.is_file():
                errors.append(f"generated marketplace missing: {marketplace_path.relative_to(ROOT)}")
            elif marketplace_path.read_text(encoding="utf-8") != rendered:
                errors.append(f"generated marketplace drifted: {marketplace_path.relative_to(ROOT)}")
    return errors


def main() -> int:
    errors = check()
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("Generated distributions match canonical sources.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
