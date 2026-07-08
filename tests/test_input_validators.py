import pytest

from app.input_validators import InputValidator
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError

@pytest.fixture
# Set max value to 1000
def validator():
    config = CalculatorConfig(max_input_value=1000)
    return InputValidator(config)

# Test integer
def test_validate_integer(validator):
    assert validator.validate_number("10") == 10.0

# Test regular float
def test_validate_float(validator):
    assert validator.validate_number("1.23") == 1.23

# Test invalid string
def test_validate_invalid_string(validator):
    with pytest.raises(ValidationError):
        validator.validate_number("hello")

# Test when exceding maximum allowed range
def test_validate_above_maximum(validator):
    with pytest.raises(ValidationError):
        validator.validate_number("1001")

