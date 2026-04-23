"""CLI tests — exercise Typer wiring without hitting the Claude API."""
from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from aichesscoach.cli import app

runner = CliRunner()

# Wide terminal so Rich does not wrap option choices and break substring checks.
_WIDE_ENV = {"COLUMNS": "200"}


def test_help_lists_analyze_command() -> None:
    result = runner.invoke(app, ["--help"], env=_WIDE_ENV)
    assert result.exit_code == 0
    assert "analyze" in result.stdout


def test_analyze_help_lists_level_choices() -> None:
    result = runner.invoke(app, ["analyze", "--help"], env=_WIDE_ENV)
    assert result.exit_code == 0
    for choice in ("beginner", "intermediate", "advanced"):
        assert choice in result.stdout


def test_analyze_rejects_missing_pgn_file(tmp_path: Path) -> None:
    missing = tmp_path / "does_not_exist.pgn"
    result = runner.invoke(app, ["analyze", str(missing)], env=_WIDE_ENV)
    assert result.exit_code != 0


def test_analyze_rejects_invalid_level(tmp_path: Path) -> None:
    pgn = tmp_path / "empty.pgn"
    pgn.write_text("", encoding="utf-8")
    result = runner.invoke(app, ["analyze", str(pgn), "--level", "grandmaster"], env=_WIDE_ENV)
    assert result.exit_code != 0
