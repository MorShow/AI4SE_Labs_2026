# /// script
# requires-python = ">=3.10"
# dependencies = ["mcp>=1.28,<2"]
# ///

"""Local MCP server exposing a single word-counting tool."""

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("ai4se-word-counter")


@mcp.tool()
def count_words(text: str) -> int:
    """Count whitespace-separated words. Empty or whitespace-only text returns 0."""
    return len(text.split())


if __name__ == "__main__":
    mcp.run(transport="stdio")
