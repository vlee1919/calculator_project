
import copy
from datetime import datetime
from app.operations import OperationFactory
from app.calculator_memento import EventManager, MementoManager, HistoryManager


class Calculator:
    
    def __init__(self):
        self.history = []  # To store the history of operations
        self.memento_manager = MementoManager() # To manage the mementos for undo/redo functionality
        self.event_manager = EventManager() # To manage event notifications
        

    def execute_operation(self, operator_cmd: str, a: float, b: float) -> float:
        """Executes the operation and manages history and mementos."""
        operation = OperationFactory().get_operation(operator_cmd)
        result = operation.execute(a, b)
        
        # Save the current state to memento before executing the operation
        self.memento_manager.backup(self.history.copy())
        
        # Update history
        self.history.append({
            "Operation": operator_cmd,
            "Input": f"{a}, {b}",
            "Result": result,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # Notify the event manager about the operation
        self.event_manager.notify({
            "Operation": operator_cmd,
            "Input": f"{a}, {b}",
            "Result": result
        })
        return result

    """Start the operation based on user input."""
    # def start_operation(self, operator_cmd: str, a: float, b: float) -> float:
    #     """Start the operation based on user input."""
    #     operation = OperationFactory().get_operation(operator_cmd)
    #     self.result = operation.execute(a, b)
    #     return self.result
    
    def get_history(self):
        return self.history

    def save_history(self, filename="history.csv"):
        history_manager = HistoryManager(filename)
        for entry in self.history:
            history_manager.update(entry)

    def undo(self):
        self.history = self.memento_manager.undo()

    def redo(self):
        self.history = self.memento_manager.redo()

    def clear_history(self):
        self.memento_manager.backup(self.history)
        self.history.clear()