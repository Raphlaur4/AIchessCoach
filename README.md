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

## Planned architecture

```
src/aichesscoach/
├── analyzer/        # key-moment detection using Stockfish
├── mcp_server/      # MCP server exposing chess analysis tools
├── skills/          # Claude Skills — coaching style per player level
├── agent/           # agentic orchestration with Claude Agent SDK
└── cli.py           # user-facing CLI (Typer)
```

## Author

Raphael Laurent — [@Raphlaur4](https://github.com/Raphlaur4)
