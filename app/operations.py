from abc import ABC, abstractmethod


class Operation(ABC):
    """Abstract base class for all calculator operations."""
    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        pass


class Addition(Operation):
    def execute(self, a: float, b: float) -> float:
        return a + b

class Subtraction(Operation):
    def execute(self, a: float, b: float) -> float:
        return a - b

class Multiplication(Operation):
    def execute(self, a: float, b: float) -> float:
        return a * b

class Division(Operation):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return a / b

class Power(Operation):
    def execute(self, a: float, b: float) -> float:
        return a ** b

class Root(Operation):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Zero root is undefined.")
        # Taking the 'b' root of 'a', equivalent to a^(1/b)
        return a ** (1 / b)

class Modulo(Operation):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Modulo by zero is not allowed.")
        return a % b

# The Operation factory class
class OperationFactory:
    """Instantiates and returns the correct
      operation object based on user input."""
    def __init__(self):
        self.operations = {
            "add": Addition(),
            "subtract": Subtraction(),
            "multiply": Multiplication(),
            "divide": Division(),
            "power": Power(),
            "root": Root(),
            "modulo": Modulo()
        }
    # Retrieves the requested operation object.
    def get_operation(self, user_input: str) -> Operation:
        if user_input not in self.operations:
            raise ValueError(f"Unknown operation: '{user_input}'")
        return self.operations[user_input]