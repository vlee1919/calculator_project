from abc import ABC, abstractmethod
import pandas as pd
import datetime
from pathlib import Path 

"""Observer base class and implementation for logging calculator operations to a CSV file."""
class Observer(ABC):
    @abstractmethod
    def update(self, data: dict):
        """Receive update from subject."""
        pass

class HistoryLogger(Observer):
    def __init__(self, filename="history.csv"):
        # Get the absolute path to the directory where this file exists
        current_dir = Path(__file__).parent
        
        # Join that directory with desired filename
        self.filepath = current_dir / filename 
        
        self.columns = ["Timestamp", "Operation", "Input", "Result"]
        
        # Check if the file already exists. If it does, read it; if not, create a new one.
        if self.filepath.exists():
            self.df = pd.read_csv(self.filepath)
        else:
            self.df = pd.DataFrame(columns=self.columns)

    """ Update method to log the data to a CSV file"""
    def update(self, data: dict):
        data['Timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = pd.DataFrame([data])
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        self.df.to_csv(self.filepath, index=False)
        
        # Print a message indicating where the file was saved
        print(f"Saved calculation to {self.filepath}")

""" Event Manager class to manage observers and notify them of events."""
class EventManager:
    def __init__(self):
        self.subscribers = []

    def attach(self, observer):
        if observer not in self.subscribers:
            self.subscribers.append(observer)

    def notify(self, data: dict):
        """Broadcast the data to all subscribers."""
        for observer in self.subscribers:
            observer.update(data)