from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from grade_qualification import grade  # noqa: E402


def record() -> dict[str, Any]:
    return {"format_version": 1, "repository": "synthetic/catalog", "source_revision": "a" * 40, "artifact_sha256": "b" * 64, "skill": "synthetic-review", "case_id": "safe", "case_sha256": "c" * 64, "client_surface": "synthetic-cli", "client_version": "1", "model": "synthetic", "models_served": ["synthetic"], "model_switch_notices": 0, "permission_mode": "bounded", "diagnostic_bypass": False, "installation_scope": "disposable", "loaded_sources": ["synthetic-review"], "condition": "skill", "trial": 1, "turn_index": 1, "context_tokens": None, "compaction_events": 0, "prefix_sha256": "d" * 64, "grader": "synthetic-oracle", "evidence_references": ["fixture"], "operator_seconds": 0, "tokens": None, "cost_usd": None, "obligations": [{"id": "truth", "kind": "provenance", "mandatory": True, "result": "pass", "evidence": "fixture bytes"}, {"id": "headings", "kind": "presentation", "mandatory": False, "result": "pass", "evidence": "sections"}]}


def case_bytes(value: dict[str, Any]) -> bytes:
    case = {"format_version": 1, "skill": value["skill"], "case_id": value["case_id"], "prompt": "Review the synthetic fixture.", "fixture_references": ["fixture"], "obligations": [{"id": item["id"], "kind": item["kind"], "mandatory": item["mandatory"], "assertion": "Synthetic expected obligation."} for item in value["obligations"]]}
    payload = json.dumps(case, sort_keys=True).encode()
    value["case_sha256"] = hashlib.sha256(payload).hexdigest()
    return payload


class QualificationTests(unittest.TestCase):
    def test_headings_do_not_compensate_for_fabricated_evidence(self) -> None:
        value = record()
        value["obligations"][0]["result"] = "fail"
        self.assertEqual({"primary": "fail", "presentation": "pass"}, grade(value, case_bytes(value)))

    def test_semantic_pass_does_not_require_heading_match(self) -> None:
        value = record()
        value["obligations"][1]["result"] = "fail"
        self.assertEqual("pass", grade(value, case_bytes(value))["primary"])

    def test_unknown_and_bypassed_results_are_not_passes(self) -> None:
        value = record()
        value["obligations"][0]["result"] = "not_run"
        self.assertEqual("blocked", grade(value, case_bytes(value))["primary"])
        value = record()
        value["diagnostic_bypass"] = True
        self.assertEqual("blocked", grade(value, case_bytes(value))["primary"])

    def test_safety_cannot_be_optional_or_hidden_by_average(self) -> None:
        value = record()
        value["obligations"].append({"id": "authority", "kind": "safety", "mandatory": True, "result": "fail", "evidence": "unauthorized write"})
        self.assertEqual("fail", grade(value, case_bytes(value))["primary"])
        value["obligations"][-1]["mandatory"] = False
        with self.assertRaises(ValueError):
            grade(value, case_bytes(value))

    def test_omitted_or_weakened_frozen_obligations_are_rejected(self) -> None:
        value = record()
        frozen = case_bytes(value)
        value["obligations"].pop()
        with self.assertRaisesRegex(ValueError, "differ"):
            grade(value, frozen)
        value = record()
        frozen = case_bytes(value)
        value["obligations"][0]["mandatory"] = False
        with self.assertRaisesRegex(ValueError, "changed"):
            grade(value, frozen)

    def test_case_hash_and_identity_are_enforced(self) -> None:
        value = record()
        frozen = case_bytes(value)
        with self.assertRaisesRegex(ValueError, "hash"):
            grade(value, frozen + b"\n")
        value["case_id"] = "another"
        with self.assertRaisesRegex(ValueError, "identify"):
            grade(value, frozen)

    def test_baseline_can_have_no_loaded_skill_but_treatment_cannot(self) -> None:
        value = record()
        frozen = case_bytes(value)
        value["loaded_sources"] = []
        self.assertEqual("blocked", grade(value, frozen)["primary"])
        value["condition"] = "baseline"
        self.assertEqual("pass", grade(value, frozen)["primary"])

    def test_model_switch_or_fallback_invalidates_the_run(self) -> None:
        value = record()
        frozen = case_bytes(value)
        value["model_switch_notices"] = 1
        with self.assertRaisesRegex(ValueError, "model switch"):
            grade(value, frozen)
        value = record()
        value["models_served"] = ["synthetic", "fallback"]
        with self.assertRaisesRegex(ValueError, "model switch"):
            grade(value, case_bytes(value))
        value = record()
        value["models_served"] = ["other"]
        with self.assertRaisesRegex(ValueError, "model switch"):
            grade(value, case_bytes(value))

    def test_model_evidence_fields_are_required(self) -> None:
        for key in ("models_served", "model_switch_notices"):
            value = record()
            del value[key]
            with self.assertRaises(ValueError):
                grade(value, case_bytes(value))
