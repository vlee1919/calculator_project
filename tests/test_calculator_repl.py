import pytest
from app.calculator_repl import calculator_repl
from unittest.mock import patch


""" Operation Tests"""
# Test Addition
def test_addition_input(capsys):

    fake_keyboard_inputs = ['add', '5', '5', 'exit']
    
    with patch('builtins.input', side_effect=fake_keyboard_inputs):

        calculator_repl()
        
    # Check what was printed to the screen --> assert match
    screen_output = capsys.readouterr().out
    assert "Result: 10" in screen_output


# Test Subtraction 
def test_subtract_input(capsys):

    fake_keyboard_inputs = ['subtract', '10', '4', 'exit']

    with patch('builtins.input', side_effect=fake_keyboard_inputs):
        calculator_repl()

    screen_output = capsys.readouterr().out
    assert "Result: 6" in screen_output


# Test Multiplication 
def test_multiply_input(capsys):

    fake_keyboard_inputs = ['multiply', '6', '7', 'exit']

    with patch('builtins.input', side_effect=fake_keyboard_inputs):
        calculator_repl()

    screen_output = capsys.readouterr().out
    assert "Result: 42" in screen_output


# Test Division
def test_divide_input(capsys):

    fake_keyboard_inputs = ['divide', '20', '5', 'exit']

    with patch('builtins.input', side_effect=fake_keyboard_inputs):
        calculator_repl()

    screen_output = capsys.readouterr().out
    assert "Result: 4" in screen_output


def test_invalid_divide_input(capsys):

    fake_keyboard_inputs = ['divide', '20', '0', 'exit']

    with patch('builtins.input', side_effect=fake_keyboard_inputs):
        calculator_repl()

    screen_output = capsys.readouterr().out
    assert "Error: Division by zero is not allowed." in screen_output


"""Invalid Inputs"""

# Test invalid user input
def test_invalid_input(capsys):

    fake_keyboard_inputs = ['randomwords', 'exit']
    
    with patch('builtins.input', side_effect=fake_keyboard_inputs):
        
        calculator_repl()
        
    screen_output = capsys.readouterr().out
    assert "Invalid operation: 'randomwords'" in screen_output


# Test empty input
def test_empty_input(capsys):

    fake_keyboard_inputs = [
        '',
        'exit'
    ]

    with patch('builtins.input', side_effect=fake_keyboard_inputs):
        calculator_repl()

    screen_output = capsys.readouterr().out

    assert "Invalid operation: ''. Please try again." in screen_output


"""Test Other inputs"""

# Test exit input
def test_exit_input(capsys):
    
    fake_keyboard_inputs = ['exit']
    
    with patch('builtins.input', side_effect=fake_keyboard_inputs):
        
        calculator_repl()
        
    # Check what was printed to the screen --> assert match
    screen_output = capsys.readouterr().out
    assert "Exiting calculator. Goodbye!" in screen_output


# Test help input
def test_help_input(capsys):

    fake_keyboard_inputs = ["help", "exit"]

    with patch("builtins.input", side_effect=fake_keyboard_inputs):
        calculator_repl()

    screen_output = capsys.readouterr().out

    assert "Available Operations:" in screen_output
    assert "Type 'history'" in screen_output


# Test history input
def test_history_input(capsys):
    
    fake_keyboard_inputs = ['add', '10', '10', 'history', 'exit']
    
    with patch('builtins.input', side_effect=fake_keyboard_inputs):

        calculator_repl()
        
    screen_output = capsys.readouterr().out
    assert "Calculation History:" in screen_output


# Test clear history
def test_clear_input(capsys):
    """Test that the clear command properly outputs its confirmation message."""
    
    fake_keyboard_inputs = ['clear', 'exit']
    
    with patch('builtins.input', side_effect=fake_keyboard_inputs):

        calculator_repl()
        
    screen_output = capsys.readouterr().out
    assert "History cleared." in screen_output


# Test both undo and redo
def test_undo_redo(capsys):

    fake_keyboard_inputs = ['add', '5', '5', 'undo', 'redo', 'exit']
    
    with patch('builtins.input', side_effect=fake_keyboard_inputs):

        calculator_repl()
    
    screen_output = capsys.readouterr().out
    assert "Last undone operation redone." in screen_output