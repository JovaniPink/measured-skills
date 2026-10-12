"""Run original compile probes and inventory installed Swift SDK interfaces.

This developer tool has no network, installation, simulator reset, or skill payload.
An expected compiler error passes only when its diagnostic matches. Runtime evidence
belongs to the separate fixture app; typechecking never qualifies a user journey.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "evals/swift-evidence-v1/cases.json"
INFRASTRUCTURE = (
    "sandbox_apply", "external macro implementation type", "unable to find utility",
    "SDK does not contain", "unable to load standard library", "license agreements",
    "unable to execute command", "unable to open output file", "error opening input file",
)


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def classify(expected: str, patterns: list[str], code: int, diagnostics: str) -> str:
    if any(fragment in diagnostics for fragment in INFRASTRUCTURE):
        return "blocked"
    matches = all(re.search(pattern, diagnostics) for pattern in patterns)
    if expected == "success":
        return "passed" if code == 0 and "warning:" not in diagnostics and matches else "failed"
    if expected == "warning":
        return "passed" if code == 0 and "warning:" in diagnostics and matches else "failed"
    if expected == "error":
        return "passed" if code != 0 and "error:" in diagnostics and matches else "failed"
    raise ValueError("unknown expectation")


def load_cases(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text())
    if not isinstance(data, dict) or set(data) != {"format_version", "cases"} or data["format_version"] != 1:
        raise ValueError("unsupported evidence manifest")
    rows = data["cases"]
    if not isinstance(rows, list) or not rows:
        raise ValueError("cases must be a nonempty list")
    seen: set[str] = set()
    required = {"id", "source", "expect", "diagnostics", "target", "language", "minimum_sdk", "authority"}
    for row in rows:
        if not isinstance(row, dict) or not required <= set(row) or set(row) - required - {"phase"}:
            raise ValueError("unsupported case fields")
        if not isinstance(row["id"], str) or not re.fullmatch(r"[a-z][a-z0-9-]+", row["id"]) or row["id"] in seen:
            raise ValueError("invalid or duplicate case ID")
        seen.add(row["id"])
        if row["expect"] not in {"success", "warning", "error"} or row["language"] not in {"5", "6"}:
            raise ValueError("invalid expectation or language")
        if any(not isinstance(row[k], str) or not re.fullmatch(r"\d+\.\d+(?:\.\d+)?", row[k]) for k in ("target", "minimum_sdk")):
            raise ValueError("invalid OS version")
        if row.get("phase", "typecheck") not in {"typecheck", "object"}:
            raise ValueError("invalid compiler phase")
        source = row["source"]
        if not isinstance(source, str) or not re.fullmatch(r"[A-Za-z0-9_-]+\.swift", source):
            raise ValueError("source must be a local Swift filename")
        candidate = path.parent / source
        if candidate.is_symlink() or not candidate.is_file():
            raise ValueError("missing or symlinked probe")
        if not isinstance(row["diagnostics"], list) or any(not isinstance(p, str) for p in row["diagnostics"]):
            raise ValueError("diagnostics must contain regular expressions")
        for pattern in row["diagnostics"]:
            re.compile(pattern)
        if row["expect"] != "success" and not row["diagnostics"]:
            raise ValueError("warning and error cases require diagnostic assertions")
        if not isinstance(row["authority"], str) or not row["authority"].startswith(("https://developer.apple.com/", "https://www.swift.org/")):
            raise ValueError("a primary authority is required")
    return rows


def scan_interface(source: str) -> list[dict[str, Any]]:
    """Lexical inventory, not a Swift parser or inherited-availability resolver."""
    rows: list[dict[str, Any]] = []
    attributes: list[str] = []
    accumulating = ""
    declaration = re.compile(r"\b(?:func|var|let|struct|class|enum|protocol|typealias|macro)\s+(`?\w+`?)")
    for number, line in enumerate(source.splitlines(), 1):
        stripped = line.strip()
        if accumulating:
            accumulating += " " + stripped
            if ")" in stripped:
                attributes.append(accumulating)
                accumulating = ""
            continue
        if stripped.startswith("@available("):
            if ")" in stripped:
                attributes.append(stripped)
            else:
                accumulating = stripped
            continue
        if not stripped or stripped.startswith(("//", "@")):
            continue
        match = declaration.search(stripped)
        if match and ("public " in stripped or "open " in stripped):
            ios = [a for a in attributes if re.search(r"\b(?:iOS|anyAppleOS)\b", a)]
            if ios:
                rows.append({"symbol": match.group(1), "line": number, "declaration": stripped,
                             "availability": attributes.copy(),
                             "soft_deprecated": any(re.search(r"deprecated:\s*100000(?:\.0)?\b", a) for a in ios)})
        attributes.clear()
    return rows


def run(command: list[str], env: dict[str, str], timeout: int = 90) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, env=env, capture_output=True, text=True, timeout=timeout, check=False)


def tool_output(command: list[str], env: dict[str, str]) -> str:
    result = run(command, env)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout.strip()


def inventory(sdk: Path, modules: list[str]) -> dict[str, Any]:
    files: list[dict[str, Any]] = []
    seen: set[Path] = set()
    for module in modules:
        folder = sdk / "System/Library/Frameworks" / (module + ".framework/Modules") / (module + ".swiftmodule")
        for path in sorted(folder.glob("*.swiftinterface")):
            if ".private." in path.name or path.resolve() in seen:
                continue
            seen.add(path.resolve())
            payload = path.read_bytes()
            files.append({"module": module, "interface": str(path.relative_to(sdk)), "sha256": digest(payload),
                          "declarations": scan_interface(payload.decode())})
    return {"modules_requested": modules, "files": files,
            "limitations": ["Lexical public Swift declarations with direct iOS/anyAppleOS availability only.",
                            "Does not resolve inherited attributes or conditional compilation; includes unavailable declarations.",
                            "Does not inventory Objective-C headers, binary-only symbols, or private interfaces.",
                            "Architecture-specific declarations remain separate, each interface is scanned once."]}


def execute(args: argparse.Namespace) -> int:
    output = Path(args.output).resolve()
    if output.exists():
        raise ValueError("output must be a new directory; preserve previous receipts")
    rows = load_cases(CASES)
    if args.case:
        known = {row["id"] for row in rows}
        if not set(args.case) <= known:
            raise ValueError("unknown case selector")
        rows = [row for row in rows if row["id"] in args.case]
    env = dict(os.environ, DEVELOPER_DIR=str(Path(args.developer_dir).resolve()))
    output.mkdir(parents=True)
    receipt: dict[str, Any] = {
        "format_version": 1, "observed_at": datetime.now(timezone.utc).isoformat(),
        "manifest_sha256": digest(CASES.read_bytes()), "source_revision": "unknown", "source_dirty": None,
        "evidence_kind": "compile" if args.mode == "compile" else "sdk_inspection",
        "results": [], "limitations": ["No runtime, accessibility, physical-device, or provider acceptance is established."]}
    try:
        receipt["source_revision"] = tool_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], env)
        receipt["source_dirty"] = bool(tool_output(["git", "-C", str(ROOT), "status", "--porcelain"], env))
        receipt["toolchain"] = tool_output(["xcodebuild", "-version"], env)
        receipt["compiler"] = tool_output(["xcrun", "swiftc", "--version"], env)
        sdk = tool_output(["xcrun", "--sdk", "iphonesimulator", "--show-sdk-path"], env)
        sdk_version = tool_output(["xcrun", "--sdk", "iphonesimulator", "--show-sdk-version"], env)
        receipt["sdk"] = {"path": sdk, "version": sdk_version, "platform": "iphonesimulator"}
        if args.mode == "inventory":
            receipt["inventory"] = inventory(Path(sdk), args.module or ["SwiftUI", "SwiftUICore", "Foundation", "Observation", "SwiftData", "MapKit", "HealthKit", "UIKit"])
            receipt["status"] = "passed" if receipt["inventory"]["files"] else "blocked"
        else:
            for row in rows:
                source = CASES.parent / row["source"]
                result: dict[str, Any] = dict(row, source_sha256=digest(source.read_bytes()), reviewed_on="2026-10-12",
                                              destination="iOS Simulator arm64", status="not_run")
                if tuple(map(int, sdk_version.split("."))) < tuple(map(int, row["minimum_sdk"].split("."))):
                    result.update(status="blocked", limitation="Installed SDK is older than this case requires.")
                else:
                    phase = row.get("phase", "typecheck")
                    options = ["-typecheck"] if phase == "typecheck" else ["-c", "-parse-as-library", "-o", str(output / (row["id"] + ".o"))]
                    command = ["xcrun", "swiftc", *options, "-sdk", sdk, "-target", f"arm64-apple-ios{row['target']}-simulator",
                               "-swift-version", row["language"], "-module-cache-path", str(output / "module-cache"), str(source)]
                    result["phase"] = phase
                    result["command"] = command
                    try:
                        completed = run(command, env)
                        diagnostics = completed.stdout + completed.stderr
                        log = row["id"] + ".log"
                        (output / log).write_text(diagnostics)
                        result.update(status=classify(row["expect"], row["diagnostics"], completed.returncode, diagnostics),
                                      exit_code=completed.returncode, diagnostics_artifact=log,
                                      diagnostics_sha256=digest(diagnostics.encode()))
                    except (OSError, subprocess.TimeoutExpired) as error:
                        result.update(status="blocked", limitation=str(error))
                receipt["results"].append(result)
                print(row["id"] + ": " + result["status"], flush=True)
            statuses = {r["status"] for r in receipt["results"]}
            receipt["status"] = "failed" if "failed" in statuses else "blocked" if "blocked" in statuses else "passed"
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as error:
        receipt.update(status="blocked", limitation=str(error))
    (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    return {"passed": 0, "failed": 1, "blocked": 2}[receipt["status"]]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("compile", "inventory"))
    parser.add_argument("--developer-dir", required=True)
    parser.add_argument("--output", required=True, help="New evidence directory, never overwrites a run")
    parser.add_argument("--case", action="append")
    parser.add_argument("--module", action="append")
    args = parser.parse_args()
    try:
        return execute(args)
    except (ValueError, OSError) as error:
        parser.error(str(error))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
