
# Local MCP Server

This project is a minimal Model Context Protocol (MCP) server built with FastMCP in Python. It exposes a few simple arithmetic tools that can be used by MCP clients such as Claude Desktop or the FastMCP inspector.

## Project Structure

- `main.py` — defines the MCP server and tools
- `pyproject.toml` — project metadata and dependencies

## Tools Exposed

The server includes these tools:

- `get_random_number(min, max)`
- `add(a, b)`
- `subtract(a, b)`
- `multiply(a, b)`

## Setup

From the project root, initialize the environment and install dependencies:

```bash
uv init .
uv add fastmcp
```

Verify installation:

```bash
uv run fastmcp version
```

## Run the MCP Server

Start the server in development mode with the built-in inspector:

```bash
uv run fastmcp dev inspector main.py
```

This opens the FastMCP inspector so you can test the tools visually.

## Install for Claude Desktop

To install the server for Claude Desktop:

```bash
uv run fastmcp install claude-desktop main.py
```

## Example Server Code

The server implementation is in [main.py](main.py). The current example registers arithmetic tools and exposes them to MCP clients.

## Notes

- This project uses Python 3.12+
- The server runs via `FastMCP`
- The `if __name__ == "_main__":` block is included for compatibility with the local execution pattern used in this example

## Quick Start

```bash
uv init .
uv add fastmcp
uv run fastmcp dev inspector main.py
```
