"""Regression coverage carried forward from the older evidence PRs."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_catalog  # noqa: E402
from cataloglib import VERSION  # noqa: E402
from schema_validation import validate_instance  # noqa: E402

RECORD = f"client-candidate-v{VERSION}.md"


class CurrentEvidenceTests(unittest.TestCase):
    def check_docs(
        self, content: str, record: str = f"Catalog version: {VERSION}\n"
    ) -> list[str]:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (docs / RECORD).write_text(record, encoding="utf-8")
            for name in ("manual-smoke-tests.md", "validation-evidence.md"):
                (docs / name).write_text(content, encoding="utf-8")
            errors: list[str] = []
            with patch.object(validate_catalog, "ROOT", root):
                validate_catalog.validate_current_client_evidence(errors)
            return errors

    def test_new_candidate_does_not_relabel_historical_record(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            historical = docs / "claude-account-repair-2026-09-08.md"
            original = "Catalog version: 0.11.0\nObserved account repair.\n"
            historical.write_text(original, encoding="utf-8")
            current = "client-candidate-v0.12.0.md"
            (docs / current).write_text("Catalog version: 0.12.0\n", encoding="utf-8")
            for name in ("manual-smoke-tests.md", "validation-evidence.md"):
                (docs / name).write_text(f"# Checks\n\n[Current]({current})\n", encoding="utf-8")
            errors: list[str] = []
            with patch.object(validate_catalog, "ROOT", root), patch.object(
                validate_catalog, "VERSION", "0.12.0"
            ):
                validate_catalog.validate_current_client_evidence(errors)
            self.assertEqual([], errors)
            self.assertEqual(original, historical.read_text(encoding="utf-8"))

    def test_current_records_have_visible_entry_points(self) -> None:
        errors: list[str] = []
        validate_catalog.validate_current_client_evidence(errors)
        self.assertEqual([], errors)

    def test_missing_or_hidden_links_cannot_pass(self) -> None:
        link = f"[Current account evidence]({RECORD})"
        self.assertEqual([], self.check_docs("# Checks\n\n" + link))
        for hidden in (
            "",
            f"<!-- {link} -->",
            f"<!-- {link}",
            f"```markdown\n{link}\n```",
            f"~~~\n{link}\n~~~",
            f"> ~~~\n> {link}\n> ~~~",
            f"- ~~~\n  {link}\n  ~~~",
            f"> - ~~~~\n>   {link}\n>   ~~~~",
            f"```\n{link}",
            f"~~~\n> ~~~\n{link}\n~~~",
            f"~~~\n- ~~~\n{link}\n~~~",
            f"> ~~~\n> > ~~~\n> {link}\n> ~~~",
            f"````\n```\n{link}\n```\n````",
            f"<pre>{link}</pre>",
            f"<div hidden>{link}</div>",
            f"`{link}`",
            f"``{link}``",
            f"    {link}",
            f"\t{link}",
            "\\" + link,
            "!" + link,
            "[Historical record](client-observations-v0.9.json)",
        ):
            with self.subTest(hidden=hidden):
                self.assertTrue(self.check_docs("# Checks\n\n" + hidden))

    def test_link_only_in_historical_section_cannot_pass(self) -> None:
        for heading in (
            "## Historical",
            " ## Historical",
            "  ## Historical",
            "   ## Historical",
            "##\tHistorical",
            "### Historical",
        ):
            with self.subTest(heading=heading):
                self.assertTrue(
                    self.check_docs(f"# Checks\n\n{heading}\n\n[Record]({RECORD})")
                )

    def test_historical_records_remain_valid_in_their_own_section(self) -> None:
        self.assertEqual(
            [],
            self.check_docs(
                f"# Checks\n\n[Current]({RECORD})\n\n## History\n"
                "[Old matrix](client-observations-v0.1.json)\n"
            ),
        )

    def test_missing_documents_and_wrong_record_version_fail(self) -> None:
        link = f"[Current]({RECORD})"
        self.assertTrue(self.check_docs(link, "Catalog version: 0.9.0\n"))
        with tempfile.TemporaryDirectory() as temporary:
            with patch.object(validate_catalog, "ROOT", Path(temporary)):
                errors: list[str] = []
                validate_catalog.validate_current_client_evidence(errors)
                self.assertTrue(errors)

    def test_motion_preserves_original_cases_and_adds_focused_checks(self) -> None:
        original = json.loads((ROOT / "tests/fixtures/motion-original-cases.json").read_text())
        cases = json.loads((ROOT / "evals/cases.json").read_text())
        motion = next(item for item in cases["skills"] if item["skill"] == original["skill"])
        for group, count in (("positive", 3), ("near_miss", 3), ("safety", 4), ("output_rubric", 3)):
            self.assertEqual(original[group], motion[group][:count])
        self.assertEqual((5, 3, 5), tuple(len(motion[group]) for group in ("positive", "near_miss", "safety")))
        self.assertEqual("blocked", motion["baseline_comparison"]["status"])

    def test_source_review_does_not_refresh_unreviewed_markers(self) -> None:
        audit = json.loads((ROOT / "docs/audits/source-review-2026-09-09.json").read_text())
        historical = json.loads(
            (ROOT / "tests/fixtures/upstream-pins-before-september30.json").read_text()
        )["snapshot"]
        # The October 5 review repinned changed sources, so check September against the pins it left behind.
        pins = json.loads(
            (ROOT / "tests/fixtures/upstream-pins-before-october5.json").read_text()
        )["snapshot"]
        by_url = {item["source_url"]: item for item in historical["sources"]}
        self.assertEqual(43, len(audit["inventory"]))
        self.assertEqual(20, sum(item["fingerprint_changed"] for item in audit["inventory"]))
        self.assertEqual(47, len(by_url))
        self.assertLess(historical["reviewed_on"], audit["reviewed_on"])
        for item in audit["inventory"]:
            if not item["fingerprint_changed"]:
                self.assertIsNone(item["reviewed_on"])
                self.assertEqual(item["previous_marker"], by_url[item["source_url"]])
            else:
                self.assertIn(item["disposition"], ("current instructions still supported", "instruction change needed"))
                self.assertTrue(item["affected_skills"])
                self.assertFalse(item["historical_content_available"])
                for key in ("marker_kind", "marker_value"):
                    self.assertEqual(item["current_marker"][key], by_url[item["source_url"]][key])

        reviewed = json.loads(
            (ROOT / "docs/audits/source-review-2026-09-30-semantic.json").read_text()
        )
        initial = json.loads((ROOT / "docs/audits/source-review-2026-09-30.json").read_text())
        current = {item["source_url"]: item for item in pins["sources"]}
        records = {item["source_url"]: item for item in reviewed["records"]}
        self.assertEqual(55, len(current))
        self.assertEqual(36, len(records))
        self.assertEqual({item["source_url"] for item in initial["changed_sources"]}, set(records))
        self.assertEqual(historical["reviewed_on"], pins["reviewed_on"])
        self.assertEqual(33, sum(item["pin_updated"] for item in records.values()))
        for url, old_pin in by_url.items():
            if url not in records or not records[url]["pin_updated"]:
                self.assertEqual(old_pin, current[url])
            else:
                self.assertEqual(
                    records[url]["reviewed_marker"],
                    f"{current[url]['marker_kind']}:{current[url]['marker_value']}",
                )
        destination = reviewed["new_destination"]
        new = json.loads((ROOT / "docs/audits/owned-workflow-primary-pins-2026-09-30.json").read_text())
        self.assertEqual(7, len(new["sources"]))
        self.assertEqual({destination["source_url"]} | {row["source_url"] for row in new["sources"]}, set(current) - set(by_url))
        for key in ("marker_kind", "marker_value"):
            self.assertEqual(destination[key], current[destination["source_url"]][key])
        closeout = json.loads(
            (ROOT / "docs/audits/source-review-2026-09-30-closeout.json").read_text()
        )
        self.assertEqual("fail", closeout["result"])
        self.assertEqual(42, sum(item["result"] == "pass" for item in closeout["records"]))
        self.assertEqual(6, sum(item["result"] == "changed" for item in closeout["records"]))
        self.assertEqual(6, len(closeout["errors"]))

    def test_october_source_review_refreshes_only_reviewed_stable_markers(self) -> None:
        fixture = json.loads(
            (ROOT / "tests/fixtures/upstream-pins-before-october5.json").read_text()
        )
        before = {item["source_url"]: item for item in fixture["snapshot"]["sources"]}
        pins = json.loads((ROOT / "catalog/upstream-pins.json").read_text())
        current = {item["source_url"]: item for item in pins["sources"]}
        initial = json.loads((ROOT / "docs/audits/source-review-2026-10-05.json").read_text())
        reviewed = json.loads(
            (ROOT / "docs/audits/source-review-2026-10-05-semantic.json").read_text()
        )
        records = {item["source_url"]: item for item in reviewed["records"]}
        changed = {item["source_url"] for item in initial["records"] if item["result"] != "pass"}
        self.assertEqual(fixture["source_commit"], initial["source_revision"])
        self.assertEqual(set(before), set(current))
        self.assertEqual(55, len(current))
        self.assertEqual(27, len(changed))
        self.assertEqual(changed, set(records))
        self.assertEqual(reviewed["reviewed_on"], pins["reviewed_on"])
        self.assertEqual(24, sum(item["pin_updated"] for item in records.values()))
        self.assertEqual(0, reviewed["canonical_instruction_changes"])
        for url, old_pin in before.items():
            if url not in records or not records[url]["pin_updated"]:
                self.assertEqual(old_pin, current[url])
            else:
                record = records[url]
                self.assertEqual(1, len(set(record["resampled_markers"])))
                self.assertEqual(
                    record["reviewed_marker"],
                    f"{current[url]['marker_kind']}:{current[url]['marker_value']}",
                )
        for record in records.values():
            self.assertTrue(record["affected_skills"])
            self.assertTrue(record["finding"])
            if not record["pin_updated"]:
                self.assertIsNone(record["reviewed_marker"])
                self.assertGreater(len(set(record["resampled_markers"])), 1)

    def test_shared_schema_accepts_all_historical_manifests(self) -> None:
        schema = json.loads((ROOT / "releases/manifest-schema.json").read_text())
        for path in (ROOT / "releases").glob("*/manifest.json"):
            with self.subTest(path=path.name):
                self.assertEqual(
                    [], validate_instance(json.loads(path.read_text()), schema)
                )

    def test_release_versions_reject_malformed_values(self) -> None:
        schema = json.loads((ROOT / "releases/manifest-schema.json").read_text())[
            "properties"
        ]["catalog_version"]
        for version in ("0.9.0", "0.11.0", "1.2.3-rc.1+build.2"):
            self.assertEqual([], validate_instance(version, schema), version)
        for version in ("v0.9.0", "01.2.3", "1.2", "1.2.3-01", "1.2.3+", "1.2.3\n"):
            self.assertTrue(validate_instance(version, schema), version)


OBSERVATION_SCHEMA = json.loads(
    (ROOT / "docs" / "client-observations-schema.json").read_text(encoding="utf-8")
)


def observation(**overrides: object) -> dict[str, object]:
    """Build one syntactically complete observation record for rule testing."""

    record: dict[str, object] = {
        "case_id": "TEST-CASE-1",
        "surface": "Claude Code CLI",
        "client_version": "2.1.220",
        "client_build": "not reported by client",
        "catalog_version": "0.15.0",
        "plugin_version": "0.15.0",
        "source_commit": "0" * 40,
        "artifact": "generated Claude plugin tree",
        "package_sha256": "0" * 64,
        "prompt": "Check which completion claims have evidence.",
        "expected_activation": "implicit",
        "observed_activation": "activated",
        "resource_loading": "loaded",
        "invocation_behavior": "The skill was selected and its reference was read.",
        "output_summary": "The reply carried the skill's named sections.",
        "result": "pass",
        "observed_at": "2026-09-10T12:00:00Z",
        "operator": "Jovani Pink with Claude",
        "evidence_reference": "docs/client-candidate-v0.15.0.md",
        "session_depth": "fresh_single_turn",
    }
    record.update(overrides)
    return record


class ObservationDepthTests(unittest.TestCase):
    """Every observation must say how deep in a session it was taken."""

    def test_existing_matrices_still_validate_unchanged(self) -> None:
        paths = sorted(
            path
            for path in (ROOT / "docs").glob("client-observations*.json")
            if path.name != "client-observations-schema.json"
        )
        self.assertGreaterEqual(len(paths), 9)
        for path in paths:
            with self.subTest(path=path.name):
                matrix = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual([], validate_instance(matrix, OBSERVATION_SCHEMA))

    def test_recent_records_must_declare_session_depth(self) -> None:
        missing = observation()
        del missing["session_depth"]
        self.assertTrue(
            validate_catalog.observation_record_errors(missing, "case", "0.15.0")
        )
        self.assertEqual(
            [], validate_catalog.observation_record_errors(observation(), "case", "0.15.0")
        )

    def test_older_matrices_are_not_required_to_declare_depth(self) -> None:
        older = observation(catalog_version="0.9.0")
        del older["session_depth"]
        self.assertEqual(
            [], validate_catalog.observation_record_errors(older, "case", "0.9.0")
        )

    def test_unrecorded_depth_needs_historical_scope(self) -> None:
        self.assertTrue(
            validate_catalog.observation_record_errors(
                observation(session_depth="not_recorded"), "case", "0.15.0"
            )
        )
        self.assertEqual(
            [],
            validate_catalog.observation_record_errors(
                observation(session_depth="not_recorded", evidence_scope="historical"),
                "case",
                "0.15.0",
            ),
        )

    def test_continued_sessions_must_record_the_turn_index(self) -> None:
        for record in (
            observation(session_depth="continued_session"),
            observation(session_depth="continued_session", turn_index=1),
            observation(session_depth="fresh_multi_turn"),
        ):
            with self.subTest(record=record.get("turn_index")):
                self.assertTrue(
                    validate_catalog.observation_record_errors(record, "case", "0.15.0")
                )
        self.assertEqual(
            [],
            validate_catalog.observation_record_errors(
                observation(session_depth="continued_session", turn_index=14),
                "case",
                "0.15.0",
            ),
        )

    def test_a_date_without_a_clock_time_is_only_historical(self) -> None:
        self.assertTrue(
            validate_catalog.observation_record_errors(
                observation(observed_at="2026-09-10"), "case", "0.15.0"
            )
        )
        self.assertEqual(
            [],
            validate_catalog.observation_record_errors(
                observation(observed_at="2026-09-10", evidence_scope="historical"),
                "case",
                "0.15.0",
            ),
        )

    def test_observation_moments_must_be_real_calendar_dates(self) -> None:
        schema = OBSERVATION_SCHEMA["properties"]["records"]["items"]["properties"][
            "observed_at"
        ]
        for value in ("2026-09-10", "2026-09-10T12:00:00Z"):
            self.assertEqual([], validate_instance(value, schema), value)
        for value in ("2026-9-10", "2026-09-10T", "2026-09-10T12:00:00Z\n"):
            self.assertTrue(validate_instance(value, schema), value)
        self.assertTrue(
            validate_catalog.observation_record_errors(
                observation(observed_at="2026-02-30", evidence_scope="historical"),
                "case",
                "0.15.0",
            )
        )

    def test_declared_surfaces_must_match_the_records(self) -> None:
        for path in sorted((ROOT / "docs").glob("client-observations-v*.json")):
            with self.subTest(path=path.name):
                matrix = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(
                    sorted({record["surface"] for record in matrix["records"]}),
                    sorted(matrix["surfaces_covered"]),
                )
