"""End-to-end test for a generated Rust project."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ._helpers import cargo_check, cargo_clippy, cargo_fmt_check, cargo_test

if TYPE_CHECKING:
    from pytest_copie.plugin import Copie


def test_e2e_rust_project(
    copie: Copie,
    default_answers: dict[str, Any],
) -> None:
    """The generated Rust project builds, lints, formats, and passes its tests."""
    result = copie.copy(extra_answers=default_answers)

    assert result.exit_code == 0
    assert result.project_dir is not None

    cargo_check(result.project_dir)
    cargo_fmt_check(result.project_dir)
    cargo_clippy(result.project_dir)
    cargo_test(result.project_dir)
