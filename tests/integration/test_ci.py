"""Integration tests for CI workflow generation."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest_copie.plugin import Result


def test_ci_workflow_generated(default_result: Result) -> None:
    """Test CI workflow contains expected Rust jobs."""
    assert default_result.project_dir is not None

    ci = (default_result.project_dir / '.github' / 'workflows' / 'ci.yml').read_text()
    assert 'cargo fmt --all -- --check' in ci
    assert 'cargo clippy --all-targets -- -D warnings' in ci
    assert 'cargo test' in ci
    assert 'dtolnay/rust-toolchain@stable' in ci
