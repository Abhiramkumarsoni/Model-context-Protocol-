from fastmcp import FastMCP
from main import app

# convert FastAPI app to MCP Server
mcp = FastMCP.from_fastapi(
    app=app,
    name="Expense Tracker server",
    )


if __name__ == "__main__":
    mcp.run() 