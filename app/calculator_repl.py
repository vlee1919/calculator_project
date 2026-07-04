"""
Calculator REPL 
"""
 
from app.operations import OperationFactory
from app.history import EventManager, AutoSaveObserver
from app.calculator import Calculator


class calculatorapp:
    def __init__(self):
        """Initialize the app and set up the observer."""
        # Setup the Event Manager
        self.event_manager = EventManager()
        
        # Setup the Logger and attach it
        self.logger = AutoSaveObserver("history.csv")
        self.event_manager.attach(self.logger)
        
        # Setup the Operation Factory
        self.factory = OperationFactory()
        
    def calculator_repl(self):
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
                
                # History Command
                if user_input == "history":
                    if self.logger.df.empty:
                        print("No history available.")
                    else:
                        print(self.logger.df)
                    continue

                # Clear History Command
                if user_input == "clear":
                    self.logger.df = self.logger.df.iloc[0:0]  # Clear the DataFrame
                    self.logger.df.to_csv(self.logger.filepath, index=False)  # Save the cleared DataFrame
                    print("History cleared.")
                    continue
                
                if user_input == "undo":
                    calculator.undo()
                    print("Operation has been undone.")
                    continue

                if user_input == "redo":
                    calculator.redo()
                    print("Operation has been redone.")
                    continue
                    
                # Splits the user input into parts and checks if it has exactly three components
                input_split = user_input.split()
                if len(input_split) != 3:
                    print("Error: Invalid input format. Please use: <operation> <number1> <number2>")
                    continue
                
                # Assign the split input to variables
                operator_cmd, str_a, str_b = input_split
                
                # Convert string inputs to floats
                a = float(str_a)
                b = float(str_b)
                

                # Perform the operation using the Calculator class
                result = calculator.start_operation(operator_cmd, a, b)


                # Formatting the result to remove trailing zeros if it's a whole number
                if result.is_integer():
                    print(f"Result: {int(result)}")
                else:
                    print(f"Result: {result}")
                
                """Logger"""
                # Notify the logger about the operation
                if self.event_manager:
                    self.event_manager.notify({
                        "Operation": operator_cmd,
                        "Input": f"{a}, {b}",
                        "Result": result
                    })


            except ValueError as e:
                # Catch errors like typing a letter instead of a number, dividing by zero, or bad commands
                print(f"Error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

