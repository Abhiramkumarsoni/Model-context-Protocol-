from fastmcp import FastMCP
import random
import json

# create the FastMCP Sever instance
mcp = FastMCP("Simple Calculator Server")

# Tool: add two numbers
@mcp.tool
def add(a:int, b:int) -> int:
    """Add two numbers.

    args:
        a (int): The first number.
        b (int): The second number.
    returns:
        int: The sum of a and b.
    """
    return a + b

# Tool: subtract two numbers
@mcp.tool
def subtract(a:int, b:int) -> int:
    """Subtract two numbers.

    args:
        a (int): The first number.
        b (int): The second number.
    returns:
        int: The difference of a and b.
    """
    return a - b

# Tool: multiply two numbers
@mcp.tool
def multiply(a:int, b:int) -> int:
    """Multiply two numbers.

    args:
        a (int): The first number.
        b (int): The second number.
    returns:
        int: The product of a and b.
    """
    return a * b

# Tool: divide two numbers
@mcp.tool
def divide(a:int, b:int) -> float:
    """Divide two numbers.

    args:
        a (int): The first number.
        b (int): The second number.
    returns:
        float: The quotient of a and b.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

# Tool: generate a random number
@mcp.tool
def random_number(min:int, max:int) -> int:
    """Generate a random number between min and max.

    args:
        min (int): The minimum value.
        max (int): The maximum value.
    returns:
        int: A random number between min and max.
    """
    return random.randint(min, max)

# resource: server information
@mcp.resource("info://server")
def server_info() -> str:
    """Get information about this server."""
    info = {
        "name": "Simple Calculator Server",
        "version": "1.0.0",
        "description": "A basic MCP server with math tools.",
        "tools": ["add", "subtract", "multiply", "divide", "random_number"],
        "author": "Abhiram Kumar Soni",
    }
    return json.dumps(info, indent=4)

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8080)


    