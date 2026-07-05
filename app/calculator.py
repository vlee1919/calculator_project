
import copy
from datetime import datetime
from app.operations import OperationFactory
from app.calculator_memento import EventManager, MementoManager, HistoryManager
import os
from pathlib import Path

class Calculator:
    
    def __init__(self):


        self.history = []  # To store the history of operations
    
        self.memento_manager = MementoManager() # To manage the mementos for undo/redo functionality
        self.event_manager = EventManager() # To manage event notifications
        self.history_manager = HistoryManager()

        self.event_manager.attach(self.history_manager)



    def execute_operation(self, operator_cmd: str, a: float, b: float) -> float:
        """Executes the operation and manages history and mementos."""
        
        
        # Save the current state to memento before executing the operation
        self.memento_manager.backup(self.history.copy())
        

        operation = OperationFactory().get_operation(operator_cmd)
        result = operation.execute(a, b)

        calculation_record = {
                    "Operation": operator_cmd,
                    "Input": f"{a}, {b}",
                    "Result": result
                }
        self.history.append(calculation_record)
        self.event_manager.notify(calculation_record)

        return result

            

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