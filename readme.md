# Triangle_Classifier

This project provides an interface for managing and visualizing data stored in a PostgreSQL database. It uses Python for backend operations and Shiny for the user interface.

## Application Behavior

- **Inputs**: New line-separated strings. Words in a string are separated by white space. When there are three separate words in a string, and each word is a number, the application outputs one word from the set [“Scalene”, “Isosceles”, “Equilateral”, “NoTriangle”].
- **Outputs**: One word from the set [“Scalene”, “Isosceles”, “Equilateral”, “NoTriangle”] is printed on stdout. Error strings are printed on stderr. Causes for errors include cases where the input string cannot be classified or execution errors.
- **Operation**: The application exits when the input string contains the word “Exit” or the word “Quit” at the beginning of the string.

## Prerequisites

- Python 3.8+
- Shiny for Python

### For the test script
- Selenium for Python
- ChromeDriver for the latest version of chrome

## Installation


### Step 1: Set Up Python Environment

1. Set up a Python virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install shiny
   pip install selenium

### Step 2:  Launch the Shiny App
   ```bash
   python path/to/app.py
   ```

### Step 3:  Launch the test app
   ```bash
   python path/to/test.py
   ```

## Usage
- Once the Shiny app is running, navigate to the provided URL (typically http://localhost:8080/).
- The test app will execute the test cases (designed for the app) to test the app's main feature.