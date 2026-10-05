from __future__ import annotations

import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from importlib.metadata import PackageNotFoundError
from pathlib import Path
from types import TracebackType
from typing import ClassVar, Literal
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_distributions import build, marketplace_documents  # noqa: E402
from cataloglib import (  # noqa: E402
    EXPLICIT_SKILLS,
    SKILLS,
    VERSION,
    filter_revoked,
    read_skill_metadata,
    skills_by_plugin,
)
from check_upstream_freshness import (  # noqa: E402
    NORMALIZED_HTML_HOSTS,
    VISIBLE_TEXT_URLS,
    _normalized_content_sha256,
    _visible_text_sha256,
    check as check_upstream_freshness,
)
from check_workflows import (  # noqa: E402
    PYYAML_VERSION,
    check as check_workflows,
    workflow_syntax_errors,
)
from check_generated import check as check_generated  # noqa: E402
from check_originality import check as check_originality  # noqa: E402
from check_public_boundary import _publishable_paths, scan as scan_public_boundary  # noqa: E402
from check_repository_independence import (  # noqa: E402
    check as check_repository_independence,
    provenance_source_errors,
    scan_text as scan_repository_independence,
)
from evaluate_gate_fixtures import evaluate as evaluate_gate_fixtures  # noqa: E402
from package_claude_ai import package  # noqa: E402
from schema_validation import validate_instance  # noqa: E402
from sync_private_overlay import sync as sync_private_overlay  # noqa: E402
import sync_private_overlay as overlay_module  # noqa: E402
from sync_private_overlay import _replace_projection  # noqa: E402
from validate_catalog import (  # noqa: E402
    immutable_action_reference_errors,
    profile_measurement_surface_errors,
    release_manifest_current_errors,
    release_manifest_source_errors,
    skill_name_errors,
    validate_all,
    validate_ci_tools,
    validate_packages,
)


