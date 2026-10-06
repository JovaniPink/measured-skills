#!/usr/bin/env python3
"""Run the complete deterministic repository validation suite."""

from __future__ import annotations

from check_generated import check as check_generated
from check_originality import check as check_originality
from check_public_boundary import scan as scan_public_boundary
from check_repository_independence import check as check_repository_independence
from behavior_study import check_manifest, load_manifest
from cataloglib import ROOT
from evaluate_gate_fixtures import evaluate as evaluate_gate_fixtures
from check_upstream_freshness import check as check_upstream_freshness
from sync_private_overlay import sync as check_private_overlay
from validate_catalog import validate_all


def run() -> list[str]:
    errors = validate_all(require_packages=True)
    errors.extend(scan_public_boundary())
    errors.extend(check_generated())
    errors.extend(check_originality())
    errors.extend(check_repository_independence())
    errors.extend(evaluate_gate_fixtures())
    errors.extend(check_manifest(load_manifest()))
    freshness_errors, _ = check_upstream_freshness(online=False)
    errors.extend(freshness_errors)
    errors.extend(
        check_private_overlay(ROOT / "examples" / "private-overlay", check_only=True)
    )
    return errors


def main() -> int:
    errors = run()
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("All deterministic catalog validations passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
