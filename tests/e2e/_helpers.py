"""Shared helpers for end-to-end tests."""

from __future__ import annotations

import subprocess
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


E2E_TIMEOUT = 120  # seconds; cargo build can be slow on first run


def cargo_check(project_dir: Path) -> None:
    """Run cargo check in the generated project."""
    result = subprocess.run(
        ['cargo', 'check'],
        cwd=str(project_dir),
        capture_output=True,
        text=True,
        timeout=E2E_TIMEOUT,
    )
    assert result.returncode == 0, f'cargo check failed:\n{result.stderr}\n{result.stdout}'


def cargo_fmt_check(project_dir: Path) -> None:
    """Run cargo fmt --check in the generated project."""
    result = subprocess.run(
        ['cargo', 'fmt', '--all', '--', '--check'],
        cwd=str(project_dir),
        capture_output=True,
        text=True,
        timeout=E2E_TIMEOUT,
    )
    assert result.returncode == 0, f'cargo fmt check failed:\n{result.stderr}\n{result.stdout}'


def cargo_clippy(project_dir: Path) -> None:
    """Run cargo clippy in the generated project."""
    result = subprocess.run(
        ['cargo', 'clippy', '--all-targets', '--', '-D', 'warnings'],
        cwd=str(project_dir),
        capture_output=True,
        text=True,
        timeout=E2E_TIMEOUT,
    )
    assert result.returncode == 0, f'cargo clippy failed:\n{result.stderr}\n{result.stdout}'


def cargo_test(project_dir: Path) -> None:
    """Run cargo test in the generated project."""
    result = subprocess.run(
        ['cargo', 'test'],
        cwd=str(project_dir),
        capture_output=True,
        text=True,
        timeout=E2E_TIMEOUT,
    )
    assert result.returncode == 0, f'cargo test failed:\n{result.stderr}\n{result.stdout}'
