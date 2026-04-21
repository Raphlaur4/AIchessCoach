# CLAUDE.md

Guidance for AI assistants working on this repo. Read this first.

## Mission

**AIchessCoach** is a portfolio project showcasing modern AI engineering primitives: Claude Agent SDK, MCP, Claude Skills, tool use. The goal is to visibly demonstrate these technologies through a small, well-structured chess coaching agent — not to build a production chess trainer.

Optimize for clarity and showcase value over depth.

## Development workflow

- Python 3.11+, managed via **`uv`**. Always prefix Python commands with `uv run` — never activate the venv manually.
- Add deps with `uv add <pkg>` or `uv add --dev <pkg>`. Don't edit `pyproject.toml` dependencies by hand.
- Run tests with `uv run pytest`.
- `uv.lock` is committed for reproducibility.

## Commit conventions

- **Conventional Commits**: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`.
- **Small, focused commits** — one logical change per commit.
- Align with the user before writing code. Propose file list and approach, wait for approval.
- Tests that cover a feature live in the same commit as that feature.
- Push after every commit (`git push`), no batching.
- Git identity uses GitHub's privacy email: `155916014+Raphlaur4@users.noreply.github.com`.
- **Do not** add `Co-Authored-By: Claude` trailers — the user opted out.

## Architecture & layout

```
src/aichesscoach/
├── parser/      # PGN and FEN parsing
├── analyzer/    # key-moment detection using Stockfish        (planned)
├── mcp_server/  # MCP server exposing chess analysis tools    (planned)
├── skills/      # Claude Skills — coaching per player level   (planned)
├── agent/       # agentic orchestration with Claude Agent SDK (planned)
└── cli.py       # Typer CLI                                   (planned)
tests/           # pytest — mirrors the src tree
examples/        # sample PGNs and demo outputs
```

The `src/` layout is intentional — avoids import shadowing.

## Testing

- `pytest` is the framework.
- Tests that depend on external binaries (e.g. Stockfish) must **skip automatically** when the binary is not found — the suite stays green on any machine.
- Every feature commit includes its tests.

## Scope discipline

This is a showcase, not a product:

- No fallbacks, retries, or error handling for scenarios that cannot happen.
- No feature flags, backwards-compat shims, or forward-looking abstractions.
- Prefer three similar lines over a premature abstraction.
- README is a first-class deliverable — keep it polished.

## Roadmap

| # | Step | Status |
|---|---|---|
| 1 | Project scaffolding (README, .gitignore, pyproject.toml) | done — `25ea23d` |
| 2 | PGN parsing with `python-chess` | done — `6502566` |
| 3 | Stockfish integration for position evaluation | done — `c162204` |
| 4 | Detect key moments (blunders, brilliant moves, turning points) | done — `b3aab1e` |
| 5 | MCP server exposing chess analysis tools | next |
| 6 | Claude Skills — skill-level-aware coaching | planned |
| 7 | Agentic loop with Claude Agent SDK | planned |
| 8 | Typer CLI | planned |
| 9 | Polish README with architecture diagram + demo | planned |
| 10 | Examples and sample outputs | planned |

When resuming work: check `git log --oneline` to confirm which steps are done, then continue at the next "next" entry.
