from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import evaluate_gate_fixtures as gates


class GateSegmentTests(unittest.TestCase):
    def test_check_flag_does_not_hide_other_segment(self) -> None:
        for separator in (" && ", " || ", "; ", " | ", "\n"):
            for first, second in (
                ("terraform fmt", "terraform fmt -check"),
                ("cargo fmt", "cargo fmt --check"),
            ):
                for command in (first + separator + second, second + separator + first):
                    with self.subTest(command=command):
                        self.assertTrue(gates.is_mutating_command(command))

    def test_flags_belong_to_their_tool(self) -> None:
        for command in (
            "terraform fmt -- -check",
            "rustfmt -- --check",
            "cargo fmt -- -- --check",
            "gofmt -- -l",
            "gofmt -l -w=true",
            "cargo fmt -l",
            "cargo fmt -d",
            "terraform fmt --check",
            "terraform fmt -l",
            "terraform fmt -diff",
            "rustfmt -l",
            "gofmt -w -l .",
        ):
            with self.subTest(command=command):
                self.assertTrue(gates.is_mutating_command(command))
        for command in (
            "terraform fmt -write=false",
            "terraform fmt -check -recursive",
            "cargo fmt -- --check",
            "rustfmt --check src.rs",
            "gofmt -l .",
            "gofmt -d .",
        ):
            with self.subTest(command=command):
                self.assertFalse(gates.is_mutating_command(command))

    def test_comments_cannot_supply_a_flag(self) -> None:
        self.assertTrue(gates.is_mutating_command("terraform fmt # -check"))
        self.assertTrue(gates.is_mutating_command("cargo fmt # --check"))
        self.assertTrue(
            gates.is_mutating_command("echo ok # cargo fmt --check\nterraform fmt")
        )
        self.assertFalse(
            gates.is_mutating_command("terraform fmt -check # formatter check")
        )

    def test_quoted_literals_are_not_commands(self) -> None:
        for command in (
            'echo "terraform fmt && cargo fmt"',
            "echo 'terraform fmt # -check'",
            'printf "%s" "cargo fmt; cargo fmt --check"',
            'echo "--write"',
            "echo apply",
            'echo "a\\"; terraform fmt"',
        ):
            with self.subTest(command=command):
                self.assertFalse(gates.is_mutating_command(command))

    def test_unsupported_constructs_are_rejected(self) -> None:
        for command in (
            "if true; then echo safe; fi",
            "while false; do echo safe; done",
            "! echo safe",
            "time echo safe",
            "dash -c 'echo safe'",
            "ksh -c 'echo safe'",
            "apply migration",
            "update dependencies",
            "python3 -c 'print(1)'",
            "echo $(terraform fmt)",
            "echo `cargo fmt`",
            'sh -c "terraform fmt -check"',
            'bash -c "echo ok"',
            "terraform fmt -check > out",
            "terraform fmt -check 2>>out",
            "cat < input",
            "(cargo fmt --check)",
            "env cargo fmt --check",
            "X=1 cargo fmt --check",
            'echo "unfinished',
            "echo ok &",
            "echo ok &&",
            "; echo ok",
            'echo "$(cargo fmt)"',
            "terraform fmt -write=false -write=true",
        ):
            with self.subTest(command=command):
                self.assertTrue(gates.is_mutating_command(command))

    def test_escaped_operators_remain_arguments(self) -> None:
        self.assertFalse(gates.is_mutating_command(r"echo \; cargo fmt"))
        self.assertFalse(gates.is_mutating_command("terraform fmt \\\n-check"))

    def test_forbidden_fixture_is_checked(self) -> None:
        real = gates.is_mutating_command
        with patch.object(
            gates,
            "is_mutating_command",
            side_effect=lambda value: False if value == "go get -u" else real(value),
        ):
            self.assertTrue(
                any("unsafe near miss" in error for error in gates.evaluate())
            )
