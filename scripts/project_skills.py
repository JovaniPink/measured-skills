#!/usr/bin/env python3
"""Compare or generate owned project skills from an exact local source commit."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile
from typing import Any

MANIFEST = "docs/skills/project.json"
RECEIPT = "docs/skills/generated.json"
ROOTS = (".agents/skills", ".codex/skills", ".claude/skills")


def sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def safe_path(root: Path, relative: str) -> Path:
    parts = PurePosixPath(relative).parts
    if not parts or relative != PurePosixPath(relative).as_posix() or any(p in {".", ".."} for p in parts) or PurePosixPath(relative).is_absolute() or "\\" in relative:
        raise ValueError(f"unsafe relative path: {relative}")
    target = root
    for part in parts:
        target = target / part
        if target.is_symlink() or (target.exists() and not ((target.is_file() or target.is_dir()) if target == root / relative else target.is_dir())):
            raise ValueError(f"unsafe path component: {target}")
    return target


def git(root: Path, *args: str) -> bytes:
    result = subprocess.run(["git", *args], cwd=root, capture_output=True, check=False)
    if result.returncode:
        raise ValueError(result.stderr.decode(errors="replace").strip())
    return result.stdout


def scalar(text: str, key: str) -> str:
    match = re.search(rf"(?m)^\s*{re.escape(key)}:\s*(.+?)\s*$", text)
    if not match:
        raise ValueError(f"missing skill field: {key}")
    return match[1].strip('"\'')


def manifest(root: Path) -> tuple[dict[str, Any], bytes, bytes]:
    payload = safe_path(root, MANIFEST).read_bytes()
    data = json.loads(payload)
    if not isinstance(data, dict) or set(data) != {"format_version", "source_commit", "prefix", "contract", "skills", "codex_version"} or data["format_version"] != 1:
        raise ValueError("unsupported project manifest")
    for key, pattern in (("source_commit", r"[0-9a-f]{40}"), ("prefix", r"[a-z0-9]+(?:-[a-z0-9]+)*")):
        if not isinstance(data[key], str) or not re.fullmatch(pattern, data[key]):
            raise ValueError(f"invalid {key}")
    if data["codex_version"] != "0.154.0":
        raise ValueError("Codex discovery requires qualified version 0.154.0")
    skills = data["skills"]
    if not isinstance(skills, list) or any(not isinstance(s, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", s) for s in skills) or len(skills) != len(set(skills)):
        raise ValueError("invalid or duplicate selected skills")
    if not isinstance(data["contract"], str) or not re.fullmatch(r"docs/skills/[a-zA-Z0-9_-]+\.md", data["contract"]):
        raise ValueError("contract must be Markdown under docs/skills")
    return data, payload, safe_path(root, data["contract"]).read_bytes()


def source_files(source: Path, revision: str, skill: str) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    prefix = f"skills/{skill}/"
    for row in git(source, "ls-tree", "-rz", revision, "--", prefix).split(b"\0"):
        if not row:
            continue
        header, name = row.split(b"\t", 1)
        if not header.startswith(b"100644 blob "):
            raise ValueError("source skills permit regular non-executable files only")
        path = name.decode()
        relative = path.removeprefix(prefix)
        if relative not in {"SKILL.md", "agents/openai.yaml"} and not (relative.startswith("references/") and Path(relative).suffix in {".md", ".json", ".txt"}):
            raise ValueError(f"unexpected source payload: {path}")
        files[relative] = git(source, "show", f"{revision}:{path}")
    if not {"SKILL.md", "agents/openai.yaml"} <= files.keys() or "references/project-contract.md" in files:
        raise ValueError(f"incomplete skill or reserved reference collision: {skill}")
    return files


def render(source: Path, root: Path) -> tuple[dict[str, bytes], dict[str, Any]]:
    data, payload, contract = manifest(root)
    revision = data["source_commit"]
    if git(source, "rev-parse", "HEAD").decode().strip() != revision:
        raise ValueError("source checkout HEAD differs from full manifest pin")
    registry = json.loads(git(source, "show", f"{revision}:catalog/revocations.json"))
    revoked = {row.get("skill") for row in registry["entries"] if row.get("skill")}
    revoked_plugins = {row.get("plugin") for row in registry["entries"] if row.get("plugin")}
    expected: dict[str, bytes] = {}
    records = []
    for skill in sorted(data["skills"]):
        files = source_files(source, revision, skill)
        text = files["SKILL.md"].decode()
        if skill in revoked or (revoked_plugins and scalar(text, "plugin") in revoked_plugins):
            continue
        invocation = scalar(text, "invocation")
        if invocation not in {"explicit", "implicit"} or (invocation == "implicit" and scalar(text, "risk_class") != "read-only"):
            raise ValueError("shared discovery permits read-only implicit skills only")
        alias = data["prefix"] + "-" + skill
        if len(alias) > 64:
            raise ValueError("project alias exceeds 64 characters")
        text = re.sub(r"(?m)^name: .+$", f"name: {alias}", text, count=1)
        text += "\n## Project contract\n\nRead [the project contract](references/project-contract.md) before applying this workflow. Recheck repository settings; report stale contracts as Blocked. User instructions and repository authority remain controlling.\n"
        paths = []
        for native in [".codex/skills" if invocation == "explicit" else ".agents/skills", ".claude/skills"]:
            base = f"{native}/{alias}"
            paths.append(base)
            for relative, value in files.items():
                if relative == "agents/openai.yaml":
                    if native == ".claude/skills":
                        continue
                    value = value.replace(f"${skill}".encode(), f"${alias}".encode())
                    if invocation == "explicit" and b"allow_implicit_invocation: false" not in value:
                        raise ValueError("explicit Codex source lacks native control")
                elif relative == "SKILL.md":
                    adapted = text.replace("---\n", "---\ndisable-model-invocation: true\n", 1) if native == ".claude/skills" and invocation == "explicit" else text
                    value = adapted.encode()
                expected[f"{base}/{relative}"] = value
            expected[f"{base}/references/project-contract.md"] = contract
        records.append({"skill": skill, "alias": alias, "invocation": invocation, "paths": paths})
    receipt = {"format_version": 1, "owner": "measured-project-skills", "prefix": data["prefix"], "source_commit": revision, "manifest_sha256": sha(payload), "contract_sha256": sha(contract), "codex_version": data["codex_version"], "skills": records, "files": {k: sha(v) for k, v in sorted(expected.items())}}
    return expected, receipt


def owned(root: Path, prefix: str) -> dict[str, str]:
    path = safe_path(root, RECEIPT)
    if not path.exists():
        return {}
    data = json.loads(path.read_bytes())
    if data.get("format_version") != 1 or data.get("owner") != "measured-project-skills" or data.get("prefix") != prefix or not isinstance(data.get("files"), dict):
        raise ValueError("invalid ownership receipt")
    for relative, digest in data["files"].items():
        safe_path(root, relative)
        parts = PurePosixPath(relative).parts
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest) or len(parts) < 4 or "/".join(parts[:2]) not in ROOTS or not parts[2].startswith(prefix + "-") or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", parts[2]):
            raise ValueError("invalid owned path or digest")
        tail = "/".join(parts[3:])
        if tail not in {"SKILL.md", "agents/openai.yaml"} and not (tail.startswith("references/") and Path(tail).suffix in {".md", ".json", ".txt"}):
            raise ValueError("unexpected owned payload")
    return dict(data["files"])


def project(source: Path, root: Path, check: bool) -> list[str]:
    if source.is_symlink() or root.is_symlink() or not source.is_dir() or not root.is_dir():
        raise ValueError("roots must be existing real directories")
    expected, receipt = render(source, root)
    previous = owned(root, receipt["prefix"])
    bases = {"/".join(PurePosixPath(p).parts[:3]) for p in expected.keys() | previous.keys()}
    for native in ROOTS:
        safe_path(root, native + "/.probe")
    for base in bases:
        directory = safe_path(root, base + "/SKILL.md").parent
        if directory.exists():
            for item in directory.rglob("*"):
                relative = item.relative_to(root).as_posix()
                safe_path(root, relative)
                if item.is_dir():
                    continue
                if relative not in previous:
                    raise ValueError(f"unowned destination collision: {relative}")
                if not check and sha(item.read_bytes()) != previous[relative]:
                    raise ValueError(f"owned file edited outside generator: {relative}")
    errors = [f"projection drift: {p}" for p, value in expected.items() if not safe_path(root, p).is_file() or safe_path(root, p).read_bytes() != value]
    errors.extend(f"obsolete projection: {p}" for p in previous.keys() - expected.keys() if safe_path(root, p).exists())
    payload = (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode()
    receipt_path = safe_path(root, RECEIPT)
    if not receipt_path.is_file() or receipt_path.read_bytes() != payload:
        errors.append("projection receipt drift")
    if check:
        return errors
    writes = dict(expected)
    writes[RECEIPT] = payload
    backups = {p: safe_path(root, p).read_bytes() if safe_path(root, p).is_file() else None for p in set(writes) | set(previous)}
    created_dirs: set[Path] = set()
    with tempfile.TemporaryDirectory(prefix=".skill-projection-", dir=root) as tmp:
        try:
            for index, (relative, value) in enumerate(sorted(writes.items())):
                target = safe_path(root, relative)
                parent = target.parent
                while not parent.exists():
                    created_dirs.add(parent)
                    parent = parent.parent
                target.parent.mkdir(parents=True, exist_ok=True)
                stage = Path(tmp) / str(index)
                stage.write_bytes(value)
                os.replace(stage, target)
            for relative in previous.keys() - expected.keys():
                safe_path(root, relative).unlink(missing_ok=True)
        except BaseException:
            for relative, previous_value in backups.items():
                target = safe_path(root, relative)
                if previous_value is None:
                    target.unlink(missing_ok=True)
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(previous_value)
            for directory in sorted(created_dirs, key=lambda p: len(p.parts), reverse=True):
                if directory.exists() and not any(directory.iterdir()):
                    directory.rmdir()
            raise
    for base in bases:
        directory = root / base
        if directory.exists():
            for child in sorted(directory.rglob("*"), key=lambda p: len(p.parts), reverse=True):
                if child.is_dir() and not any(child.iterdir()):
                    child.rmdir()
            if not any(directory.iterdir()):
                directory.rmdir()
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        errors = project(args.source_root, args.project_root, args.check)
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"BLOCKED: {error}")
        return 1
    if errors:
        print("\n".join(errors))
        return 1
    print("Project skill bytes match the pinned source and contract." if args.check else "Generated owned project skills; behavioral qualification pending.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
