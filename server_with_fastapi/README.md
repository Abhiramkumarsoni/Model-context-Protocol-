# Expense Tracker API + MCP Server

This project demonstrates how to build an expense tracker API with FastAPI and then convert it into an MCP server using FastMCP.

## Overview

The workflow is:

1. Initialize a project with uv
2. Add FastMCP
3. Check the installed FastMCP version
4. Build the FastAPI expense tracker
5. Convert the FastAPI app into an MCP server
6. Run the MCP inspector or install it for Claude Desktop

## Project structure

- [main.py](main.py) — FastAPI application with expense endpoints
- [server.py](server.py) — MCP server created from the FastAPI app
- [categories.json](categories.json) — category metadata
- [expenses.db](expenses.db) — SQLite database file created automatically

## Step-by-step setup

### 1. Initialize the project

```powershell
uv init .
```

### 2. Add FastMCP

```powershell
uv add fastmcp
```

### 3. Verify the installation

```powershell
uv run fastmcp version
```

### 4. Create the FastAPI app

The app in [main.py](main.py) defines the expense tracker routes and database logic.

It includes endpoints such as:

- POST /expenses
- GET /expenses
- GET /expenses/summary
- GET /categories

### 5. Convert FastAPI into an MCP server

The file [server.py](server.py) creates the MCP server using:

```python
from fastmcp import FastMCP
from main import app

mcp = FastMCP.from_fastapi(
    app=app,
    name="Expense Tracker server",
)
```

This exposes the FastAPI endpoints through an MCP server interface.

## Run the FastAPI app

```powershell
cd "C:\MCP\server_with_fastapi"
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Open:

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

## Run the MCP inspector

```powershell
cd "C:\MCP\server_with_fastapi"
uv run fastmcp dev inspector main.py
```

This is the visual inspector used to test and inspect the MCP server.

## Install for Claude Desktop

```powershell
cd "C:\MCP\server_with_fastapi"
uv run fastmcp install claude-desktop main.py
```

## Example request

```json
{
  "date": "2026-09-22",
  "amount": 45.75,
  "category": "Food",
  "subcategory": "Groceries",
  "note": "Weekly shopping"
}
```

## Features

- Add expenses
- List expenses by date range
- Summarize totals by category
- Read category metadata
- Expose the same workflow through both HTTP and MCP

## Notes

- The project stores expense data locally in SQLite.
- The FastAPI API is the main HTTP interface.
- The MCP server is generated from that same API so the logic can be reused across tools and clients.
