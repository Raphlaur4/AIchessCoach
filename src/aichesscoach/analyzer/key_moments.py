"""Key-moment detection: find blunders, mistakes, and inaccuracies in a game."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import chess

from aichesscoach.analyzer.engine import DEFAULT_DEPTH, Evaluation, StockfishEngine
from aichesscoach.parser import ParsedGame

MATE_CP = 100_000

INACCURACY_CP = 50
MISTAKE_CP = 100
BLUNDER_CP = 200


class Severity(str, Enum):
    INACCURACY = "inaccuracy"
    MISTAKE = "mistake"
    BLUNDER = "blunder"


@dataclass(frozen=True)
class KeyMoment:
    """A move that caused a significant evaluation drop for its player."""

    ply: int
    move_san: str
    fen_before: str
    fen_after: str
    eval_before: Evaluation
    eval_after: Evaluation
    cp_loss: int
    severity: Severity


def _eval_to_mover_cp(ev: Evaluation, white_moved: bool) -> int:
    """Convert an Evaluation (white POV) to centipawns from the mover's POV."""
    if ev.is_mate:
        assert ev.mate_in is not None
        cp = (MATE_CP - abs(ev.mate_in)) * (1 if ev.mate_in > 0 else -1)
    else:
        assert ev.score_cp is not None
        cp = ev.score_cp
    return cp if white_moved else -cp


def _classify(cp_loss: int) -> Severity | None:
    if cp_loss >= BLUNDER_CP:
        return Severity.BLUNDER
    if cp_loss >= MISTAKE_CP:
        return Severity.MISTAKE
    if cp_loss >= INACCURACY_CP:
        return Severity.INACCURACY
    return None


def analyze_game(
    game: ParsedGame,
    engine: StockfishEngine,
    depth: int = DEFAULT_DEPTH,
) -> list[KeyMoment]:
    """Return every move that was an inaccuracy, mistake, or blunder."""
    moments: list[KeyMoment] = []
    fen_before = chess.STARTING_FEN
    eval_before = engine.evaluate(fen_before, depth=depth)
    for position in game.positions:
        fen_after = position.fen
        eval_after = engine.evaluate(fen_after, depth=depth)
        white_moved = position.ply % 2 == 1
        cp_loss = _eval_to_mover_cp(eval_before, white_moved) - _eval_to_mover_cp(
            eval_after, white_moved
        )
        severity = _classify(cp_loss)
        if severity is not None:
            moments.append(
                KeyMoment(
                    ply=position.ply,
                    move_san=position.move_san,
                    fen_before=fen_before,
                    fen_after=fen_after,
                    eval_before=eval_before,
                    eval_after=eval_after,
                    cp_loss=cp_loss,
                    severity=severity,
                )
            )
        fen_before = fen_after
        eval_before = eval_after
    return moments
