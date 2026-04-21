"""MCP server exposing AIchessCoach's chess analysis tools.

Three tools are published:
  - evaluate_position — Stockfish eval of a single FEN
  - parse_pgn         — headers + move-by-move positions
  - analyze_game      — list of inaccuracies / mistakes / blunders

Any MCP client (Claude Desktop, Claude Code, the Agent SDK…) can connect
to this server and call these tools without needing to know about Stockfish
or python-chess.
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from aichesscoach.analyzer import StockfishEngine
from aichesscoach.analyzer import analyze_game as _analyze_game
from aichesscoach.analyzer.engine import DEFAULT_DEPTH, Evaluation
from aichesscoach.parser import parse_pgn as _parse_pgn

mcp = FastMCP("AIchessCoach")


def _eval_to_dict(ev: Evaluation) -> dict:
    return {
        "score_cp": ev.score_cp,
        "mate_in": ev.mate_in,
        "is_mate": ev.is_mate,
    }


@mcp.tool()
def evaluate_position(fen: str, depth: int = DEFAULT_DEPTH) -> dict:
    """Evaluate a chess position with Stockfish. Score is from white's POV."""
    with StockfishEngine() as engine:
        ev = engine.evaluate(fen, depth=depth)
    return _eval_to_dict(ev)


@mcp.tool()
def parse_pgn(pgn: str) -> dict:
    """Parse a PGN string. Returns headers and one position per ply (FEN after the move)."""
    game = _parse_pgn(pgn)
    return {
        "headers": game.headers,
        "positions": [
            {"ply": p.ply, "move_san": p.move_san, "fen": p.fen}
            for p in game.positions
        ],
    }


@mcp.tool()
def analyze_game(pgn: str, depth: int = DEFAULT_DEPTH) -> dict:
    """Return every inaccuracy, mistake, or blunder in a PGN game."""
    game = _parse_pgn(pgn)
    with StockfishEngine() as engine:
        moments = _analyze_game(game, engine, depth=depth)
    return {
        "moments": [
            {
                "ply": m.ply,
                "move_san": m.move_san,
                "severity": m.severity.value,
                "cp_loss": m.cp_loss,
                "fen_before": m.fen_before,
                "fen_after": m.fen_after,
                "eval_before": _eval_to_dict(m.eval_before),
                "eval_after": _eval_to_dict(m.eval_after),
            }
            for m in moments
        ]
    }
