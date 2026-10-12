"""Build and run the synthetic fixture on an explicitly selected, booted simulator.

No simulator creation/reset, network, developer identity, or product installation.
The caller owns the destination and authorizes installation of this fixture only.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import plistlib
import re
import shutil
import subprocess
import time
from typing import Any

from swift_evidence import ROOT, digest

IDENTIFIER = "org.measured.synthetic.swift-evidence"
SOURCE = ROOT / "evals/swift-evidence-v1/runtime/Fixture.swift"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--developer-dir", required=True)
    parser.add_argument("--destination", required=True, help="UUID of caller-owned booted simulator")
    parser.add_argument("--output", required=True, help="New evidence directory")
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9A-Fa-f-]{36}", args.destination):
        parser.error("destination must be an explicit simulator UUID")
    output = Path(args.output).resolve()
    if output.exists():
        parser.error("output must not exist; retain previous receipts")
    output.mkdir(parents=True)
    env = dict(os.environ, DEVELOPER_DIR=args.developer_dir)
    receipt: dict[str, Any] = {"format_version": 1, "observed_at": datetime.now(timezone.utc).isoformat(),
                               "evidence_kind": "simulator", "destination": args.destination,
                               "source_sha256": digest(SOURCE.read_bytes()), "commands": [], "status": "blocked",
                               "limitations": ["Synthetic fixture; no app, accessibility, device, performance, or provider qualification."]}

    def run(command: list[str], timeout: int = 120) -> str:
        result = subprocess.run(command, env=env, capture_output=True, text=True, timeout=timeout, check=False)
        index = len(receipt["commands"])
        name = f"command-{index}.log"
        (output / name).write_text(result.stdout + result.stderr)
        receipt["commands"].append({"command": command, "exit_code": result.returncode, "log": name})
        if result.returncode:
            raise RuntimeError(f"Command {index} failed; inspect {name}")
        return result.stdout.strip()

    try:
        receipt["toolchain"] = run(["xcodebuild", "-version"])
        receipt["compiler"] = run(["xcrun", "swiftc", "--version"])
        receipt["source_revision"] = run(["git", "-C", str(ROOT), "rev-parse", "HEAD"])
        receipt["source_dirty"] = bool(run(["git", "-C", str(ROOT), "status", "--porcelain"]))
        devices = json.loads(run(["xcrun", "simctl", "list", "devices", "-j"]))["devices"]
        matches = [(runtime, device) for runtime, rows in devices.items() for device in rows if device["udid"] == args.destination]
        if len(matches) != 1 or matches[0][1]["state"] != "Booted":
            raise RuntimeError("Selected destination must already be booted; this runner does not create or boot devices")
        receipt["runtime"], receipt["device"] = matches[0]
        sdk = run(["xcrun", "--sdk", "iphonesimulator", "--show-sdk-path"])
        receipt["sdk_version"] = run(["xcrun", "--sdk", "iphonesimulator", "--show-sdk-version"])
        app = output / "Evidence.app"
        app.mkdir()
        plist = {"CFBundleIdentifier": IDENTIFIER, "CFBundleName": "Swift Evidence", "CFBundleExecutable": "Evidence",
                 "CFBundlePackageType": "APPL", "CFBundleVersion": "1", "CFBundleShortVersionString": "1.0",
                 "MinimumOSVersion": "27.0", "UIDeviceFamily": [1, 2], "UILaunchScreen": {},
                 "UIApplicationSceneManifest": {"UIApplicationSupportsMultipleScenes": True}}
        (app / "Info.plist").write_bytes(plistlib.dumps(plist))
        receipt["deployment_target"] = "27.0"
        receipt["language_mode"] = "6"
        run(["xcrun", "swiftc", "-parse-as-library", "-swift-version", "6", "-sdk", sdk,
             "-target", "arm64-apple-ios27.0-simulator", str(SOURCE), "-o", str(app / "Evidence")])
        run(["codesign", "--force", "--sign", "-", str(app)])
        run(["xcrun", "simctl", "install", args.destination, str(app)])
        container = Path(run(["xcrun", "simctl", "get_app_container", args.destination, IDENTIFIER, "data"]))
        result_file = container / "Documents/runtime-results.json"
        if result_file.exists():
            # Remove only this fixture's stale result, never app or simulator data.
            result_file.unlink()
        run(["xcrun", "simctl", "launch", "--terminate-running-process", args.destination, IDENTIFIER])
        deadline = time.monotonic() + 60
        while not result_file.exists() and time.monotonic() < deadline:
            time.sleep(0.2)
        if not result_file.exists():
            raise RuntimeError("Fixture produced no result within 60 seconds")
        rows = json.loads(result_file.read_text())
        expected = {"state-styling-retains-reference", "state-explicit-identity-recreates", "binding-equal-writes-call-setter",
                    "binding-programmatic-change-bypasses-setter", "draft-edit-does-not-save", "draft-cancel", "draft-explicit-save",
                    "geometry-short-wide", "animation-completion-delivered"}
        if not isinstance(rows, list) or len(rows) != len(expected) or {r["id"] for r in rows} != expected:
            raise RuntimeError("Fixture result inventory is incomplete")
        shutil.copyfile(result_file, output / "runtime-results.json")
        receipt["results"] = rows
        receipt["status"] = "passed" if all(row["status"] == "passed" for row in rows) else "failed"
    except (OSError, RuntimeError, subprocess.TimeoutExpired, ValueError, KeyError) as error:
        receipt["error"] = str(error)
    finally:
        (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"status": receipt["status"], "output": str(output)}))
    return {"passed": 0, "failed": 1, "blocked": 2}[receipt["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
