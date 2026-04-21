"""Tests for the MCP server — in-memory client, no subprocess."""

import json
from pathlib import Path

import pytest
from mcp.shared.memory import create_connected_server_and_client_session
from mcp.types import CallToolResult, TextContent

from aichesscoach.analyzer import find_stockfish
from aichesscoach.mcp_server import mcp

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.skipif(
        find_stockfish() is None,
        reason="Stockfish binary not found — run scripts/install_stockfish.ps1",
    ),
]

SAMPLE_PGN = Path(__file__).parent.parent / "examples" / "sample_game.pgn"
STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
FOOLS_MATE_PGN = """[Event "Fool's Mate"]

1. f3 e5 2. g4 Qh4# 0-1
"""


def _payload(result: CallToolResult) -> object:
    assert not result.isError
    block = result.content[0]
    assert isinstance(block, TextContent)
    return json.loads(block.text)


async def test_list_tools_exposes_all_three() -> None:
    async with create_connected_server_and_client_session(mcp._mcp_server) as client:
        listed = await client.list_tools()
    names = {t.name for t in listed.tools}
    assert {"evaluate_position", "parse_pgn", "analyze_game"} <= names


async def test_evaluate_position_returns_score() -> None:
    async with create_connected_server_and_client_session(mcp._mcp_server) as client:
        result = await client.call_tool(
            "evaluate_position", {"fen": STARTING_FEN, "depth": 8}
        )
    data = _payload(result)
    assert isinstance(data, dict)
    assert "score_cp" in data and "mate_in" in data and "is_mate" in data


async def test_analyze_game_flags_fools_mate_as_blunder() -> None:
    async with create_connected_server_and_client_session(mcp._mcp_server) as client:
        result = await client.call_tool(
            "analyze_game", {"pgn": FOOLS_MATE_PGN, "depth": 8}
        )
    data = _payload(result)
    assert isinstance(data, dict)
    moments = data["moments"]
    assert any(m["ply"] == 3 and m["severity"] == "blunder" for m in moments)


async def test_parse_pgn_returns_headers_and_positions() -> None:
    async with create_connected_server_and_client_session(mcp._mcp_server) as client:
        result = await client.call_tool("parse_pgn", {"pgn": SAMPLE_PGN.read_text()})
    data = _payload(result)
    assert isinstance(data, dict)
    assert "headers" in data and "positions" in data
    assert len(data["positions"]) > 0