class CatalogTests(unittest.TestCase):
    def test_catalog_and_generated_distributions_validate(self) -> None:
        self.assertEqual([], validate_all(require_packages=True))
        self.assertEqual([], check_generated())
        self.assertEqual([], check_originality())
        self.assertEqual([], check_repository_independence())
        self.assertEqual([], scan_public_boundary())

    def test_retired_external_audit_records_are_absent(self) -> None:
        retired = {
            "provenance/public-source-audit.json",
            "provenance/public-source-audit-schema.json",
            "provenance/inventory-summary.json",
            "provenance/inventory-summary-schema.json",
        }
        self.assertEqual(
            retired, {path for path in retired if not (ROOT / path).exists()}
        )

    def test_reasoning_plugin_keeps_discovery_scope_focused(self) -> None:
        reasoning = skills_by_plugin()["measured-reasoning"]
        self.assertEqual(11, len(reasoning))
        descriptions = [
            read_skill_metadata(ROOT / "skills" / skill)["description"]
            for skill in reasoning
        ]
        self.assertLess(sum(len(description) for description in descriptions), 4000)
        self.assertEqual(len(descriptions), len(set(descriptions)))

    def test_reader_guide_matches_canonical_catalog(self) -> None:
        guide = (ROOT / "docs" / "skill-catalog-reader-guide.md").read_text(
            encoding="utf-8"
        )
        canonical = skills_by_plugin()
        section_plugins = {
            "## Next.js workflows: measured-nextjs-workflows": "measured-nextjs-workflows",
            "## Swift workflows: measured-swift-workflows": "measured-swift-workflows",
            "## Core skills: measured-skills": "measured-skills",
            "## Engineering build: measured-engineering-build": "measured-engineering-build",
            "## Engineering review: measured-engineering-review": "measured-engineering-review",
            "## Engineering delivery: measured-engineering-delivery": "measured-engineering-delivery",
            "## Stack profiles: measured-stack-profiles": "measured-stack-profiles",
            "## Operations skills: measured-operations": "measured-operations",
            "## Reasoning skills: measured-reasoning": "measured-reasoning",
            "## AI systems skills: measured-ai-systems": "measured-ai-systems",
            "## Agent platform skills: measured-agent-platforms": "measured-agent-platforms",
        }
        documented: dict[str, list[str]] = {plugin: [] for plugin in canonical}
        documented_explicit: set[str] = set()
        current_plugin: str | None = None
        current_skill: str | None = None

        for line in guide.splitlines():
            if line in section_plugins:
                current_plugin = section_plugins[line]
                current_skill = None
            elif line.startswith("## "):
                current_plugin = None
                current_skill = None
            elif current_plugin and line.startswith("### "):
                current_skill = line.removeprefix("### ")
                documented[current_plugin].append(current_skill)
            elif current_skill and line == "Invocation: `explicit-only`.":
                documented_explicit.add(current_skill)

        self.assertEqual(
            {plugin: list(skills) for plugin, skills in canonical.items()},
            documented,
        )
        self.assertEqual(set(EXPLICIT_SKILLS), documented_explicit)
        self.assertIn(f"contains {len(SKILLS)} portable agent skills", guide)

        for plugin, skills in canonical.items():
            explicit = [skill for skill in skills if skill in EXPLICIT_SKILLS]
            explicit_cell = ", ".join(f"`{skill}`" for skill in explicit) or "None"
            self.assertIn(f"| `{plugin}` | {len(skills)} | {explicit_cell} |", guide)
        self.assertIn(
            f"| **Total** | **{len(SKILLS)}** | **{len(EXPLICIT_SKILLS)} skills** |",
            guide,
        )

    def test_skill_cheatsheet_matches_canonical_catalog(self) -> None:
        cheatsheet = (ROOT / "docs" / "skill-cheatsheet.md").read_text(encoding="utf-8")
        canonical = skills_by_plugin()
        section_plugins = {
            "## Next.js workflows: measured-nextjs-workflows": "measured-nextjs-workflows",
            "## Swift workflows: measured-swift-workflows": "measured-swift-workflows",
            "## Core: measured-skills": "measured-skills",
            "## Engineering build: measured-engineering-build": "measured-engineering-build",
            "## Engineering review: measured-engineering-review": "measured-engineering-review",
            "## Engineering delivery: measured-engineering-delivery": "measured-engineering-delivery",
            "## Stack profiles: measured-stack-profiles": "measured-stack-profiles",
            "## Operations: measured-operations": "measured-operations",
            "## Reasoning: measured-reasoning": "measured-reasoning",
            "## AI systems: measured-ai-systems": "measured-ai-systems",
            "## Agent platforms: measured-agent-platforms": "measured-agent-platforms",
        }
        documented: dict[str, list[str]] = {plugin: [] for plugin in canonical}
        documented_invocation: dict[str, str] = {}
        current_plugin: str | None = None

        for line in cheatsheet.splitlines():
            if line in section_plugins:
                current_plugin = section_plugins[line]
            elif line.startswith("## "):
                current_plugin = None
            elif current_plugin and line.startswith("| `"):
                cells = [cell.strip() for cell in line.strip("|").split("|")]
                skill = cells[0].strip("`")
                documented[current_plugin].append(skill)
                documented_invocation[skill] = cells[2]

        self.assertEqual(
            {plugin: list(skills) for plugin, skills in canonical.items()},
            documented,
        )
        self.assertEqual(set(SKILLS), set(documented_invocation))
        for skill, invocation in documented_invocation.items():
            expected = "Explicit-only" if skill in EXPLICIT_SKILLS else "Implicit"
            self.assertEqual(expected, invocation, skill)
        self.assertIn(f"catalog contains {len(SKILLS)} skills", cheatsheet)

    def test_v06_mutating_workflows_are_explicit_and_bounded(self) -> None:
        expected = {
            "prototype-spike",
            "merge-conflict-reconciliation",
            "guided-configuration",
            "task-handoff",
            "workflow-retrospective",
        }
        self.assertTrue(expected.issubset(EXPLICIT_SKILLS))
        conflict = (
            ROOT / "skills" / "merge-conflict-reconciliation" / "SKILL.md"
        ).read_text(encoding="utf-8")
        for boundary in ("abort", "Stage, continue, commit, push", "destructive reset"):
            self.assertIn(boundary, conflict)
        prototype = (ROOT / "skills" / "prototype-spike" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("not production readiness", prototype)
        self.assertIn(
            "Do not commit, merge, deploy, migrate, publish, or promote", prototype
        )

    def test_v06_focused_references_exist(self) -> None:
        references = {
            "implementation-planning": {
                "specification-synthesis.md",
                "work-packages.md",
                "decision-map.md",
            },
            "multi-agent-orchestration": {
                "candidate-comparison.md",
                "coverage-fanout.md",
                "client-mapping.md",
            },
        }
        for skill, expected in references.items():
            actual = {
                path.name
                for path in (ROOT / "skills" / skill / "references").glob("*.md")
            }
            self.assertTrue(expected.issubset(actual))

    def test_originality_scan_rejects_generic_copy_attribution(self) -> None:
        with tempfile.TemporaryDirectory(prefix="originality-regression-") as temporary:
            candidate = Path(temporary) / "SKILL.md"
            candidate.write_text(
                "This workflow was copied " + "from an upstream skill.\n",
                encoding="utf-8",
            )
            from check_originality import _scan_text

            errors = _scan_text(
                candidate.as_posix(), candidate.read_text(encoding="utf-8")
            )
            self.assertEqual(1, len(errors))
            self.assertIn("external implementation attribution", errors[0])

    def test_repository_independence_rejects_external_repositories_and_mappings(
        self,
    ) -> None:
        repository_url = "https://" + "github.com/" + "example-org/example-skills"
        marketplace_id = "marketplace add " + "example-org/example-skills"
        package_id = "plugin install " + "external-skill@external-marketplace"
        mapping = '"public_' + 'mapping": ["local-skill"]'
        self.assertTrue(scan_repository_independence("fixture.md", repository_url))
        self.assertTrue(scan_repository_independence("fixture.md", marketplace_id))
        self.assertTrue(scan_repository_independence("fixture.md", package_id))
        self.assertTrue(scan_repository_independence("fixture.json", mapping))

    def test_primary_authority_hosts_gate_provenance_sources(self) -> None:
        from check_repository_independence import PRIMARY_AUTHORITY_HOSTS

        self.assertIn("docs.oasis-open.org", PRIMARY_AUTHORITY_HOSTS)
        self.assertNotIn("example.com", PRIMARY_AUTHORITY_HOSTS)
        pinned = {
            source["source_url"]
            for source in json.loads(
                (ROOT / "catalog" / "upstream-pins.json").read_text(encoding="utf-8")
            )["sources"]
        }
        for entry in json.loads(
            (ROOT / "provenance" / "catalog.json").read_text(encoding="utf-8")
        )["entries"]:
            self.assertIn(entry["source_url"], pinned)

    def test_repository_independence_keeps_narrow_repository_link_exceptions(
        self,
    ) -> None:
        owned = "https://" + "github.com/" + "JovaniPink/measured-skills"
        action = "https://" + "github.com/" + "actions/checkout"
        ci_tool = "https://" + "github.com/" + "python/mypy"
        workflow_parser = "https://" + "github.com/" + "yaml/pyyaml"
        package_id = "plugin install " + "measured-engineering@measured-skills"
        self.assertEqual([], scan_repository_independence("README.md", owned))
        self.assertEqual(
            [], scan_repository_independence("provenance/ci-actions.json", action)
        )
        self.assertEqual(
            [], scan_repository_independence("provenance/ci-tools.json", ci_tool)
        )
        self.assertEqual(
            [],
            scan_repository_independence("provenance/ci-tools.json", workflow_parser),
        )
        self.assertEqual([], scan_repository_independence("docs/README.md", package_id))
        self.assertTrue(scan_repository_independence("docs/example.md", action))
        self.assertTrue(scan_repository_independence("docs/example.md", ci_tool))

    def test_repository_independence_allows_only_the_reviewed_google_agents_cli_link(
        self,
    ) -> None:
        agents_cli = "https://" + "github.com/" + "google/agents-cli"
        unrelated = "https://" + "github.com/" + "google/unrelated"
        self.assertEqual(
            [], scan_repository_independence("docs/google-adk.md", agents_cli)
        )
        self.assertTrue(scan_repository_independence("docs/example.md", agents_cli))
        self.assertTrue(scan_repository_independence("docs/google-adk.md", unrelated))

    def test_provenance_sources_are_primary_authorities(self) -> None:
        self.assertEqual([], provenance_source_errors())

    def test_v09_taxonomy_reconciles_with_canonical_skills(self) -> None:
        schema = json.loads(
            (ROOT / "catalog" / "skills-schema.json").read_text(encoding="utf-8")
        )
        catalog = json.loads(
            (ROOT / "catalog" / "skills.json").read_text(encoding="utf-8")
        )
        self.assertEqual([], validate_instance(catalog, schema))
        records = {record["skill"]: record for record in catalog["skills"]}
        self.assertEqual(set(SKILLS), set(records))
        for skill, record in records.items():
            metadata = read_skill_metadata(ROOT / "skills" / skill)
            self.assertEqual(metadata["plugin"], record["plugin"])
            self.assertEqual(metadata["risk_class"], record["risk_class"])
            self.assertEqual(metadata["invocation"], record["invocation"])
            self.assertTrue((ROOT / record["maturity_evidence"]).is_file())
            self.assertNotIn(skill, record["composes_with"])
            self.assertNotIn(skill, record["conflicts_with"])
            for related in record["composes_with"] + record["conflicts_with"]:
                self.assertIn(related, records)

    def test_v09_packs_and_recipes_reconcile_and_fit_discovery_budget(self) -> None:
        schema = json.loads(
            (ROOT / "catalog" / "packs-schema.json").read_text(encoding="utf-8")
        )
        catalog = json.loads(
            (ROOT / "catalog" / "packs.json").read_text(encoding="utf-8")
        )
        self.assertEqual([], validate_instance(catalog, schema))
        plugins = skills_by_plugin()
        packs = {record["plugin"]: record for record in catalog["plugin_packs"]}
        self.assertEqual(set(plugins), set(packs))
        for plugin, record in packs.items():
            self.assertEqual(list(plugins[plugin]), record["skills"])
            expected = sum(
                len(read_skill_metadata(ROOT / "skills" / skill)["description"])
                for skill in record["skills"]
            )
            self.assertEqual(expected, record["description_characters"])
            expected_status = (
                "over-limit"
                if expected > 8000
                else "warning"
                if expected >= 6000
                else "within-budget"
            )
            self.assertEqual(expected_status, record["budget_status"])

        for recipe in catalog["recipes"]:
            self.assertIn(len(recipe["skills"]), {2, 3})
            self.assertEqual(len(recipe["skills"]), len(set(recipe["skills"])))
            expected = sum(
                len(read_skill_metadata(ROOT / "skills" / skill)["description"])
                for skill in recipe["skills"]
            )
            self.assertEqual(expected, recipe["description_characters"])
            self.assertLessEqual(recipe["description_characters"], 8000)
            expected_status = "warning" if expected >= 6000 else "within-budget"
            self.assertEqual(expected_status, recipe["budget_status"])

    def test_v10_profiles_are_skill_level_activation_units(self) -> None:
        schema = json.loads(
            (ROOT / "catalog" / "profiles-schema.json").read_text(encoding="utf-8")
        )
        catalog = json.loads(
            (ROOT / "catalog" / "profiles.json").read_text(encoding="utf-8")
        )
        self.assertEqual([], validate_instance(catalog, schema))
        profiles = {record["id"]: record for record in catalog["profiles"]}
        delivery = profiles["delivery-typescript-experimental"]
        self.assertEqual(
            [
                "problem-framing",
                "implementation-planning",
                "test-driven-change",
                "cross-stack-quality-gates",
                "code-change-review",
                "publish-change-safely",
                "typescript-javascript-engineering-profile",
            ],
            delivery["skills"],
        )
        self.assertEqual("experimental", delivery["disposition"])
        self.assertEqual("none", delivery["behavioral_evidence"]["status"])
        self.assertIsNone(delivery["behavioral_evidence"]["evidence_reference"])
        self.assertEqual(
            {"codex", "claude-code", "antigravity-cli"},
            set(delivery["target_surfaces"]),
        )
        self.assertNotEqual(
            delivery["discovery_measurements"]["codex"]["budget_policy"],
            delivery["discovery_measurements"]["claude-code"]["budget_policy"],
        )
        antigravity = delivery["discovery_measurements"]["antigravity-cli"]
        self.assertEqual("not_observed", antigravity["observed_listing_state"])
        self.assertNotRegex(
            antigravity["budget_policy"], r"\b(?:8000|8,000|one percent|1%)\b"
        )
        self.assertEqual("blocked", delivery["surface_evidence"]["codex"]["status"])
        self.assertEqual(
            "blocked", delivery["surface_evidence"]["antigravity-cli"]["status"]
        )
        self.assertIn(
            "publish-change-safely",
            delivery["surface_evidence"]["antigravity-cli"]["reason"],
        )
        self.assertEqual(
            set(delivery["target_surfaces"]), set(delivery["surface_evidence"])
        )
        self.assertEqual(
            set(delivery["target_surfaces"]), set(delivery["discovery_measurements"])
        )

    def test_v10_profiles_allow_every_target_surface_only_when_measurements_match(
        self,
    ) -> None:
        schema = json.loads(
            (ROOT / "catalog" / "profiles-schema.json").read_text(encoding="utf-8")
        )
        catalog = json.loads(
            (ROOT / "catalog" / "profiles.json").read_text(encoding="utf-8")
        )
        candidate = copy.deepcopy(catalog["profiles"][0])
        measurement = candidate["discovery_measurements"].pop("codex")
        evidence = candidate["surface_evidence"].pop("codex")
        candidate["target_surfaces"] = ["gemini-managed-agent"]
        candidate["discovery_measurements"] = {"gemini-managed-agent": measurement}
        candidate["surface_evidence"] = {"gemini-managed-agent": evidence}
        self.assertEqual(
            [],
            validate_instance(
                {
                    "$schema": "./profiles-schema.json",
                    "catalog_version": VERSION,
                    "profiles": [candidate],
                },
                schema,
            ),
        )
        self.assertEqual([], profile_measurement_surface_errors(candidate))

        missing = copy.deepcopy(candidate)
        missing["discovery_measurements"] = {}
        self.assertTrue(
            validate_instance(
                {
                    "$schema": "./profiles-schema.json",
                    "catalog_version": VERSION,
                    "profiles": [missing],
                },
                schema,
            )
        )
        self.assertTrue(profile_measurement_surface_errors(missing))

        extra = copy.deepcopy(candidate)
        extra["discovery_measurements"]["codex"] = measurement
        self.assertEqual(
            [],
            validate_instance(
                {
                    "$schema": "./profiles-schema.json",
                    "catalog_version": VERSION,
                    "profiles": [extra],
                },
                schema,
            ),
        )
        self.assertTrue(profile_measurement_surface_errors(extra))

    def test_v10_profile_schema_resolves_measurement_references_and_nullable_types(
        self,
    ) -> None:
        schema = json.loads(
            (ROOT / "catalog" / "profiles-schema.json").read_text(encoding="utf-8")
        )
        catalog = json.loads(
            (ROOT / "catalog" / "profiles.json").read_text(encoding="utf-8")
        )
        broken = copy.deepcopy(catalog)
        profile = broken["profiles"][0]
        del profile["discovery_measurements"]["codex"]["budget_policy"]
        profile["behavioral_evidence"] = {
            "status": "partial",
            "observed_against_version": 10,
            "observed_at": {},
            "evidence_reference": [],
        }
        errors = validate_instance(broken, schema)
        self.assertTrue(any("budget_policy" in error for error in errors))
        self.assertTrue(any("observed_against_version" in error for error in errors))
        self.assertTrue(any("observed_at" in error for error in errors))
        self.assertTrue(any("evidence_reference" in error for error in errors))

    def test_v10_google_surfaces_are_independent_and_preconditioned(self) -> None:
        schema = json.loads(
            (ROOT / "catalog" / "google-surfaces-schema.json").read_text(
                encoding="utf-8"
            )
        )
        catalog = json.loads(
            (ROOT / "catalog" / "google-surfaces.json").read_text(encoding="utf-8")
        )
        self.assertEqual([], validate_instance(catalog, schema))
        records = {record["surface"]: record for record in catalog["records"]}
        expected = {
            "antigravity-cli",
            "gemini-cli-enterprise",
            "antigravity-desktop",
            "antigravity-sdk",
            "gemini-managed-agent",
            "google-adk",
            "agents-cli",
            "data-agent-kit",
            "gemini-enterprise-agent-platform",
        }
        self.assertEqual(expected, set(records))
        self.assertEqual(
            "primary-google-behavioral-portability", records["antigravity-cli"]["lane"]
        )
        self.assertEqual("observed", records["antigravity-cli"]["evidence_status"])
        self.assertEqual("manual", records["antigravity-cli"]["evidence_class"])
        self.assertEqual(
            "client-specific-install-and-control-checks", records["antigravity-cli"]["precondition"]
        )
        self.assertEqual(
            "conditional-enterprise-compatibility",
            records["gemini-cli-enterprise"]["lane"],
        )
        self.assertEqual("conditional", records["data-agent-kit"]["lifecycle_status"])
        self.assertEqual("blocked", records["data-agent-kit"]["evidence_status"])
        self.assertEqual(
            "separate-reviewed-tool-compatibility-test", records["data-agent-kit"]["precondition"]
        )
        self.assertIn("confirm it separately", records["data-agent-kit"]["claim"])
        self.assertEqual("forbidden", catalog["cross_lane_aggregation"])
        self.assertNotIn("success_rate", catalog)
        self.assertNotIn("aggregate", catalog)

    def test_v10_active_google_guidance_qualifies_gemini_cli(self) -> None:
        active_guidance = (
            ROOT / "README.md",
            ROOT / "docs" / "README.md",
            ROOT / "docs" / "quickstart.md",
            ROOT / "docs" / "architecture.md",
            ROOT / "docs" / "choose-your-skills.md",
            ROOT / "docs" / "client-surface-research.md",
            ROOT / "docs" / "agent-platform-boundaries.md",
            ROOT / "docs" / "google-adk.md",
            ROOT / "docs" / "google-agent-surfaces.md",
        )
        for path in active_guidance:
            text = path.read_text(encoding="utf-8")
            for paragraph in text.split("\n\n"):
                if "Gemini CLI" not in paragraph:
                    continue
                self.assertRegex(
                    paragraph,
                    r"(?i)Antigravity|enterprise|historical|transition|conditional",
                    path.relative_to(ROOT).as_posix(),
                )

    def test_v10_evidence_axes_do_not_collapse_workflow_and_runtime_state(self) -> None:
        schema = json.loads(
            (ROOT / "catalog" / "evidence-schema.json").read_text(encoding="utf-8")
        )
        catalog = json.loads(
            (ROOT / "catalog" / "evidence.json").read_text(encoding="utf-8")
        )
        self.assertEqual([], validate_instance(catalog, schema))
        records = {record["skill"]: record for record in catalog["skills"]}
        self.assertEqual(set(SKILLS), set(records))
        for record in records.values():
            self.assertEqual("candidate", record["workflow_maturity"])
            self.assertIn(
                record["behavioral_evidence"]["status"], {"none", "partial", "verified"}
            )
            self.assertEqual("not_applicable", record["runtime_eligibility"])
            self.assertNotIn("client_compatibility", record)

    def test_v10_repository_guidance_routes_subtree_rules(self) -> None:
        root_guidance = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("applicable subtree", root_guidance)
        for subtree in ("catalog", "evals", "scripts", "skills"):
            agents = ROOT / subtree / "AGENTS.md"
            claude = ROOT / subtree / "CLAUDE.md"
            self.assertTrue(agents.is_file(), subtree)
            self.assertEqual(
                "@AGENTS.md\n", claude.read_text(encoding="utf-8"), subtree
            )

    def test_v09_every_skill_has_complete_evaluation_contract(self) -> None:
        schema = json.loads(
            (ROOT / "evals" / "schema.json").read_text(encoding="utf-8")
        )
        catalog = json.loads(
            (ROOT / "evals" / "cases.json").read_text(encoding="utf-8")
        )
        self.assertEqual([], validate_instance(catalog, schema))
        self.assertEqual(set(SKILLS), {record["skill"] for record in catalog["skills"]})
        for record in catalog["skills"]:
            self.assertGreaterEqual(len(record["output_rubric"]), 3)
            self.assertIn(
                record["baseline_comparison"]["status"],
                {"pass", "fail", "blocked", "not_supported"},
            )

    def test_v09_observation_schema_has_distinct_api_and_google_surfaces(self) -> None:
        schema = json.loads(
            (ROOT / "docs" / "client-observations-schema.json").read_text(
                encoding="utf-8"
            )
        )
        surface_enum = schema["properties"]["records"]["items"]["properties"][
            "surface"
        ]["enum"]
        for surface in (
            "Gemini CLI",
            "Gemini CLI Enterprise",
            "Antigravity CLI",
            "Antigravity Desktop",
            "Antigravity SDK",
            "Gemini Managed Agent",
            "OpenAI Skills API",
            "Anthropic Skills API",
            "Anthropic Managed Agents",
        ):
            self.assertIn(surface, surface_enum)
        matrix = json.loads(
            (ROOT / "docs" / "client-observations-v0.9.json").read_text(
                encoding="utf-8"
            )
        )
        gemini_rows = [
            record for record in matrix["records"] if record["surface"] == "Gemini CLI"
        ]
        self.assertTrue(gemini_rows)
        self.assertEqual(
            {"historical"}, {record["evidence_scope"] for record in gemini_rows}
        )

    def test_v09_validation_evidence_matches_observed_matrix(self) -> None:
        matrix = json.loads(
            (ROOT / "docs" / "client-observations-v0.9.json").read_text(
                encoding="utf-8"
            )
        )
        evidence = (ROOT / "docs" / "validation-evidence.md").read_text(
            encoding="utf-8"
        )
        summary = matrix["summary"]
        expected = (
            f"Manual matrix: {summary['total']} exact-version rows; {summary['pass']} pass, "
            f"{summary['fail']} fail, {summary['blocked']} blocked, "
            f"{summary['not_supported']} not supported, and {summary['not_run']} not run"
        )
        self.assertIn(expected, evidence)
        self.assertNotIn("no v0.9 rows", evidence)
        self.assertIn(
            "`python3 -m unittest discover -s tests -v`: PASS - 56 regression tests",
            evidence,
        )

    def test_validation_evidence_records_suite_size_without_requiring_a_pass(self) -> None:
        evidence = (ROOT / "docs" / "validation-evidence.md").read_text(
            encoding="utf-8"
        )
        observed_test_count = unittest.defaultTestLoader.discover(
            str(ROOT / "tests")
        ).countTestCases()
        self.assertIn("## v0.10 behavioral-evidence candidate", evidence)
        self.assertIn(
            f"Current test suite: {observed_test_count} regression tests.",
            evidence,
        )

    def test_v09_changed_upstreams_have_human_readable_review_records(self) -> None:
        schema = json.loads(
            (ROOT / "catalog" / "upstream-reviews-schema.json").read_text(
                encoding="utf-8"
            )
        )
        catalog = json.loads(
            (ROOT / "catalog" / "upstream-reviews.json").read_text(encoding="utf-8")
        )
        self.assertEqual([], validate_instance(catalog, schema))
        expected = {
            "https://a2a-protocol.org/v1.0.0/specification/",
            "https://agentskills.io/specification",
            "https://developer.hashicorp.com/terraform/language",
            "https://docs.github.com/en/pull-requests/reference/pull-request-reviews.md",
            "https://docs.python.org/3/",
            "https://docs.python.org/3/library/unittest.html",
            "https://git-scm.com/docs/git-merge",
            "https://git-scm.com/docs/git-worktree",
            "https://learn.chatgpt.com/docs/agent-configuration/subagents",
            "https://genai.owasp.org/initiatives/agentic-security-initiative/",
            "https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/",
            "https://opentelemetry.io/docs/concepts/signals/",
            "https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/",
            "https://antigravity.google/docs/skills/",
            "https://www.antigravity.google/docs/cli/plugins/",
            "https://agent-plugins.org/specification",
            "https://antigravity.google/docs/cli/headless/",
            "https://ai.google.dev/gemini-api/docs/agents",
            "https://docs.cloud.google.com/data-agent-kit/overview",
            "https://ai.google.dev/gemini-api/docs/latest-model",
            "https://www.antigravity.google/docs/sdk/overview",
            "https://developers.googleblog.com/agents-cli-in-agent-platform-create-to-production-in-one-cli/",
            "https://docs.cloud.google.com/gemini-enterprise-agent-platform/overview",
        }
        expected.update({
            "https://airc.nist.gov/",
            "https://learn.microsoft.com/en-us/dotnet/",
            "https://trailhead.salesforce.com/content/learn/modules/apex_database/apex_database_intro",
            "https://www.drupal.org/docs/develop",
            "https://www.swift.org/documentation/",
            "https://www.typescriptlang.org/docs/",
            "https://docs.swift.org/latest/documentation/",
            "https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html",
            "https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html",
            "https://adk-labs.github.io/adk-docs/",
            "https://adk-labs.github.io/adk-docs/safety/",
            "https://adk-labs.github.io/adk-docs/sessions/",
            "https://docs.spring.io/spring-boot/",
            "https://owasp.org/www-project-application-security-verification-standard/",
            "https://slsa.dev/spec/v1.2/provenance",
            "https://www.postgresql.org/docs/current/",
            "https://www.antigravity.google/docs/plugins?tab=cli",
        })
        expected.update({
            "https://nextjs.org/docs/app/guides/ai-agents",
            "https://nextjs.org/docs/app/guides/authentication",
            "https://react.dev/learn/you-might-not-need-an-effect",
        })
        records = {record["url"]: record for record in catalog["reviews"]}
        self.assertEqual(expected, set(records))
        for record in records.values():
            self.assertEqual("reviewed", record["status"])
            self.assertGreaterEqual(len(record["affected_skills"]), 1)
            self.assertTrue(record["finding"])
            self.assertTrue(record["action"])

    def test_v09_subagent_mapping_preserves_surface_and_configuration_boundaries(
        self,
    ) -> None:
        mapping = (
            ROOT
            / "skills"
            / "multi-agent-orchestration"
            / "references"
            / "client-mapping.md"
        ).read_text(encoding="utf-8")
        for required in (
            "exact surface",
            "account capability",
            "reasoning level",
            "permission mode",
            "Do not treat one trigger path as proof for another",
            "Use the smallest useful fanout",
            "verify the actual configuration instead of assuming it",
        ):
            self.assertIn(required, mapping)

    def test_v09_open_spec_name_limits_are_enforced(self) -> None:
        self.assertEqual([], skill_name_errors("safe-skill"))
        self.assertTrue(skill_name_errors("bad--skill"))
        self.assertTrue(skill_name_errors("a" * 65))
        self.assertTrue(skill_name_errors("Bad-Skill"))

    def test_v09_release_manifest_tracks_governance_records(self) -> None:
        manifest = json.loads(
            (ROOT / "releases" / "0.9.0" / "manifest.json").read_text(encoding="utf-8")
        )
        paths = {artifact["path"] for artifact in manifest["artifacts"]}
        self.assertTrue(
            {
                "catalog/skills.json",
                "catalog/packs.json",
                "catalog/upstream-reviews.json",
                "evals/cases.json",
                "provenance/catalog.json",
            }.issubset(paths)
        )

    def test_v10_release_manifest_tracks_google_surface_record(self) -> None:
        manifest = json.loads(
            (ROOT / "releases" / "0.10.0" / "manifest.json").read_text(encoding="utf-8")
        )
        paths = {artifact["path"] for artifact in manifest["artifacts"]}
        self.assertIn("catalog/google-surfaces.json", paths)

    def test_v10_release_manifest_requires_reachable_ancestor_and_matching_bytes(
        self,
    ) -> None:
        def git(root: Path, *arguments: str) -> str:
            completed = subprocess.run(
                ["git", *arguments],
                cwd=root,
                check=True,
                text=True,
                capture_output=True,
            )
            return completed.stdout.strip()

        with tempfile.TemporaryDirectory(prefix="release-lineage-") as temporary:
            repository = Path(temporary)
            git(repository, "init", "--initial-branch=main")
            git(repository, "config", "user.name", "Release Test")
            git(repository, "config", "user.email", "release-test@example.invalid")
            artifact = repository / "artifact.txt"
            artifact.write_text("initial\n", encoding="utf-8")
            git(repository, "add", "artifact.txt")
            git(repository, "commit", "-m", "initial")
            initial = git(repository, "rev-parse", "HEAD")

            git(repository, "switch", "-c", "source")
            artifact.write_text("source\n", encoding="utf-8")
            git(repository, "commit", "-am", "source")
            source = git(repository, "rev-parse", "HEAD")
            expected = hashlib.sha256(b"source\n").hexdigest()
            document: dict[str, object] = {
                "source_commit": source,
                "artifacts": [
                    {"kind": "file", "path": "artifact.txt", "sha256": expected}
                ],
            }
            self.assertEqual([], release_manifest_source_errors(document, repository))
            self.assertEqual([], release_manifest_current_errors(document, repository))

            unavailable = copy.deepcopy(document)
            unavailable["source_commit"] = "0" * 40
            self.assertIn(
                "source commit is unavailable",
                "\n".join(release_manifest_source_errors(unavailable, repository)),
            )

            byte_mismatched: dict[str, object] = {
                "source_commit": source,
                "artifacts": [
                    {"kind": "file", "path": "artifact.txt", "sha256": "f" * 64}
                ],
            }
            self.assertIn(
                "source checksum drift",
                "\n".join(release_manifest_source_errors(byte_mismatched, repository)),
            )

            git(repository, "switch", "-c", "side", initial)
            artifact.write_text("side\n", encoding="utf-8")
            git(repository, "commit", "-am", "side")
            self.assertIn(
                "not an ancestor",
                "\n".join(release_manifest_source_errors(document, repository)),
            )

            git(repository, "switch", "source")
            artifact.write_text("changed\n", encoding="utf-8")
            self.assertIn(
                "current checksum drift",
                "\n".join(release_manifest_current_errors(document, repository)),
            )

    def test_native_invocation_controls_match_canonical_metadata(self) -> None:
        for skill in SKILLS:
            canonical = read_skill_metadata(ROOT / "skills" / skill)
            plugin = canonical["plugin"]
            claude = read_skill_metadata(
                ROOT / "plugins" / "claude" / plugin / "skills" / skill
            )
            self.assertEqual(
                "explicit" if skill in EXPLICIT_SKILLS else "implicit",
                canonical["invocation"],
            )
            self.assertEqual(
                "true" if skill in EXPLICIT_SKILLS else "false",
                claude["claude_explicit"],
            )

    def test_clean_generation_and_packaging_in_temporary_directory(self) -> None:
        with tempfile.TemporaryDirectory(prefix="skill-catalog-test-") as temporary:
            temporary_root = Path(temporary)
            _, claude_plugins, antigravity_plugins = build(
                temporary_root / "plugins", write_marketplaces=False
            )
            generated = {
                path.name
                for plugin in claude_plugins.values()
                for path in (plugin / "skills").iterdir()
            }
            self.assertEqual(set(SKILLS), generated)
            antigravity_generated = {
                path.name
                for plugin in antigravity_plugins.values()
                for path in (plugin / "skills").iterdir()
            }
            self.assertEqual(set(SKILLS) - EXPLICIT_SKILLS, antigravity_generated)
            archives = package(temporary_root / "archives")
            self.assertEqual(len(SKILLS), len(archives))

    def test_generation_check_is_non_mutating_and_includes_marketplaces(self) -> None:
        before = subprocess.run(
            ["git", "status", "--short"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        self.assertEqual([], check_generated())
        after = subprocess.run(
            ["git", "status", "--short"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        self.assertEqual(before, after)
        codex, _, antigravity = marketplace_documents()
        self.assertEqual(
            set(skills_by_plugin()), {entry["name"] for entry in codex["plugins"]}
        )
        self.assertEqual(
            set(skills_by_plugin()), {entry["name"] for entry in antigravity["plugins"]}
        )
        for entry in codex["plugins"]:
            self.assertEqual(
                {"source": "local", "path": f"./plugins/codex/{entry['name']}"},
                entry["source"],
            )
            self.assertEqual(
                {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                entry["policy"],
            )
        for ag_entry in antigravity["plugins"]:
            self.assertEqual(
                {"source": "local", "path": f"./plugins/antigravity/{ag_entry['name']}"},
                ag_entry["source"],
            )

    def test_schema_validation_enforces_types_enums_dates_and_unknown_fields(
        self,
    ) -> None:
        schema = json.loads(
            (ROOT / "provenance" / "schema.json").read_text(encoding="utf-8")
        )
        catalog = json.loads(
            (ROOT / "provenance" / "catalog.json").read_text(encoding="utf-8")
        )
        broken = json.loads(json.dumps(catalog))
        broken["reviewed_on"] = "not-a-date"
        broken["entries"][0]["disposition"] = "adapt"
        broken["entries"][0]["reviewed_material"] = "SKILL.md"
        broken["entries"][0]["unexpected"] = True
        errors = validate_instance(broken, schema)
        self.assertTrue(any("valid date" in error for error in errors))
        self.assertTrue(any("must be one of" in error for error in errors))
        self.assertTrue(any("expected array" in error for error in errors))
        self.assertTrue(any("additional property" in error for error in errors))

    def test_original_work_roadmap_has_no_external_inventory_track(self) -> None:
        roadmap = json.loads(
            (ROOT / "incubator" / "roadmap.json").read_text(encoding="utf-8")
        )
        tracks = {track["id"]: track for track in roadmap["tracks"]}
        self.assertNotIn("additional-stack-profiles", tracks)
        self.assertEqual("released", tracks["acceptance-evidence-ledger"]["status"])
        self.assertEqual("v0.7", tracks["acceptance-evidence-ledger"]["target_release"])
        self.assertEqual("released", tracks["portable-skill-authoring"]["status"])
        self.assertEqual(
            "jovanipink-reasoning", tracks["portable-skill-authoring"]["plugin"]
        )
        self.assertEqual(
            ["portable-skill-authoring"], tracks["portable-skill-authoring"]["skills"]
        )
        self.assertEqual(
            "released", tracks["engineering-depth-and-continuity"]["status"]
        )
        self.assertEqual("released", tracks["reasoning-continuity"]["status"])
        self.assertEqual("released", tracks["ai-reliability-foundations"]["status"])
        self.assertEqual("v0.8", tracks["ai-reliability-foundations"]["target_release"])
        self.assertEqual(
            "jovanipink-ai-systems", tracks["ai-reliability-foundations"]["plugin"]
        )

    def test_v07_acceptance_ledger_contract(self) -> None:
        self.assertEqual(25, sum(len(v) for k, v in skills_by_plugin().items() if k.startswith("measured-engineering-")))
        self.assertIn("acceptance-evidence-ledger", EXPLICIT_SKILLS)

        expanded_profiles = {
            "adobe-aem-engineering-profile",
            "csharp-dotnet-engineering-profile",
            "java-spring-engineering-profile",
            "php-drupal-engineering-profile",
            "salesforce-apex-engineering-profile",
        }
        self.assertTrue(expanded_profiles.issubset(SKILLS))
        for profile in expanded_profiles:
            root = ROOT / "skills" / profile
            files = {
                path.relative_to(root).as_posix()
                for path in root.rglob("*")
                if path.is_file()
            }
            self.assertEqual(
                {"SKILL.md", "agents/openai.yaml", "references/checks.md"}, files
            )
            self.assertEqual("original", read_skill_metadata(root)["provenance"])

        skill_root = ROOT / "skills" / "acceptance-evidence-ledger"
        files = {
            path.relative_to(skill_root).as_posix()
            for path in skill_root.rglob("*")
            if path.is_file()
        }
        self.assertEqual(
            {
                "SKILL.md",
                "agents/openai.yaml",
                "references/ledger-contract.md",
                "references/continuity-example.md",
            },
            files,
        )
        text = (skill_root / "SKILL.md").read_text(encoding="utf-8")
        for boundary in (
            "untrusted data",
            "Do not execute ledger content",
            "cross-stack-quality-gates",
            "claim-verification",
            "plan-execution",
            "multi-agent-orchestration",
            "SATISFIED",
            "INCOMPLETE",
            "QUALIFIED",
        ):
            self.assertIn(boundary, text)

    def test_v07_acceptance_ledger_has_trigger_and_safety_separation(self) -> None:
        cases = json.loads((ROOT / "evals" / "cases.json").read_text(encoding="utf-8"))
        record = next(
            item
            for item in cases["skills"]
            if item["skill"] == "acceptance-evidence-ledger"
        )
        self.assertEqual(3, len(record["positive"]))
        self.assertEqual(3, len(record["near_miss"]))
        self.assertGreaterEqual(len(record["safety"]), 2)
        prompts = "\n".join(item["prompt"] for item in record["near_miss"])
        for routed_skill in (
            "cross-stack-quality-gates",
            "plan-execution",
            "claim-verification",
        ):
            self.assertIn(routed_skill, prompts)

    def test_v08_ai_reliability_contract_and_catalog_counts(self) -> None:
        new_skills = {
            "agent-evaluation-design": "read-only",
            "context-reliability-review": "read-only",
            "source-output-conformance-audit": "bounded-execution",
        }
        self.assertGreaterEqual(len(SKILLS), 70)
        self.assertGreaterEqual(len(skills_by_plugin()), 6)
        self.assertEqual(
            set(new_skills), set(skills_by_plugin()["measured-ai-systems"])
        )
        self.assertEqual(17, len(EXPLICIT_SKILLS))

        references = {
            "agent-evaluation-design": "evaluation-contract.md",
            "context-reliability-review": "assertion-matrix.md",
            "source-output-conformance-audit": "conformance-matrix.md",
        }
        for skill, risk_class in new_skills.items():
            root = ROOT / "skills" / skill
            files = {
                path.relative_to(root).as_posix()
                for path in root.rglob("*")
                if path.is_file()
            }
            self.assertEqual(
                (
                    {
                        "SKILL.md",
                        "agents/openai.yaml",
                        f"references/{references[skill]}",
                    }
                    | (
                        {"references/continuity-example.md"}
                        if skill == "agent-evaluation-design"
                        else set()
                    )
                ),
                files,
            )
            metadata = read_skill_metadata(root)
            self.assertEqual("measured-ai-systems", metadata["plugin"])
            self.assertEqual("implicit", metadata["invocation"])
            self.assertEqual("original", metadata["provenance"])
            self.assertEqual(risk_class, metadata["risk_class"])

    def test_v09_agent_platform_contract_and_catalog_counts(self) -> None:
        new_skills = {
            "agent-context-state-memory-design": "state-memory-lifecycle.md",
            "agent-protocol-interoperability-review": "protocol-boundaries.md",
            "agent-tool-action-boundary-review": "tool-action-matrix.md",
            "agentic-system-security-review": "agentic-threat-domains.md",
            "google-adk-engineering-profile": "adk-version-boundaries.md",
            "retrieval-grounding-quality-review": "retrieval-evidence-matrix.md",
        }
        self.assertEqual(86, len(SKILLS))
        self.assertEqual(11, len(skills_by_plugin()))
        self.assertEqual(
            set(new_skills), set(skills_by_plugin()["measured-agent-platforms"])
        )
        self.assertEqual(17, len(EXPLICIT_SKILLS))

        for skill, reference in new_skills.items():
            root = ROOT / "skills" / skill
            files = {
                path.relative_to(root).as_posix()
                for path in root.rglob("*")
                if path.is_file()
            }
            self.assertEqual(
                {"SKILL.md", "agents/openai.yaml", f"references/{reference}"},
                files,
            )
            metadata = read_skill_metadata(root)
            self.assertEqual("measured-agent-platforms", metadata["plugin"])
            self.assertEqual("implicit", metadata["invocation"])
            self.assertEqual("clean-room", metadata["provenance"])
            self.assertEqual("read-only", metadata["risk_class"])

        security = (
            ROOT / "skills" / "agentic-system-security-review" / "SKILL.md"
        ).read_text(encoding="utf-8")
        for boundary in (
            "application-security-review",
            "skill-security-review",
            "cannot grant a tool",
            "direct and indirect prompt injection",
            "cross-user and cross-tenant",
        ):
            self.assertIn(boundary, security)

        adk = (
            ROOT / "skills" / "google-adk-engineering-profile" / "SKILL.md"
        ).read_text(encoding="utf-8")
        for boundary in (
            "experimental",
            "SkillToolset",
            "runtime bundle",
            "does not authorize deployment",
        ):
            self.assertIn(boundary, adk)

        protocol = (
            ROOT / "skills" / "agent-protocol-interoperability-review" / "SKILL.md"
        ).read_text(encoding="utf-8")
        for boundary in (
            "normative schemas",
            "signature verification",
            "functional equivalence",
            "authorization-required state is a request for authorization",
        ):
            self.assertIn(boundary, protocol)

        retrieval = (
            ROOT / "skills" / "retrieval-grounding-quality-review" / "SKILL.md"
        ).read_text(encoding="utf-8")
        for boundary in (
            "embeddings as sensitive derived data",
            "inversion or reconstruction",
            "tone, and task usefulness",
        ):
            self.assertIn(boundary, retrieval)

    def test_v08_ai_reliability_routing_and_safety_separation(self) -> None:
        cases = json.loads((ROOT / "evals" / "cases.json").read_text(encoding="utf-8"))
        records = {
            item["skill"]: item
            for item in cases["skills"]
            if item["skill"]
            in {
                "agent-evaluation-design",
                "context-reliability-review",
                "source-output-conformance-audit",
            }
        }
        self.assertEqual(3, len(records))
        for record in records.values():
            self.assertGreaterEqual(len(record["positive"]), 3)
            self.assertGreaterEqual(len(record["near_miss"]), 3)
            self.assertGreaterEqual(len(record["safety"]), 1)
            self.assertGreaterEqual(len(record["output_rubric"]), 3)
            self.assertNotEqual("not_run", record["baseline_comparison"]["status"])

        near_misses = "\n".join(
            case["prompt"]
            for record in records.values()
            for case in record["near_miss"]
        )
        for collision in (
            "test-strategy",
            "test-quality-review",
            "acceptance-evidence-ledger",
            "authority-boundary-review",
            "ConvergeQL-style model review",
        ):
            self.assertIn(collision, near_misses)

        evaluation = (
            ROOT / "skills" / "agent-evaluation-design" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("evaluation contract", evaluation)
        self.assertIn("paid or external evaluation", evaluation)
        context = (
            ROOT / "skills" / "context-reliability-review" / "SKILL.md"
        ).read_text(encoding="utf-8")
        for boundary in (
            "effective time",
            "recorded time",
            "supersession",
            "revocation",
        ):
            self.assertIn(boundary, context)
        conformance = (
            ROOT / "skills" / "source-output-conformance-audit" / "SKILL.md"
        ).read_text(encoding="utf-8")
        for dimension in (
            "correctness",
            "completeness",
            "storage correctness",
            "reproducibility",
            "unresolved evidence",
        ):
            self.assertIn(dimension, conformance)

    def test_client_observation_matrix_is_reconciled_and_terminal(self) -> None:
        paths = sorted(
            path
            for path in (ROOT / "docs").glob("client-observations*.json")
            if path.name != "client-observations-schema.json"
        )
        self.assertGreaterEqual(len(paths), 2)
        for path in paths:
            matrix = json.loads(path.read_text(encoding="utf-8"))
            records = matrix["records"]
            self.assertEqual(matrix["summary"]["total"], len(records))
            self.assertEqual(
                len(records), len({record["case_id"] for record in records})
            )
            self.assertNotIn("not_run", {record["result"] for record in records})
            self.assertEqual(
                set(matrix["surfaces_covered"]),
                {record["surface"] for record in records},
            )

    def test_v04_records_chatgpt_web_as_a_distinct_surface(self) -> None:
        matrix = json.loads(
            (ROOT / "docs" / "client-observations-v0.4.json").read_text(
                encoding="utf-8"
            )
        )
        web_records = [
            record for record in matrix["records"] if record["surface"] == "ChatGPT Web"
        ]
        self.assertEqual(6, len(web_records))
        self.assertEqual({"blocked"}, {record["result"] for record in web_records})
        self.assertTrue(
            any("no skills" in record["invocation_behavior"] for record in web_records)
        )

    def test_v08_records_each_client_lifecycle_observation_separately(self) -> None:
        matrix = json.loads(
            (ROOT / "docs" / "client-observations-v0.8.json").read_text(
                encoding="utf-8"
            )
        )
        expected_phases = {
            "INSTALL",
            "DISCOVERY",
            "IMPLICIT",
            "REFERENCE",
            "REFUSAL",
            "UPDATE",
            "REMOVAL",
        }
        by_surface: dict[str, set[str]] = {}
        for record in matrix["records"]:
            by_surface.setdefault(record["surface"], set()).add(
                record["case_id"].rsplit("-", 1)[-1]
            )
        self.assertEqual(6, len(by_surface))
        self.assertEqual(
            {surface: expected_phases for surface in by_surface}, by_surface
        )
        self.assertEqual(
            {"blocked"}, {record["result"] for record in matrix["records"]}
        )

    def test_boundary_scan_covers_publishable_root_and_local_denylist(self) -> None:
        publishable = {
            path.relative_to(ROOT).as_posix() for path in _publishable_paths(ROOT)
        }
        for expected in (
            "README.md",
            ".github/workflows/validate.yml",
            "scripts/check_public_boundary.py",
        ):
            self.assertIn(expected, publishable)
        with tempfile.TemporaryDirectory(prefix="boundary-regression-") as temporary:
            temporary_root = Path(temporary)
            candidate = temporary_root / "candidate.md"
            denylist = temporary_root / "denylist.txt"
            candidate.write_text("synthetic confidential canary\n", encoding="utf-8")
            denylist.write_text("confidential canary\n", encoding="utf-8")
            errors = scan_public_boundary(
                [candidate], denylist_path=denylist, include_packages=False
            )
            self.assertEqual(1, len(errors))
            self.assertIn("local denylist", errors[0])

    def test_boundary_scan_rejects_non_ascii_and_non_us_english(self) -> None:
        with tempfile.TemporaryDirectory(prefix="language-boundary-") as temporary:
            candidate = Path(temporary) / "candidate.md"
            non_us_spelling = "organi" + "sation"
            candidate.write_text(
                f"plain{chr(0x2014)}text with {non_us_spelling}{chr(7)}\n",
                encoding="utf-8",
            )
            errors = scan_public_boundary([candidate], include_packages=False)
            self.assertTrue(any("non-ASCII character" in error for error in errors))
            self.assertTrue(any("non-US English spelling" in error for error in errors))
            self.assertTrue(any("ASCII control character" in error for error in errors))

    def test_boundary_scan_preserves_exact_external_tokens(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="language-token-boundary-"
        ) as temporary:
            candidate = Path(temporary) / "candidate.md"
            candidate.write_text(
                "External references:\n"
                "- https://example.com/catalogue/reference\n"
                "- [Acme Colour API](https://example.com/api)\n"
                "- `assets/catalogue/reference.json`\n",
                encoding="utf-8",
            )
            self.assertEqual(
                [], scan_public_boundary([candidate], include_packages=False)
            )

    def test_boundary_scan_still_rejects_reader_authored_spelling(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="language-prose-boundary-"
        ) as temporary:
            candidate = Path(temporary) / "candidate.md"
            candidate.write_text(
                "The cata" + "logue describes the API.\n", encoding="utf-8"
            )
            errors = scan_public_boundary([candidate], include_packages=False)
            self.assertEqual(1, len(errors))
            self.assertIn("non-US English spelling", errors[0])

    def test_compound_skill_titles_follow_editorial_style(self) -> None:
        expected = {
            "cross-capability-dependency-mapping": "Cross-Capability Dependency Mapping",
            "cross-stack-quality-gates": "Cross-Stack Quality Gates",
            "dependency-supply-chain-review": "Dependency and Supply-Chain Review",
            "high-signal-technical-writing": "High-Signal Technical Writing",
            "multi-agent-orchestration": "Multi-Agent Orchestration",
            "public-private-boundary-review": "Public-Private Boundary Review",
            "source-grounded-research": "Source-Grounded Research",
            "test-driven-change": "Test-Driven Change",
        }
        for skill, title in expected.items():
            body = (ROOT / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
            interface = (ROOT / "skills" / skill / "agents" / "openai.yaml").read_text(
                encoding="utf-8"
            )
            self.assertIn(f"# {title}\n", body)
            self.assertIn(f'display_name: "{title}"', interface)

    def test_claude_archives_are_reproducible(self) -> None:
        with tempfile.TemporaryDirectory(prefix="package-determinism-") as temporary:
            temporary_root = Path(temporary)
            first = package(temporary_root / "first")
            second = package(temporary_root / "second")
            first_hashes = [
                hashlib.sha256(path.read_bytes()).hexdigest() for path in first
            ]
            second_hashes = [
                hashlib.sha256(path.read_bytes()).hexdigest() for path in second
            ]
            self.assertEqual(first_hashes, second_hashes)

    def test_stack_reference_covers_declared_languages(self) -> None:
        text = (
            ROOT
            / "skills"
            / "cross-stack-quality-gates"
            / "references"
            / "gate-discovery.md"
        ).read_text(encoding="utf-8")
        for stack in (
            "Go",
            "Python",
            "Swift",
            "TypeScript",
            "JavaScript",
            "SQL",
            "Terraform",
        ):
            self.assertIn(stack, text)

    def test_cross_stack_fixtures_do_not_assume_a_universal_gate(self) -> None:
        self.assertEqual([], evaluate_gate_fixtures())

    def test_archives_have_valid_layout(self) -> None:
        errors: list[str] = []
        validate_packages(errors)
        self.assertEqual([], errors)

    def test_workflow_actions_require_immutable_revisions(self) -> None:
        mutable = "steps:\n  - uses: actions/checkout@v7\n"
        local = "steps:\n  - uses: ./local-action\n"
        self.assertEqual(
            [
                "fixture.yml: action reference must use a 40-character commit SHA: actions/checkout@v7"
            ],
            immutable_action_reference_errors(mutable, "fixture.yml"),
        )
        self.assertEqual([], immutable_action_reference_errors(local, "fixture.yml"))

    def test_workflow_syntax_gate_catches_unquoted_only_binary_regression(self) -> None:
        workflow = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")
        quoted = (
            'run: "python3 -m pip install --require-hashes --only-binary=:all: '
            '-r requirements-ci-linux.txt"'
        )
        unquoted = "run: " + quoted.removeprefix('run: "').removesuffix('"')
        self.assertIn(quoted, workflow)
        self.assertEqual([], workflow_syntax_errors(workflow, "fixture.yml"))

        mutated = workflow.replace(quoted, unquoted)
        expected_line = mutated.count("\n", 0, mutated.index(unquoted)) + 1
        errors = workflow_syntax_errors(mutated, "fixture.yml")
        self.assertEqual(1, len(errors))
        self.assertIn(f"fixture.yml:{expected_line}:", errors[0])
        self.assertIn("mapping values are not allowed here", errors[0])

    def test_workflow_syntax_gate_rejects_invalid_document_roots(self) -> None:
        self.assertEqual(
            ["empty.yml: workflow must not be empty"],
            workflow_syntax_errors("", "empty.yml"),
        )
        self.assertEqual(
            ["sequence.yml: workflow root must be a mapping"],
            workflow_syntax_errors("- item\n", "sequence.yml"),
        )

    def test_workflow_syntax_gate_fails_closed_on_parser_version(self) -> None:
        with patch("check_workflows.version", side_effect=PackageNotFoundError):
            self.assertEqual(
                [
                    f"PyYAML {PYYAML_VERSION} is required; install requirements-ci-linux.txt on Linux"
                ],
                check_workflows(),
            )
        with patch("check_workflows.version", return_value="0.0.0"):
            self.assertEqual(
                [f"PyYAML {PYYAML_VERSION} is required; found 0.0.0"],
                check_workflows(),
            )

    def test_repository_workflows_pass_syntax_gate(self) -> None:
        self.assertEqual([], check_workflows())

    def test_ci_python_tools_are_typed_linted_and_hash_locked(self) -> None:
        errors: list[str] = []
        validate_ci_tools(errors)
        self.assertEqual([], errors)
        requirements = (ROOT / "requirements-ci-linux.txt").read_text(encoding="utf-8")
        workflow = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")
        self.assertIn("--only-binary=:all:", requirements)
        self.assertIn("PyYAML==6.0.3", requirements)
        self.assertIn("types-PyYAML==6.0.12.20260815", requirements)
        self.assertEqual(8, requirements.count("--hash=sha256:"))
        self.assertIn(
            'run: "python3 -m pip install --require-hashes --only-binary=:all: '
            '-r requirements-ci-linux.txt"',
            workflow,
        )
        self.assertIn("run: python3 scripts/check_workflows.py", workflow)

    def test_subagent_client_mapping_tracks_current_security_boundaries(self) -> None:
        mapping = (
            ROOT
            / "skills"
            / "multi-agent-orchestration"
            / "references"
            / "client-mapping.md"
        ).read_text(encoding="utf-8")
        for required_text in (
            "custom-agent configuration",
            "registered tools",
            "active trust boundary",
            "not permission to broaden",
        ):
            self.assertIn(required_text, mapping)

    def test_revocation_filter_withdraws_catalog_advertisement(self) -> None:
        self.assertEqual(
            ("kept-skill",),
            filter_revoked(
                ("kept-skill", "revoked-skill"), frozenset({"revoked-skill"})
            ),
        )

    def test_private_overlay_example_is_drift_free(self) -> None:
        self.assertEqual(
            [],
            sync_private_overlay(
                ROOT / "examples" / "private-overlay", check_only=True
            ),
        )

    def test_private_overlay_sync_allows_repository_agents_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary).resolve() / "repo"
            shutil.copytree(ROOT / "examples" / "private-overlay", repo)
            (repo / "AGENTS.md").write_text("# Repository guidance\n", encoding="utf-8")
            self.assertEqual([], sync_private_overlay(repo, check_only=False))
            self.assertEqual([], sync_private_overlay(repo, check_only=True))

    def test_private_overlay_refuses_existing_projection_without_source(self) -> None:
        for projection in (".claude/skills", ".agents/skills"):
            for check_only in (False, True):
                with self.subTest(projection=projection, check_only=check_only):
                    with tempfile.TemporaryDirectory() as temporary:
                        repo = Path(temporary).resolve()
                        (repo / projection / "local-skill").mkdir(parents=True)
                        errors = sync_private_overlay(repo, check_only=check_only)
                        self.assertEqual(1, len(errors))
                        self.assertIn("existing repo-local skill convention", errors[0])
                        self.assertTrue((repo / projection / "local-skill").is_dir())

    def test_private_overlay_refuses_symlinked_projection_paths(self) -> None:
        # A symlinked .agents/.claude parent (or skills folder) must never let sync
        # remove or replace a directory outside the repository.
        for link in (".agents", ".claude", ".agents/skills", ".claude/skills"):
            for check_only in (False, True):
                with self.subTest(link=link, check_only=check_only):
                    with tempfile.TemporaryDirectory() as temporary:
                        root = Path(temporary).resolve()
                        repo = root / "repo"
                        shutil.copytree(ROOT / "examples" / "private-overlay", repo)
                        outside = root / "outside"
                        target = outside / "skills" if link.endswith("skills") else outside
                        (outside / "skills").mkdir(parents=True)
                        (outside / "skills" / "SENTINEL").write_text("keep", encoding="utf-8")
                        linked = repo / link
                        if linked.exists() or linked.is_symlink():
                            shutil.rmtree(linked)
                        linked.parent.mkdir(parents=True, exist_ok=True)
                        linked.symlink_to(target, target_is_directory=True)
                        with self.assertRaises(ValueError):
                            sync_private_overlay(repo, check_only=check_only)
                        self.assertTrue((outside / "skills" / "SENTINEL").is_file())

    def test_private_overlay_replacement_does_not_follow_swapped_symlinks(self) -> None:
        # The destructive step must enforce no-follow itself, not rely on an earlier
        # pathname check that a concurrent process could invalidate.
        for link in (".agents", ".agents/skills"):
            with self.subTest(link=link):
                with tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary).resolve()
                    repo = root / "repo"
                    repo.mkdir()
                    expected = root / "expected"
                    (expected / "demo").mkdir(parents=True)
                    (expected / "demo" / "SKILL.md").write_text("x", encoding="utf-8")
                    outside = root / "outside"
                    (outside / "skills").mkdir(parents=True)
                    (outside / "skills" / "SENTINEL").write_text("keep", encoding="utf-8")
                    linked = repo / link
                    linked.parent.mkdir(parents=True, exist_ok=True)
                    linked.symlink_to(outside if link == ".agents" else outside / "skills", target_is_directory=True)
                    repo_fd = os.open(repo, os.O_RDONLY)
                    try:
                        with self.assertRaises((OSError, ValueError)):
                            _replace_projection(repo_fd, ".agents/skills", expected)
                    finally:
                        os.close(repo_fd)
                    self.assertTrue((outside / "skills" / "SENTINEL").is_file())

    def test_private_overlay_replacement_replaces_real_projection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            repo = root / "repo"
            (repo / ".agents" / "skills" / "stale").mkdir(parents=True)
            expected = root / "expected"
            (expected / "demo" / "references").mkdir(parents=True)
            (expected / "demo" / "SKILL.md").write_text("new", encoding="utf-8")
            (expected / "demo" / "references" / "note.md").write_text("ref", encoding="utf-8")
            repo_fd = os.open(repo, os.O_RDONLY)
            try:
                _replace_projection(repo_fd, ".agents/skills", expected)
            finally:
                os.close(repo_fd)
            actual = repo / ".agents" / "skills"
            self.assertFalse((actual / "stale").exists())
            self.assertEqual("new", (actual / "demo" / "SKILL.md").read_text(encoding="utf-8"))
            self.assertEqual("ref", (actual / "demo" / "references" / "note.md").read_text(encoding="utf-8"))
            self.assertEqual([".agents/skills"], [p.relative_to(repo).as_posix() for p in repo.glob(".agents/*")])

    def test_private_overlay_replacement_stays_on_the_opened_repository(self) -> None:
        # Once the repository handle is open, renaming the repository and putting a
        # symlink in its place must not redirect the replacement outside it.
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            repo = root / "repo"
            (repo / ".agents").mkdir(parents=True)
            expected = root / "expected"
            (expected / "demo").mkdir(parents=True)
            (expected / "demo" / "SKILL.md").write_text("x", encoding="utf-8")
            outside = root / "outside"
            (outside / ".agents" / "skills").mkdir(parents=True)
            (outside / ".agents" / "skills" / "SENTINEL").write_text("keep", encoding="utf-8")
            repo_fd = os.open(repo, os.O_RDONLY)
            try:
                repo.rename(root / "moved")
                repo.symlink_to(outside, target_is_directory=True)
                _replace_projection(repo_fd, ".agents/skills", expected)
            finally:
                os.close(repo_fd)
            self.assertTrue((outside / ".agents" / "skills" / "SENTINEL").is_file())
            self.assertTrue((root / "moved" / ".agents" / "skills" / "demo" / "SKILL.md").is_file())

    def test_private_overlay_validates_every_target_before_replacing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            repo = root / "repo"
            shutil.copytree(ROOT / "examples" / "private-overlay", repo)
            self.assertEqual([], sync_private_overlay(repo, check_only=False))
            (repo / ".agents" / "skills" / "MARKER").write_text("before", encoding="utf-8")
            shutil.rmtree(repo / ".claude")
            (root / "outside").mkdir()
            (repo / ".claude").symlink_to(root / "outside", target_is_directory=True)
            with self.assertRaises(ValueError):
                sync_private_overlay(repo, check_only=False)
            self.assertTrue((repo / ".agents" / "skills" / "MARKER").is_file())

    def test_private_overlay_check_runs_without_no_follow_support(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary).resolve() / "repo"
            shutil.copytree(ROOT / "examples" / "private-overlay", repo)
            with unittest.mock.patch.object(overlay_module, "_directory_flags", return_value=None):
                self.assertEqual([], sync_private_overlay(repo, check_only=True))
                with self.assertRaises(ValueError):
                    sync_private_overlay(repo, check_only=False)

    def test_private_overlay_repository_handle_refuses_symlinked_ancestors(self) -> None:
        # O_NOFOLLOW on the last component alone is not enough: a symlinked ancestor
        # must also be refused when the repository handle is acquired.
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            (root / "real" / "repo").mkdir(parents=True)
            (root / "link").symlink_to(root / "real", target_is_directory=True)
            with self.assertRaises(OSError):
                fd = overlay_module._open_directory_path(root / "link" / "repo")
                os.close(fd)
            fd = overlay_module._open_directory_path(root / "real" / "repo")
            try:
                self.assertEqual(os.fstat(fd).st_ino, (root / "real" / "repo").stat().st_ino)
            finally:
                os.close(fd)

    def test_private_overlay_sync_refuses_symlinked_repository_path(self) -> None:
        # The public entry point must refuse a --repo path with a symlinked ancestor
        # instead of resolving it and writing into the link target.
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            shutil.copytree(ROOT / "examples" / "private-overlay", root / "real" / "repo")
            (root / "link").symlink_to(root / "real", target_is_directory=True)
            before = sorted(p.relative_to(root / "real").as_posix() for p in (root / "real").rglob("*"))
            with self.assertRaises(ValueError):
                sync_private_overlay(root / "link" / "repo", check_only=False)
            after = sorted(p.relative_to(root / "real").as_posix() for p in (root / "real").rglob("*"))
            self.assertEqual(before, after)

    def test_private_overlay_source_snapshot_reads_the_bound_repository(self) -> None:
        # After the handle is bound, swapping a different repository into the path must
        # not change what is read.
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            repo = root / "repo"
            (repo / ".agent-skills" / "skills" / "original").mkdir(parents=True)
            (repo / ".agent-skills" / "skills" / "original" / "SKILL.md").write_text("one", encoding="utf-8")
            impostor = root / "impostor"
            (impostor / ".agent-skills" / "skills" / "replacement").mkdir(parents=True)
            repo_fd = overlay_module._open_directory_path(repo)
            try:
                repo.rename(root / "moved")
                impostor.rename(repo)
                snapshot = overlay_module._snapshot_source(repo_fd, root / "snapshot")
            finally:
                os.close(repo_fd)
            self.assertEqual(["original"], sorted(p.name for p in snapshot.iterdir()))
            self.assertEqual("one", (snapshot / "original" / "SKILL.md").read_text(encoding="utf-8"))

    def test_upstream_review_freshness_is_current_offline(self) -> None:
        # Judge the committed pins on the day they were reviewed. The overdue
        # boundary is covered in test_tooling_hardening.py, and validate.py
        # applies the real date.
        from datetime import date

        pins = json.loads(
            (ROOT / "catalog" / "upstream-pins.json").read_text(encoding="utf-8")
        )
        errors, report = check_upstream_freshness(
            online=False, today=date.fromisoformat(pins["reviewed_on"])
        )
        self.assertEqual([], errors)
        self.assertEqual("pass", report["result"])

    def test_reviewed_google_sources_are_freshness_pinned(self) -> None:
        reviews = json.loads(
            (ROOT / "catalog" / "upstream-reviews.json").read_text(encoding="utf-8")
        )
        pins = json.loads(
            (ROOT / "catalog" / "upstream-pins.json").read_text(encoding="utf-8")
        )
        google_reviews = {
            record["url"]
            for record in reviews["reviews"]
            if any(host in record["url"] for host in ("google", "agent-plugins.org"))
        }
        pinned = {record["source_url"] for record in pins["sources"]}
        self.assertTrue(google_reviews)
        self.assertTrue(google_reviews.issubset(pinned))

    def test_freshness_comparison_preserves_the_pinned_marker_kind(self) -> None:
        from check_upstream_freshness import _fetch_marker

        class Response:
            headers: ClassVar[dict[str, str]] = {
                "ETag": '"transient"',
                "Last-Modified": "Sun, 23 Aug 2026 18:16:51 GMT",
            }

            def __enter__(self) -> Response:
                return self

            def __exit__(
                self,
                exc_type: type[BaseException] | None,
                exc_value: BaseException | None,
                traceback: TracebackType | None,
            ) -> Literal[False]:
                return False

            def read(self) -> bytes:
                return b"stable authority content"

        with patch(
            "check_upstream_freshness.urllib.request.urlopen", return_value=Response()
        ):
            kind, value = _fetch_marker(
                "https://example.com/specification", preferred_kind="content-sha256"
            )
        self.assertEqual("content-sha256", kind)
        self.assertEqual(hashlib.sha256(b"stable authority content").hexdigest(), value)

    def test_freshness_normalization_ignores_only_per_request_html_values(self) -> None:
        first = b"""<meta name="csrf-token" content="first" />
<script>NREUM.info={"queueTime":1,"applicationTime":131}</script>
<meta content='visitor-one' name='ua:temp_visitor_id'>
<input type="hidden" name="form_build_id" value="form-first" />
<div class="view-dom-id-0123456789abcdef0123456789abcdef"></div>
<script>{"theme_token":"theme-first"}</script>
<script nonce="nonce-first">stable()</script>
<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js/one" data-cf-beacon='{"token":"one"}'></script>
<script nonce="nonce-first">(function(){var a='/cdn-cgi/challenge-platform/one';})();</script>
<main>Official authority content</main>"""
        second = b"""<meta name="csrf-token" content="second" />
<script>NREUM.info={"queueTime":9,"applicationTime":157}</script>
<meta content='visitor-two' name='ua:temp_visitor_id'>
<input type="hidden" name="form_build_id" value="form-second" />
<div class="view-dom-id-fedcba9876543210fedcba9876543210"></div>
<script>{"theme_token":"theme-second"}</script>
<script nonce="nonce-second">stable()</script>
<script nonce="nonce-second">(function(){var a='/cdn-cgi/challenge-platform/two';})();</script>
<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js/two" data-cf-beacon='{"token":"two"}'></script>
<main>Official authority content</main>"""
        changed = second.replace(
            b"Official authority content", b"Changed authority content"
        )
        self.assertEqual(
            _normalized_content_sha256(first), _normalized_content_sha256(second)
        )
        self.assertEqual(
            _normalized_content_sha256(first, strip_trailing=True),
            _normalized_content_sha256(first + b"\r\n", strip_trailing=True),
        )
        self.assertNotEqual(
            _normalized_content_sha256(first), _normalized_content_sha256(changed)
        )

    def test_freshness_normalization_ignores_only_batcache_timing_comments(self) -> None:
        body = b"<main>Official authority content</main>\n"
        cached = body + (
            b"<!--\n\tgenerated 158 seconds ago\n\tgenerated in 3.968 seconds\n"
            b"\tserved from batcache in 0.004 seconds\n\texpires in 142 seconds\n-->"
        )
        fresh = body + (
            b"<!--\n\tgenerated in 3.598 seconds\n\t81234 bytes batcached for 300 seconds\n-->"
        )
        self.assertEqual(_normalized_content_sha256(body), _normalized_content_sha256(cached))
        self.assertEqual(_normalized_content_sha256(body), _normalized_content_sha256(fresh))
        self.assertNotEqual(
            _normalized_content_sha256(cached),
            _normalized_content_sha256(cached.replace(b"Official", b"Changed")),
        )
        other_comment = body + b"<!-- generated in 3 seconds by an editor note -->"
        self.assertNotEqual(
            _normalized_content_sha256(body), _normalized_content_sha256(other_comment)
        )

    def test_visible_text_marker_ignores_markup_and_script_order_only(self) -> None:
        first = (
            b'<html data-dpl-id="a"><head><title>ASVS | OWASP</title><style>.x{}</style></head><body>'
            b"<h1>ASVS</h1><p>Verifiable   requirements.</p>"
            b'<script>$RC("B:1","S:1")</script><script>self.__next_f.push([1,"a"])</script>'
            b"</body></html>"
        )
        second = (
            b'<html data-dpl-id="a"><head></head><body><h1 class="t">ASVS</h1>\n'
            b'<script>self.__next_f.push([1,"b"])</script><p>Verifiable requirements.</p>'
            b"<template>hidden</template><noscript>enable js</noscript>"
            b"<title>ASVS | OWASP</title></body></html>"
        )
        changed = second.replace(b"Verifiable", b"Optional")
        self.assertEqual(_visible_text_sha256(first), _visible_text_sha256(second))
        self.assertNotEqual(_visible_text_sha256(first), _visible_text_sha256(changed))

    def test_visible_text_marker_is_limited_to_reviewed_urls(self) -> None:
        from check_upstream_freshness import _fetch_marker

        schema = json.loads(
            (ROOT / "catalog" / "upstream-pins-schema.json").read_text(encoding="utf-8")
        )
        kinds = schema["properties"]["sources"]["items"]["properties"]["marker_kind"]["enum"]
        self.assertIn("visible-text-sha256", kinds)
        self.assertEqual(
            {"https://owasp.org/www-project-application-security-verification-standard/"},
            set(VISIBLE_TEXT_URLS),
        )

        class Response:
            headers: ClassVar[dict[str, str]] = {"Last-Modified": "Sun, 23 Aug 2026 18:16:51 GMT"}

            def __enter__(self) -> Response:
                return self

            def __exit__(
                self,
                exc_type: type[BaseException] | None,
                exc_value: BaseException | None,
                traceback: TracebackType | None,
            ) -> Literal[False]:
                return False

            def read(self) -> bytes:
                return b"<p>Readable text</p><script>x()</script>"

        with patch(
            "check_upstream_freshness.urllib.request.urlopen", return_value=Response()
        ):
            with self.assertRaises(ValueError):
                _fetch_marker("https://example.com/page", preferred_kind="visible-text-sha256")
            url = next(iter(VISIBLE_TEXT_URLS))
            self.assertEqual(
                ("visible-text-sha256", _visible_text_sha256(b"<p>Readable text</p>")),
                _fetch_marker(url),
            )
            self.assertEqual(
                ("visible-text-sha256", _visible_text_sha256(b"<p>Readable text</p>")),
                _fetch_marker(url, preferred_kind="visible-text-sha256"),
            )

    def test_dynamic_official_document_hosts_use_normalized_markers(self) -> None:
        self.assertTrue(
            {
                "developers.googleblog.com",
                "genai.owasp.org",
                "learn.chatgpt.com",
            }.issubset(NORMALIZED_HTML_HOSTS)
        )

    def test_default_normalized_marker_preserves_trailing_whitespace_policy(
        self,
    ) -> None:
        from check_upstream_freshness import _fetch_marker

        class Response:
            headers: ClassVar[dict[str, str]] = {}

            def __enter__(self) -> Response:
                return self

            def __exit__(
                self,
                exc_type: type[BaseException] | None,
                exc_value: BaseException | None,
                traceback: TracebackType | None,
            ) -> Literal[False]:
                return False

            def read(self) -> bytes:
                return b"stable authority content\r\n"

        url = (
            "https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/"
        )
        with patch(
            "check_upstream_freshness.urllib.request.urlopen", return_value=Response()
        ):
            kind, value = _fetch_marker(url)
        self.assertEqual("normalized-content-sha256", kind)
        self.assertEqual(
            _normalized_content_sha256(
                b"stable authority content", strip_trailing=True
            ),
            value,
        )

    def test_upstream_freshness_uses_primary_authority_urls_only(self) -> None:
        errors, report = check_upstream_freshness(online=False)
        self.assertEqual([], errors)
        self.assertEqual("pass", report["result"])


if __name__ == "__main__":
    unittest.main()
