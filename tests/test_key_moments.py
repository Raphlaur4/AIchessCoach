"""Tests for key-moment detection (blunders, mistakes, inaccuracies)."""

from pathlib import Path

import pytest

from aichesscoach.analyzer import (
    KeyMoment,
    Severity,
    StockfishEngine,
    analyze_game,
    find_stockfish,
)
from aichesscoach.parser import parse_pgn

pytestmark = pytest.mark.skipif(
    find_stockfish() is None,
    reason="Stockfish binary not found — run scripts/install_stockfish.ps1",
)

SAMPLE_PGN = Path(__file__).parent.parent / "examples" / "sample_game.pgn"

# 1. f3 e5 2. g4 Qh4# — the shortest possible loss for white.
FOOLS_MATE_PGN = """[Event "Fool's Mate"]

1. f3 e5 2. g4 Qh4# 0-1
"""


def test_fools_mate_flags_g4_as_blunder() -> None:
    game = parse_pgn(FOOLS_MATE_PGN)
    with StockfishEngine() as engine:
        moments = analyze_game(game, engine, depth=8)
    # Ply 3 is white's 2.g4, which walks straight into mate — must be a blunder.
    blunders_on_ply_3 = [
        m for m in moments if m.ply == 3 and m.severity == Severity.BLUNDER
    ]
    assert len(blunders_on_ply_3) == 1
    assert blunders_on_ply_3[0].move_san == "g4"


def test_quiet_opening_has_no_blunders() -> None:
    game = parse_pgn(SAMPLE_PGN.read_text())
    with StockfishEngine() as engine:
        moments = analyze_game(game, engine, depth=8)
    assert all(m.severity != Severity.BLUNDER for m in moments)


def test_key_moments_carry_full_context() -> None:
    game = parse_pgn(FOOLS_MATE_PGN)
    with StockfishEngine() as engine:
        moments = analyze_game(game, engine, depth=8)
    assert moments, "Fool's mate should produce at least one key moment"
    m = moments[0]
    assert isinstance(m, KeyMoment)
    assert m.fen_before != m.fen_after
    assert m.cp_loss >= 50
