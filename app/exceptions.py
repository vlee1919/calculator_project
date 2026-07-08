
class CalculatorError(Exception):
    """
    Base exception class for calculator-specific errors.

    All custom exceptions for the calculator application inherit from this class,
    allowing for unified error handling.
    """
    pass


class ValidationError(CalculatorError):
    """
    Raised when input validation fails.

    This exception is triggered when user inputs do not meet the required criteria,
    such as entering non-numeric values or exceeding maximum allowed values.
    """
    pass


