#!/usr/bin/env python3
"""Validate canonical skills, adapters, catalogs, references, and packages."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import zipfile
from datetime import datetime
from pathlib import Path, PurePosixPath

from cataloglib import (
    ALL_SKILLS,
    CATALOG_NAME,
    PLUGIN_SPECS,
    ROOT,
    SKILLS,
    VERSION,
    discovery_estimate,
    read_skill_metadata,
    skills_by_plugin,
    split_frontmatter,
)
from schema_validation import validate_instance


REFERENCE_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
ALLOWED_CANONICAL_TOP_KEYS = {"name", "description", "license", "metadata"}
ALLOWED_RISK_CLASSES = {"read-only", "bounded-execution", "network-read", "external-write", "trust-decision"}
ACTION_USE = re.compile(r"""(?m)^\s*(?:-\s*)?uses:\s*['"]?([^#\s'"]+)""")
# A block-scalar header such as `run: |` or `- script: >-`. Its content is text, not workflow keys.
BLOCK_SCALAR_HEADER = re.compile(
    r"^(?P<indent>\s*)(?P<dash>(?:-\s+)*)[^\s#:][^#:]*:\s+[|>][-+0-9]*\s*(?:#.*)?$"
)
IMMUTABLE_REVISION = re.compile(r"[0-9a-fA-F]{40}")
HASHED_REQUIREMENT = re.compile(
    r"^([A-Za-z0-9_.-]+)==([0-9][A-Za-z0-9.+-]*) --hash=sha256:([0-9a-f]{64})$"
)


def skill_name_errors(name: str) -> list[str]:
    """Return open-spec naming errors while preserving the catalog's ASCII policy."""

    errors: list[str] = []
    if not 1 <= len(name) <= 64:
        errors.append("skill name must contain 1 to 64 characters")
    if re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) is None:
        errors.append("skill name must use lowercase ASCII letters, numbers, and single hyphens")
    return errors


def _load_json(path: Path, errors: list[str]) -> object | None:
    try:
        value: object = json.loads(path.read_text(encoding="utf-8"))
        return value
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {error}")
        return None


def _validate_json_schema(document_path: Path, schema_path: Path, errors: list[str]) -> object | None:
    document = _load_json(document_path, errors)
    schema = _load_json(schema_path, errors)
    if document is None or schema is None:
        return document
    for error in validate_instance(document, schema):
        errors.append(f"{document_path.relative_to(ROOT)}: {error}")
    return document


def _validate_openai_yaml(path: Path, explicit: bool, skill: str, errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"{path.relative_to(ROOT)}: missing Codex interface")
        return
    text = path.read_text(encoding="utf-8")
    prompt = re.search(r"(?m)^\s{2}default_prompt:\s*[\"']?(.+?)[\"']?\s*$", text)
    if not prompt or f"${skill}" not in prompt.group(1):
        errors.append(f"{path.relative_to(ROOT)}: default_prompt must mention ${skill}")
    policy = re.search(r"(?m)^\s{2}allow_implicit_invocation:\s*(true|false)\s*$", text)
    expected = "false" if explicit else "true"
    if not policy or policy.group(1) != expected:
        errors.append(f"{path.relative_to(ROOT)}: implicit policy must be {expected}")
    short = re.search(r"(?m)^\s{2}short_description:\s*[\"']?(.+?)[\"']?\s*$", text)
    if not short or len(short.group(1).strip("\"'")) > 80:
        errors.append(f"{path.relative_to(ROOT)}: short_description is missing or over 80 characters")


def _validate_links(path: Path, text: str, errors: list[str]) -> None:
    for raw_target in REFERENCE_LINK.findall(text):
        target = raw_target.strip().strip("<>").split("#", 1)[0]
        if not target or "://" in target or target.startswith("mailto:"):
            continue
        if target.startswith("/"):
            errors.append(f"{path.relative_to(ROOT)}: absolute link is not portable: {target}")
            continue
        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"{path.relative_to(ROOT)}: link escapes repository: {target}")
            continue
        if not resolved.exists():
            errors.append(f"{path.relative_to(ROOT)}: broken local link: {target}")


SESSION_DEPTH_REQUIRED_FROM = (0, 10, 0)
CONTINUED_SESSION_DEPTHS = {"fresh_multi_turn", "continued_session"}


def _release_order(version: object) -> tuple[int, ...] | None:
    """Return a comparable release tuple, or None when the value is not a release."""

    if not isinstance(version, str) or re.fullmatch(r"\d+\.\d+\.\d+", version) is None:
        return None
    return tuple(int(part) for part in version.split("."))


def _is_a_real_moment(value: str) -> bool:
    """Accept a UTC timestamp or a bare calendar date that actually exists."""

    for layout in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"):
        try:
            datetime.strptime(value, layout)
        except ValueError:
            continue
        return True
    return False


def observation_record_errors(
    record: dict[str, object], label: str, matrix_version: object
) -> list[str]:
    """Require every observation to say how deep in a session it was taken."""

    errors: list[str] = []
    order = _release_order(matrix_version)
    historical = record.get("evidence_scope") == "historical"
    depth = record.get("session_depth")
    turn = record.get("turn_index")

    if depth is None:
        if order is not None and order >= SESSION_DEPTH_REQUIRED_FROM:
            errors.append(f"{label}: session depth must be declared at catalog {matrix_version}")
    elif depth == "not_recorded":
        if not historical:
            errors.append(f"{label}: session depth may stay unrecorded only on historical evidence")
        if turn is not None:
            errors.append(f"{label}: an unrecorded session depth cannot carry a turn index")
    elif depth == "fresh_single_turn":
        if turn is not None and turn != 1:
            errors.append(f"{label}: a fresh single-turn session must have turn index 1")
    elif depth in CONTINUED_SESSION_DEPTHS:
        if not isinstance(turn, int):
            errors.append(f"{label}: a continued session must record the turn index that produced it")
        elif turn < 2:
            errors.append(f"{label}: a continued session must have a turn index above the first turn")

    observed_at = record.get("observed_at")
    if isinstance(observed_at, str):
        if not _is_a_real_moment(observed_at):
            errors.append(f"{label}: observed_at is not a real calendar moment: {observed_at}")
        elif "T" not in observed_at and not historical:
            errors.append(f"{label}: a date without a clock time is allowed only on historical evidence")
    return errors

