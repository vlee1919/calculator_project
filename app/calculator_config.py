"""Calculator Configuration"""

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
def get_project_root():
    # current directory --> app/calculator_config.py
    current_directory = Path(__file__)
    # app --> calc_project
    return current_directory.parent.parent

class CalculatorConfig:

    def __init__(self, 
        base_directory=None, 
        max_history_size = None,
        auto_save=None,
        precision=None,
        max_input_value=None,
        default_encoding=None
    ):
        """Base Directory"""
        project_root = get_project_root()
        self.base_directory = base_directory or Path(
            os.getenv('CALCULATOR_BASE_DIR', str(project_root))
        ).resolve()


        """History Settings"""
        
        # Set max history size
        self.max_history_size = max_history_size or int(
            os.getenv('CALCULATOR_MAX_HISTORY_SIZE', '100')
        )

        # Auto-save 
        auto_save_env = os.getenv('CALCULATOR_AUTO_SAVE', 'true').lower()
        self.auto_save = auto_save if auto_save is not None else (
            auto_save_env == 'true' or auto_save_env == "1"
        )

        """Calculation Settings"""

        # Set the decimal place of the result
        self.precision = precision or int(
            os.getenv('CALCULATOR_PRECISION', '10')
        )

        # Set max allowed input
        self.max_input_value = max_input_value or float(
            os.getenv('CALCULATOR_MAX_INPUT_VALUE', "1e999")
        )

        # Set default encoding for files
        self.default_encoding = default_encoding or os.getenv(
            'CALCULATOR_DEFAULT_ENCODING', 'utf-8'
        )


    @property
    def log_directory(self):
        # Log director path
        return Path(os.getenv(
            'CALCULATOR_LOG_DIR',
            str(self.base_directory / "logs")
        )).resolve()

    @property
    def log_file(self) -> Path:
        # File path for storing log 
        return Path(os.getenv(
            'CALCULATOR_LOG_FILE',
            str(self.log_directory / "calculator.log")
        )).resolve()    
    
    @property
    def history_directory(self):
        return Path(os.getenv(
            'CALCULATOR_HISTORY_DIRECTORY',
            str(self.base_directory / "history")
        )).resolve()

    @property
    def history_file(self):
        # History file path 
        return Path(os.getenv(
            'CALCULATOR_HISTORY_FILE',
            str(self.history_directory/ "calculator_history.csv")
        )).resolve()
    