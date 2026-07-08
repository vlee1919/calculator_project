from pathlib import Path
import pytest

from app.calculator_config import (
    CalculatorConfig,
    get_project_root,
)

# Test project root
def test_get_project_root():

    root = get_project_root()

    assert root.exists()
    assert root.is_dir()

# Test just default configuration
def test_default_config():

    config = CalculatorConfig()

    assert config.base_directory.exists()
    assert config.max_history_size == 100
    assert config.auto_save is True
    assert config.precision == 10
    assert config.default_encoding == "utf-8"


# Test custom configuration
def test_custom_config(tmp_path):

    config = CalculatorConfig(
        base_directory=tmp_path,
        max_history_size=50,
        auto_save=False,
        precision=4,
        max_input_value=1000,
        default_encoding="ascii",
    )

    assert config.base_directory == tmp_path
    assert config.max_history_size == 50
    assert config.auto_save is False
    assert config.precision == 4
    assert config.max_input_value == 1000
    assert config.default_encoding == "ascii"

# Test history directory
def test_history_directory(tmp_path):

    config = CalculatorConfig(base_directory=tmp_path)

    expected = (tmp_path / "history").resolve()

    assert config.history_directory == expected

# Test History file
def test_history_file(tmp_path):

    config = CalculatorConfig(base_directory=tmp_path)

    expected = (
        tmp_path /
        "history" /
        "calculator_history.csv"
    ).resolve()

    assert config.history_file == expected

# Test log directory
def test_log_directory(tmp_path):

    config = CalculatorConfig(base_directory=tmp_path)

    expected = (tmp_path / "logs").resolve()

    assert config.log_directory == expected

# Test log file
def test_log_file(tmp_path):

    config = CalculatorConfig(base_directory=tmp_path)

    expected = (
        tmp_path /
        "logs" /
        "calculator.log"
    ).resolve()

    assert config.log_file == expected


