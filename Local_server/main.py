import random
from fastmcp import FastMCP

mcp = FastMCP("A simple FastMCP example")

@mcp.tool()
def get_random_number(min: int, max: int) -> int:
    return random.randint(min, max)

@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    return a - b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    return a * b


if __name__ == "_main__":
    mcp.run()
