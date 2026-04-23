# AIchessCoach

> Chess Coach Agent — identifies and explains the key moments of a chess game in natural language, adapted to the player's skill level.

## What it does

Give it a chess game (PGN to start — FEN sequences and GIF on the roadmap), and the agent:

1. Walks through the game move by move
2. Detects **key moments** — blunders, brilliant moves, turning points
3. Explains them in **plain language**, calibrated to a configurable skill level (beginner / intermediate / advanced)

## Why this repo

A focused portfolio project demonstrating hands-on use of modern AI engineering primitives:

- **Agentic loop** — orchestrated with the Claude Agent SDK
- **Tool use** — Stockfish-powered evaluation exposed as first-class tools
- **MCP server** — chess analysis tools exposed via the Model Context Protocol
- **Claude Skills** — coaching style packaged as reusable skills per player level
- **Modern Python** — `uv`, `pyproject.toml`, `src/` layout, `typer` CLI

## Status

Work in progress. Built step by step — the [commit history](https://github.com/Raphlaur4/AIchessCoach/commits/main) documents the incremental build-up.

## Stack

| Component | Choice |
|---|---|
| Language | Python 3.11+ |
| Package manager | [`uv`](https://github.com/astral-sh/uv) |
| Chess logic | [`python-chess`](https://python-chess.readthedocs.io) |
| Engine | [Stockfish](https://stockfishchess.org/) |
| LLM | Claude (Anthropic SDK) |
| Agent framework | Claude Agent SDK |
| Skills | Claude Skills |
| Tool protocol | MCP (Model Context Protocol) |
| CLI | [Typer](https://typer.tiangolo.com/) |

## Installation

Prerequisites: Python 3.11+ and [`uv`](https://github.com/astral-sh/uv).

```bash
git clone https://github.com/Raphlaur4/AIchessCoach.git
cd AIchessCoach
uv sync
```

Stockfish is required for position evaluation and is not committed to the repo.

**Windows:**

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install_stockfish.ps1
```

**macOS / Linux:**

```bash
brew install stockfish       # macOS
sudo apt install stockfish   # Debian/Ubuntu
```

Run the test suite to confirm everything is wired up:

```bash
uv run pytest
```

## MCP server

The chess analysis tools are exposed as an [MCP](https://modelcontextprotocol.io/) server, so any MCP-compatible client (Claude Desktop, Claude Code, the Agent SDK…) can consume them without touching Stockfish or `python-chess` directly.

Three tools are published:

| Tool | Purpose |
|---|---|
| `evaluate_position` | Stockfish evaluation of a single FEN |
| `parse_pgn` | Headers + move-by-move positions |
| `analyze_game` | All inaccuracies, mistakes, and blunders in a game |

Run the server over stdio:

```bash
uv run python -m aichesscoach.mcp_server
```

To wire it into Claude Desktop, add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "aichesscoach": {
      "command": "uv",
      "args": ["run", "python", "-m", "aichesscoach.mcp_server"],
      "cwd": "/absolute/path/to/AIchessCoach"
    }
  }
}
```

## Agent

The agentic loop is built on the [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk-python). It wires the in-process MCP server (chess analysis tools) and the project-scoped Claude Skills (coaching style per level) into a single async entry point.

```python
import asyncio
from aichesscoach.agent import analyze_game

pgn = open("mygame.pgn").read()
coaching = asyncio.run(analyze_game(pgn, level="beginner"))
print(coaching)
```

**Prerequisites:**

- `ANTHROPIC_API_KEY` environment variable set.
- [Claude Code CLI](https://docs.claude.com/en/docs/claude-code) installed and on `PATH` (the SDK wraps it).

Flow for each call:
1. The agent loads the skill matching the requested level from `.claude/skills/`.
2. Claude is given the PGN and may call `evaluate_position`, `parse_pgn`, or `analyze_game` as many times as needed.
3. The coaching text produced by the model is returned as a single string.

## Architecture

```
src/aichesscoach/
├── parser/          # PGN parsing
├── analyzer/        # key-moment detection using Stockfish
├── mcp_server/      # MCP server exposing chess analysis tools
├── agent/           # agentic orchestration with Claude Agent SDK
└── cli.py           # user-facing CLI (Typer)                     (planned)
.claude/
└── skills/          # Claude Skills — coaching style per player level
```

Skills live under `.claude/skills/` because that is the convention the Claude Agent SDK uses to auto-discover project-scoped skills.

## Author

Raphael Laurent — [@Raphlaur4](https://github.com/Raphlaur4)
