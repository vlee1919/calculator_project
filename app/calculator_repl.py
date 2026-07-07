"""
Calculator REPL 
"""
import logging
from app.operations import OperationFactory
from app.calculator import Calculator
from app. calculator_memento import EventManager, HistoryManager, MementoManager
from app.exceptions import OperationError, ValidationError

def calculator_repl():
    print("Calculator REPL")
    print("Format: <operation> <number1> <number2>")
    print("Please enter a mathematical operation or type 'help' to see available commands.")
    print("Enter 'exit' to quit the calculator.\n")

    # Initialize the Calculator
    calculator = Calculator()

    while True:
        try:
            
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
                    for entry in history:
                        print(f"{entry['Timestamp']}: {entry['Operation']} {entry['Input']} = {entry['Result']}")
                continue
            
            # Undo 
            if user_input == "undo":
                if calculator.undo():
                    print("Last operation undone.")
                else:
                    print("Nothing to undo.")
                continue
            
            # Redo
            if user_input == "redo":
                if calculator.redo():
                    print("Last undone operation redone.")
                else:
                    print("Nothing to redo.")
                continue
            
            # Clear History
            if user_input == "clear":
                calculator.clear_history()
                print("History cleared.")
                continue
            
            # Manually save to history
            if user_input == "save":
                calculator.save_history()
                print("History saved.")
                continue
            
            # Manually load from history
            if user_input == "load":
                calculator.load_history()
                print("History loaded.")
                continue
            
            if user_input in ["add",
                              "subtract",
                              "multiply",
                              "divide",
                              "power",
                              "root",
                              "modulus",
                              "int_divide",
                              "percent",
                              "abs_diff"
                            ]:
                try:

                    # Get the first and second operand
                    a = float(input("Type the first operand: "))
                    b = float(input("Type the second operand: "))
            
                    operator_cmd = user_input

                    # Perform the operation using the Calculator class
                    result = calculator.execute_operation(operator_cmd, a, b)

                    # Formatting the result to remove trailing zeros if it's a whole number
                    if result.is_integer():
                        print(f"Result: {int(result)}")
                    else:
                        print(f"Result: {result}")
                
                except KeyboardInterrupt:
                    # Handle Ctrl+C interruption gracefully
                    print("\nOperation cancelled")
                    continue
                except EOFError:
                    # Handle end-of-file (e.g., Ctrl+D) gracefully
                    print("\nInput terminated. Exiting...")
                    break

                except Exception as e:
                    print(f"Error: {e}")
                    continue

        except ValueError as e:
            # Catch errors like typing a letter instead of a number, dividing by zero, or bad commands
            print(f"Error: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred in the Calculator REPL: {e}")
            print(f"An unexpected error occurred: {e}")

