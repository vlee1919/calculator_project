
from datetime import datetime
from app.operations import OperationFactory
from app.calculator_memento import EventManager, MementoManager, HistoryManager, LoggingObserver, AutoSaveObserver
from app.calculator_config import CalculatorConfig
import os
from pathlib import Path
import logging
import pandas as pd
from typing import Optional

class Calculator:
    def __init__(self, config: Optional[CalculatorConfig] = None):

        if config is None:
            config = CalculatorConfig()
        
        self.config = config
    
        self.memento_manager = MementoManager() # To manage the mementos for undo/redo functionality
        self.event_manager = EventManager() # To manage event notifications
        self.history_manager = HistoryManager(self.config) 


        # Create observers
        autosave = AutoSaveObserver(self.history_manager)
        logger = LoggingObserver()

        # Attach observers to this calculation session
        self.event_manager.attach(self.history_manager)
        self.event_manager.attach(autosave)
        self.event_manager.attach(logger)


        # Check if log directory exist --> if not, create directory
        os.makedirs(self.config.log_directory, exist_ok=True)
        self.setup_logging()

        # Log: Successfully inititalize calculator
        logging.info("Succesfuly initialize Calculator")

        # load history from CSV
        self.history = self.history_manager.load_history()


    def setup_logging(self):

        """Setup logging as well as its configurations."""
        try:
            # Check if log directory exist --> make directory if not 
            os.makedirs(self.config.log_directory, exist_ok=True)
            log_file = self.config.log_file.resolve()

            # Logging configuration
            logging.basicConfig(
                filename=str(self.config.log_file), # log file path
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

        try:
            result = operation.execute(a, b)
        except Exception as e:
            logging.error(f"Calculation failed: {e}")
            raise
        
        calculation_record = {
                    "Operation": operator_cmd,
                    "Input": f"{a}, {b}",
                    "Result": result
                }
        # Save to history list
        self.history.append(calculation_record)

        # Notify observer
        self.event_manager.notify(calculation_record)

        return result

            
    # Retrieve history in current session
    def get_history(self):
        return self.history

    # Undo --> call undo function from calculator_memento
    def undo(self):
        previous_state = self.memento_manager.undo(self.history)

        if previous_state is not None:
            self.history = previous_state
            self.history_manager.df = pd.DataFrame(self.history)
            self.history_manager.save() # Saves to CSV

            logging.info("Undo operation executed.")           
            return True
        return False

    # Redo--> call redo function from calculator_memento
    def redo(self):
        restored_state = self.memento_manager.redo(self.history)

        if restored_state is not None:
            self.history = restored_state
            self.history_manager.df = pd.DataFrame(self.history)
            self.history_manager.save() # Save to CSV

            logging.info("Redo operation executed.")       
            return True
        return False
    
    # Clear History 
    def clear_history(self):
        self.memento_manager.backup(self.history)

        # Clear Calculation history
        self.history.clear()
        # Clear the dataframe
        self.history_manager.df = self.history_manager.df.iloc[0:0]
        # Save empty history to CSV
        self.history_manager.save()
        logging.info("History cleared.")

    # Manually save the calculation history to the CSV file
    def save_history(self):
        self.history_manager.save()
        logging.info("History manually saved.")

    # Manually load calculation history from the CSV file
    def load_history(self):
        self.history = self.history_manager.load_history()
        logging.info("History manually loaded.")