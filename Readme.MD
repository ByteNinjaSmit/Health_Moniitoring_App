Here's the updated README.md file with the added instructions for running the application, along with the requirements.txt instructions:

# Health Monitor Application

This repository contains a health monitoring application built with Python. The application includes features such as user authentication using a SQL database and health monitoring using data science techniques.

## Getting Started

To get started with the application, follow the steps below:

### Start in Virtual Environment

Before running the application, it's recommended to set up a virtual environment to manage dependencies.

#### For Windows:

```bash
myenv\Scripts\activate
```

#### For macOS / Linux:

```bash
source myenv/bin/activate
```

#### Deactivate Virtual Environment:

To deactivate the virtual environment, simply run:

```bash
deactivate
```

### Database Connected File

The `Main.py` file in this repository is responsible for handling user authentication and database connection.

### Health Monitor

The health monitoring functionality of the application is implemented in two files:

- `Health_Monitor.ipynb`: This Jupyter Notebook contains the logic and analysis for health monitoring using data science techniques.

- `health_monitor.py`: This Python script contains the implementation of the health monitoring functionality without GUI.

- `Health_Monitor_GUI.py`: This Python file provides a graphical user interface (GUI) for interacting with the health monitoring functionality.

### Required Packages

Before running the application, make sure to install the following Python packages:

- sqlite3
- plyer
- pyfiglet
- tkinter
- tkcalendar
- pandas
- matplotlib

You can install these packages using pip:

```bash
pip install sqlite3 plyer pyfiglet tkinter tkcalendar pandas matplotlib
```

### Additional Imports

Make sure to include the following imports in your Python files:

```python
import sqlite3
import os
import time
from plyer import notification
from datetime import datetime
import pyfiglet 
import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Health_Monitor_GUI import run_health_data_entry
```

### Running the Application

To run the application, execute the `Main.py` file using Python:

```bash
pip install -r requirements.txt
python Main.py
```
