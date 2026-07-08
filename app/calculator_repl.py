"""
Calculator REPL 
"""
import logging
from app.operations import OperationFactory
from app.calculator import Calculator
from app. calculator_memento import EventManager, HistoryManager, MementoManager
from app.input_validators import InputValidator
from colorama import init, Fore, Back, Style
init(autoreset=True)

def calculator_repl():
    print(Fore.CYAN + Style.BRIGHT + "===== Calculator REPL =====")
    print(Fore.YELLOW +"Format: <operation> <number1> <number2>")
    print(Fore.GREEN +"Please enter a mathematical operation or type 'help' to see available commands.")
    print(Fore.RED +"Enter 'exit' to quit the calculator.\n")

    # Initialize the Calculator
    calculator = Calculator()
    try:
        while True:
            try:
                # User Input
                user_input = input(Fore.CYAN +"Your input> ").strip().lower()
                
                # Exit command
                if user_input == "exit":
                    print(Fore.CYAN +"Exiting calculator. Goodbye!")
                    break
                
                # Help Command
                if user_input == "help":
                    print(Fore.MAGENTA + Style.BRIGHT +"Available Operations: add, subtract, multiply, divide, power, root, modulo, int_divide, percent, abs_diff")
                    print("Type 'history' to view the history of calculations.")
                    print("Type 'clear' to clear the history.")
                    print("Type 'undo' to undo the last operation.")
                    print("Type 'redo' to redo the last undone operation.")
                    print("Type 'save' to manually save calculation history.")
                    print("Type 'load' to manually load calculation history.")
                    print("Type 'help' to see this message again.")
                    print("Type 'exit' to quit the calculator.")
                    continue
                
                # # Show History 
                if user_input == "history":
                    history = calculator.get_history()
                    if not history:
                        print("No history available.")
                    else:
                        print(Fore.CYAN + Style.BRIGHT +"\nCalculation History:")
                        for entry in history:
                            print(f"{entry['Timestamp']}: {entry['Operation']} {entry['Input']} = {entry['Result']}")
                    continue
                
                # Undo 
                if user_input == "undo":
                    if calculator.undo():
                        print(Fore.GREEN +"Last operation undone.")
                    else:
                        print(Fore.YELLOW +"Nothing to undo.")
                    continue
                
                # Redo
                if user_input == "redo":
                    if calculator.redo():
                        print(Fore.GREEN +"Last undone operation redone.")
                    else:
                        print(Fore.YELLOW +"Nothing to redo.")
                    continue
                
                # Clear History
                if user_input == "clear":
                    calculator.clear_history()
                    print(Fore.GREEN +"History cleared.")
                    continue
                
                # Manually save to history
                if user_input == "save":
                    calculator.save_history()
                    print(Fore.GREEN +"History saved.")
                    continue
                
                # Manually load from history
                if user_input == "load":
                    calculator.load_history()
                    print(Fore.GREEN +"History loaded.")
                    continue
                
                if user_input in ["add",
                                "subtract",
                                "multiply",
                                "divide",
                                "power",
                                "root",
                                "modulo",
                                "int_divide",
                                "percent",
                                "abs_diff"
                                ]:    
                    try:
                        # Check user input data type and see if its within configuration range
                        validator = InputValidator() 
                        
                        a = validator.validate_number(input("Type the first operand: "))
                        b = validator.validate_number(input("Type the second operand: "))

                        operator_cmd = user_input

                        # Perform the operation using the Calculator class
                        result = calculator.execute_operation(operator_cmd, a, b)

                        # Formatting the result to remove trailing zeros if it's a whole number
                        if result.is_integer():
                            print(f"Result: {int(result)}")
                        else:
                            print(Fore.GREEN + Style.BRIGHT + f"Result: {result}")

                    except ValueError as e:
                    # Catch errors like typing a letter instead of a number, dividing by zero, or bad commands
                        print(Fore.RED +f"Error: {e}")
                    continue
                else:
                    print(Fore.RED +f"Invalid operation: '{user_input}'. Please try again.")

            except KeyboardInterrupt:
                # Ctrl+C interruption 
                print(Fore.RED +"\nOperation cancelled")
                continue
            except Exception as e:
                print(Fore.RED +f"Error: {e}")
                continue

    except Exception as e:
        logging.error(f"An unexpected error occurred in the Calculator REPL: {e}")
        print(Fore.RED +f"An unexpected error occurred: {e}")

