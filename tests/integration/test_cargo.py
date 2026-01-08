"""Integration tests for Cargo.toml generation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest

if TYPE_CHECKING:
    from pytest_copie.plugin import Result


@pytest.fixture
def cargo_toml(default_result: Result) -> str:
    """Fixture to read the generated Cargo.toml content."""
    assert default_result.project_dir

    cargo_path = default_result.project_dir / 'Cargo.toml'
    assert cargo_path.exists()
    return cargo_path.read_text()


def test_cargo_toml_generated(default_answers: dict[str, Any], cargo_toml: str) -> None:
    """Test that Cargo.toml is generated with correct values."""
    assert '[package]' in cargo_toml
    assert f'name = "{default_answers["project_name"]}"' in cargo_toml
    assert f'version = "{default_answers["project_version"]}"' in cargo_toml
    assert f'description = "{default_answers["project_description"]}"' in cargo_toml
    assert 'edition = "2021"' in cargo_toml
    assert f'license = "{default_answers["copyright_license"]}"' in cargo_toml

    if default_answers['copyright_license'] != 'Unlicense':
        holder = default_answers['copyright_holder_name']
        email = default_answers['copyright_holder_email']
        assert f'authors = ["{holder} <{email}>"]' in cargo_toml
    else:
        assert 'authors' not in cargo_toml

    vcs_github_path = default_answers['vcs_github_path']
    assert f'repository = "https://github.com/{vcs_github_path}"' in cargo_toml
    assert f'homepage = "https://github.com/{vcs_github_path}"' in cargo_toml
    assert f'documentation = "https://github.com/{vcs_github_path}/blob/main/README.md"' in cargo_toml

    assert '[dependencies]' in cargo_toml
    assert 'cargo-husky' in cargo_toml
    assert 'user-hooks' in cargo_toml


def test_cargo_keywords(
    copie: object,
    default_answers: dict[str, Any],
) -> None:
    """Test that Cargo.toml keywords are formatted correctly."""
    answers = default_answers.copy()
    answers['project_keywords'] = 'rust, cli, tool'
    result = copie.copy(extra_answers=answers)  # type: ignore[union-attr]

    assert result.exit_code == 0
    assert result.project_dir is not None

    cargo = (result.project_dir / 'Cargo.toml').read_text()
    assert 'keywords = ["rust", "cli", "tool"]' in cargo


def test_src_lib_rs_generated(default_answers: dict[str, Any], default_result: Result) -> None:
    """Test that src/lib.rs is generated with correct content."""
    assert default_result.project_dir is not None

    lib_path = default_result.project_dir / 'src' / 'lib.rs'
    assert lib_path.exists()

    content = lib_path.read_text()
    assert default_answers['project_description'] in content
    assert 'pub fn greeting()' in content
    assert '#[cfg(test)]' in content
    assert 'fn test_greeting()' in content
