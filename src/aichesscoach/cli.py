"""Typer CLI — user-facing entry point for the chess-coach agent."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Annotated

import typer

from aichesscoach.agent import Level, analyze_game

app = typer.Typer(
    help="Chess Coach Agent — identifies and explains key moments of a chess game.",
    no_args_is_help=True,
)


@app.callback()
def _root() -> None:
    """Keep the subcommand structure (prevents Typer from collapsing a single-command app)."""


@app.command()
def analyze(
    pgn_path: Annotated[
        Path,
        typer.Argument(exists=True, dir_okay=False, readable=True, help="Path to a PGN file."),
    ],
    level: Annotated[
        Level,
        typer.Option(help="Target skill level for the coaching."),
    ] = "intermediate",
) -> None:
    """Analyze a chess game and produce level-appropriate coaching."""
    sys.stdout.reconfigure(encoding="utf-8")
    pgn = pgn_path.read_text(encoding="utf-8")
    typer.echo(asyncio.run(analyze_game(pgn, level=level)))


if __name__ == "__main__":
    app()
