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


def artifact_inventory() -> dict[str, str]:
    """Return the complete current release inventory, shared with validation."""
    artifacts: dict[str, str] = {}
    for client in ("codex", "claude", "antigravity"):
        groups = antigravity_groups() if client == "antigravity" else skills_by_plugin()
        for plugin in groups:
            artifacts[f"plugins/{client}/{plugin}"] = "tree"
    for relative in (
        ".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json",
        ".gemini/plugins/marketplace.json", "catalog/skills.json", "catalog/packs.json",
        "catalog/plugin-migrations.json", "catalog/profiles.json", "catalog/google-surfaces.json",
        "catalog/evidence.json", "catalog/compatibility.json", "catalog/deprecations.json",
        "catalog/revocations.json", "catalog/upstream-reviews.json", "catalog/upstream-pins.json",
        "evals/cases.json", "evals/daily-engineering/cases.json",
        "evals/daily-engineering/cli-smoke-2026-10-20.json", "provenance/catalog.json",
    ):
        artifacts[relative] = "file"
    for skill in SKILLS:
        artifacts[f"dist/claude-ai/{skill}-{VERSION}.zip"] = "zip"
    return dict(sorted(artifacts.items()))


def build(source_commit: str, output: Path | None = None, created_on: date | None = None) -> Path:
    if re.fullmatch(r"[0-9a-f]{40}", source_commit) is None:
        raise ValueError("source commit must be a full 40-character lowercase Git SHA")
    _require_clean_source_checkout(source_commit)
    artifacts: list[dict[str, str]] = []
    for relative, kind in artifact_inventory().items():
        path = ROOT / relative
        digest = _tree_hash(path) if kind == "tree" else _file_hash(path)
        artifacts.append({"kind": kind, "path": relative, "sha256": digest})
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
