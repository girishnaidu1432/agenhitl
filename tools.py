import math
from langchain_core.tools import Tool

def add(a: float, b: float) -> float:
    """Add two numbers"""
    return a + b

def subtract(a: float, b: float) -> float:
    """Subtract b from a"""
    return a - b

def multiply(a: float, b: float) -> float:
    """Multiply two numbers"""
    return a * b

def divide(a: float, b: float) -> float:
    """Divide a by b"""
    return a / b

def sin(a: float) -> float:
    """Sine of a (radians)"""
    return math.sin(a)

def cos(a: float) -> float:
    """Cosine of a (radians)"""
    return math.cos(a)

def radians(a: float) -> float:
    """Convert degrees to radians"""
    return math.radians(a)

def exponentiation(a: float, b: float) -> float:
    """a raised to the power of b"""
    return a ** b

def sqrt(a: float) -> float:
    """Square root of a"""
    return math.sqrt(a)

def ceil(a: float) -> float:
    """Ceiling of a"""
    return math.ceil(a)

tools = [
    Tool.from_function(add),
    Tool.from_function(subtract),
    Tool.from_function(multiply),
    Tool.from_function(divide),
    Tool.from_function(sin),
    Tool.from_function(cos),
    Tool.from_function(radians),
    Tool.from_function(exponentiation),
    Tool.from_function(sqrt),
    Tool.from_function(ceil),
]
