"""Tests for PGN parsing."""

from pathlib import Path

import pytest

from aichesscoach.parser import ParsedGame, parse_pgn

SAMPLE_PGN = Path(__file__).parent.parent / "examples" / "sample_game.pgn"


def test_parse_returns_parsed_game() -> None:
    game = parse_pgn(SAMPLE_PGN.read_text())
    assert isinstance(game, ParsedGame)


def test_headers_are_extracted() -> None:
    game = parse_pgn(SAMPLE_PGN.read_text())
    assert game.headers["White"] == "Alice"
    assert game.headers["Black"] == "Bob"
    assert game.headers["Result"] == "1-0"


def test_positions_match_move_count() -> None:
    game = parse_pgn(SAMPLE_PGN.read_text())
    # Ruy Lopez mainline to move 5 for both sides = 10 half-moves
    assert len(game.positions) == 10


def test_first_move_is_e4() -> None:
    game = parse_pgn(SAMPLE_PGN.read_text())
    first = game.positions[0]
    assert first.ply == 1
    assert first.move_san == "e4"


def test_fens_are_well_formed() -> None:
    game = parse_pgn(SAMPLE_PGN.read_text())
    for pos in game.positions:
        # A valid FEN has 6 space-separated fields
        assert pos.fen.count(" ") == 5


def test_ply_is_sequential() -> None:
    game = parse_pgn(SAMPLE_PGN.read_text())
    assert [p.ply for p in game.positions] == list(range(1, len(game.positions) + 1))


def test_empty_pgn_raises() -> None:
    with pytest.raises(ValueError):
        parse_pgn("")
