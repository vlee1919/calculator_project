import pytest
from app.calculator_repl import calculator_repl
from unittest.mock import patch



# Test an operation
def test_operation_input(capsys):
    

    fake_keyboard_inputs = ['add', '5', '5', 'exit']
    
    with patch('builtins.input', side_effect=fake_keyboard_inputs):

        calculator_repl()
        
    # Check what was printed to the screen --> assert match
    screen_output = capsys.readouterr().out
    assert "Result: 10" in screen_output

# Test invalid user input
def test_invalid_input(capsys):

    fake_keyboard_inputs = ['randomwords', 'exit']
    
    with patch('builtins.input', side_effect=fake_keyboard_inputs):
        
        calculator_repl()
        
    screen_output = capsys.readouterr().out
    assert "Invalid operation: 'randomwords'" in screen_output

# Test exit input
def test_exit_input(capsys):
    
    fake_keyboard_inputs = ['exit']
    
    with patch('builtins.input', side_effect=fake_keyboard_inputs):
        
        calculator_repl()
        
    # Check what was printed to the screen --> assert match
    screen_output = capsys.readouterr().out
    assert "Exiting calculator. Goodbye!" in screen_output

