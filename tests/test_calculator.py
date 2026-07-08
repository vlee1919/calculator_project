import pandas as pd
import pytest
from pathlib import Path

from app.calculator import Calculator
from app.calculator_config import CalculatorConfig

# Setup temporary directory --> for history related testing
@pytest.fixture
def calculator(tmp_path):
    config = CalculatorConfig(base_directory=tmp_path)
    return Calculator(config)

# Test initializing calculator
def test_calculator_initializes(calculator):

    assert calculator is not None
    assert calculator.get_history() == []

"""Operration test"""

# Test valid operation
def test_execute_operation(calculator):

    result = calculator.execute_operation("add", 2, 3)

    assert result == 5
    assert len(calculator.get_history()) == 1

    record = calculator.get_history()[0]

    assert record["Operation"] == "add"
    assert record["Input"] == "2, 3"
    assert record["Result"] == 5

# Test invalid operation
def test_invalid_operation(calculator):

    with pytest.raises(ValueError):
        calculator.execute_operation("invalid", 1, 2)

"""Calculation History Tests"""

# Test the Undo method
def test_undo(calculator):

    calculator.execute_operation("add", 2, 3)

    assert len(calculator.get_history()) == 1
    assert calculator.undo()

    assert calculator.get_history() == []

# Test the Redo method
def test_redo(calculator):

    calculator.execute_operation("add", 2, 3)

    calculator.undo()
    assert calculator.redo()

    assert len(calculator.get_history()) == 1

# Test the clear method
def test_clear_history(calculator):

    calculator.execute_operation("add", 2, 3)
    calculator.execute_operation("multiply", 4, 5)

    assert len(calculator.get_history()) == 2

    calculator.clear_history()

    assert calculator.get_history() == []

# Test the manual save method
def test_save_history(calculator):

    calculator.execute_operation("add", 2, 3)
    calculator.save_history()

    assert calculator.config.history_file.exists()

    df = pd.read_csv(calculator.config.history_file)

    assert len(df) == 1
    assert df.iloc[0]["Operation"] == "add" # Check operation is located on the first row

# Test the manual load method
def test_load_history(calculator):

    calculator.execute_operation("add", 2, 3)
    calculator.save_history()
    calculator.history = []

    calculator.load_history()

    assert len(calculator.get_history()) == 1
    assert calculator.get_history()[0]["Operation"] == "add" # Check operation is located on the first row

# Test creating history file
def test_history_file_created(calculator):

    calculator.execute_operation("subtract", 10, 5)
    assert calculator.config.history_file.exists()