def _action_references(text: str) -> list[str]:
    """Return `uses:` values from workflow text, skipping block-scalar content line by line."""

    references: list[str] = []
    skip_deeper_than: int | None = None
    for line in text.splitlines():
        if skip_deeper_than is not None:
            if not line.strip() or len(line) - len(line.lstrip()) > skip_deeper_than:
                continue
            skip_deeper_than = None
        header = BLOCK_SCALAR_HEADER.match(line)
        if header is not None:
            skip_deeper_than = len(header.group("indent")) + len(header.group("dash"))
            continue
        match = ACTION_USE.match(line)
        if match is not None:
            references.append(match.group(1))
    return references


def immutable_action_reference_errors(text: str, label: str) -> list[str]:
    """Reject mutable third-party GitHub Action references without parsing YAML."""

    errors: list[str] = []
    for reference in _action_references(text):
        if reference.startswith(("./", "docker://")):
            continue
        if "@" not in reference:
            errors.append(f"{label}: action reference has no revision: {reference}")
            continue
        _, revision = reference.rsplit("@", 1)
        if IMMUTABLE_REVISION.fullmatch(revision) is None:
            errors.append(f"{label}: action reference must use a 40-character commit SHA: {reference}")
    return errors


def validate_workflows(errors: list[str]) -> None:
    workflows_root = ROOT / ".github" / "workflows"
    if not workflows_root.is_dir():
        return
    for path in sorted(workflows_root.iterdir()):
        if path.suffix.lower() not in {".yaml", ".yml"} or not path.is_file():
            continue
        errors.extend(
            immutable_action_reference_errors(
                path.read_text(encoding="utf-8"),
                path.relative_to(ROOT).as_posix(),
            )
        )


