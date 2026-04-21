"""Stockfish UCI engine wrapper for position evaluation."""

from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from types import TracebackType
from typing import Self

import chess
import chess.engine

DEFAULT_DEPTH = 14
_REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_BINARY = _REPO_ROOT / "bin" / "stockfish" / "stockfish-windows-x86-64-avx2.exe"


@dataclass(frozen=True)
class Evaluation:
    """Stockfish's verdict on a position, from White's point of view."""

    score_cp: int | None
    mate_in: int | None

    @property
    def is_mate(self) -> bool:
        return self.mate_in is not None


def find_stockfish(explicit: str | Path | None = None) -> Path | None:
    """Resolve the Stockfish binary path.

    Order: explicit argument > STOCKFISH_PATH env var > PATH lookup > repo default.
    Returns None if no binary is found.
    """
    if explicit is not None:
        path = Path(explicit)
        return path if path.is_file() else None

    env = os.environ.get("STOCKFISH_PATH")
    if env:
        path = Path(env)
        if path.is_file():
            return path

    on_path = shutil.which("stockfish")
    if on_path:
        return Path(on_path)

    if DEFAULT_BINARY.is_file():
        return DEFAULT_BINARY

    return None


class StockfishEngine:
    """Context manager around a Stockfish UCI engine process."""

    def __init__(self, binary: str | Path | None = None) -> None:
        resolved = find_stockfish(binary)
        if resolved is None:
            raise FileNotFoundError(
                "Stockfish binary not found. Run scripts/install_stockfish.ps1 "
                "on Windows, or install via your package manager and set STOCKFISH_PATH."
            )
        self.binary = resolved
        self._engine: chess.engine.SimpleEngine | None = None

    def __enter__(self) -> Self:
        self._engine = chess.engine.SimpleEngine.popen_uci(str(self.binary))
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        if self._engine is not None:
            self._engine.quit()
            self._engine = None

    def evaluate(self, fen: str, depth: int = DEFAULT_DEPTH) -> Evaluation:
        """Evaluate a FEN position, returning a score from White's point of view."""
        if self._engine is None:
            raise RuntimeError("Engine is not running. Use as a context manager.")
        board = chess.Board(fen)
        info = self._engine.analyse(board, chess.engine.Limit(depth=depth))
        score = info["score"].white()
        if score.is_mate():
            return Evaluation(score_cp=None, mate_in=score.mate())
        return Evaluation(score_cp=score.score(), mate_in=None)
