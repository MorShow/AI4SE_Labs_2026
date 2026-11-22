# Task 7 Local MCP Server

- Created [server.py](server.py) using the official MCP Python SDK's `FastMCP` and local STDIO transport. The script declares its SDK dependency inline so `uv` can install it automatically.
- Added one tool, `count_words(text)`, which counts whitespace-separated words using `len(text.split())`. Empty or whitespace-only input returns zero, and punctuation stays attached to words.
- Verified MCP initialization, discovery of exactly one tool, and four calls covering ordinary text, empty input, whitespace-only input, and mixed whitespace. The coding-assistant invocation evidence will be added after connecting the server.

## Setup and demonstration

1. From the repository root, run `cd Week_08_Dissecting/solutions/Task_7`. Codex will launch the STDIO server and communicate with it using JSON-RPC.
2. Register it with `codex mcp add ai4se-word-counter -- uv run --python C:/Python313/python.exe --script "$((Resolve-Path ./server.py).Path)"`. The Python path matches the current computer and can be replaced on another machine.
3. Open a new Codex CLI session and ask `Use the count_words MCP tool to count the words in "This is a simple MCP tool."` Save the actual tool call and result as evidence. The expected count is 6.

Implementation and connection follow the [MCP Python SDK guide](https://github.com/modelcontextprotocol/python-sdk/tree/v1.x) and [Codex MCP guide](https://learn.chatgpt.com/docs/extend/mcp).
