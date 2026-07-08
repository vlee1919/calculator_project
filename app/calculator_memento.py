import pandas as pd
import datetime
from pathlib import Path 
import copy
from app.calculator_config import CalculatorConfig
import os
from pandas.errors import EmptyDataError
import logging
from abc import ABC, abstractmethod

class Observer(ABC):
# Abstract class for Observer
    @abstractmethod
    def update(self, data: dict):
        pass

class EventManager:
    # Initialize an empty list of subscribers
    def __init__(self):
        self.subscribers = []
        
    # Attaches a new observer --> HistoryManager
    def attach(self, observer):
        self.subscribers.append(observer)

    # Notify the subscriber when an event has occured
    def notify(self, data: dict):
        for subscriber in self.subscribers:
            subscriber.update(data)

"""The "Caretaker" class that manages the memento objects for undo and redo functionality."""
class HistoryManager(Observer):
    def __init__(self, config: CalculatorConfig):
        self.config = config
        self.filepath = config.history_file

        # Check if history directory exist
        os.makedirs(self.config.history_directory, exist_ok=True)
        
        self.df = pd.DataFrame(columns=["Timestamp", 
                                         "Operation", 
                                         "Input", 
                                         "Result"])

        if self.filepath.exists() and self.filepath.stat().st_size > 0: # Check if the file is not 0 bytes
            try:
                self.df = pd.read_csv(
                    self.filepath,
                    encoding=self.config.default_encoding
                )
            except EmptyDataError:
                pass
        else:
            self.save() # If the file is empty, it will call save which creates the csv with the timestamps
    
    # Update the history with new calculation entry. Save to a dataframe.
    def update(self, data: dict):
        data['Timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Add timestamp to the record
        new_row = pd.DataFrame([data]) # Convert dictionary to dataframe
        self.df = pd.concat([self.df, new_row], ignore_index=True) # Add to current existing history & renumber index rows
    
    # Save to CSV from Dict
    def save(self):    
        self.df.to_csv(self.filepath, 
                       index=False, 
                       encoding=self.config.default_encoding) # Serialize data
        print(f"History saved to {self.filepath}") 
    
    # Load history from CSV to Dict
    # def load_history(self):
    #     if self.filepath.exists() and self.filepath.stat().st_size > 0:
    #         self.df = pd.read_csv(
    #             self.filepath,
    #             encoding=self.config.default_encoding
    #             )
    #     else:
    #         self.df = pd.DataFrame(
    #             columns=["Timestamp", "Operation", "Input", "Result"]
    #             )
    #     return self.df.to_dict(orient="records")

    def load_history(self):
        if self.filepath.exists():
            try:
                self.df = pd.read_csv(
                    self.filepath,
                    encoding=self.config.default_encoding
                )
            except EmptyDataError:
                self.df = pd.DataFrame(
                    columns=["Timestamp", "Operation", "Input", "Result"]
                )
                self.save()
        else:
            self.df = pd.DataFrame(
                columns=["Timestamp", "Operation", "Input", "Result"]
            )
            self.save()

        return self.df.to_dict(orient="records")

class Memento:
    # Object with a copy of the calculator's state.
    def __init__(self, state):
        self.state = copy.deepcopy(state)

class MementoManager:
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    # Back up state to undo stack
    def backup(self, state):
        # Add to the undo stack and clear the redo stack when a new operation is performed.
        self.undo_stack.append(Memento(state))
        self.redo_stack.clear()

    # Undo function
    def undo(self, current_state):
        if self.undo_stack:
            previous = self.undo_stack.pop()

            # send to redo stack
            self.redo_stack.append(Memento(current_state))
            return previous.state
        return None

    # Redo function
    def redo(self, current_state):
        if self.redo_stack:
            restored = self.redo_stack.pop()
            
            # send to undo stack
            self.undo_stack.append(Memento(current_state))
            return restored.state
        return None

# Automatically save when calculation is performed
class AutoSaveObserver(Observer):
    def __init__(self, history_manager: HistoryManager):
        self.history_manager = history_manager
    def update(self, data: dict):
        self.history_manager.save()

# Log the operation, input and result
class LoggingObserver(Observer):
    def update(self, data: dict):
        logging.info(
            f"{data['Operation']} | "
            f"{data['Input']} = "
            f"{data['Result']}"
        )