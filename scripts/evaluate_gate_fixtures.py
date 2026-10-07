#!/usr/bin/env python3
"""Validate representative cross-stack gate-discovery fixtures without mutation."""

from __future__ import annotations

import json
import shlex

from cataloglib import ROOT


def _segments(command: str) -> list[list[str]]:
    """Tokenize a bounded shell subset without expanding or executing anything."""
    segments: list[list[str]] = []
    buffer: list[str] = []
    quote = ""
    index = 0
    needs_operand = False

    def flush(required: bool) -> None:
        nonlocal needs_operand
        text = "".join(buffer).strip()
        buffer.clear()
        if text:
            segments.append(shlex.split(text, comments=False, posix=True))
            needs_operand = False
        elif required:
            raise ValueError("empty executable segment")

    while index < len(command):
        char = command[index]
        if char == "\\" and quote != "'":
            if index + 1 == len(command):
                raise ValueError("unfinished escape")
            if command[index + 1] != "\n":
                buffer.extend((char, command[index + 1]))
            index += 2
            continue
        if char in "\"'":
            if not quote:
                quote = char
            elif quote == char:
                quote = ""
            buffer.append(char)
        elif quote == "'":
            buffer.append(char)
        elif char in "`$":
            raise ValueError("expansion is outside the bounded grammar")
        elif quote:
            buffer.append(char)
        elif char == "#" and (not buffer or buffer[-1].isspace()):
            while index < len(command) and command[index] != "\n":
                index += 1
            continue
        elif char in "<>(){}":
            raise ValueError("redirection or grouping is unsupported")
        elif char in ";|&\n":
            if char == "\n":
                flush(False)
            else:
                flush(True)
                if (
                    char in "|&"
                    and index + 1 < len(command)
                    and command[index + 1] == char
                ):
                    index += 1
                elif char == "&":
                    raise ValueError("background execution is unsupported")
                needs_operand = char in "|&"
        else:
            buffer.append(char)
        index += 1
    if quote:
        raise ValueError("unfinished quote")
    flush(False)
    if needs_operand or not segments:
        raise ValueError("unfinished executable sequence")
    return segments


def _option_tokens(args: list[str]) -> list[str]:
    """Stop interpreting options at the executable's end-of-options marker."""
    return args[: args.index("--")] if "--" in args else args


def _mutating_segment(argv: list[str]) -> bool:
    tool = argv[0].rsplit("/", 1)[-1]
    args = argv[1:]
    if tool in {"apply", "update"}:
        return True
    if (
        tool
        in {
            "if",
            "then",
            "else",
            "elif",
            "fi",
            "for",
            "while",
            "until",
            "do",
            "done",
            "case",
            "esac",
            "select",
            "time",
            "coproc",
            "!",
            "dash",
            "ksh",
            "nohup",
            "env",
            "sudo",
            "sh",
            "bash",
            "zsh",
            "fish",
            "cmd",
            "powershell",
            "eval",
            "source",
            ".",
            "exec",
            "command",
            "xargs",
        }
        or "=" in argv[0]
    ):
        return True
    if tool in {"echo", "printf"}:
        return False
    if tool == "terraform" and args[:1] == ["fmt"]:
        flags = _option_tokens(args[1:])
        return any(
            flag.startswith("-write=") and flag != "-write=false" for flag in flags
        ) or not ("-check" in flags or "-write=false" in flags)
    if tool == "cargo" and args[:1] == ["fmt"]:
        flags = args[1:]
        # Cargo forwards options after its first separator to rustfmt.
        if "--" in flags:
            split = flags.index("--")
            flags = flags[:split] + _option_tokens(flags[split + 1 :])
        return "--check" not in flags
    if tool == "rustfmt":
        return "--check" not in _option_tokens(args)
    if tool == "gofmt":
        flags = _option_tokens(args)
        return any(flag == "-w" or flag.startswith("-w=") for flag in flags) or not any(
            flag in flags for flag in ("-l", "-d")
        )
    if tool == "go" and (
        args[:1] in (["generate"], ["fmt"], ["get"]) or args[:2] == ["mod", "tidy"]
    ):
        return True
    if tool in {"npm", "pnpm", "yarn", "pip", "pip3", "uv", "poetry", "cargo"} and any(
        arg in {"install", "add", "upgrade", "remove", "update"} for arg in args
    ):
        return True
    if tool == "python" or tool.startswith("python3"):
        if args[:1] == ["-c"] or args[:2] == ["-m", "pip"]:
            return True
    return (
        any(
            arg in {"apply", "update", "-u", "-U", "--fix", "--write", "-w"}
            for arg in args
        )
        or "fmt" in args
    )


def is_mutating_command(command: str) -> bool:
    """Flag mutation or unsupported syntax, not certify arbitrary shell safety.

    False means no tracked-source/dependency mutation was detected in this bounded
    inspection. Package scripts and unknown executables still require review.
    """
    try:
        return any(_mutating_segment(argv) for argv in _segments(command))
    except (ValueError, IndexError):
        return True


def evaluate() -> list[str]:
    errors: list[str] = []
    document = json.loads(
        (ROOT / "evals" / "quality-gate-fixtures.json").read_text(encoding="utf-8")
    )
    fixtures = document.get("fixtures", [])
    stacks = {fixture.get("stack") for fixture in fixtures}
    expected = {"Go", "Python", "Swift", "TypeScript/JavaScript", "SQL", "Terraform"}
    if stacks != expected:
        errors.append(
            f"fixture stacks must be {sorted(expected)}, found {sorted(stacks)}"
        )
    command_sets: set[tuple[str, ...]] = set()
    for fixture in fixtures:
        path = ROOT / fixture["path"]
        missing = [
            signal
            for signal in fixture.get("signals", [])
            if not (path / signal).is_file()
        ]
        if missing:
            errors.append(f"{fixture['stack']}: missing discovery signals {missing}")
        candidates = fixture.get("safe_candidates", [])
        command_sets.add(tuple(candidates))
        for command in candidates:
            if is_mutating_command(command):
                errors.append(
                    f"{fixture['stack']}: mutating candidate is not a validation gate: {command}"
                )
        if not candidates and fixture.get("expected_status") != "INCOMPLETE":
            errors.append(f"{fixture['stack']}: no candidates must produce INCOMPLETE")
        for command in fixture.get("forbidden", []):
            if not is_mutating_command(command):
                errors.append(
                    f"{fixture['stack']}: unsafe near miss was not rejected: {command}"
                )
        if not fixture.get("forbidden"):
            errors.append(
                f"{fixture['stack']}: fixture must name at least one unsafe near miss"
            )
        if not fixture.get("judgment_failure"):
            errors.append(
                f"{fixture['stack']}: fixture must name a stack-specific judgment failure"
            )
        if fixture.get("stack") == "Swift":
            observation = fixture.get("observed_macos")
            if not isinstance(observation, dict) or observation.get("result") not in {
                "pass",
                "fail",
                "blocked",
            }:
                errors.append(
                    "Swift: fixture must record a terminal observed macOS result"
                )
    if len(command_sets) != len(fixtures):
        errors.append(
            "fixtures must not collapse stacks into one universal command set"
        )
    return errors


def main() -> int:
    errors = evaluate()
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print(
        "Cross-stack gate fixture evaluation passed without running mutating commands."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
