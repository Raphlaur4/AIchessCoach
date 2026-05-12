# Examples

Sample PGNs paired with coaching outputs produced by the agent. Browse them to see what the project does without setting up authentication or running anything yourself.

| Game | PGN | Level | Coaching output |
|---|---|---|---|
| Fool's Mate | [`fools_mate.pgn`](fools_mate.pgn) | `beginner` | [`fools_mate_output.md`](fools_mate_output.md) |
| Morphy — Opera Game (1858) | [`morphy_opera_game.pgn`](morphy_opera_game.pgn) | `advanced` | [`morphy_opera_game_output.md`](morphy_opera_game_output.md) |

## Regenerating an output

Run the CLI from the repo root:

```bash
uv run aichesscoach analyze examples/morphy_opera_game.pgn --level advanced
```

By default the agent matches the user's language. The sample outputs here were captured by prompting explicitly for English so the README reads in a single language.
