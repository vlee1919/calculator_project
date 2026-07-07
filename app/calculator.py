
import copy
from datetime import datetime
from app.operations import OperationFactory
from app.calculator_memento import EventManager, MementoManager, HistoryManager
from app.calculator_config import CalculatorConfig
import os
from pathlib import Path
import logging
import pandas as pd
from typing import Any, Dict, List, Optional, Union

class Calculator:
    
    def __init__(self, config: Optional[CalculatorConfig] = None):


        self.history = []  # To store the history of operations
    
        self.memento_manager = MementoManager() # To manage the mementos for undo/redo functionality
        self.event_manager = EventManager() # To manage event notifications
        self.history_manager = HistoryManager()

        self.event_manager.attach(self.history_manager)
        
        
        self.config = CalculatorConfig

        if config is None:
            # Determine the project root directory if no configuration is provided
            current_file = Path(__file__)
            project_root = current_file.parent.parent
            config = CalculatorConfig(base_directory=project_root)


        os.makedirs(self.config.log_directory, exist_ok=True)
        self.setup_logging()

        # Log: Successfully inititalize calculator
        logging.info("Succesfuly initialize Calculator")

        # Load previous history from CSV
        self.load_history()

    def load_history(self):

        if not self.history_manager.df.empty:
            self.history = self.history_manager.df.to_dict(orient="records")

    def setup_logging(self):
        """Setup logging as well as its configurations."""
        try:
            # Check if log directory exist --> make directory if not 
            os.makedirs(self.config.log_directory, exist_ok=True)
            log_file = self.config.log_file.resolve()

            # Logging configuration
            logging.basicConfig(
                filename="app.log", # log file
                level=logging.INFO,
                format="%(asctime)s - %(levelname)s - %(message)s",
            )
            
            logging.info(f"Logging initialized at: {log_file}")

        except Exception as e:
            print(f"Error initalizing logging.: {e}")
            raise
    

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
        # Save to history list
        self.history.append(calculation_record)

        # Notify observer --> HistoryManager will save to CSV
        self.event_manager.notify(calculation_record)


        self.history_manager.save()
        
        return result

            

    def get_history(self):
        return self.history

    def save_history(self, filename="history.csv"):
        history_manager = HistoryManager(filename)
        for entry in self.history:
            history_manager.update(entry)

    def undo(self):
        previous_state = self.memento_manager.undo(self.history)

        if previous_state is not None:
            self.history = previous_state

            self.history_manager.df = pd.DataFrame(self.history)
            self.history_manager.save() # Saves to CSV

            return True
        
        return False

    def redo(self):
        restored_state = self.memento_manager.redo(self.history)

        if restored_state is not None:
            self.history = restored_state

            self.history_manager.df = pd.DataFrame(self.history)
            self.history_manager.save() # Save to CSV

            return True
        
        return False
    

    # def redo(self):
    #     self.history = self.memento_manager.redo()

    def clear_history(self):
        self.memento_manager.backup(self.history)

        # Clear Calculation history
        self.history.clear()

        # Clear the dataframe
        self.history_manager.df = self.history_manager.df.iloc[0:0]

        # Save empty history to CSV
        self.history_manager.save()