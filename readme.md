# Enhanced Calculator Application

## Project Description
The Enhanced Calculator Application is a command-line application that demonstrates object-oriented programming concepts and several software design patterns. It supports common arithmetic operations while maintaining a  calculation history, logging user activity, and providing undo/redo functionality.

---
## Features
- Addition
- Subtraction
- Multiplication
- Division
- Power
- Root
- Modulus
- Integer Division
- Percentage
- Absolute Difference
- Undo and Redo

- Calculation history (CSV)
- Automatic history saving
- Manual save and load commands
- Application logging
- Configurable settings using a `.env` file
---


# Installation

## Clone the repository

```bash
git clone <repository-url>
cd <repository-name>
```

## Create a virtual environment

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

---

# Configuration

The calculator uses environment variables stored in a `.env` file.

Create a file named
```
.env
```
in the project root.

Example:

```env
CALCULATOR_BASE_DIR=.
CALCULATOR_HISTORY_DIRECTORY=history
CALCULATOR_HISTORY_FILE=history/calculator_history.csv

CALCULATOR_LOG_DIR=logs
CALCULATOR_LOG_FILE=logs/calculator.log

CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=10
CALCULATOR_MAX_INPUT_VALUE=1000000
CALCULATOR_DEFAULT_ENCODING=utf-8
```

The application automatically creates the history and log directories if they do not already exist.

---

# Running the Calculator

Start the calculator with

```bash
python main.py
```

The calculator launches an interactive command-line interface.

Example:

```
Your input> add

Type the first operand: 5

Type the second operand: 7

Result: 12
```

---

# Available Commands

| Command | Description |
|----------|-------------|
| add | Addition |
| subtract | Subtraction |
| multiply | Multiplication |
| divide | Division |
| power | Exponentiation |
| root | Root calculation |
| modulus | Modulus |
| int_divide | Integer division |
| percent | Percentage |
| abs_diff | Absolute difference |
| history | Display calculation history |
| undo | Undo previous calculation |
| redo | Redo previous calculation |
| clear | Clear calculation history |
| save | Save history to CSV |
| load | Load history from CSV |
| help | Display available commands |
| exit | Exit the calculator |

---

# Calculation History

Calculation history is stored as a CSV file using pandas.

Each record contains:

- Timestamp
- Operation
- Input
- Result

History can be:

- automatically saved after each calculation
- manually saved using the `save` command
- manually loaded using the `load` command

---

# Logging

The calculator uses Python's built-in `logging` module.

Log entries include:

- calculator startup
- calculations performed
- undo operations
- redo operations
- manual history saves
- manual history loads
- cleared history
- errors

Logs are written to:

```
logs/calculator.log
```

The log location can be changed in the `.env` configuration.

---

# Testing

Run all unit tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

Enforce minimum coverage:

```bash
pytest --cov=app --cov-fail-under=90
```