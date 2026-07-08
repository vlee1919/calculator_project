from app.exceptions import ValidationError
from app.calculator_config import CalculatorConfig

"""Validates user input before calculations are performed."""
class InputValidator:

    # Initialize configuration
    def __init__(self, config: CalculatorConfig = None):
        self.config = config or CalculatorConfig()

    # Takes the values entered and confirm if it is a float and is within the range set in configuration
    def validate_number(self, value):
        try:
            number = float(value)
        except (TypeError, ValueError):
            raise ValidationError(f"Invalid number: '{value}'")

        if abs(number) > self.config.max_input_value:
            raise ValidationError(
                f"Input exceeds the maximum allowed value "
                f"({self.config.max_input_value})."
            )
        return number