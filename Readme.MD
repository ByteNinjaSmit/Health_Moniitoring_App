Here's the updated README.md file with the added instructions for running the application, along with the requirements.txt instructions:

# Health Monitor Application

This repository contains a health monitoring application built with Python. The application includes features such as user authentication using a SQL database and health monitoring using data science techniques.

## Overview

The Health Monitor Application allows users to create an account, log in, and access various health monitoring features. Users can input personal information such as name, birth date, gender, height, and weight, which are stored securely in a SQLite database. The application provides functionalities for monitoring heart rate status, tracking hydration, calculating BMI (Body Mass Index), checking physical health metrics, updating weight and height, generating diet plans, and more.

## Getting Started

To get started with the application, follow the steps below:

## How it Works

Showed At Last In detailed Information

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

## How to Run the Application

1. Make sure you have Python installed on your system.
2. Clone this repository to your local machine.
3. Navigate to the project directory.
4. Install the required Python packages listed in `requirements.txt` by running:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the application by executing the `Main.py` file:
   ```bash
   python Main.py
   ```
6. Follow the on-screen instructions to interact with the application and explore its features.

Feel free to explore the code and contribute to its development!

---


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

# Health Monitor Application

This repository contains a health monitoring application built with Python. The application includes features such as user authentication using a SQL database, health monitoring using data science techniques, and a graphical user interface (GUI) for easy interaction.


## How it Works

### User Authentication:

- Users can create an account by providing a username and password.
- Existing users can log in using their credentials.
- Passwords are securely stored using encryption techniques.

### Personal Information:

- Upon logging in, users can view their personal information, including name, birth date, gender, height, and weight.
- Additional information such as age is calculated dynamically based on the birth date provided by the user.

### Health Monitoring Features:

1. **Heart Rate Status:**
   - Users can input their heart rate to check their heart rate status.
   - The application calculates heart rate status based on age, gender, and heart rate input.
   
2. **Hydration Tracking:**
   - Users can track their hydration levels throughout the day.
   - The application provides reminders to drink water and monitors progress towards hydration goals.

3. **BMI Calculation and Fitness Check:**
   - Users can calculate their BMI (Body Mass Index) based on their height and weight.
   - The application categorizes BMI into different fitness levels (Underweight, Normal weight, Overweight, Obese) and provides fitness recommendations.

4. **Physical Health Monitor:**
   - Users can access a graphical interface to monitor their physical health metrics.
   - The application displays visual representations of health data using charts and graphs.

5. **Weight and Height Update:**
   - Users can update their weight and height information at any time.
   - The application stores historical weight data for tracking progress over time.

6. **Diet Plan Generation:**
   - Users can generate personalized diet plans based on their current weight, target BMI, daily calorie burn, and dietary preferences.
   - The application provides meal suggestions and estimated timeframes for achieving weight goals.

### Graphical User Interface (GUI):

- The application features a graphical user interface (GUI) built using the Tkinter library.
- Users can interact with the application seamlessly through the GUI, making it user-friendly and intuitive.
