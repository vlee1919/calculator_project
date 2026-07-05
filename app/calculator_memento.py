import pandas as pd
import datetime
from pathlib import Path 
import copy

class EventManager:
    def __init__(self):
        self.subscribers = []

    def attach(self, observer):
        self.subscribers.append(observer)

    def notify(self, data: dict):
        for subscriber in self.subscribers:
            subscriber.update(data)

"""The "Caretaker" class that manages the memento objects for undo and redo functionality."""
class HistoryManager:
    def __init__(self, filename="history.csv"):
            
        self.filepath = Path(__file__).parent / filename
        self.df = pd.DataFrame(columns=["Timestamp", "Operation", "Input", "Result"])
        if self.filepath.exists():
            self.df = pd.read_csv(self.filepath)
        
    def update(self, data: dict):
        """"Update the history with a new calculation entry."""
        data['Timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = pd.DataFrame([data])
        self.df = pd.concat([self.df, new_row], ignore_index=True)
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

    def backup(self, state):
        """Add to the undo stack and clear the redo stack when a new operation is performed."""
        self.undo_stack.append(Memento(state))
        self.redo_stack.clear()

    def undo(self):
        """Pop from the undo stack and push to the redo stack."""
        if self.undo_stack:
            memento = self.undo_stack.pop()
            self.redo_stack.append(Memento(memento.state))
            return memento.state
        return None

    def redo(self):
        """Pop from the redo stack and push to the undo stack."""
        if self.redo_stack:
            memento = self.redo_stack.pop()
            self.undo_stack.append(Memento(memento.state))
            return memento.state
        return None


