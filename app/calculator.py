
import copy
from datetime import datetime
from app.operations import OperationFactory
from app.calculator_memento import CalcMemento


class Calculator:
    
    def __init__(self):

        self.result = 0
        self.history = []

    def save_state(self):
        """Save the current state of the calculator."""
        state = {
            'result': self.result,
            'timestamp': datetime.datetime.now()
        }
        self.history.append(copy.deepcopy(state))

    def restore_state(self, index):
        """Restore the calculator to a previous state."""
        if 0 <= index < len(self.history):
            state = self.history[index]
            self.result = state['result']
            return True
        return False
    

    """Start the operation based on user input."""
    def start_operation(self, operator_cmd: str, a: float, b: float) -> float:
        """Start the operation based on user input."""
        operation = OperationFactory().get_operation(operator_cmd)
        self.result = operation.execute(a, b)
        return self.result
    

    def undo(self, memento: CalcMemento):
        """Undo the last operation."""
        if memento.undo():
            print("Undo successful.")
        else:
            print("No operations to undo.")
    
    def redo(self, memento: CalcMemento):
        """Redo the last undone operation."""
        if memento.redo():
            print("Redo successful.")
        else:
            print("No operations to redo.")
    
    def get_history(self):
        """Return the history of operations."""
        return self.history
    
    def clear_history(self):
        """Clear the history of operations."""
        self.history.clear()