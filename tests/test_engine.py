"""Tests for the Stockfish engine wrapper."""

from pathlib import Path

import pytest

from aichesscoach.analyzer import Evaluation, StockfishEngine, find_stockfish
from aichesscoach.parser import parse_pgn

pytestmark = pytest.mark.skipif(
    find_stockfish() is None,
    reason="Stockfish binary not found — run scripts/install_stockfish.ps1",
)

SAMPLE_PGN = Path(__file__).parent.parent / "examples" / "sample_game.pgn"
STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
# Position after 1.f3 e5 2.g4?? — black can mate in 1 with Qh4#.
FOOLS_MATE_FEN = "rnbqkbnr/pppp1ppp/8/4p3/6P1/5P2/PPPPP2P/RNBQKBNR b KQkq g3 0 2"


def test_evaluation_is_returned() -> None:
    with StockfishEngine() as engine:
        ev = engine.evaluate(STARTING_FEN, depth=8)
    assert isinstance(ev, Evaluation)


def test_starting_position_is_roughly_balanced() -> None:
    with StockfishEngine() as engine:
        ev = engine.evaluate(STARTING_FEN, depth=10)
    assert ev.score_cp is not None
    assert not ev.is_mate
    # First-move advantage is small — well under a full pawn.
    assert abs(ev.score_cp) < 100


def test_fools_mate_is_detected() -> None:
    with StockfishEngine() as engine:
        ev = engine.evaluate(FOOLS_MATE_FEN, depth=5)
    assert ev.is_mate
    assert ev.mate_in is not None
    # From White's point of view, Black mating yields a negative distance.
    assert ev.mate_in < 0


def test_engine_evaluates_game_positions() -> None:
    game = parse_pgn(SAMPLE_PGN.read_text())
    with StockfishEngine() as engine:
        for pos in game.positions[:3]:
            ev = engine.evaluate(pos.fen, depth=8)
            assert ev.score_cp is not None or ev.is_mate
