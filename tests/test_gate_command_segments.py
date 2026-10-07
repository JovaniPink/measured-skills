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
            "terraform fmt -l",
            "terraform fmt -diff",
            "rustfmt -l",
            "gofmt -w -l .",
        ):
            with self.subTest(command=command):
                self.assertTrue(gates.is_mutating_command(command))
        for command in (
            "terraform fmt --check",
            "terraform fmt -write=false",
            "terraform fmt -check -recursive",
            "cargo fmt -- --check",
            "rustfmt --check src.rs",
            "gofmt -l .",
            "gofmt -d .",
        ):
            with self.subTest(command=command):
                self.assertFalse(gates.is_mutating_command(command))

    def test_terraform_effective_boolean_options(self) -> None:
        for command in (
            "terraform fmt -check -check=false",
            "terraform fmt -check --check=false",
            "terraform fmt -write=false --write=true",
            "terraform fmt main.tf -check",
            "terraform fmt 'a file.tf' --check",
            "terraform fmt -write=false -unknown",
            "terraform fmt -check=invalid",
            "terraform fmt -check false",
            "terraform fmt -- -check",
            "terraform fmt ---check",
        ):
            with self.subTest(command=command):
                self.assertTrue(gates.is_mutating_command(command))
        for command in (
            "terraform fmt -check=true",
            "terraform fmt -check=false --check",
            "terraform fmt -write=true --write=false",
            "terraform fmt --check -write=true",
            "terraform fmt -write=false -check=false",
            "terraform fmt -check -list=false -diff -recursive -no-color",
            "terraform fmt -write=false -- '-check'",
        ):
            with self.subTest(command=command):
                self.assertFalse(gates.is_mutating_command(command))
        for value in ("1", "t", "T", "true", "TRUE", "True"):
            self.assertFalse(
                gates.is_mutating_command(f"terraform fmt --check={value}")
            )
        for value in ("0", "f", "F", "false", "FALSE", "False"):
            self.assertTrue(gates.is_mutating_command(f"terraform fmt -check={value}"))
            self.assertFalse(
                gates.is_mutating_command(f"terraform fmt --write={value}")
            )

    def test_terraform_disabled_check_cannot_hide_a_compound_mutation(self) -> None:
        mutating = "terraform fmt -check -check=false"
        safe = "terraform fmt --check=true"
        for separator in (" && ", " || ", "; ", " | ", "\n"):
            for command in (mutating + separator + safe, safe + separator + mutating):
                with self.subTest(command=command):
                    self.assertTrue(gates.is_mutating_command(command))

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
