# tools.py
import math
from langchain.agents import Tool

def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b

def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

def divide(a: float, b: float) -> float:
    """Divide a by b."""
    return a / b

# Define the tools with descriptions
tools = [
    Tool(name="add", func=add, description="Add two numbers."),
    Tool(name="subtract", func=subtract, description="Subtract b from a."),
    Tool(name="multiply", func=multiply, description="Multiply two numbers."),
    Tool(name="divide", func=divide, description="Divide a by b.")
]
