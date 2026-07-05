"""
Calculator REPL 
"""
import logging
from app.operations import OperationFactory
from app.calculator import Calculator
from app. calculator_memento import EventManager, HistoryManager, MementoManager


def calculator_repl():
    print("Calculator REPL")
    print("Format: <operation> <number1> <number2>")
    print("Please enter a mathematical operation or type 'help' to see available commands.")
    print("Enter 'exit' to quit the calculator.")
    print("Type 'exit' to quit.\n")
    while True:
        try:
            # Initialize the Calculator
            calculator = Calculator()

            # User Input
            user_input = input("Your input> ").strip().lower()
            
            # Exit command
            if user_input == "exit":
                print("Exiting calculator. Goodbye!")
                break
            
            # Help Command
            if user_input == "help":
                print("Available Operations: add, subtract, multiply, divide, power, root, modulo, int_divide, percent, abs_diff")
                print("Type 'history' to view the history of calculations.")
                print("Type 'clear' to clear the history.")
                print("Type 'undo' to undo the last operation.")
                print("Type 'redo' to redo the last undone operation.")
                print("Type 'help' to see this message again.")
                print("Type 'exit' to quit the calculator.")
                continue
            
            # # Show History 
            if user_input == "history":
                history = calculator.get_history()
                if not history:
                    print("No history available.")
                else:
                    print("\nCalculation History:")
                    for entry in calculator.history:
                        print(f"{entry['Timestamp']}: {entry['Operation']} {entry['Input']} = {entry['Result']}")
                continue
            
            if user_input == "undo":
                calculator.undo()
                print("Last operation undone.")
                continue

            if user_input == "redo":
                calculator.redo()
                print("Last undone operation redone.")
                continue

            if user_input == "clear":
                calculator.clear_history()
                print("History cleared.")
                continue

         
            # Splits the user input into parts and checks if it has exactly three components
            input_split = user_input.split()
            if len(input_split) != 3:
                print("Error: Invalid input format. Please use: <operation> <number1> <number2> or type 'help' for available commands.")
                continue
            
            # Assign the split input to variables
            operator_cmd, str_a, str_b = input_split

            # Convert string inputs to floats
            a = float(str_a)
            b = float(str_b)
            

            # Perform the operation using the Calculator class
            result = calculator.execute_operation(operator_cmd, a, b)

            # Formatting the result to remove trailing zeros if it's a whole number
            if result.is_integer():
                print(f"Result: {int(result)}")
            else:
                print(f"Result: {result}")
        

        except ValueError as e:
            # Catch errors like typing a letter instead of a number, dividing by zero, or bad commands
            print(f"Error: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred in the Calculator REPL: {e}")
            print(f"An unexpected error occurred: {e}")

