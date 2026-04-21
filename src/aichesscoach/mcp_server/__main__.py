"""Run the MCP server over stdio: `uv run python -m aichesscoach.mcp_server`."""

from aichesscoach.mcp_server.server import mcp

if __name__ == "__main__":
    mcp.run()
