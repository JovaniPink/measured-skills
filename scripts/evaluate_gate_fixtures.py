#!/usr/bin/env python3
"""Validate representative cross-stack gate-discovery fixtures without mutation."""

from __future__ import annotations

import json
import re

from cataloglib import ROOT


MUTATING_TOKENS = (" apply", " update", " -u", "--fix", "snapshot -u")
# Flag-aware patterns: a formatter only counts as mutating without its check or list flag.
MUTATING_PATTERNS = (
    re.compile(r"(?:^|\s)(?:--write|-w)(?:\s|$)"),
    re.compile(r"\bgo (?:generate|fmt|get|mod tidy)\b"),
    re.compile(r"\b(?:npm|pnpm|yarn|pip3?|uv|poetry|cargo) (?:install|add|upgrade|remove)\b"),
    re.compile(r"\bfmt\b(?!.*\s(?:-check|--check|-l|-d)(?:\s|$))"),
)


def is_mutating_command(command: str) -> bool:
    """Return True when a candidate gate command would change files or dependencies."""

    lowered = f" {command.lower()}"
    return any(token in lowered for token in MUTATING_TOKENS) or any(
        pattern.search(lowered) for pattern in MUTATING_PATTERNS
    )


def evaluate() -> list[str]:
    errors: list[str] = []
    document = json.loads((ROOT / "evals" / "quality-gate-fixtures.json").read_text(encoding="utf-8"))
    fixtures = document.get("fixtures", [])
    stacks = {fixture.get("stack") for fixture in fixtures}
    expected = {"Go", "Python", "Swift", "TypeScript/JavaScript", "SQL", "Terraform"}
    if stacks != expected:
        errors.append(f"fixture stacks must be {sorted(expected)}, found {sorted(stacks)}")
    command_sets: set[tuple[str, ...]] = set()
    for fixture in fixtures:
        path = ROOT / fixture["path"]
        missing = [signal for signal in fixture.get("signals", []) if not (path / signal).is_file()]
        if missing:
            errors.append(f"{fixture['stack']}: missing discovery signals {missing}")
        candidates = fixture.get("safe_candidates", [])
        command_sets.add(tuple(candidates))
        for command in candidates:
            if is_mutating_command(command):
                errors.append(f"{fixture['stack']}: mutating candidate is not a validation gate: {command}")
        if not candidates and fixture.get("expected_status") != "INCOMPLETE":
            errors.append(f"{fixture['stack']}: no candidates must produce INCOMPLETE")
        if not fixture.get("forbidden"):
            errors.append(f"{fixture['stack']}: fixture must name at least one unsafe near miss")
        if not fixture.get("judgment_failure"):
            errors.append(f"{fixture['stack']}: fixture must name a stack-specific judgment failure")
        if fixture.get("stack") == "Swift":
            observation = fixture.get("observed_macos")
            if not isinstance(observation, dict) or observation.get("result") not in {"pass", "fail", "blocked"}:
                errors.append("Swift: fixture must record a terminal observed macOS result")
    if len(command_sets) != len(fixtures):
        errors.append("fixtures must not collapse stacks into one universal command set")
    return errors


def main() -> int:
    errors = evaluate()
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("Cross-stack gate fixture evaluation passed without running mutating commands.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
