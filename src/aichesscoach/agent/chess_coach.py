"""Agentic orchestration with the Claude Agent SDK.

Wires our in-process MCP server (chess analysis tools) and our Claude Skills
(coaching styles per player level) into a single async entry point.
"""
from __future__ import annotations

from pathlib import Path
from typing import Literal

from claude_agent_sdk import ClaudeAgentOptions, query
from claude_agent_sdk.types import (
    AssistantMessage,
    McpSdkServerConfig,
    TextBlock,
)

from aichesscoach.mcp_server import mcp

Level = Literal["beginner", "intermediate", "advanced"]

_LEVEL_TO_SKILL: dict[Level, str] = {
    "beginner": "beginner-chess-coach",
    "intermediate": "intermediate-chess-coach",
    "advanced": "advanced-chess-coach",
}

_PROJECT_ROOT = Path(__file__).resolve().parents[3]

_SYSTEM_PROMPT = (
    "You are a chess coach. Given a PGN of a chess game, use the available "
    "MCP chess analysis tools to identify the key moments (blunders, mistakes, "
    "inaccuracies), then explain them to the player. Follow the coaching style "
    "described in the loaded skill."
)


async def analyze_game(pgn: str, level: Level = "intermediate") -> str:
    """Run the chess-coach agent on a PGN and return the final coaching text."""
    skill = _LEVEL_TO_SKILL[level]
    options = ClaudeAgentOptions(
        mcp_servers={
            "chess": McpSdkServerConfig(
                type="sdk",
                name="chess",
                instance=mcp._mcp_server,
            ),
        },
        allowed_tools=[
            "mcp__chess__evaluate_position",
            "mcp__chess__parse_pgn",
            "mcp__chess__analyze_game",
        ],
        system_prompt=_SYSTEM_PROMPT,
        skills=[skill],
        setting_sources=["project"],
        cwd=str(_PROJECT_ROOT),
    )

    prompt = f"Coach the player on this game:\n\n{pgn}"
    chunks: list[str] = []
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    chunks.append(block.text)
    return "\n".join(chunks)
