"""PGN parsing — turns a PGN string into an ordered sequence of positions."""

from __future__ import annotations

from dataclasses import dataclass, field
from io import StringIO

import chess.pgn


@dataclass(frozen=True)
class Position:
    """A single position reached during a game."""

    ply: int
    move_san: str
    fen: str


@dataclass(frozen=True)
class ParsedGame:
    """A parsed chess game: headers plus the ordered sequence of positions."""

    headers: dict[str, str]
    positions: list[Position] = field(default_factory=list)


def parse_pgn(pgn_text: str) -> ParsedGame:
    """Parse a PGN string into headers and the full sequence of positions."""
    game = chess.pgn.read_game(StringIO(pgn_text))
    if game is None:
        raise ValueError("Empty or invalid PGN")

    headers = dict(game.headers)
    board = game.board()
    positions: list[Position] = []
    for ply, move in enumerate(game.mainline_moves(), start=1):
        san = board.san(move)
        board.push(move)
        positions.append(Position(ply=ply, move_san=san, fen=board.fen()))

    return ParsedGame(headers=headers, positions=positions)
