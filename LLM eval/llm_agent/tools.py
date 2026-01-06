import math

def calculate_expression(expression: str) -> float:
    try:
        return eval(expression)
    except Exception as e:
        raise ValueError(f"Invalid expression: {e}")

def square_root(value: float) -> float:
    if value < 0:
        raise ValueError("Cannot take square root of negative number")
    return math.sqrt(value)

TOOL_REGISTRY = {
    "calculate_expression": calculate_expression,
    "square_root": square_root
}
