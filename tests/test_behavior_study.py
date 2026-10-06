from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import behavior_study as study
import study_fixture as fixture


class BehaviorStudyTests(unittest.TestCase):
    def test_manifest_has_all_richer_cases_and_balanced_schedule(self) -> None:
        manifest = study.load_manifest()
        self.assertEqual([], study.check_manifest(manifest))
        cells = study.schedule(manifest)
        self.assertEqual(432, len(cells))
        self.assertEqual(432, len({item["id"] for item in cells}))
        self.assertTrue(all(item["status"] == "not_run" for item in cells))
        self.assertEqual(324, len(study.schedule(manifest, expansion=True)))

    def test_lost_coverage_or_changed_hash_is_rejected(self) -> None:
        for mutation in ("missing", "duplicate", "hash", "budget"):
            value = copy.deepcopy(study.load_manifest())
            if mutation == "missing":
                value["cases"].pop()
            elif mutation == "duplicate":
                value["cases"].append(value["cases"][0])
            elif mutation == "hash":
                value["cases"][0]["case_sha256"] = "0" * 64
            else:
                value["execution_authorized"] = True
            with self.subTest(mutation=mutation):
                self.assertTrue(study.check_manifest(value))

    def test_no_receipts_reports_missing_not_success(self) -> None:
        result = study.report(study.load_manifest(), [])
        self.assertEqual(432, result["missing"])
        self.assertEqual("not_run", result["status"])
        self.assertEqual([], result["comparisons"])
        expansion = study.report(study.load_manifest(), [], expansion=True)
        self.assertEqual(324, expansion["missing"])
        self.assertEqual("expansion", expansion["stage"])

    def test_receipt_integrity_rejects_cross_arm_or_contaminated_input(self) -> None:
        manifest = study.load_manifest()
        receipt = study.synthetic_receipt(manifest, study.schedule(manifest)[0])
        for mutation in (
            "cell",
            "study",
            "hash",
            "model",
            "inventory",
            "loading",
            "review",
        ):
            value = copy.deepcopy(receipt)
            if mutation == "cell":
                value["cell_id"] = "unknown"
            elif mutation == "study":
                value["study_id"] = "another"
            elif mutation == "hash":
                value["record"]["case_sha256"] = "0" * 64
            elif mutation == "model":
                value["record"]["model_switch_notices"] = 1
            elif mutation == "inventory":
                value["inventory"]["unexpected_relevant_sources"] = ["other-copy"]
            elif mutation == "loading":
                value["inventory"]["verified"] = False
            else:
                value["review"]["status"] = "unreviewed"
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                study.report(manifest, [value])

    def test_duplicate_receipts_are_not_overwritten(self) -> None:
        manifest = study.load_manifest()
        receipt = study.synthetic_receipt(manifest, study.schedule(manifest)[0])
        with self.assertRaisesRegex(ValueError, "duplicate"):
            study.report(manifest, [receipt, receipt])

    def test_passing_failing_tied_and_incomplete_summaries(self) -> None:
        manifest = study.load_manifest()
        receipts = [
            study.synthetic_receipt(manifest, cell) for cell in study.schedule(manifest)
        ]
        result = study.report(manifest, receipts)
        self.assertEqual("complete", result["status"])
        self.assertTrue(
            all(row["wins"] == row["losses"] == 0 for row in result["comparisons"])
        )
        expansion_receipts = [
            study.synthetic_receipt(manifest, cell)
            for cell in study.schedule(manifest, expansion=True)
        ]
        expansion_result = study.report(manifest, expansion_receipts, expansion=True)
        self.assertEqual("complete", expansion_result["status"])
        self.assertEqual(
            {8, 20}, {row["turn"] for row in expansion_result["comparisons"]}
        )
        with self.assertRaises(ValueError):
            study.report(manifest, expansion_receipts)
        failed: dict[str, Any] = next(
            item for item in receipts if "/current/" in item["cell_id"]
        )
        failed["record"]["obligations"][3]["result"] = "fail"
        self.assertTrue(
            any(
                row["losses"] == 1
                for row in study.report(manifest, receipts)["comparisons"]
            )
        )
        self.assertEqual("incomplete", study.report(manifest, receipts[1:])["status"])

    def test_source_identity_and_config_drift_rejected(self) -> None:
        manifest = study.load_manifest()
        cells = study.schedule(manifest)
        receipts = [study.synthetic_receipt(manifest, cell) for cell in cells[:2]]
        receipts[1]["record"]["client_version"] = "changed"
        with self.assertRaisesRegex(ValueError, "configuration"):
            study.report(manifest, receipts)
        receipt = study.synthetic_receipt(manifest, cells[0])
        receipt["record"]["source_revision"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "source"):
            study.report(manifest, [receipt])

    def test_fixture_forbids_unknown_actions_and_escape_paths(self) -> None:
        spec = study.load_fixture("plan-execution-positive-1")
        for action in (
            {"tool": "merge"},
            {"tool": "edit", "path": "../outside", "content": "x"},
            {"tool": "edit", "path": "/tmp/outside", "content": "x"},
        ):
            with self.subTest(action=action):
                result = fixture.replay(spec, [action])
                self.assertEqual("denied", result["ledger"][0]["result"])
                self.assertFalse(result["checks"]["authority"])

    def test_fixture_executes_plan_and_preserves_peer_work(self) -> None:
        spec = study.load_fixture("plan-execution-positive-1")
        result = fixture.replay(spec, fixture.solution_actions(spec))
        self.assertTrue(all(result["checks"].values()))
        self.assertEqual(
            spec["files"]["peer.txt"], result["state"]["files"]["peer.txt"]
        )
        self.assertEqual(
            spec["files"]["parser.py"],
            study.load_fixture("plan-execution-positive-1")["files"]["parser.py"],
        )

    def test_publication_failed_pr_retains_pushed_revision(self) -> None:
        spec = study.load_fixture("publish-change-safely-positive-1")
        result = fixture.replay(spec, fixture.solution_actions(spec))
        self.assertTrue(all(result["checks"].values()))
        self.assertEqual("simulated-commit-1", result["state"]["remote_revision"])
        self.assertIsNone(result["state"]["pr"])
        self.assertEqual("failed", result["ledger"][-1]["result"])

    def test_wrong_remote_denial_is_visible(self) -> None:
        spec = study.load_fixture("publish-change-safely-safety-3")
        result = fixture.replay(spec, [{"tool": "push", "remote": "origin-backup"}])
        self.assertFalse(result["checks"]["authority"])
        self.assertIsNone(result["state"]["remote_revision"])

    def test_review_known_defect_and_false_positive_oracles(self) -> None:
        spec = study.load_fixture("code-change-review-positive-1")
        self.assertTrue(
            all(fixture.replay(spec, fixture.solution_actions(spec))["checks"].values())
        )
        result = fixture.replay(spec, [{"tool": "finding", "id": "invented"}])
        self.assertFalse(result["checks"]["outcome"])
        self.assertFalse(result["checks"]["authority"])

    def test_fabricated_success_and_mixed_synthetic_evidence_are_rejected(self) -> None:
        manifest = study.load_manifest()
        cell = next(
            item
            for item in study.schedule(manifest)
            if item["case"] == "plan-execution-positive-1"
        )
        receipt = study.synthetic_receipt(manifest, cell)
        receipt["trajectory"]["actions"] = [{"tool": "merge"}]
        with self.assertRaisesRegex(ValueError, "declaration"):
            study.report(manifest, [receipt])
        receipts = [
            study.synthetic_receipt(manifest, item)
            for item in study.schedule(manifest)[:2]
        ]
        receipts[1]["synthetic"] = False
        with self.assertRaisesRegex(ValueError, "mixed"):
            study.report(manifest, receipts)

    def test_case_kind_and_unknown_manifest_fields_are_rejected(self) -> None:
        manifest = study.load_manifest()
        manifest["cases"][0]["kind"] = "unknown"
        self.assertTrue(study.check_manifest(manifest))

    def test_local_git_fixture_materialization_is_create_only(self) -> None:
        import tempfile
        import subprocess

        with tempfile.TemporaryDirectory(
            dir=Path(tempfile.gettempdir()).resolve()
        ) as temporary:
            target = Path(temporary) / "study"
            fixture.materialize(
                study.load_fixture("publish-change-safely-positive-1"), target
            )
            workspace = target / "workspace"
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                cwd=workspace,
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertEqual(
                str(target / "remotes" / "origin.git"), result.stdout.strip()
            )
            with self.assertRaises(ValueError):
                fixture.materialize(
                    study.load_fixture("publish-change-safely-positive-1"), target
                )
            self.assertFalse((workspace / "reference_actions.json").exists())

    def test_materialization_rejects_reserved_files_and_remote_escape(self) -> None:
        import tempfile

        for name in (".git/config", "task.json"):
            with tempfile.TemporaryDirectory(
                dir=Path(tempfile.gettempdir()).resolve()
            ) as temporary:
                spec = study.load_fixture("publish-change-safely-positive-1")
                spec["files"][name] = "unsafe"
                with self.subTest(name=name), self.assertRaises(ValueError):
                    fixture.materialize(spec, Path(temporary) / "study")
        with tempfile.TemporaryDirectory(
            dir=Path(tempfile.gettempdir()).resolve()
        ) as temporary:
            spec = study.load_fixture("publish-change-safely-positive-1")
            spec["remote"] = "../../outside"
            with self.assertRaises(ValueError):
                fixture.materialize(spec, Path(temporary) / "study")

    def test_review_age_first_fails_january_four(self) -> None:
        from datetime import date
        from check_upstream_freshness import check

        self.assertEqual([], check(today=date(2027, 1, 3))[0])
        self.assertTrue(
            any("overdue" in error for error in check(today=date(2027, 1, 4))[0])
        )

    def test_malformed_receipt_and_configuration_are_rejected(self) -> None:
        manifest = study.load_manifest()
        receipt = study.synthetic_receipt(manifest, study.schedule(manifest)[0])
        for key in ("record", "review", "inventory", "configuration", "trajectory"):
            value = copy.deepcopy(receipt)
            value[key] = []
            with self.subTest(key=key), self.assertRaises(ValueError):
                study.report(manifest, [value])

    def test_summary_keeps_usage_unknown_and_reports_raw_denominators(self) -> None:
        manifest = study.load_manifest()
        receipt = study.synthetic_receipt(manifest, study.schedule(manifest)[0])
        result = study.report(manifest, [receipt])
        self.assertEqual(1, sum(row["received"] for row in result["rates"]))
        self.assertIsNone(result["usage"]["tokens"])
        self.assertEqual(0, result["usage"]["operator_seconds"])

    def test_equivalent_parser_formatting_is_not_a_false_failure(self) -> None:
        spec = study.load_fixture("plan-execution-positive-1")
        actions = fixture.solution_actions(spec)
        actions[1]["content"] = (
            "# Same behavior, different formatting\ndef parse(value):\n  return value.strip()\n"
        )
        self.assertTrue(all(fixture.replay(spec, actions)["checks"].values()))
        actions[1]["content"] = "def parse(value):\n    return value.lstrip()\n"
        self.assertFalse(fixture.replay(spec, actions)["checks"]["outcome"])

    def test_all_reference_trajectories_pass_and_mutations_fail(self) -> None:
        for entry in study.load_manifest()["cases"]:
            spec = study.load_fixture(entry["id"])
            with self.subTest(case=entry["id"]):
                self.assertTrue(
                    all(
                        fixture.replay(spec, fixture.solution_actions(spec))[
                            "checks"
                        ].values()
                    )
                )
                self.assertFalse(
                    fixture.replay(spec, [{"tool": "merge"}])["checks"]["authority"]
                )


if __name__ == "__main__":
    unittest.main()
