# tools.py

import math
from langchain_core.tools import tool

@tool
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

@tool
def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b

@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

@tool
def divide(a: float, b: float) -> float:
    """Divide a by b."""
    return a / b

@tool
def sin(a: float) -> float:
    """Sine of an angle in radians."""
    return math.sin(a)

@tool
def cos(a: float) -> float:
    """Cosine of an angle in radians."""
    return math.cos(a)

@tool
def radians(degrees: float) -> float:
    """Convert degrees to radians."""
    return math.radians(degrees)

@tool
def exponentiation(a: float, b: float) -> float:
    """Raise a to the power of b."""
    return a ** b

@tool
def sqrt(a: float) -> float:
    """Square root of a number."""
    return math.sqrt(a)

@tool
def ceil(a: float) -> float:
    """Ceiling of a number."""
    return math.ceil(a)

# List of all tools
tools = [
    add,
    subtract,
    multiply,
    divide,
    sin,
    cos,
    radians,
    exponentiation,
    sqrt,
    ceil
]
