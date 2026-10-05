#!/usr/bin/env python3
"""Build a deterministic release manifest for an exact tested source commit."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import date
from pathlib import Path

from cataloglib import ROOT, SKILLS, VERSION, directory_hashes, skills_by_plugin
from build_distributions import antigravity_groups


def _file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _tree_hash(path: Path) -> str:
    value = json.dumps(directory_hashes(path), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _git_text(arguments: list[str]) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.returncode != 0:
        raise ValueError(completed.stderr.strip() or f"git {' '.join(arguments)} failed")
    return completed.stdout.strip()


def _require_clean_source_checkout(source_commit: str) -> None:
    _git_text(["cat-file", "-e", f"{source_commit}^{{commit}}"])
    if _git_text(["rev-parse", "HEAD"]) != source_commit:
        raise ValueError("source commit must equal the clean checkout HEAD")
    if _git_text(["status", "--porcelain"]):
        raise ValueError("release manifest generation requires a clean checkout")


def _require_tracked_source_artifact(relative: str) -> None:
    _git_text(["cat-file", "-e", f"HEAD:{relative}"])


def build(source_commit: str, output: Path | None = None, created_on: date | None = None) -> Path:
    if re.fullmatch(r"[0-9a-f]{40}", source_commit) is None:
        raise ValueError("source commit must be a full 40-character lowercase Git SHA")
    _require_clean_source_checkout(source_commit)
    artifacts: list[dict[str, str]] = []
    for client in ("codex", "claude", "antigravity"):
        groups = antigravity_groups() if client == "antigravity" else skills_by_plugin()
        for plugin in groups:
            path = ROOT / "plugins" / client / plugin
            artifacts.append({"kind": "tree", "path": path.relative_to(ROOT).as_posix(), "sha256": _tree_hash(path)})
    for path in (
        ROOT / ".agents" / "plugins" / "marketplace.json",
        ROOT / ".claude-plugin" / "marketplace.json",
        ROOT / ".gemini" / "plugins" / "marketplace.json",
        ROOT / "catalog" / "skills.json",
        ROOT / "catalog" / "packs.json",
        ROOT / "catalog" / "plugin-migrations.json",
        ROOT / "catalog" / "profiles.json",
        ROOT / "catalog" / "google-surfaces.json",
        ROOT / "catalog" / "evidence.json",
        ROOT / "catalog" / "compatibility.json",
        ROOT / "catalog" / "deprecations.json",
        ROOT / "catalog" / "revocations.json",
        ROOT / "catalog" / "upstream-reviews.json",
        ROOT / "catalog" / "upstream-pins.json",
        ROOT / "evals" / "cases.json",
        ROOT / "provenance" / "catalog.json",
    ):
        artifacts.append({"kind": "file", "path": path.relative_to(ROOT).as_posix(), "sha256": _file_hash(path)})
    for skill in SKILLS:
        archive = ROOT / "dist" / "claude-ai" / f"{skill}-{VERSION}.zip"
        if not archive.is_file():
            raise FileNotFoundError(f"missing packaged skill: {archive}")
        artifacts.append({"kind": "zip", "path": archive.relative_to(ROOT).as_posix(), "sha256": _file_hash(archive)})
    for artifact in artifacts:
        _require_tracked_source_artifact(artifact["path"])
    value = {
        "$schema": "../manifest-schema.json",
        "catalog_version": VERSION,
        "source_commit": source_commit,
        "created_on": (created_on or date.today()).isoformat(),
        "artifacts": sorted(artifacts, key=lambda item: item["path"]),
    }
    target = (output or ROOT / "releases" / VERSION / "manifest.json").resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    return target


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    target = build(args.source_commit, args.output)
    print(f"Wrote {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
