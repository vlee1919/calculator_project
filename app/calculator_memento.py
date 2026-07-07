import pandas as pd
import datetime
from pathlib import Path 
import copy

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
class HistoryManager:
    def __init__(self, filename="history.csv"):
            
        history_dir = Path(__file__).parent / "history"
        history_dir.mkdir(exist_ok=True)

        self.filepath = history_dir / filename

        self.df = pd.DataFrame(columns=["Timestamp", 
                                        "Operation", 
                                        "Input", 
                                        "Result"])
        if self.filepath.exists():
            self.df = pd.read_csv(self.filepath)
    
    # Update the history with new calculation entry. Save to a dataframe.
    def update(self, data: dict):
        data['Timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Add timestamp to the record
        new_row = pd.DataFrame([data]) # Convert dictionary to dataframe
        self.df = pd.concat([self.df, new_row], ignore_index=True) # Add to current existing history & renumber index rows
    
    # Save to CSV
    def save(self):    
        self.df.to_csv(self.filepath, index=False)
        print(f"Saved calculation to {self.filepath}")

class Memento:
    # Object with a copy of the calculator's state.
    def __init__(self, state):
        self.state = copy.deepcopy(state)

class MementoManager:
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    # Back up to the 
    def backup(self, state):
        print("Backing up:", state)
        # Add to the undo stack and clear the redo stack when a new operation is performed.
        self.undo_stack.append(Memento(state))
        self.redo_stack.clear()


    # Undo 
    def undo(self, current_state):
        if self.undo_stack:
            previous = self.undo_stack.pop()

            # send to redo stack
            self.redo_stack.append(Memento(current_state))

            return previous.state

        return None

    # Redo 
    def redo(self, current_state):
        if self.redo_stack:
            restored = self.redo_stack.pop()

            # send to undo stack
            self.undo_stack.append(Memento(current_state))

            return restored.state

        return None