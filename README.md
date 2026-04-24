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

## Demo

Real coaching output produced by the CLI on the Fool's Mate (`1. f3 e5 2. g4 Qh4#`) at the beginner level:

```bash
uv run aichesscoach analyze fools_mate.pgn --level beginner
```

<details>
<summary>Click to expand the full coaching output</summary>

### 🎓 Analyse de ta partie — Le Fool's Mate (Mat du Fou)

Tu viens de vivre quelque chose d'assez rare : **le mat le plus rapide possible aux échecs**, en seulement 2 coups ! C'est le moment idéal pour comprendre pourquoi ça s'est passé. 😊

---

#### ⚠️ Coup 1 — `f3` (Erreur)

**Ce qui s'est passé :** Le pion en f3 ne développe aucune pièce et n'aide pas à contrôler le centre.

**Pourquoi c'est risqué :** Ce pion ouvre en partie la **diagonale e1–h4**, qui mène directement à ton roi. À ce stade, ce n'est pas encore fatal — mais c'est une première fissure dans la sécurité du roi.

**À retenir :** Au début d'une partie, essaie de jouer des coups qui *développent* tes pièces (cavaliers, fous) ou qui contrôlent le centre avec les pions e4 ou d4.

---

#### 🚨 Coup 3 — `g4` (**Blunder** — erreur fatale)

**Ce qui s'est passé :** La dame noire a joué `Qh4#` — **échec et mat !** La partie est terminée en 2 coups.

**Pourquoi ça s'est produit :** En jouant g4, tu as complètement ouvert la diagonale e1–h4. La dame adverse a pu s'y engouffrer d'un seul coup, attaquant le roi que *rien* ne protégeait sur cette ligne.

**À retenir :** Avant de déplacer les pions f et g, demande-toi toujours : *"Est-ce que j'expose une route vers mon roi ?"* Ces deux pions sont les gardes du corps du roi — les écarter tous les deux en deux coups, c'est le laisser sans défense.

---

#### 💡 La leçon principale

> **La sécurité du roi passe avant tout.** Les pions f et g forment un bouclier naturel devant ton roi. Les avancer en début de partie, surtout sans raison tactique, c'est inviter l'adversaire à attaquer.

Ne te décourage pas — même les grands joueurs ont un jour perdu vite. L'important, c'est de comprendre *pourquoi* ! Tu veux analyser une autre partie ? 🏆

</details>

By default the agent matches the user's locale, which is why this sample is in French. Swap the system prompt (or export `LANG=en_US`) to get English output.

## Architecture

```mermaid
flowchart LR
    User([User]) --> CLI[Typer CLI<br/>aichesscoach analyze]
    CLI --> Agent[Claude Agent SDK<br/>agentic loop]
    Agent -- loads skill --> Skills[(Claude Skills<br/>3 levels)]
    Agent -- tool calls --> MCP[MCP server<br/>in-process]
    MCP --> Parser[python-chess<br/>PGN parser]
    MCP --> Analyzer[analyzer<br/>Stockfish]
```

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

## Quickstart

Once installed, run the CLI on any PGN file:

```bash
uv run aichesscoach analyze path/to/game.pgn --level beginner
```

The agent loads the matching skill, asks Claude to analyze the game via the MCP tools, and prints the coaching to stdout.

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

**Authentication:** set `ANTHROPIC_API_KEY` in the environment, or log in with the Claude Code CLI on the same machine — the SDK picks up whichever is available. The SDK ships its own bundled Claude Code binary, so nothing extra needs to be on `PATH`.

Flow for each call:
1. The agent loads the skill matching the requested level from `.claude/skills/`.
2. Claude is given the PGN and may call `evaluate_position`, `parse_pgn`, or `analyze_game` as many times as needed.
3. The coaching text produced by the model is returned as a single string.

## CLI

A [Typer](https://typer.tiangolo.com/) CLI wraps the agent for terminal use.

```bash
uv run aichesscoach analyze path/to/game.pgn --level beginner
```

Options:

- `--level [beginner|intermediate|advanced]` — selects the coaching skill (default: `intermediate`).
- `--help` — show usage, available commands, and option details.

The CLI requires the same prerequisites as the agent (authentication as above, plus Stockfish for the underlying analysis tools).

## Skills

Three [Claude Skills](https://docs.claude.com/en/docs/claude-code/skills) live under `.claude/skills/`, one per player level. Each is a folder containing a `SKILL.md` with YAML frontmatter (`name`, `description`) and coaching instructions that Claude follows when the skill is loaded.

| Skill | For |
|---|---|
| `beginner-chess-coach` | new or casual players (< ~1200) |
| `intermediate-chess-coach` | club-level players (~1200–1800) |
| `advanced-chess-coach` | tournament-level players (1800+) |

Skills are discovered automatically by the Claude Agent SDK because `.claude/skills/` is its standard project-scoped location.

## Project layout

```
src/aichesscoach/
├── parser/          # PGN parsing
├── analyzer/        # key-moment detection using Stockfish
├── mcp_server/      # MCP server exposing chess analysis tools
├── agent/           # agentic orchestration with Claude Agent SDK
└── cli.py           # user-facing CLI (Typer)
.claude/
└── skills/          # Claude Skills — coaching style per player level
```

## Author

Raphael Laurent — [@Raphlaur4](https://github.com/Raphlaur4)
