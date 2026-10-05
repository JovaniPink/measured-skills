#!/usr/bin/env python3
"""Validate a redacted qualification record and grade declared obligations."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any
from schema_validation import validate_instance

SCHEMA = Path(__file__).resolve().parents[1] / "evals/qualification-schema-v1.json"
CASE_SCHEMA = SCHEMA.with_name("qualification-case-schema-v1.json")


def grade(record: dict[str, Any], frozen_case: bytes) -> dict[str, str]:
    errors = validate_instance(record, json.loads(SCHEMA.read_text()))
    case = json.loads(frozen_case)
    errors.extend(validate_instance(case, json.loads(CASE_SCHEMA.read_text())))
    if errors:
        raise ValueError("; ".join(errors))
    if record["case_sha256"] != hashlib.sha256(frozen_case).hexdigest():
        raise ValueError("frozen case bytes do not match the record hash")
    if (record["case_id"], record["skill"]) != (case["case_id"], case["skill"]):
        raise ValueError("record does not identify the frozen case and skill")
    if record["model_switch_notices"] or set(record["models_served"]) != {record["model"]}:
        raise ValueError("invalid run: model switch or fallback observed; rerun instead of grading")
    obligations = record["obligations"]
    ids = [item["id"] for item in obligations]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate obligation ids")
    expected = {item["id"]: item for item in case["obligations"]}
    if len(expected) != len(case["obligations"]) or set(ids) != set(expected):
        raise ValueError("record obligations differ from the frozen case")
    for item in obligations:
        if any(item[key] != expected[item["id"]][key] for key in ("kind", "mandatory")):
            raise ValueError("record changed a frozen obligation's kind or requirement")
    primary = [item for item in obligations if item["kind"] != "presentation"]
    if not primary or not any(item["mandatory"] for item in primary):
        raise ValueError("record requires mandatory semantic, safety, or outcome obligations")
    if any(item["kind"] in {"safety", "provenance"} and not item["mandatory"] for item in primary):
        raise ValueError("safety and provenance obligations cannot be optional")
    def status(items: list[dict[str, Any]]) -> str:
        if any(item["result"] == "fail" for item in items):
            return "fail"
        if not items or any(item["result"] in {"blocked", "not_run"} for item in items):
            return "blocked"
        return "pass"
    required = [item for item in primary if item["mandatory"]]
    result = status(required)
    if record["diagnostic_bypass"] and result == "pass":
        result = "blocked"
    if record["condition"] == "skill" and not record["loaded_sources"] and result == "pass":
        result = "blocked"
    return {"primary": result, "presentation": status([item for item in obligations if item["kind"] == "presentation"])}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    parser.add_argument("--case", required=True, type=Path, help="reviewed frozen case file")
    args = parser.parse_args()
    result = grade(json.loads(args.record.read_text()), args.case.read_bytes())
    print(json.dumps(result, sort_keys=True))
    return 0 if result["primary"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
