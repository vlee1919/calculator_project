

"""Manages the undo and redo functionality for the calculator."""
class CalcMemento:
    def __init__(self, calculator):
        self.calculator = calculator
        self.undo_stack = []
        self.redo_stack = []

    def backup(self):
        """Save the current state of the calculator."""
        self.undo_stack.append(self.calculator.save_state())
        # Clear the redo stack whenever a new operation is performed
        self.redo_stack.clear()
    
    def undo(self):
        """Restore the calculator to the previous state."""
        if self.undo_stack:
            # Save the current state to the redo stack before undoing
            self.redo_stack.append(self.calculator.save_state())
            last_state = self.undo_stack.pop()
            self.calculator.restore_state(last_state)
            return True
        return False
    
    def redo(self):
        """Restore the calculator to the next state."""
        if self.redo_stack:
            # Save the current state to the undo stack before redoing
            self.undo_stack.append(self.calculator.save_state())
            next_state = self.redo_stack.pop()
            self.calculator.restore_state(next_state)
            return True
        return False

    