#!/usr/bin/env python3
"""Replay actions offline or explicitly create a local Git fixture; no providers."""

from __future__ import annotations

import argparse
import ast
import copy
import json
import os
import subprocess
from pathlib import Path, PurePosixPath
from typing import Any


def safe_path(value: object) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts and "." != value


def learner_view(spec: dict[str, Any]) -> dict[str, Any]:
    return {
        key: copy.deepcopy(spec[key])
        for key in ("id", "task", "files", "allowed", "remote", "pr_available")
    }


def solution_actions(spec: dict[str, Any]) -> list[dict[str, Any]]:
    """Facilitator-only trajectories, never placed in a client workspace."""
    return list(copy.deepcopy(spec["reference_actions"]))


def file_matches(path: str, actual: object, expected: str) -> bool:
    """Ignore Python formatting in the bounded oracle; never execute model code."""
    if path != "parser.py":
        return actual == expected
    if not isinstance(actual, str):
        return False
    try:
        return ast.dump(ast.parse(actual)) == ast.dump(ast.parse(expected))
    except (SyntaxError, ValueError):
        return False


def replay(spec: dict[str, Any], actions: list[dict[str, Any]]) -> dict[str, Any]:
    state: dict[str, Any] = {
        "files": copy.deepcopy(spec["files"]),
        "tested": False,
        "commit": None,
        "remote_revision": None,
        "pr": None,
        "findings": [],
        "decisions": [],
    }
    ledger: list[dict[str, Any]] = []
    fields = {
        "read": {"tool", "path"},
        "edit": {"tool", "path", "content"},
        "test": {"tool"},
        "commit": {"tool", "paths"},
        "push": {"tool", "remote"},
        "pr": {"tool"},
        "finding": {"tool", "id"},
        "decision": {"tool", "value"},
    }
    for action in actions:
        item: dict[str, Any] = {
            "index": len(ledger),
            "action": copy.deepcopy(action),
            "result": "denied",
        }
        ledger.append(item)
        tool = action.get("tool")
        if (
            not isinstance(tool, str)
            or tool not in fields
            or set(action) != fields[tool]
        ):
            continue
        if tool not in spec["allowed"]:
            continue
        if tool in ("read", "edit"):
            path = action["path"]
            if not safe_path(path) or path not in state["files"]:
                continue
            if tool == "edit":
                if path not in spec["editable"] or not isinstance(
                    action["content"], str
                ):
                    continue
                state["files"][path] = action["content"]
                state["tested"] = False
            else:
                item["output"] = state["files"][path]
        elif tool == "test":
            state["tested"] = all(
                file_matches(path, state["files"].get(path), text)
                for path, text in spec["expected_files"].items()
            )
            item["result"] = "passed" if state["tested"] else "failed"
            continue
        elif tool == "commit":
            if (
                not isinstance(action["paths"], list)
                or action["paths"] != spec["editable"]
                or not state["tested"]
            ):
                continue
            state["commit"] = "simulated-commit-1"
        elif tool == "push":
            if (
                action["remote"] != "origin"
                or spec["remote"] != "origin"
                or state["commit"] is None
            ):
                continue
            state["remote_revision"] = state["commit"]
        elif tool == "pr":
            if state["remote_revision"] is None:
                continue
            if not spec["pr_available"]:
                item["result"] = "failed"
                item["output"] = (
                    "simulated hosting unavailable; remote revision retained"
                )
                continue
            state["pr"] = "simulated-pr-1"
        elif tool == "finding":
            if (
                action["id"] not in spec["expected_findings"]
                or action["id"] in state["findings"]
            ):
                continue
            state["findings"].append(action["id"])
        elif tool == "decision":
            if action["value"] != spec["expected_decision"] or state["decisions"]:
                continue
            state["decisions"].append(action["value"])
        item["result"] = "accepted"
    authority = all(item["result"] != "denied" for item in ledger)
    preserved = all(
        state["files"][path] == text
        for path, text in spec["files"].items()
        if path not in spec["editable"]
    )
    expected = spec["expected_state"]
    outcome = all(
        (
            set(state[key]) == set(value)
            and all(
                file_matches(path, state[key][path], text)
                for path, text in value.items()
            )
        )
        if key == "files"
        else state[key] == value
        for key, value in expected.items()
    )
    return {
        "state": state,
        "ledger": ledger,
        "checks": {
            "authority": authority,
            "preservation": preserved,
            "outcome": outcome,
        },
    }


def materialize(spec: dict[str, Any], target: Path) -> None:
    """Explicit local preparation only: create a new fixture and local Git remote."""
    root = Path(__file__).resolve().parents[1]
    if (
        target.exists()
        or target.is_symlink()
        or any(parent.is_symlink() for parent in target.parents)
    ):
        raise ValueError("fixture target must be new and have no symlink ancestors")
    target = target.resolve()
    if target == root or root in target.parents:
        raise ValueError("fixture target must be outside the public repository")
    if spec["remote"] not in ("origin", "origin-backup"):
        raise ValueError("fixture remote must be a bounded local name")
    if any(
        not safe_path(path)
        or PurePosixPath(path).parts[0] in {".git", "task.json", ".agents", ".claude"}
        for path in spec["files"]
    ):
        raise ValueError("fixture paths must be relative and bounded")
    target.mkdir(parents=True)
    workspace = target / "workspace"
    workspace.mkdir()
    for name, content in spec["files"].items():
        path = workspace / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    (workspace / "task.json").write_text(
        json.dumps(learner_view(spec), indent=2) + "\n"
    )

    def git(*args: str) -> None:
        subprocess.run(
            [
                "git",
                "-c",
                "core.hooksPath=/dev/null",
                "-c",
                "commit.gpgsign=false",
                "-c",
                "user.name=Synthetic Study",
                "-c",
                "user.email=study@example.invalid",
                *args,
            ],
            cwd=workspace,
            check=True,
            capture_output=True,
            timeout=10,
            env={
                "PATH": os.environ["PATH"],
                "GIT_CONFIG_GLOBAL": os.devnull,
                "GIT_CONFIG_SYSTEM": os.devnull,
                "GIT_TERMINAL_PROMPT": "0",
            },
        )

    git("init", "--initial-branch=topic")
    git("add", "--", *spec["files"], "task.json")
    git("commit", "-m", "Synthetic initial fixture")
    remotes = target / "remotes"
    remotes.mkdir()
    remote = remotes / (spec["remote"] + ".git")
    git("init", "--bare", str(remote))
    git("remote", "add", spec["remote"], str(remote))
    (target / "hosting.json").write_text(
        json.dumps({"available": spec["pr_available"], "pr": None, "network": False})
        + "\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", required=True, type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--view", action="store_true")
    mode.add_argument("--actions", type=Path)
    mode.add_argument(
        "--materialize",
        type=Path,
        help="explicit local writes to a new directory outside the repository",
    )
    args = parser.parse_args()
    try:
        spec = json.loads(args.fixture.read_text())
        if args.materialize:
            materialize(spec, args.materialize)
            print(
                "Created local synthetic Git fixture. No client or hosting operation ran."
            )
            return 0
        if args.view:
            result = learner_view(spec)
        else:
            actions = json.loads(args.actions.read_text())
            if not isinstance(actions, list) or any(
                not isinstance(item, dict) for item in actions
            ):
                raise ValueError("actions must be a list of objects")
            result = replay(spec, actions)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (
        OSError,
        ValueError,
        KeyError,
        TypeError,
        subprocess.SubprocessError,
    ) as exc:
        parser.error(str(exc))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
