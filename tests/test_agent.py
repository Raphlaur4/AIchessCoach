"""End-to-end test for the chess-coach agent.

Skips automatically when the required prerequisites are missing so the suite
stays green on any machine. Running it hits the real Claude API and therefore
consumes quota.
"""
from __future__ import annotations

import os

import pytest

from aichesscoach.agent import analyze_game
from aichesscoach.analyzer.engine import find_stockfish

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.skipif(
        not os.environ.get("ANTHROPIC_API_KEY"),
        reason="ANTHROPIC_API_KEY is not set",
    ),
    pytest.mark.skipif(
        find_stockfish() is None,
        reason="Stockfish is not installed",
    ),
]

FOOLS_MATE = """[Event "Fool's Mate"]

1. f3 e5 2. g4 Qh4# 0-1
"""


async def test_agent_produces_coaching_for_fools_mate() -> None:
    output = await analyze_game(FOOLS_MATE, level="beginner")
    assert output.strip(), "Agent produced no output"
