#!/usr/bin/env python3
"""Check or summarize frozen study evidence offline. Never invoke a client."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path
from typing import Any

from grade_qualification import grade
from schema_validation import validate_instance
from study_fixture import replay, solution_actions

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "evals" / "behavior-study"
ARMS = ("none", "historical", "current")
CLIENTS = ("codex-cli", "claude-code")
SKILLS = ("code-change-review", "plan-execution", "publish-change-safely")
SOURCES = {
    "historical": "70182b250beb70bfb210e658387416b891918df1",
    "current": "a155250d65112a18e3d633403c4c99be881be433",
}

STUDY_SOURCES = {
    "workflow-behavior-2026-10": SOURCES,
    "workflow-behavior-2026-10-v2": {
        "historical": SOURCES["historical"],
        "current": "5ff97f764760ec865ca4fe7ffe37aa31c01d770f",
    },
}
STUDY_KITS = {
    "workflow-behavior-2026-10": KIT,
    "workflow-behavior-2026-10-v2": ROOT / "evals" / "behavior-study-v2",
}


def kit_for(manifest: dict[str, Any]) -> Path:
    identity = manifest.get("study_id")
    if not isinstance(identity, str) or identity not in STUDY_KITS:
        raise ValueError("unknown frozen study identity")
    return STUDY_KITS[identity]


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def encoded(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def bundle_hash(revision: str, skill: str) -> str:
    prefix = f"skills/{skill}/"
    listing = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", revision, "--", prefix],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    if not listing:
        raise ValueError("source bundle unavailable")
    files = {}
    for path in listing:
        payload = subprocess.run(
            ["git", "show", f"{revision}:{path}"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
        files[path.removeprefix(prefix)] = digest(payload)
    return digest(encoded(files))


def load_manifest(path: Path | None = None) -> dict[str, Any]:
    return json.loads((path or KIT / "study.json").read_text())  # type: ignore[no-any-return]


def load_fixture(
    case_id: str, manifest: dict[str, Any] | None = None
) -> dict[str, Any]:
    manifest = manifest or load_manifest()
    if case_id not in {entry["id"] for entry in manifest["cases"]}:
        raise ValueError("unknown fixture")
    return json.loads((kit_for(manifest) / "fixtures" / f"{case_id}.json").read_text())  # type: ignore[no-any-return]


def check_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        kit = kit_for(manifest)
        sources = STUDY_SOURCES[manifest["study_id"]]
        expected = {
            "format_version",
            "study_id",
            "execution_authorized",
            "source_revisions",
            "bundle_hashes",
            "clients",
            "arms",
            "repetitions",
            "cases",
            "prefixes",
        }
        if (
            set(manifest) != expected
            or manifest["format_version"] != 1
            or manifest["execution_authorized"] is not False
        ):
            return ["manifest shape or preparation authority changed"]
        if manifest["source_revisions"] != sources:
            errors.append("study or source identity changed")
        if (
            manifest["clients"] != list(CLIENTS)
            or manifest["arms"] != list(ARMS)
            or type(manifest["repetitions"]) is not int
            or manifest["repetitions"] != 3
        ):
            errors.append("coverage axes changed")
        canonical = json.loads(
            subprocess.run(
                ["git", "show", f"{sources['current']}:evals/cases.json"],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            ).stdout
        )["skills"]
        expected_ids = {
            case["id"]
            for group in canonical
            if group["skill"] in SKILLS
            for kind in ("positive", "near_miss", "safety")
            for case in group[kind]
        }
        canonical_index = {
            case["id"]: (group["skill"], kind)
            for group in canonical
            if group["skill"] in SKILLS
            for kind in ("positive", "near_miss", "safety")
            for case in group[kind]
        }
        ids = [item["id"] for item in manifest["cases"]]
        if len(ids) != len(set(ids)) or set(ids) != expected_ids:
            errors.append("missing, duplicate, or unexpected case coverage")
        for entry in manifest["cases"]:
            if (
                set(entry) != {"id", "skill", "kind", "case_sha256", "fixture_sha256"}
                or entry["id"] not in expected_ids
                or (entry["skill"], entry["kind"]) != canonical_index[entry["id"]]
            ):
                errors.append("case identity or shape mismatch")
                continue
            case_bytes = (kit / "cases" / f"{entry['id']}.json").read_bytes()
            fixture_bytes = (kit / "fixtures" / f"{entry['id']}.json").read_bytes()
            case = json.loads(case_bytes)
            schema = json.loads(
                (ROOT / "evals/qualification-case-schema-v1.json").read_text()
            )
            errors.extend(validate_instance(case, schema))
            if (
                digest(case_bytes) != entry["case_sha256"]
                or digest(fixture_bytes) != entry["fixture_sha256"]
            ):
                errors.append("frozen case or fixture hash changed")
            if case["skill"] != entry["skill"] or case["case_id"] != entry["id"]:
                errors.append("frozen case identity changed")
            spec = json.loads(fixture_bytes)
            if spec["id"] != entry["id"] or not all(
                replay(spec, solution_actions(spec))["checks"].values()
            ):
                errors.append("fixture reference trajectory failed")
        for arm in ("historical", "current"):
            for skill in SKILLS:
                if manifest["bundle_hashes"][arm][skill] != bundle_hash(
                    sources[arm], skill
                ):
                    errors.append("source bundle hash changed")
        expected_prefixes = {
            str(turn): digest((kit / "prefixes" / f"turn-{turn}.txt").read_bytes())
            for turn in (1, 8, 20)
        }
        if manifest["prefixes"] != expected_prefixes:
            errors.append("context prefix changed")
    except (
        KeyError,
        TypeError,
        ValueError,
        OSError,
        subprocess.CalledProcessError,
    ) as exc:
        errors.append(f"invalid study: {exc}")
    return errors


def schedule(manifest: dict[str, Any], expansion: bool = False) -> list[dict[str, Any]]:
    cells = []
    entries = manifest["cases"]
    if expansion:
        entries = [
            next(
                item
                for item in entries
                if item["skill"] == skill and item["kind"] == kind
            )
            for skill in SKILLS
            for kind in ("positive", "near_miss", "safety")
        ]
    for client in CLIENTS:
        for index, entry in enumerate(entries):
            for turn in (8, 20) if expansion else (1,):
                for trial in range(1, 4):
                    rotation = (index + trial - 1) % 3
                    for arm in ARMS[rotation:] + ARMS[:rotation]:
                        cell = {
                            "client": client,
                            "case": entry["id"],
                            "skill": entry["skill"],
                            "arm": arm,
                            "trial": trial,
                            "turn": turn,
                            "status": "not_run",
                        }
                        cell["id"] = f"{client}/{arm}/{entry['id']}/{trial}/{turn}"
                        cells.append(cell)
    return cells


def synthetic_receipt(manifest: dict[str, Any], cell: dict[str, Any]) -> dict[str, Any]:
    """Test-only declarations. A synthetic receipt cannot become client evidence."""
    entry = next(item for item in manifest["cases"] if item["id"] == cell["case"])
    case = json.loads(
        (kit_for(manifest) / "cases" / f"{cell['case']}.json").read_text()
    )
    arm = cell["arm"]
    source = manifest["source_revisions"][
        "historical" if arm == "historical" else "current"
    ]
    bundle = (
        digest(b"absent")
        if arm == "none"
        else manifest["bundle_hashes"][arm][cell["skill"]]
    )
    loaded = [] if arm == "none" else [bundle]
    record = {
        "format_version": 1,
        "repository": "synthetic/study",
        "source_revision": source,
        "artifact_sha256": bundle,
        "skill": cell["skill"],
        "case_id": cell["case"],
        "case_sha256": entry["case_sha256"],
        "client_surface": cell["client"],
        "client_version": "synthetic",
        "model": "synthetic",
        "models_served": ["synthetic"],
        "model_switch_notices": 0,
        "permission_mode": "synthetic-bounded",
        "diagnostic_bypass": False,
        "installation_scope": "synthetic-disposable",
        "loaded_sources": loaded,
        "condition": "baseline" if arm == "none" else "skill",
        "trial": cell["trial"],
        "turn_index": cell["turn"],
        "context_tokens": None,
        "compaction_events": 0,
        "prefix_sha256": manifest["prefixes"][str(cell["turn"])],
        "grader": "synthetic-only",
        "evidence_references": ["synthetic-only"],
        "operator_seconds": 0,
        "tokens": None,
        "cost_usd": None,
        "obligations": [
            {key: obligation[key] for key in ("id", "kind", "mandatory")}
            | {"result": "pass", "evidence": "synthetic-only"}
            for obligation in case["obligations"]
        ],
    }
    return {
        "study_id": manifest["study_id"],
        "cell_id": cell["id"],
        "synthetic": True,
        "fixture_sha256": entry["fixture_sha256"],
        "record": record,
        "configuration": {
            "reasoning": "synthetic",
            "tools": ["fixture"],
            "permission": "bounded",
        },
        "trajectory": {
            "actions": solution_actions(load_fixture(cell["case"], manifest)),
            "final_report": "synthetic-only",
        },
        "inventory": {
            "verified": True,
            "loaded_hashes": loaded,
            "unexpected_relevant_sources": [],
        },
        "review": {
            "status": "reviewed",
            "reviewer": "synthetic-only",
            "evidence": "synthetic-only",
        },
    }


def report(
    manifest: dict[str, Any], receipts: list[dict[str, Any]], expansion: bool = False
) -> dict[str, Any]:
    errors = check_manifest(manifest)
    if errors:
        raise ValueError("; ".join(errors))
    planned = {cell["id"]: cell for cell in schedule(manifest, expansion)}
    seen: dict[str, str] = {}
    configurations: dict[str, bytes] = {}
    synthetic: set[bool] = set()
    if not isinstance(receipts, list):
        raise ValueError("receipts must be a list")
    for receipt in receipts:
        if not isinstance(receipt, dict):
            raise ValueError("receipt must be an object")
        cell_id = receipt.get("cell_id")
        if (
            not isinstance(cell_id, str)
            or cell_id not in planned
            or receipt.get("study_id") != manifest["study_id"]
        ):
            raise ValueError("receipt outside frozen study coverage")
        if cell_id in seen:
            raise ValueError("duplicate receipt identity")
        if (
            set(receipt)
            != {
                "study_id",
                "cell_id",
                "synthetic",
                "fixture_sha256",
                "record",
                "configuration",
                "inventory",
                "review",
                "trajectory",
            }
            or type(receipt["synthetic"]) is not bool
        ):
            raise ValueError("receipt envelope shape mismatch")
        for field in ("record", "review", "inventory", "configuration", "trajectory"):
            if not isinstance(receipt[field], dict):
                raise ValueError("receipt nested fields must be objects")
        config_value = receipt["configuration"]
        if (
            set(config_value) != {"reasoning", "tools", "permission"}
            or any(
                not isinstance(config_value[key], str) or not config_value[key].strip()
                for key in ("reasoning", "permission")
            )
            or not isinstance(config_value["tools"], list)
            or not config_value["tools"]
            or any(
                not isinstance(tool, str) or not tool for tool in config_value["tools"]
            )
        ):
            raise ValueError("invalid frozen configuration fields")
        if receipt["inventory"].get("verified") is not True:
            raise ValueError("loading inventory is not verified")
        synthetic.add(receipt["synthetic"])
        if len(synthetic) > 1:
            raise ValueError("mixed synthetic and observed evidence")
        cell = planned[cell_id]
        entry = next(item for item in manifest["cases"] if item["id"] == cell["case"])
        record = receipt["record"]
        arm = cell["arm"]
        source = manifest["source_revisions"][
            "historical" if arm == "historical" else "current"
        ]
        bundle = (
            digest(b"absent")
            if arm == "none"
            else manifest["bundle_hashes"][arm][cell["skill"]]
        )
        expected = {
            "source_revision": source,
            "artifact_sha256": bundle,
            "skill": cell["skill"],
            "case_id": cell["case"],
            "client_surface": cell["client"],
            "trial": cell["trial"],
            "turn_index": cell["turn"],
            "prefix_sha256": manifest["prefixes"][str(cell["turn"])],
            "condition": "baseline" if arm == "none" else "skill",
        }
        if any(record.get(key) != value for key, value in expected.items()):
            raise ValueError("receipt source, arm, or cell identity mismatch")
        loaded = [] if arm == "none" else [bundle]
        if (
            receipt["inventory"]
            != {
                "verified": True,
                "loaded_hashes": loaded,
                "unexpected_relevant_sources": [],
            }
            or record["loaded_sources"] != loaded
        ):
            raise ValueError("unverified loading or contaminated inventory")
        if (
            receipt["fixture_sha256"] != entry["fixture_sha256"]
            or receipt["review"].get("status") != "reviewed"
            or not receipt["review"].get("reviewer")
            or not receipt["review"].get("evidence")
        ):
            raise ValueError("fixture mismatch or human review pending")
        config = encoded(
            [
                record["client_version"],
                record["model"],
                record["permission_mode"],
                record["installation_scope"],
                receipt["configuration"],
            ]
        )
        if (
            cell["client"] in configurations
            and configurations[cell["client"]] != config
        ):
            raise ValueError("configuration drift within client lane")
        configurations[cell["client"]] = config
        frozen = (kit_for(manifest) / "cases" / f"{cell['case']}.json").read_bytes()
        result = grade(record, frozen)
        trajectory = receipt["trajectory"]
        if (
            not isinstance(trajectory, dict)
            or set(trajectory) != {"actions", "final_report"}
            or not isinstance(trajectory["actions"], list)
            or any(not isinstance(item, dict) for item in trajectory["actions"])
            or not isinstance(trajectory["final_report"], str)
            or not trajectory["final_report"].strip()
        ):
            raise ValueError("invalid trajectory evidence")
        observed = replay(load_fixture(cell["case"], manifest), trajectory["actions"])[
            "checks"
        ]
        checks = {
            "authority": observed["authority"] and observed["preservation"],
            "outcome": observed["outcome"],
        }
        declarations = {item["id"]: item["result"] for item in record["obligations"]}
        if any(
            declarations[key] != ("pass" if passed else "fail")
            for key, passed in checks.items()
        ):
            raise ValueError(
                "deterministic declaration disagrees with observed fixture trajectory"
            )
        seen[cell_id] = result["primary"]
    rates = []
    for client in CLIENTS:
        for skill in SKILLS:
            for arm in ARMS:
                group = [
                    seen[cell_id]
                    for cell_id, cell in planned.items()
                    if cell_id in seen
                    and cell["client"] == client
                    and cell["skill"] == skill
                    and cell["arm"] == arm
                ]
                total = sum(
                    cell["client"] == client
                    and cell["skill"] == skill
                    and cell["arm"] == arm
                    for cell in planned.values()
                )
                rates.append(
                    {
                        "client": client,
                        "skill": skill,
                        "arm": arm,
                        "planned": total,
                        "received": len(group),
                        "pass": group.count("pass"),
                        "fail": group.count("fail"),
                        "blocked": group.count("blocked"),
                    }
                )
    usage: dict[str, int | float | None] = {}
    for field in ("operator_seconds", "tokens", "cost_usd"):
        usage_values = [receipt["record"][field] for receipt in receipts]
        if any(
            value is not None
            and (
                type(value) not in (int, float) or not math.isfinite(value) or value < 0
            )
            for value in usage_values
        ):
            raise ValueError("invalid finite usage value")
        usage[field] = (
            None
            if not usage_values or any(value is None for value in usage_values)
            else sum(usage_values)
        )
    comparisons = []
    for client in CLIENTS:
        for skill in SKILLS:
            entries = [
                item
                for item in manifest["cases"]
                if item["skill"] == skill
                and any(cell["case"] == item["id"] for cell in planned.values())
            ]
            for turn in (8, 20) if expansion else (1,):
                for baseline in ("none", "historical"):
                    counts = {"wins": 0, "losses": 0, "ties": 0, "unpaired_cases": 0}
                    for entry in entries:
                        values = {
                            arm: [
                                seen.get(f"{client}/{arm}/{entry['id']}/{trial}/{turn}")
                                for trial in range(1, 4)
                            ]
                            for arm in (baseline, "current")
                        }
                        if any(
                            value not in ("pass", "fail")
                            for group in values.values()
                            for value in group
                        ):
                            counts["unpaired_cases"] += 1
                            continue
                        delta = values["current"].count("pass") - values[
                            baseline
                        ].count("pass")
                        counts[
                            "wins" if delta > 0 else "losses" if delta < 0 else "ties"
                        ] += 1
                    if counts["unpaired_cases"] != len(entries):
                        comparisons.append(
                            {
                                "client": client,
                                "skill": skill,
                                "baseline": baseline,
                                "turn": turn,
                                **counts,
                            }
                        )
    return {
        "study_id": manifest["study_id"],
        "stage": "expansion" if expansion else "core",
        "synthetic_only": synthetic == {True},
        "status": "not_run"
        if not seen
        else "complete"
        if len(seen) == len(planned)
        else "incomplete",
        "planned": len(planned),
        "received": len(seen),
        "missing": len(planned) - len(seen),
        "outcomes": {
            status: list(seen.values()).count(status)
            for status in ("pass", "fail", "blocked")
        },
        "comparisons": comparisons,
        "rates": rates,
        "usage": usage,
        "claim": "No catalog, publication, or client-parity qualification.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--schedule", choices=("core", "expansion"))
    mode.add_argument(
        "--report", type=Path, help="private JSON list of receipt envelopes"
    )
    parser.add_argument(
        "--expansion",
        action="store_true",
        help="report only the separate later-context stage",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=ROOT / "evals/behavior-study-v2/study.json",
        help="explicit frozen v1 or v2 study manifest",
    )
    args = parser.parse_args()
    if args.expansion and not args.report:
        parser.error("--expansion requires --report")
    try:
        manifest = load_manifest(args.manifest)
        errors = check_manifest(manifest)
        if errors:
            raise ValueError("; ".join(errors))
        if args.schedule:
            print(
                json.dumps(schedule(manifest, args.schedule == "expansion"), indent=2)
            )
        elif args.report:
            print(
                json.dumps(
                    report(
                        manifest, json.loads(args.report.read_text()), args.expansion
                    ),
                    indent=2,
                )
            )
        else:
            print(
                "Preparation valid: 24 cases, 432 core cells, 324 expansion cells; all not_run. No clients invoked."
            )
        return 0
    except (OSError, ValueError, TypeError, KeyError) as exc:
        parser.error(str(exc))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
