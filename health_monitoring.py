import calendar
import sqlite3
from sqlite3 import Error
import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import datetime


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Successfully connected to SQLite version: {sqlite3.version}")
    except Error as e:
        print(e)
    return conn

def create_users_table(conn):
    sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                    id INTEGER PRIMARY KEY,
                                    username TEXT NOT NULL UNIQUE,
                                    password TEXT NOT NULL,
                                    height REAL NOT NULL,
                                    weight REAL NOT NULL,
                                    age INTEGER NOT NULL
                                );"""
    try:
        c = conn.cursor()
        c.execute(sql_create_users_table)
    except Error as e:
        print(e)

def create_activity_table(conn):
    sql_create_activity_table = """CREATE TABLE IF NOT EXISTS activity (
                                        id INTEGER PRIMARY KEY,
                                        user_id INTEGER NOT NULL,
                                        date TEXT NOT NULL,
                                        activity TEXT NOT NULL,
                                        duration INTEGER NOT NULL,
                                        FOREIGN KEY(user_id) REFERENCES users(id)
                                    );"""
    try:
        c = conn.cursor()
        c.execute(sql_create_activity_table)
    except Error as e:
        print(e)

def create_nutrition_table(conn):
    sql_create_nutrition_table = """CREATE TABLE IF NOT EXISTS nutrition (
                                        id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                                        date TEXT NOT NULL,
                                        calories INTEGER NOT NULL,
                                        FOREIGN KEY(user_id) REFERENCES users(id)
                                    );"""
    try:
        c = conn.cursor()
        c.execute(sql_create_nutrition_table)
    except Error as e:
        print(e)

def create_sleep_table(conn):
    sql_create_sleep_table = """CREATE TABLE IF NOT EXISTS sleep (
                                        id INTEGER PRIMARY KEY,
                                        user_id INTEGER NOT NULL,
                                date TEXT NOT NULL,
                                        hours REAL NOT NULL,
                                        FOREIGN KEY(user_id) REFERENCES users(id)
                                    );"""
    try:
        c = conn.cursor()
        c.execute(sql_create_sleep_table)
    except Error as e:
        print(e)

def create_heart_rate_table(conn):
    sql_create_heart_rate_table = """CREATE TABLE IF NOT EXISTS heart_rate (
                                        id INTEGER PRIMARY KEY,
                                        user_id INTEGER NOT NULL,
                                        date TEXT NOT NULL,
                                        heart_rate INTEGER NOT NULL,
                                        FOREIGN KEY(user_id) REFERENCES users(id)
                                    );"""
    try:
        c = conn.cursor()
        c.execute(sql_create_heart_rate_table)
    except Error as e:
        print(e)

def create_blood_pressure_table(conn):
    sql_create_blood_pressure_table = """CREATE TABLE IF NOT EXISTS blood_pressure (
                                        id INTEGER PRIMARY KEY,
                                        user_id INTEGER NOT NULL,
                                        date TEXT NOT NULL,
                                        systolic INTEGER NOT NULL,
                                        diastolic INTEGER NOT NULL,
                                        FOREIGN KEY(user_id) REFERENCES users(id)
                                    );"""
    try:
        c = conn.cursor()
        c.execute(sql_create_blood_pressure_table)
    except Error as e:
        print(e)

def insert_user(conn, username, password, height, weight, age):
    sql_insert_user = '''INSERT INTO users(username,password,height,weight,age) VALUES(?,?,?,?,?);'''
    cur = conn.cursor()
    cur.execute(sql_insert_user, (username, password, height, weight, age))
    conn.commit()
    return cur.lastrowid

def authenticate_user(conn, username, password):
    sql_select_user = '''SELECT * FROM users WHERE username=? AND password=?;'''
    cur = conn.cursor()
    cur.execute(sql_select_user, (username, password))
    user = cur.fetchone()
    return user
def register_user(conn, username, password, height, weight, age):
    sql_check_user = '''SELECT COUNT(*) FROM users WHERE username=?;'''
    cur = conn.cursor()
    cur.execute(sql_check_user, (username,))
    count = cur.fetchone()[0]

    if count > 0:
        print("Username already exists. Please choose a different username.")
        return None
    else:
        sql_insert_user = '''INSERT INTO users(username,password,height,weight,age) VALUES(?,?,?,?,?);'''
        cur = conn.cursor()
        cur.execute(sql_insert_user, (username, password, height, weight, age))
        conn.commit()
        return cur.lastrowid
def add_activity(conn, activity):
    sql_insert_activity = '''INSERT INTO activity(user_id,date,activity,duration) VALUES(?,?,?,?);'''
    cur = conn.cursor()
    cur.execute(sql_insert_activity, activity)
    conn.commit()
    return cur.lastrowid

def add_nutrition(conn, nutrition):
    sql_insert_nutrition = '''INSERT INTO nutrition(user_id,date,calories) VALUES(?,?,?);'''
    cur = conn.cursor()
    cur.execute(sql_insert_nutrition, nutrition)
    conn.commit()
    return cur.lastrowid

def add_sleep(conn, sleep):
    sql_insert_sleep = '''INSERT INTO sleep(user_id,date,hours) VALUES(?,?,?);'''
    cur = conn.cursor()
    cur.execute(sql_insert_sleep, sleep)
    conn.commit()
    return cur.lastrowid

def add_heart_rate(conn, heart_rate):
    sql_insert_heart_rate = '''INSERT INTO heart_rate(user_id,date,heart_rate) VALUES(?,?,?);'''
    cur = conn.cursor()
    cur.execute(sql_insert_heart_rate, heart_rate)
    conn.commit()
    return cur.lastrowid

def add_blood_pressure(conn, blood_pressure):
    sql_insert_blood_pressure = '''INSERT INTO blood_pressure(user_id,date,systolic,diastolic) VALUES(?,?,?,?);'''
    cur = conn.cursor()
    cur.execute(sql_insert_blood_pressure, blood_pressure)
    conn.commit()
    return cur.lastrowid

def get_activity_by_date(conn, user_id, date):
    sql_select_activity = '''SELECT * FROM activity WHERE user_id=? AND date=?;'''
    cur = conn.cursor()
    cur.execute(sql_select_activity, (user_id, date))
    activity = cur.fetchone()
    return activity

def get_nutrition_by_date(conn, user_id, date):
    sql_select_nutrition = '''SELECT * FROM nutrition WHERE user_id=? AND date=?;'''
    cur = conn.cursor()
    cur.execute(sql_select_nutrition, (user_id, date))
    nutrition = cur.fetchone()
    return nutrition

def get_sleep_by_date(conn, user_id, date):
    sql_select_sleep = '''SELECT * FROM sleep WHERE user_id=? AND date=?;'''
    cur = conn.cursor()
    cur.execute(sql_select_sleep, (user_id, date))
    sleep = cur.fetchone()
    return sleep

def get_heart_rate_by_date(conn, user_id, date):
    sql_select_heart_rate = '''SELECT * FROM heart_rate WHERE user_id=? AND date=?;'''
    cur = conn.cursor()
    cur.execute(sql_select_heart_rate, (user_id, date))
    heart_rate = cur.fetchone()
    return heart_rate

def get_blood_pressure_by_date(conn, user_id, date):
    sql_select_blood_pressure = '''SELECT * FROM blood_pressure WHERE user_id=? AND date=?;'''
    cur = conn.cursor()
    cur.execute(sql_select_blood_pressure, (user_id, date))
    blood_pressure = cur.fetchone()
    return blood_pressure

def get_activity_logs(conn, user_id):
    sql_select_activity_logs = '''SELECT date, activity, duration FROM activity WHERE user_id=?;'''
    cur = conn.cursor()
    cur.execute(sql_select_activity_logs, (user_id,))
    activity_logs = cur.fetchall()
    return activity_logs

def get_nutrition_logs(conn, user_id):
    sql_select_nutrition_logs = '''SELECT date, calories FROM nutrition WHERE user_id=?;'''
    cur = conn.cursor()
    cur.execute(sql_select_nutrition_logs, (user_id,))
    nutrition_logs = cur.fetchall()
    return nutrition_logs

def get_sleep_logs(conn, user_id):
    sql_select_sleep_logs = '''SELECT date, hours FROM sleep WHERE user_id=?;'''
    cur = conn.cursor()
    cur.execute(sql_select_sleep_logs, (user_id,))
    sleep_logs = cur.fetchall()
    return sleep_logs

def get_heart_rate_logs(conn, user_id):
    sql_select_heart_rate_logs = '''SELECT date, heart_rate FROM heart_rate WHERE user_id=?;'''
    cur = conn.cursor()
    cur.execute(sql_select_heart_rate_logs, (user_id,))
    heart_rate_logs = cur.fetchall()
    return heart_rate_logs

def get_blood_pressure_logs(conn, user_id):
    sql_select_blood_pressure_logs = '''SELECT date, systolic, diastolic FROM blood_pressure WHERE user_id=?;'''
    cur = conn.cursor()
    cur.execute(sql_select_blood_pressure_logs, (user_id,))
    blood_pressure_logs = cur.fetchall()
    return blood_pressure_logs

def update_activity(conn, activity):
    sql_update_activity = '''UPDATE activity SET activity=?, duration=? WHERE id=?;'''
    cur = conn.cursor()
    cur.execute(sql_update_activity, activity)
    conn.commit()

def update_nutrition(conn, nutrition):
    sql_update_nutrition = '''UPDATE nutrition SET calories=? WHERE id=?;'''
    cur = conn.cursor()
    cur.execute(sql_update_nutrition, nutrition)
    conn.commit()

def update_sleep(conn, sleep):
    sql_update_sleep = '''UPDATE sleep SET hours=? WHERE id=?;'''
    cur = conn.cursor()
    cur.execute(sql_update_sleep, sleep)
    conn.commit()

def update_heart_rate(conn, heart_rate):
    sql_update_heart_rate = '''UPDATE heart_rate SET heart_rate=? WHERE id=?;'''
    cur = conn.cursor()
    cur.execute(sql_update_heart_rate, heart_rate)
    conn.commit()

def update_blood_pressure(conn, blood_pressure):
    sql_update_blood_pressure = '''UPDATE blood_pressure SET systolic=?, diastolic=? WHERE id=?;'''
    cur = conn.cursor()
    cur.execute(sql_update_blood_pressure, blood_pressure)
    conn.commit()

def delete_activity(conn, activity_id):
    sql_delete_activity = '''DELETE FROM activity WHERE id=?;'''
    cur = conn.cursor()
    cur.execute(sql_delete_activity, (activity_id,))
    conn.commit()

def delete_nutrition(conn, nutrition_id):
    sql_delete_nutrition = '''DELETE FROM nutrition WHERE id=?;'''
    cur = conn.cursor()
    cur.execute(sql_delete_nutrition, (nutrition_id,))
    conn.commit()

def delete_sleep(conn, sleep_id):
    sql_check_sleep = '''SELECT COUNT(*) FROM sleep WHERE id=?;'''
    cur = conn.cursor()
    cur.execute(sql_check_sleep, (sleep_id,))
    count = cur.fetchone()[0]

    if count > 0:
        sql_delete_sleep = '''DELETE FROM sleep WHERE id=?;'''
        cur = conn.cursor()
        cur.execute(sql_delete_sleep, (sleep_id,))
        conn.commit()
        return True
    else:
        print(f"No sleep record found with id {sleep_id}")
        return False

def delete_heart_rate(conn, heart_rate_id):
    sql_delete_heart_rate = '''DELETE FROM heart_rate WHERE id=?;'''
    cur = conn.cursor()
    cur.execute(sql_delete_heart_rate, (heart_rate_id,))
    conn.commit()

def delete_blood_pressure(conn, blood_pressure_id):
    sql_delete_blood_pressure = '''DELETE FROM blood_pressure WHERE id=?;'''
    cur = conn.cursor()
    cur.execute(sql_delete_blood_pressure, (blood_pressure_id,))
    conn.commit()

def get_average_heart_rate(conn, user_id):
    sql_select_average_heart_rate = '''SELECT AVG(heart_rate) FROM heart_rate WHERE user_id=?;'''
    cur = conn.cursor()
    cur.execute(sql_select_average_heart_rate, (user_id,))
    avg_heart_rate = cur.fetchone()[0]
    return avg_heart_rate

def get_average_blood_pressure(conn, user_id):
    sql_select_average_blood_pressure = '''SELECT AVG(systolic) as avg_systolic, AVG(diastolic) as avg_diastolic FROM blood_pressure WHERE user_id=?;'''
    cur = conn.cursor()
    cur.execute(sql_select_average_blood_pressure, (user_id,))
    avg_blood_pressure = cur.fetchone()
    return avg_blood_pressure

def view_health_insights(conn, user_id):
    activity_logs = get_activity_logs(conn, user_id)
    nutrition_logs = get_nutrition_logs(conn, user_id)
    sleep_logs = get_sleep_logs(conn, user_id)
    heart_rate_logs = get_heart_rate_logs(conn, user_id)
    blood_pressure_logs = get_blood_pressure_logs(conn, user_id)

    data = {
        "Date": [],
        "Activity": [],
        "Duration": [],
        "Calories": [],
        "Hours": [],
        "Heart Rate": [],
        "Systolic": [],
        "Diastolic": [],
    }

    for activity_log in activity_logs:
        date, activity, duration = activity_log
        data["Date"].append(date)
        data["Activity"].append(activity)
        data["Duration"].append(duration)

    for nutrition_log in nutrition_logs:
        date, calories = nutrition_log
        data["Date"].append(date)
        data["Calories"].append(calories)

    for sleep_log in sleep_logs:
        date, hours = sleep_log
        data["Date"].append(date)
        data["Hours"].append(hours)

    for heart_rate_log in heart_rate_logs:
        date, heart_rate = heart_rate_log
        data["Date"].append(date)
        data["Heart Rate"].append(heart_rate)

    for blood_pressure_log in blood_pressure_logs:
        date, systolic, diastolic = blood_pressure_log
        data["Date"].append(date)
        data["Systolic"].append(systolic)
        data["Diastolic"].append(diastolic)

    df = pd.DataFrame(data)
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)

    avg_heart_rate = get_average_heart_rate(conn, user_id)
    avg_blood_pressure = get_average_blood_pressure(conn, user_id)

    messagebox.showinfo("Health Insights", f"Your average heart rate is {avg_heart_rate}. Your average blood pressure is {avg_blood_pressure[0]}/{avg_blood_pressure[1]}.")

def set_goals(conn, user_id):
    goals = {
        "Fitness": {"Goal": 0, "Current": 0},
        "Nutrition": {"Goal": 0, "Current": 0},
        "Sleep": {"Goal": 0, "Current": 0},
        "Heart Rate": {"Goal": 0, "Current": 0},
        "Blood Pressure": {"Goal": (0, 0), "Current": (0, 0)},
    }

    # Get user input for fitness goal
    fitness_goal = input("Enter your fitness goal (number of minutes): ")
    if fitness_goal.isdigit():
        goals["Fitness"]["Goal"] = int(fitness_goal)
    else:
        print("Invalid fitness goal. Please enter a valid integer.")
        return

    # Get user input for nutrition goal
    nutrition_goal = input("Enter your nutrition goal (number of calories): ")
    if nutrition_goal.isdigit():
        goals["Nutrition"]["Goal"] = int(nutrition_goal)
    else:
        print("Invalid nutrition goal. Please enter a valid integer.")
        return

    # Get user input for sleep goal
    sleep_goal = input("Enter your sleep goal (number of hours): ")
    if sleep_goal.isdigit():
        goals["Sleep"]["Goal"] = int(sleep_goal)
    else:
        print("Invalid sleep goal. Please enter a valid integer.")
        return

    # Get user input for heart rate goal
    heart_rate_goal = input("Enter your heart rate goal (beats per minute): ")
    if heart_rate_goal.isdigit():
        goals["Heart Rate"]["Goal"] = int(heart_rate_goal)
    else:
        print("Invalid heart rate goal. Please enter a valid integer.")
        return

    # Get user input for blood pressure goal
    blood_pressure_goal = input("Enter your blood pressure goal (systolic/diastolic): ")
    if blood_pressure_goal.count("/") == 1:
        systolic, diastolic = blood_pressure_goal.split("/")
        if systolic.isdigit() and diastolic.isdigit():
            goals["Blood Pressure"]["Goal"] = (int(systolic), int(diastolic))
        else:
            print("Invalid blood pressure goal. Please enter valid integers for systolic and diastolic values.")
            return
    else:
        print("Invalid blood pressure goal. Please enter a valid value in the format 'systolic/diastolic'.")
        return

    # Get current values for fitness, nutrition, sleep, heart rate, and blood pressure
    goals["Fitness"]["Current"] = get_activity_duration_by_date(conn, user_id, calendar.today().strftime("%Y-%m-%d"))
    goals["Nutrition"]["Current"] = get_calories_by_date(conn, user_id, calendar.today().strftime("%Y-%m-%d"))
    goals["Sleep"]["Current"] = get_sleep_hours_by_date(conn, user_id, calendar.today().strftime("%Y-%m-%d"))
    goals["Heart Rate"]["Current"] = get_heart_rate_by_date(conn, user_id, calendar.today().strftime("%Y-%m-%d"))[2]
    goals["Blood Pressure"]["Current"] = (get_blood_pressure_by_date(conn, user_id, calendar.today().strftime("%Y-%m-%d"))[2], get_blood_pressure_by_date(conn, user_id, calendar.today().strftime("%Y-%m-%d"))[3])

    # Save goals to a file
    with open("goals.txt", "w") as f:
        f.write(str(goals))

    # Display a message to confirm that goals have been set
    messagebox.showinfo("Goals", "Wellness goals have been set.")

def get_activity_duration_by_date(conn, user_id, date):
    sql_select_activity = '''SELECT duration FROM activity WHERE user_id=? AND date=?;'''
    cur = conn.cursor()
    cur.execute(sql_select_activity, (user_id, date))
    activity = cur.fetchone()
    if activity:
        return activity[0]
    else:
        return 0

def get_calories_by_date(conn, user_id, date):
    nutrition = get_nutrition_by_date(conn, user_id, date)
    if nutrition:
        return nutrition[2]
    else:
        return 0

def get_sleep_hours_by_date(conn, user_id, date):
    sleep = get_sleep_by_date(conn, user_id, date)
    if sleep:
        return sleep[2]
    else:
        return 0
def check_recommendations(conn, user_id):
    # Get user's current activity, nutrition, sleep, heart rate, and blood pressure data
    activity_logs = get_activity_logs(conn, user_id)
    nutrition_logs = get_nutrition_logs(conn, user_id)
    sleep_logs = get_sleep_logs(conn, user_id)
    heart_rate_logs = get_heart_rate_logs(conn, user_id)
    blood_pressure_logs = get_blood_pressure_logs(conn, user_id)

    # Calculate the user's average heart rate and blood pressure
    avg_heart_rate = get_average_heart_rate(conn, user_id)
    avg_blood_pressure = get_average_blood_pressure(conn, user_id)

    # Provide recommendations based on the user's data
    if avg_heart_rate > 100:
        print("Your average heart rate is high. Consider reducing your activity level or consulting a doctor.")
    if avg_blood_pressure[0] > 140 or avg_blood_pressure[1] > 90:
        print("Your average blood pressure is high. Consider reducing your sodium intake or consulting a doctor.")
    if len(activity_logs) < 5:
        print("You have not been very active lately. Consider increasing your activity level.")
    if len(nutrition_logs) < 3:
        print("You have not been eating enough. Consider increasing your calorie intake.")
    if len(sleep_logs) < 7:
        print("You have not been getting enough sleep. Consider increasing your sleep duration.")
def main():
    conn = sqlite3.connect('wellness_tracker.db')
    print(f"Successfully connected to SQLite version: {sqlite3.version}")
    if conn is not None:
        create_users_table(conn)
        create_activity_table(conn)
        create_nutrition_table(conn)
        create_sleep_table(conn)
        create_heart_rate_table(conn)
        create_blood_pressure_table(conn)

        # Register or login user
        # conn = sqlite3.connect('activity_tracker.db')
        # Register or login user
        # user = register_or_login_user(conn)
        while True:
            user_choice = input("1. Register\n2. Login\nEnter your choice: ")
            if user_choice == "1":
                # Register user
                username = input("Enter a username: ")
                password = input("Enter a password: ")
                height = float(input("Enter your height (in meters): "))
                weight = float(input("Enter your weight (in kg): "))
                age = int(input("Enter your age: "))

                user = register_user(conn, username, password, height, weight, age)
                if user:
                    print(f"User {username} registered successfully!")
                    break
                else:
                    print("Registration failed. Please try again.")


            elif user_choice == "2":
                # Login user
                username = input("Enter your username: ")
                password = input("Enter your password: ")

                user = authenticate_user(conn, username, password)
                if user:
                        # Display the user interface
                        display_ui(conn, user)

                        # Get the user's current activity, nutrition, and sleep data
                        activity_logs = get_activity_logs(conn, user[0])
                        nutrition_logs = get_nutrition_logs(conn, user[0])
                        sleep_logs = get_sleep_logs(conn, user[0])

                        # Calculate the user's total steps, calories consumed, and sleep duration
                        total_steps = get_total_steps(conn, user[0])
                        total_calories_consumed = get_calories_by_date(conn, user[0], datetime.date.today().strftime("%Y-%m-%d"))
                        total_sleep_duration = get_total_sleep_duration(conn, user[0])

                        # Display the user's current activity, nutrition, and sleep data
                        print(f"Total steps: {total_steps}")
                        print(f"Total calories consumed: {total_calories_consumed}")
                        print(f"Total sleep duration: {total_sleep_duration} minutes")

                        # Check recommendations
                        check_recommendations(conn, user[0])

                        # Close the connection to the database
                        conn.close()

                    # Set up UI
                    window = tk.Tk()
                    window.title("Wellness Tracker")
                    window.geometry("500x400")

                    # Activity Logs
                    activity_logs = get_activity_logs(conn, user[0])

                    # Nutrition Information
                    total_calories_consumed = get_calories_by_date(conn, user[0], calendar.today().strftime("%Y-%m-%d"))

                    # Sleep Patterns
                    current_sleep = get_sleep_hours_by_date(conn, user[0], calendar.today().strftime("%Y-%m-%d"))

                    # Health Data
                    label_user_name = tk.Label(window, text=f"User: {username}")
                    label_height = tk.Label(window, text=f"Height: {user[4]} meters")
                    label_weight = tk.Label(window, text=f"Weight: {user[5]} kg")
                    label_age = tk.Label(window, text=f"Age: {user[6]}")

                    # Activity Levels
                    daily_step_goal = 10000
                    current_steps = get_activity_duration_by_date(conn, user[0], calendar.today().strftime("%Y-%m-%d"))

                    # Nutrition Information
                    daily_calorie_goal = 2500

                    # Sleep Patterns
                    sleep_goal = 8

                    # Buttons
                    button_recommendations = tk.Button(window, text="Health Recommendations", command=lambda: check_recommendations(conn, user[0]))
                    button_recommendations.pack()

                    button_health_insights = tk.Button(window, text="View Health Insights", command=lambda: view_health_insights(conn, user[0]))
                    button_health_insights.pack()

                    button_set_goals = tk.Button(window, text="Set Goals", command=lambda: set_goals(conn, user[0]))
                    button_set_goals.pack()

                    # Goals Entry
                    entry_fitness_goal = tk.Entry(window)
                    entry_nutrition_goal = tk.Entry(window)
                    entry_sleep_goal = tk.Entry(window)

                    # Grid Layout
                    label_user_name = tk.Label(window, text="User Name")
                    label_user_name.grid(row=0, column=0, padx=10, pady=10)

                    label_height = tk.Label(window, text="Height")
                    label_height.grid(row=1, column=0, padx=10, pady=10)

                    label_weight = tk.Label(window, text="Weight")
                    label_weight.grid(row=2, column=0, padx=10, pady=10)

                    label_age = tk.Label(window, text="Age")
                    label_age.grid(row=3, column=0, padx=10, pady=10)

                    label_daily_step_goal = tk.Label(window, text="Daily Step Goal")
                    label_daily_step_goal.grid(row=4, column=0, padx=10, pady=10)

                    label_current_steps = tk.Label(window, text="Current Steps")
                    label_current_steps.grid(row=5, column=0, padx=10, pady=10)

                    label_daily_calorie_goal = tk.Label(window, text="Daily Calorie Goal")
                    label_daily_calorie_goal.grid(row=6, column=0, padx=10, pady=10)

                    label_total_calories_consumed = tk.Label(window, text="Total Calories Consumed")
                    label_total_calories_consumed.grid(row=7, column=0, padx=10, pady=10)

                    label_sleep_goal = tk.Label(window, text="Sleep Goal")
                    label_sleep_goal.grid(row=8, column=0, padx=10, pady=10)

                    label_current_sleep = tk.Label(window, text="Current Sleep")
                    label_current_sleep.grid(row=9, column=0, padx=10, pady=10)

                    button_recommendations = tk.Button(window, text="Recommendations")
                    button_recommendations.grid(row=10, column=0, padx=10, pady=10)

                    button_health_insights = tk.Button(window, text="Health Insights")
                    button_health_insights.grid(row=11, column=0, padx=10, pady=10)

                    button_set_goals = tk.Button(window, text="Set Goals")
                    button_set_goals.grid(row=12, column=0, padx=10, pady=10)

                    entry_fitness_goal = tk.Entry(window)
                    entry_fitness_goal.grid(row=13, column=0, padx=10, pady=10)

                    entry_nutrition_goal = tk.Entry(window)
                    entry_nutrition_goal.grid(row=14, column=0, padx=10, pady=10)

                    entry_sleep_goal = tk.Entry(window)
                    entry_sleep_goal.grid(row=15, column=0, padx=10, pady=10)

                    window.mainloop()
                else:
                    print("Invalid username or password. Please try again.")

    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    main()