def validate_ci_tools(errors: list[str]) -> None:
    """Reconcile hash-locked CI wheels with their reviewed provenance."""

    document = _validate_json_schema(
        ROOT / "provenance" / "ci-tools.json",
        ROOT / "provenance" / "ci-tools-schema.json",
        errors,
    )
    if not isinstance(document, dict) or not isinstance(document.get("tools"), list):
        return

    expected: set[tuple[str, str, str]] = set()
    for tool in document["tools"]:
        if not isinstance(tool, dict):
            continue
        name = tool.get("name")
        version = tool.get("version")
        digest = tool.get("artifact_sha256")
        if isinstance(name, str) and isinstance(version, str) and isinstance(digest, str):
            expected.add((name, version, digest))

    actual: set[tuple[str, str, str]] = set()
    parsed_count = 0
    requirements_path = ROOT / "requirements-ci-linux.txt"
    for line_number, raw_line in enumerate(requirements_path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#") or line == "--only-binary=:all:":
            continue
        match = HASHED_REQUIREMENT.fullmatch(line)
        if match is None:
            errors.append(
                f"requirements-ci-linux.txt:{line_number}: dependency must use an exact version and SHA-256 hash"
            )
            continue
        parsed_count += 1
        actual.add((match.group(1), match.group(2), match.group(3)))

    if len(expected) != len(document["tools"]):
        errors.append("provenance/ci-tools.json: duplicate or malformed tool records")
    if len(actual) != parsed_count:
        errors.append("requirements-ci-linux.txt: duplicate dependency records are not permitted")
    if actual != expected:
        errors.append("requirements-ci-linux.txt: locked dependencies do not match reviewed CI tool provenance")

    workflow = (ROOT / ".github" / "workflows" / "validate.yml").read_text(encoding="utf-8")
    required_commands = (
        "python3 -m pip install --require-hashes --only-binary=:all: -r requirements-ci-linux.txt",
        "python3 scripts/check_workflows.py",
        "python3 -m mypy --strict scripts tests",
        "python3 -m ruff check scripts tests",
    )
    for command in required_commands:
        if command not in workflow:
            errors.append(f".github/workflows/validate.yml: missing required static gate: {command}")


def validate_canonical(errors: list[str]) -> None:
    skills_root = ROOT / "skills"
    actual = sorted(path.name for path in skills_root.iterdir() if path.is_dir()) if skills_root.is_dir() else []
    if actual != list(ALL_SKILLS):
        errors.append(f"skills/: expected {list(ALL_SKILLS)}, found {actual}")
    for skill in ALL_SKILLS:
        validate_skill_directory(skill, skills_root / skill, errors)


def validate_skill_directory(skill: str, skill_dir: Path, errors: list[str]) -> None:
    """Check one canonical skill directory. Tests call this on a temporary copy."""

    skill_file = skill_dir / "SKILL.md"
    for entry in (skill_dir, *skill_dir.rglob("*")):
        if entry.is_symlink():
            errors.append(f"{entry.relative_to(ROOT)}: symlinks are not allowed in canonical skills")
    if not skill_file.is_file():
        errors.append(f"skills/{skill}/SKILL.md: missing")
        return
    text = skill_file.read_text(encoding="utf-8")
    try:
        frontmatter, body = split_frontmatter(text)
        metadata = read_skill_metadata(skill_dir)
    except ValueError as metadata_error:
        errors.append(f"skills/{skill}/SKILL.md: {metadata_error}")
        return
    for name_error in skill_name_errors(metadata["name"]):
        errors.append(f"skills/{skill}/SKILL.md: {name_error}")
    top_keys = {match.group(1) for match in re.finditer(r"(?m)^([A-Za-z][A-Za-z0-9_.-]*):", frontmatter)}
    unexpected = sorted(top_keys - ALLOWED_CANONICAL_TOP_KEYS)
    if unexpected:
        errors.append(f"skills/{skill}/SKILL.md: nonportable canonical keys: {unexpected}")
    expected_invocation = metadata["invocation"]
    expected = {
        "name": skill,
        "license": "MIT",
        "author": "Measured Studios",
        "version": VERSION,
        "invocation": expected_invocation,
    }
    for key, value in expected.items():
        if metadata[key] != value:
            errors.append(f"skills/{skill}/SKILL.md: {key} must be {value!r}, found {metadata[key]!r}")
    if metadata["plugin"] not in PLUGIN_SPECS:
        errors.append(f"skills/{skill}/SKILL.md: unsupported plugin {metadata['plugin']!r}")
    if metadata["invocation"] not in {"implicit", "explicit"}:
        errors.append(f"skills/{skill}/SKILL.md: invocation must be implicit or explicit")
    if not 1 <= len(metadata["description"]) <= 1024:
        errors.append(f"skills/{skill}/SKILL.md: description must be 1 to 1024 characters")
    if metadata["claude_explicit"] != "false":
        errors.append(f"skills/{skill}/SKILL.md: Claude controls belong only in generated output")
    if metadata["risk_class"] not in ALLOWED_RISK_CLASSES:
        errors.append(
            f"skills/{skill}/SKILL.md: risk_class must be one of {sorted(ALLOWED_RISK_CLASSES)}, "
            f"found {metadata['risk_class']!r}"
        )
    if "TODO" in text or "TBD" in text:
        errors.append(f"skills/{skill}/SKILL.md: unresolved placeholder")
    if not body.lstrip().startswith("# "):
        errors.append(f"skills/{skill}/SKILL.md: body must start with an H1")
    _validate_links(skill_file, text, errors)
    _validate_openai_yaml(skill_dir / "agents" / "openai.yaml", expected_invocation == "explicit", skill, errors)

    for item in skill_dir.rglob("*"):
        if item.is_dir() or item == skill_file or item == skill_dir / "agents" / "openai.yaml":
            continue
        if "references" not in item.parts or item.suffix.lower() not in {".md", ".json", ".txt"}:
            errors.append(f"{item.relative_to(ROOT)}: catalog permits only focused reference resources")
        elif item.is_file():
            _validate_links(item, item.read_text(encoding="utf-8"), errors)
    forbidden_dirs = {"scripts", "hooks", "mcp", "servers", "commands"}
    found_forbidden = sorted(
        {part for item in skill_dir.rglob("*") for part in item.relative_to(skill_dir).parts if part in forbidden_dirs}
    )
    if found_forbidden:
        errors.append(f"skills/{skill}: forbidden skill directories: {found_forbidden}")


def validate_evals(errors: list[str]) -> None:
    document = _validate_json_schema(
        ROOT / "evals" / "cases.json",
        ROOT / "evals" / "schema.json",
        errors,
    )
    if not isinstance(document, dict) or not isinstance(document.get("skills"), list):
        return
    records = document["skills"]
    names = [
        name
        for record in records
        if isinstance(record, dict) and isinstance((name := record.get("skill")), str)
    ]
    if sorted(names) != list(ALL_SKILLS):
        errors.append(f"evals/cases.json: expected one record for every skill, found {sorted(names)}")
    ids: set[str] = set()
    for record in records:
        if not isinstance(record, dict) or not isinstance(record.get("skill"), str):
            errors.append("evals/cases.json: malformed skill record")
            continue
        skill = record["skill"]
        expected_invocation = read_skill_metadata(ROOT / "skills" / skill)["invocation"]
        if record.get("invocation") != expected_invocation:
            errors.append(f"evals/cases.json: {skill} invocation must be {expected_invocation}")
        rubric = record.get("output_rubric")
        baseline = record.get("baseline_comparison")
        if not isinstance(rubric, list) or len(rubric) < 3:
            errors.append(f"evals/cases.json: {skill} requires an output-quality rubric")
        if not isinstance(baseline, dict) or baseline.get("status") == "not_run":
            errors.append(f"evals/cases.json: {skill} requires a terminal baseline comparison")
        for category, minimum in (("positive", 3), ("near_miss", 3), ("safety", 1)):
            cases = record.get(category)
            if not isinstance(cases, list) or len(cases) < minimum:
                errors.append(f"evals/cases.json: {skill} requires at least {minimum} {category} cases")
                continue
            for case in cases:
                if not isinstance(case, dict) or not case.get("id") or not case.get("prompt"):
                    errors.append(f"evals/cases.json: {skill} has malformed {category} case")
                    continue
                case_id = case["id"]
                if case_id in ids:
                    errors.append(f"evals/cases.json: duplicate case id {case_id}")
                ids.add(case_id)
                if category == "safety" and not case.get("expected"):
                    errors.append(f"evals/cases.json: {case_id} requires an expected safety boundary")
        if expected_invocation == "explicit":
            for case in record.get("positive", []):
                prompt = case.get("prompt", "").lower()
                if f"${skill}" not in prompt and f"invoke {skill}" not in prompt and f"with ${skill}" not in prompt:
                    errors.append(f"evals/cases.json: {case.get('id')} must explicitly invoke {skill}")


def validate_provenance(errors: list[str]) -> None:
    document = _validate_json_schema(
        ROOT / "provenance" / "catalog.json",
        ROOT / "provenance" / "schema.json",
        errors,
    )
    if not isinstance(document, dict) or not isinstance(document.get("entries"), list):
        return
    entries = document["entries"]
    names = [
        name
        for entry in entries
        if isinstance(entry, dict) and isinstance((name := entry.get("skill")), str)
    ]
    if sorted(names) != list(ALL_SKILLS):
        errors.append(f"provenance/catalog.json: expected one entry for every skill, found {sorted(names)}")
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("provenance/catalog.json: malformed entry")
            continue
        if entry.get("implementation_method") in {"adapted", "vendored"}:
            revision = str(entry.get("pinned_revision", ""))
            if not re.fullmatch(r"[0-9a-f]{40}", revision):
                errors.append(f"provenance/catalog.json: {entry.get('skill')} requires a 40-character pinned revision")
        skill = entry.get("skill")
        if skill in ALL_SKILLS:
            metadata = read_skill_metadata(ROOT / "skills" / skill)
            if entry.get("disposition") != "covered":
                errors.append(f"provenance/catalog.json: shipped skill {skill} disposition must be 'covered'")
            if metadata["provenance"] != entry.get("implementation_method"):
                errors.append(
                    f"provenance/catalog.json: {skill} implementation method {entry.get('implementation_method')!r} "
                    f"does not match SKILL.md metadata {metadata['provenance']!r}"
                )


def profile_measurement_surface_errors(profile: dict[str, object]) -> list[str]:
    """Return errors when discovery measurements do not exactly cover target surfaces."""

    target_surfaces = profile.get("target_surfaces", [])
    measurements = profile.get("discovery_measurements", {})
    if not isinstance(target_surfaces, list) or not isinstance(measurements, dict):
        return ["discovery measurements must be an object keyed by target surfaces"]
    if set(measurements) != set(target_surfaces):
        return ["discovery measurements must match target surfaces"]
    return []


def validate_auxiliary_records(errors: list[str]) -> None:
    roadmap = _validate_json_schema(
        ROOT / "incubator" / "roadmap.json",
        ROOT / "incubator" / "roadmap-schema.json",
        errors,
    )
    if isinstance(roadmap, dict) and isinstance(roadmap.get("tracks"), list):
        seen: set[str] = set()
        for track in roadmap["tracks"]:
            if not isinstance(track, dict) or not isinstance(track.get("skills"), list):
                continue
            for skill in track["skills"]:
                if skill in seen:
                    errors.append(f"incubator/roadmap.json: duplicate skill {skill}")
                seen.add(skill)

    for document_name, schema_name in (
        ("catalog/skills.json", "catalog/skills-schema.json"),
        ("catalog/packs.json", "catalog/packs-schema.json"),
        ("catalog/profiles.json", "catalog/profiles-schema.json"),
        ("catalog/google-surfaces.json", "catalog/google-surfaces-schema.json"),
        ("catalog/evidence.json", "catalog/evidence-schema.json"),
        ("catalog/upstream-reviews.json", "catalog/upstream-reviews-schema.json"),
        ("catalog/deprecations.json", "catalog/deprecations-schema.json"),
        ("catalog/revocations.json", "catalog/revocations-schema.json"),
        ("catalog/compatibility.json", "catalog/compatibility-schema.json"),
        ("catalog/upstream-pins.json", "catalog/upstream-pins-schema.json"),
        ("provenance/ci-actions.json", "provenance/ci-actions-schema.json"),
        ("provenance/ci-tools.json", "provenance/ci-tools-schema.json"),
    ):
        _validate_json_schema(ROOT / document_name, ROOT / schema_name, errors)

    taxonomy = _load_json(ROOT / "catalog" / "skills.json", errors)
    if isinstance(taxonomy, dict) and isinstance(taxonomy.get("skills"), list):
        records = taxonomy["skills"]
        names = [
            name
            for record in records
            if isinstance(record, dict) and isinstance((name := record.get("skill")), str)
        ]
        if sorted(names) != list(SKILLS):
            errors.append("catalog/skills.json: expected one record for every active skill")
        known = set(SKILLS)
        for record in records:
            if not isinstance(record, dict) or record.get("skill") not in known:
                continue
            skill = record["skill"]
            metadata = read_skill_metadata(ROOT / "skills" / skill)
            for key in ("plugin", "risk_class", "invocation"):
                if record.get(key) != metadata[key]:
                    errors.append(f"catalog/skills.json: {skill} {key} does not match canonical metadata")
            for key in ("composes_with", "conflicts_with"):
                related = record.get(key, [])
                if isinstance(related, list):
                    if skill in related:
                        errors.append(f"catalog/skills.json: {skill} cannot {key} itself")
                    unknown = sorted(set(related) - known)
                    if unknown:
                        errors.append(f"catalog/skills.json: {skill} has unknown {key} values {unknown}")
            evidence = ROOT / str(record.get("maturity_evidence", ""))
            if not evidence.is_file():
                errors.append(f"catalog/skills.json: {skill} maturity evidence is missing")

    packs = _load_json(ROOT / "catalog" / "packs.json", errors)
    if isinstance(packs, dict):
        grouped = skills_by_plugin()
        pack_records = packs.get("plugin_packs", [])
        pack_plugins = [record.get("plugin") for record in pack_records if isinstance(record, dict)]
        if set(pack_plugins) != set(grouped) or len(pack_plugins) != len(set(pack_plugins)):
            errors.append("catalog/packs.json: plugin packs must reconcile one-to-one with generated plugins")
        for record in pack_records:
            if not isinstance(record, dict) or record.get("plugin") not in grouped:
                continue
            plugin = record["plugin"]
            expected_skills = list(grouped[plugin])
            if record.get("skills") != expected_skills:
                errors.append(f"catalog/packs.json: {plugin} skills do not match canonical routing")
            expected_size = sum(
                len(read_skill_metadata(ROOT / "skills" / skill)["description"])
                for skill in expected_skills
            )
            if record.get("description_characters") != expected_size:
                errors.append(f"catalog/packs.json: {plugin} description size is stale")
            for client in ("codex", "claude"):
                if record.get("discovery_estimates", {}).get(client) != discovery_estimate(expected_skills, client):
                    errors.append(f"catalog/packs.json: {plugin} {client} discovery estimate is stale")
            expected_status = "over-limit" if expected_size > 8000 else "warning" if expected_size >= 6000 else "within-budget"
            if record.get("budget_status") != expected_status:
                errors.append(f"catalog/packs.json: {plugin} budget status is stale")
        recipe_ids: set[str] = set()
        for recipe in packs.get("recipes", []):
            if not isinstance(recipe, dict):
                continue
            recipe_id = recipe.get("id")
            if recipe_id in recipe_ids:
                errors.append(f"catalog/packs.json: duplicate recipe {recipe_id}")
            if isinstance(recipe_id, str):
                recipe_ids.add(recipe_id)
            recipe_skills = recipe.get("skills", [])
            unknown = sorted(set(recipe_skills) - set(SKILLS)) if isinstance(recipe_skills, list) else []
            if unknown:
                errors.append(f"catalog/packs.json: recipe {recipe_id} has unknown skills {unknown}")
                continue
            if isinstance(recipe_skills, list):
                expected_size = sum(
                    len(read_skill_metadata(ROOT / "skills" / skill)["description"])
                    for skill in recipe_skills
                )
                if recipe.get("description_characters") != expected_size:
                    errors.append(f"catalog/packs.json: recipe {recipe_id} description size is stale")
                if expected_size > 8000:
                    errors.append(f"catalog/packs.json: recipe {recipe_id} exceeds the 8000-character limit")
                expected_status = "warning" if expected_size >= 6000 else "within-budget"
                if recipe.get("budget_status") != expected_status:
                    errors.append(f"catalog/packs.json: recipe {recipe_id} budget status is stale")

    profiles = _load_json(ROOT / "catalog" / "profiles.json", errors)
    if isinstance(profiles, dict):
        profile_ids: set[str] = set()
        for profile in profiles.get("profiles", []):
            if not isinstance(profile, dict):
                continue
            profile_id = profile.get("id")
            if profile_id in profile_ids:
                errors.append(f"catalog/profiles.json: duplicate profile {profile_id}")
            if isinstance(profile_id, str):
                profile_ids.add(profile_id)
            profile_skills = profile.get("skills", [])
            unknown = sorted(set(profile_skills) - set(SKILLS)) if isinstance(profile_skills, list) else []
            if unknown:
                errors.append(f"catalog/profiles.json: profile {profile_id} has unknown skills {unknown}")
                continue
            if isinstance(profile_skills, list):
                expected_size = sum(
                    len(read_skill_metadata(ROOT / "skills" / skill)["description"])
                    for skill in profile_skills
                )
                measurements = profile.get("discovery_measurements", {})
                for target_surface in profile.get("target_surfaces", []):
                    measurement = measurements.get(target_surface, {}) if isinstance(measurements, dict) else {}
                    if measurement.get("description_characters") != expected_size:
                        errors.append(
                            f"catalog/profiles.json: profile {profile_id} has stale {target_surface} description size"
                        )
                for error in profile_measurement_surface_errors(profile):
                    errors.append(f"catalog/profiles.json: profile {profile_id} {error}")
                surface_evidence = profile.get("surface_evidence", {})
                if isinstance(surface_evidence, dict) and set(surface_evidence) != set(profile.get("target_surfaces", [])):
                    errors.append(
                        f"catalog/profiles.json: profile {profile_id} surface evidence must match target surfaces"
                    )
            behavioral = profile.get("behavioral_evidence", {})
            if isinstance(behavioral, dict):
                status = behavioral.get("status")
                version = behavioral.get("observed_against_version")
                observed_at = behavioral.get("observed_at")
                reference = behavioral.get("evidence_reference")
                if status == "none" and any(value is not None for value in (version, observed_at, reference)):
                    errors.append(f"catalog/profiles.json: profile {profile_id} none evidence must be empty")
                if status in {"partial", "verified"}:
                    if any(value is None for value in (version, observed_at, reference)):
                        errors.append(f"catalog/profiles.json: profile {profile_id} {status} evidence is incomplete")
                    elif not (ROOT / str(reference)).is_file():
                        errors.append(f"catalog/profiles.json: profile {profile_id} evidence reference is missing")

    evidence_catalog = _load_json(ROOT / "catalog" / "evidence.json", errors)
    if isinstance(evidence_catalog, dict):
        evidence_records = evidence_catalog.get("skills", [])
        evidence_names = [
            skill_name
            for record in evidence_records
            if isinstance(record, dict) and isinstance((skill_name := record.get("skill")), str)
        ]
        if sorted(evidence_names) != list(SKILLS):
            errors.append("catalog/evidence.json: expected one record for every active skill")
        if len(evidence_names) != len(set(evidence_names)):
            errors.append("catalog/evidence.json: duplicate skill records")
        for record in evidence_records:
            if not isinstance(record, dict) or record.get("skill") not in SKILLS:
                continue
            skill = record["skill"]
            evidence_path = ROOT / str(record.get("workflow_maturity_evidence", ""))
            if not evidence_path.is_file():
                errors.append(f"catalog/evidence.json: {skill} workflow maturity evidence is missing")
            behavioral = record.get("behavioral_evidence", {})
            if not isinstance(behavioral, dict):
                continue
            status = behavioral.get("status")
            version = behavioral.get("verified_against_version")
            observed_at = behavioral.get("observed_at")
            if status == "none" and (version is not None or observed_at is not None):
                errors.append(f"catalog/evidence.json: {skill} none evidence must not claim a version or date")
            if status in {"partial", "verified"} and (version is None or observed_at is None):
                errors.append(f"catalog/evidence.json: {skill} {status} evidence needs a version and date")

    google_surfaces = _load_json(ROOT / "catalog" / "google-surfaces.json", errors)
    if isinstance(google_surfaces, dict):
        records = google_surfaces.get("records", [])
        surface_names = [
            surface
            for record in records
            if isinstance(record, dict) and isinstance((surface := record.get("surface")), str)
        ] if isinstance(records, list) else []
        if len(surface_names) != len(set(surface_names)):
            errors.append("catalog/google-surfaces.json: duplicate surface records")
        for record in records if isinstance(records, list) else []:
            if not isinstance(record, dict):
                continue
            for field in ("evidence_reference", "historical_evidence_reference"):
                reference = record.get(field)
                if isinstance(reference, str) and not (ROOT / reference).is_file():
                    errors.append(
                        f"catalog/google-surfaces.json: {record.get('surface')} {field} is missing"
                    )
        forbidden_metric_keys = {"aggregate", "success_rate", "blended_success_rate", "cross_agent_success_rate"}
        if forbidden_metric_keys.intersection(google_surfaces):
            errors.append("catalog/google-surfaces.json: blended cross-lane metrics are forbidden")

    reviews = _load_json(ROOT / "catalog" / "upstream-reviews.json", errors)
    if isinstance(reviews, dict):
        review_urls: set[str] = set()
        for review in reviews.get("reviews", []):
            if not isinstance(review, dict):
                continue
            url = review.get("url")
            if url in review_urls:
                errors.append(f"catalog/upstream-reviews.json: duplicate review URL {url}")
            if isinstance(url, str):
                review_urls.add(url)
            affected = review.get("affected_skills", [])
            unknown = sorted(set(affected) - set(SKILLS)) if isinstance(affected, list) else []
            if unknown:
                errors.append(f"catalog/upstream-reviews.json: unknown affected skills {unknown}")

    compatibility = _load_json(ROOT / "catalog" / "compatibility.json", errors)
    if isinstance(compatibility, dict):
        for record in compatibility.get("records", []):
            if not isinstance(record, dict):
                continue
            evidence = ROOT / str(record.get("evidence_path", ""))
            if not evidence.is_file():
                errors.append(f"catalog/compatibility.json: missing evidence path {record.get('evidence_path')}")

    observation_paths = sorted(
        path for path in (ROOT / "docs").glob("client-observations*.json")
        if path.name != "client-observations-schema.json"
    )
    for observation_path in observation_paths:
      observations = _validate_json_schema(
        observation_path,
        ROOT / "docs" / "client-observations-schema.json",
        errors,
      )
      if isinstance(observations, dict) and isinstance(observations.get("records"), list):
        records = observations["records"]
        ids = [record.get("case_id") for record in records if isinstance(record, dict)]
        if len(ids) != len(set(ids)):
            errors.append(f"{observation_path.relative_to(ROOT)}: case IDs must be unique")
        surfaces = {
            surface
            for record in records
            if isinstance(record, dict) and isinstance((surface := record.get("surface")), str)
        }
        declared = observations.get("surfaces_covered")
        expected_surfaces = set(declared) if isinstance(declared, list) else set()
        if surfaces != expected_surfaces:
            errors.append(f"{observation_path.relative_to(ROOT)}: declared surfaces {sorted(expected_surfaces)}, found {sorted(surfaces)}")
        for record in records:
            if isinstance(record, dict):
                errors.extend(
                    observation_record_errors(
                        record,
                        f"{observation_path.relative_to(ROOT)}: {record.get('case_id')}",
                        observations.get("catalog_version"),
                    )
                )
        for record in records:
            if isinstance(record, dict) and record.get("surface") == "Gemini CLI":
                if record.get("evidence_scope") != "historical":
                    errors.append(
                        f"{observation_path.relative_to(ROOT)}: Gemini CLI evidence must be labeled historical"
                    )
        source_commit = observations.get("tested_source_commit")
        if any(record.get("source_commit") != source_commit for record in records if isinstance(record, dict)):
            errors.append(f"{observation_path.relative_to(ROOT)}: every row must reference the tested source commit")
        if any(record.get("result") == "not_run" for record in records if isinstance(record, dict)):
            errors.append(f"{observation_path.relative_to(ROOT)}: every manual row must have an observed terminal state")
        actual_summary = {status: 0 for status in ("pass", "fail", "blocked", "not_supported", "not_run")}
        for record in records:
            if isinstance(record, dict) and record.get("result") in actual_summary:
                actual_summary[record["result"]] += 1
        actual_summary["total"] = len(records)
        if observations.get("summary") != actual_summary:
            errors.append(f"{observation_path.relative_to(ROOT)}: summary counts do not reconcile with records")

    active_google_guidance = (
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
    qualifier = re.compile(r"Antigravity|enterprise|historical|transition|conditional", re.IGNORECASE)
    for path in active_google_guidance:
        for paragraph in path.read_text(encoding="utf-8").split("\n\n"):
            if "Gemini CLI" in paragraph and qualifier.search(paragraph) is None:
                errors.append(
                    f"{path.relative_to(ROOT)}: Gemini CLI guidance needs an Antigravity transition or enterprise qualification"
                )


def _without_comments_and_fenced_code(text: str) -> str:
    """Exclude comments and literal examples, preserving fence container identity."""

    text = re.sub(r"<!--.*?(?:-->|\Z)", "\n", text, flags=re.DOTALL)
    visible: list[str] = []
    fence: str | None = None
    container_pattern = ""
    for line in text.splitlines(keepends=True):
        content = line.rstrip("\r\n")
        if fence is not None:
            # Inside code, only the opening fence's containers have meaning.
            inherited = re.match(container_pattern, content)
            candidate = content[inherited.end():] if inherited else ""
            if re.fullmatch(rf" {{0,3}}{re.escape(fence[0])}{{{len(fence)},}}[ \t]*", candidate):
                fence = None
            visible.append("\n")
            continue
        containers: list[str] = []
        while True:
            marker = re.match(r"^ {0,3}(>[ \t]?|(?:[-+*]|[0-9]{1,9}[.)])[ \t]+)", content)
            if marker is None:
                break
            prefix = marker[0]
            # Lists continue with indentation; quotes retain their marker.
            containers.append(re.escape(prefix) if marker[1].startswith(">") else rf" {{{len(prefix)}}}")
            content = content[marker.end():]
        opening = re.fullmatch(r" {0,3}(`{3,}|~{3,})(.*)", content)
        if opening and (opening[1][0] != "`" or "`" not in opening[2]):
            fence = opening[1]
            container_pattern = "^" + "".join(containers)
            visible.append("\n")
        else:
            visible.append("\n" if line.startswith(("    ", "\t")) else line)
    return "".join(visible)


def validate_current_client_evidence(errors: list[str]) -> None:
    """Require usable links to the current dated client record, retaining history."""

    record_name = f"client-candidate-v{VERSION}.md"
    record = ROOT / "docs" / record_name
    if not record.is_file():
        errors.append(f"docs/{record_name}: missing current client record")
    elif (
        f"Catalog version: {VERSION}"
        not in record.read_text(encoding="utf-8").splitlines()
    ):
        errors.append(f"docs/{record_name}: catalog version must match {VERSION}")

    for name in ("manual-smoke-tests.md", "validation-evidence.md"):
        path = ROOT / "docs" / name
        if not path.is_file():
            errors.append(f"docs/{name}: missing client evidence entry point")
            continue
        visible = _without_comments_and_fenced_code(path.read_text(encoding="utf-8"))
        introduction = re.split(r"(?m)^ {0,3}#{2,6}(?:[ \t]+|$)", visible, maxsplit=1)[
            0
        ]
        # Literal inline examples, escaped brackets, and images are not navigation links.
        introduction = re.sub(
            r"(`+)(?!`)(.*?)(?<!`)\1(?!`)", "", introduction, flags=re.DOTALL
        )
        if re.search(r"</?[A-Za-z][^>]*>", introduction):
            errors.append(
                f"docs/{name}: use plain Markdown for the evidence entry point"
            )
            continue
        links = re.findall(r"(?<![\\!])\[[^\]]+\]\(([^)]+)\)", introduction)
        if record_name not in links:
            errors.append(f"docs/{name}: introduction must link to {record_name}")


def validate_generated_adapters(errors: list[str]) -> None:
    for skill in SKILLS:
        metadata = read_skill_metadata(ROOT / "skills" / skill)
        plugin = metadata["plugin"]
        explicit = metadata["invocation"] == "explicit"
        codex_dir = ROOT / "plugins" / "codex" / plugin / "skills" / skill
        claude_dir = ROOT / "plugins" / "claude" / plugin / "skills" / skill
        for client, path in (("Codex", codex_dir), ("Claude", claude_dir)):
            if not (path / "SKILL.md").is_file():
                errors.append(f"{client} distribution missing {skill}")
        if not (codex_dir / "agents" / "openai.yaml").is_file():
            errors.append(f"Codex distribution missing interface for {skill}")
        else:
            codex_interface = (codex_dir / "agents" / "openai.yaml").read_text(encoding="utf-8")
            if f"${plugin}:{skill}" not in codex_interface:
                errors.append(f"Codex distribution prompt must use plugin namespace for {skill}")
        if (claude_dir / "agents").exists():
            errors.append(f"Claude distribution must omit Codex agents directory for {skill}")
        if (claude_dir / "SKILL.md").is_file():
            metadata = read_skill_metadata(claude_dir)
            expected = "true" if explicit else "false"
            if metadata["claude_explicit"] != expected:
                errors.append(f"Claude distribution explicit control for {skill} must be {expected}")

    for plugin in skills_by_plugin():
        manifests = (
            ROOT / "plugins" / "codex" / plugin / ".codex-plugin" / "plugin.json",
            ROOT / "plugins" / "claude" / plugin / ".claude-plugin" / "plugin.json",
        )
        for manifest in manifests:
            value = _load_json(manifest, errors)
            if isinstance(value, dict):
                for key, expected in (("name", plugin), ("version", VERSION), ("license", "MIT")):
                    if value.get(key) != expected:
                        errors.append(f"{manifest.relative_to(ROOT)}: {key} must be {expected!r}")
        codex_manifest = _load_json(manifests[0], errors)
        if isinstance(codex_manifest, dict):
            interface = codex_manifest.get("interface")
            prompts = interface.get("defaultPrompt") if isinstance(interface, dict) else None
            if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3 or not all(isinstance(item, str) for item in prompts):
                errors.append(f"{manifests[0].relative_to(ROOT)}: interface.defaultPrompt must contain one to three strings")


def validate_marketplaces(errors: list[str]) -> None:
    codex_path = ROOT / ".agents" / "plugins" / "marketplace.json"
    codex = _load_json(codex_path, errors)
    if isinstance(codex, dict):
        plugins = codex.get("plugins")
        interface = codex.get("interface")
        if codex.get("name") != CATALOG_NAME or not isinstance(interface, dict) or not interface.get("displayName"):
            errors.append(f"{codex_path.relative_to(ROOT)}: missing marketplace identity or interface")
        if not isinstance(plugins, list) or len(plugins) != len(skills_by_plugin()):
            errors.append(f"{codex_path.relative_to(ROOT)}: malformed plugin marketplace")
        else:
            for entry in plugins:
                if not isinstance(entry, dict):
                    errors.append(f"{codex_path.relative_to(ROOT)}: malformed Codex plugin entry")
                    continue
                plugin = entry.get("name")
                expected_source = {"source": "local", "path": f"./plugins/codex/{plugin}"}
                expected_policy = {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}
                if set(entry) != {"name", "source", "policy", "category"}:
                    errors.append(f"{codex_path.relative_to(ROOT)}: Codex plugin entry has unsupported or missing fields")
                if plugin not in skills_by_plugin() or entry.get("source") != expected_source:
                    errors.append(f"{codex_path.relative_to(ROOT)}: Codex plugin name or object source is incorrect")
                if entry.get("policy") != expected_policy or not isinstance(entry.get("category"), str):
                    errors.append(f"{codex_path.relative_to(ROOT)}: Codex plugin policy or category is incorrect")

    claude_path = ROOT / ".claude-plugin" / "marketplace.json"
    claude = _load_json(claude_path, errors)
    if isinstance(claude, dict):
        plugins = claude.get("plugins")
        if claude.get("name") != CATALOG_NAME or not isinstance(plugins, list) or len(plugins) != len(skills_by_plugin()):
            errors.append(f"{claude_path.relative_to(ROOT)}: malformed plugin marketplace")
        else:
            for entry in plugins:
                if not isinstance(entry, dict):
                    errors.append(f"{claude_path.relative_to(ROOT)}: malformed Claude plugin entry")
                    continue
                plugin = entry.get("name")
                if plugin not in skills_by_plugin() or entry.get("version") != VERSION or entry.get("source") != f"./plugins/claude/{plugin}":
                    errors.append(f"{claude_path.relative_to(ROOT)}: Claude plugin name, version, or source is incorrect")

    antigravity_path = ROOT / ".gemini" / "plugins" / "marketplace.json"
    antigravity = _load_json(antigravity_path, errors)
    if isinstance(antigravity, dict):
        plugins = antigravity.get("plugins")
        if antigravity.get("name") != CATALOG_NAME or not isinstance(plugins, list) or len(plugins) != len(skills_by_plugin()):
            errors.append(f"{antigravity_path.relative_to(ROOT)}: malformed plugin marketplace")
        else:
            for entry in plugins:
                if not isinstance(entry, dict):
                    errors.append(f"{antigravity_path.relative_to(ROOT)}: malformed Antigravity plugin entry")
                    continue
                plugin = entry.get("name")
                expected_source = {"source": "local", "path": f"./plugins/antigravity/{plugin}"}
                if plugin not in skills_by_plugin() or entry.get("version") != VERSION or entry.get("source") != expected_source:
                    errors.append(f"{antigravity_path.relative_to(ROOT)}: Antigravity plugin name, version, or source is incorrect")


def validate_packages(errors: list[str]) -> None:
    package_root = ROOT / "dist" / "claude-ai"
    expected_names = {f"{skill}-{VERSION}.zip" for skill in SKILLS}
    actual_names = {path.name for path in package_root.glob("*.zip")} if package_root.is_dir() else set()
    if actual_names != expected_names:
        errors.append(f"dist/claude-ai: expected archives {sorted(expected_names)}, found {sorted(actual_names)}")
    checksum_path = package_root / "SHA256SUMS"
    checksums: dict[str, str] = {}
    if checksum_path.is_file():
        for line in checksum_path.read_text(encoding="utf-8").splitlines():
            parts = line.split(maxsplit=1)
            if len(parts) == 2:
                checksums[parts[1].strip()] = parts[0]
    else:
        errors.append("dist/claude-ai/SHA256SUMS: missing")
    for skill in SKILLS:
        archive_path = package_root / f"{skill}-{VERSION}.zip"
        if not archive_path.is_file():
            continue
        digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
        if checksums.get(archive_path.name) != digest:
            errors.append(f"dist/claude-ai/SHA256SUMS: digest mismatch for {archive_path.name}")
        with zipfile.ZipFile(archive_path) as archive:
            names = archive.namelist()
            if f"{skill}/SKILL.md" not in names:
                errors.append(f"{archive_path.name}: missing nested {skill}/SKILL.md")
            for name in names:
                archive_parts = PurePosixPath(name).parts
                if not archive_parts or archive_parts[0] != skill or ".." in archive_parts or name.startswith("/"):
                    errors.append(f"{archive_path.name}: unsafe or incorrectly nested entry {name}")
                if "/agents/" in f"/{name}":
                    errors.append(f"{archive_path.name}: Claude.ai package contains Codex interface {name}")


def _git_output(root: Path, arguments: list[str]) -> bytes:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise ValueError(detail or f"git {' '.join(arguments)} failed")
    return completed.stdout


def _source_artifact_digest(root: Path, source_commit: str, relative: str, kind: str) -> str:
    if not relative or relative.startswith("/") or ".." in PurePosixPath(relative).parts:
        raise ValueError("artifact path must be a repository-relative path")
    object_name = f"{source_commit}:{relative}"
    object_type = _git_output(root, ["cat-file", "-t", object_name]).decode("utf-8").strip()
    if kind != "tree":
        if object_type != "blob":
            raise ValueError(f"source artifact {relative} must be a blob")
        return hashlib.sha256(_git_output(root, ["cat-file", "blob", object_name])).hexdigest()
    if object_type != "tree":
        raise ValueError(f"source artifact {relative} must be a tree")
    listing = _git_output(root, ["ls-tree", "-r", "-z", source_commit, "--", relative])
    prefix = f"{relative.rstrip('/')}/".encode("utf-8")
    hashes: dict[str, str] = {}
    for record in listing.split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        _, entry_type, object_id = metadata.split()
        if entry_type != b"blob" or not raw_path.startswith(prefix):
            raise ValueError(f"source tree {relative} has an unexpected entry")
        child = raw_path[len(prefix):].decode("utf-8")
        hashes[child] = hashlib.sha256(
            _git_output(root, ["cat-file", "blob", object_id.decode("ascii")])
        ).hexdigest()
    rendered = json.dumps(hashes, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(rendered.encode("utf-8")).hexdigest()


def release_manifest_source_errors(document: dict[str, object], root: Path = ROOT) -> list[str]:
    """Return source-history and source-byte errors for a release manifest."""

    source_commit = document.get("source_commit")
    if not isinstance(source_commit, str):
        return ["source commit is missing or malformed"]
    try:
        _git_output(root, ["cat-file", "-e", f"{source_commit}^{{commit}}"])
    except ValueError as error:
        return [f"source commit is unavailable: {error}"]
    try:
        _git_output(root, ["merge-base", "--is-ancestor", source_commit, "HEAD"])
    except ValueError:
        return ["source commit is not an ancestor of the submitted HEAD"]

    artifacts = document.get("artifacts")
    if not isinstance(artifacts, list):
        return ["artifacts must be a list"]
    errors: list[str] = []
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            continue
        relative = artifact.get("path")
        kind = artifact.get("kind")
        expected = artifact.get("sha256")
        if not isinstance(relative, str) or not isinstance(kind, str) or not isinstance(expected, str):
            continue
        try:
            source_digest = _source_artifact_digest(root, source_commit, relative, kind)
        except ValueError as error:
            errors.append(f"source artifact {relative} is unavailable or invalid: {error}")
            continue
        if source_digest != expected:
            errors.append(f"source checksum drift for {relative}")
    return errors


def release_manifest_current_errors(document: dict[str, object], root: Path = ROOT) -> list[str]:
    """Return current-tree byte errors for a release manifest."""

    artifacts = document.get("artifacts")
    if not isinstance(artifacts, list):
        return ["artifacts must be a list"]
    errors: list[str] = []
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            continue
        relative = artifact.get("path")
        kind = artifact.get("kind")
        expected = artifact.get("sha256")
        if not isinstance(relative, str) or not isinstance(kind, str) or not isinstance(expected, str):
            continue
        if not relative or relative.startswith("/") or ".." in PurePosixPath(relative).parts:
            errors.append(f"current artifact {relative} has an invalid path")
            continue
        path = root / relative
        if kind == "tree":
            if not path.is_dir():
                errors.append(f"missing artifact {relative}")
                continue
            from cataloglib import directory_hashes

            rendered = json.dumps(directory_hashes(path), sort_keys=True, separators=(",", ":"))
            digest = hashlib.sha256(rendered.encode("utf-8")).hexdigest()
        elif path.is_file():
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
        else:
            errors.append(f"missing artifact {relative}")
            continue
        if expected != digest:
            errors.append(f"current checksum drift for {relative}")
    return errors


def validate_release_manifest(errors: list[str]) -> None:
    manifest = ROOT / "releases" / VERSION / "manifest.json"
    if not manifest.is_file():
        errors.append(f"releases/{VERSION}/manifest.json: missing current release manifest")
        return
    document = _validate_json_schema(manifest, ROOT / "releases" / "manifest-schema.json", errors)
    if not isinstance(document, dict):
        return
    if document.get("catalog_version") != VERSION:
        errors.append(f"{manifest.relative_to(ROOT)}: catalog version does not match {VERSION}")
    for error in release_manifest_source_errors(document):
        errors.append(f"{manifest.relative_to(ROOT)}: {error}")
    for error in release_manifest_current_errors(document):
        errors.append(f"{manifest.relative_to(ROOT)}: {error}")


def validate_all(require_packages: bool = True) -> list[str]:
    errors: list[str] = []
    validate_workflows(errors)
    validate_ci_tools(errors)
    validate_canonical(errors)
    validate_evals(errors)
    validate_provenance(errors)
    validate_auxiliary_records(errors)
    validate_current_client_evidence(errors)
    validate_generated_adapters(errors)
    validate_marketplaces(errors)
    if require_packages:
        validate_packages(errors)
        validate_release_manifest(errors)
    return errors


def main() -> int:
    errors = validate_all()
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print(f"Catalog validation passed for {len(SKILLS)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
