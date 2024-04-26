import sqlite3
import os
import time
import msvcrt
from datetime import datetime
import pyfiglet 
import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Health_Monitor_GUI import run_health_data_entry

class AdditionalInfoCollector:
    def __init__(self, conn):
        self.conn = conn

    def collect_additional_info(self, user_id):
        # Prompt user to enter additional information
        name = input("Enter your name: ")
        birth_date = input("Enter your birth date (dd-mm-yyyy): ")
        gender = input("Enter your gender (M/F): ")
        height = float(input("Enter your height (in cm): "))
        weight = float(input("Enter your weight (in kg): "))

        # Update user record with additional information
        cursor = self.conn.cursor()
        cursor.execute("UPDATE users SET name=?, birth_date=?, gender=?, height=?, weight=?, additional_info_provided=1 WHERE id=?",
                       (name, birth_date, gender, height, weight, user_id))
        self.conn.commit()
        print("Additional information stored successfully!")
        time.sleep(1)

class Menu:
    def __init__(self, login_system):
        self.login_system = login_system
        self.header_bar_shown = False

    def display_personal_information(self):
        if not self.header_bar_shown:
            self.header_bar_shown = True

        print("Personal Information:")
        cursor = self.login_system.conn.cursor()
        cursor.execute("SELECT name, birth_date, gender, height, weight FROM users WHERE id=?", (self.login_system.user_id,))
        user_info = cursor.fetchone()
        if user_info:
            name, birth_date, gender, height, weight = user_info
            age = self.login_system.calculate_age(birth_date)
            if age is not None:
                print("Name: {}, Age: {} years, Gender: {}, Height: {} cm, Weight: {} kg".format(name, age, gender, height, weight))
            else:
                print("Name: {}, Birth Date: {}, Gender: {}, Height: {} cm, Weight: {} kg".format(name, birth_date, gender, height, weight))
        else:
            print("User information not available.")
            
            
            
    def display_switch_case_menu(self):
        print("\nSwitch Case Menu:")
        print("1) Heart Rate Status")
        print("2) Hydration Tracking")
        print("3) Body Ratio & Fitness Check")
        print("4) Check Physical Health Monitor")
        print("5) Update Weight")
        print("6) Update Height")
        print("7) Check Diet Plan")
        print("8) Logout")

    def handle_menu_selection(self, choice):
        if choice == '1':
            age = self.login_system.calculate_age(self.login_system.user_info[1])
            gender = self.login_system.user_info[2]
            heart_rate = int(input("Enter your heart rate: "))
            status = self.login_system.calculation.get_heart_rate_status(age, gender, heart_rate)
            print("Heart Rate Status:", status)
            
        elif choice == '2':
            self.login_system.hydration_tracking()
            
        elif choice == '3':
                height = self.login_system.user_info[3] 
                weight = self.login_system.user_info[4]  
                bmi= self.login_system.calculation.bmi(weight, height)
                print(f"Your BMI is : {bmi:0,.2f}")
                if bmi < 18.5:
                    print( "Your Fitness Is: Underweight")
                elif 18.5 <= bmi < 25:
                    print ("Your Fitness Is: Normal weight")
                elif 25 <= bmi < 30:
                    print ("Your Fitness Is: Overweight")
                else:
                    print( "Your Fitness Is: Obese")
                time.sleep(3)
                
        elif choice == '4':
            run_health_data_entry()
            
        elif choice == '5':
            updated_weight = self.login_system.calculation.update_weight(self.login_system.user_id)
            self.login_system.user_info[4] = updated_weight  # Update user's weight in user_info
            self.display_personal_information()
            
        elif choice == '6':
            self.login_system.update_height()
        elif choice == '7':
            height = self.login_system.user_info[3] 
            weight = self.login_system.user_info[4] 
            bmi= self.login_system.calculation.bmi(weight, height)
            n_bmi=float(input("Enter Your Target BMI: "))
            daily_calorie_burn_options = int(input("How Much Calorie You Burning Daily: "))
            r_diet = input("You Are vegetarian Or Not(Yes/No): ")
            self.login_system.calculation.fitness_plan(bmi,weight,n_bmi,daily_calorie_burn_options,r_diet)
            
        elif choice == '8':
            self.login_system.logout()
            return True  # Signal to exit menu loop
        else:
            print("Invalid choice. Please try again.")

    def run(self):
        while True:
            self.login_system.clear_terminal()
            if not self.login_system.logged_in:
                print("1. Create account")
                print("2. Login")
                print("3. Forgot password")
                print("4. Exit")
                choice = input("Enter your choice: ")

                if choice == '1':
                    self.login_system.create_account()
                elif choice == '2':
                    self.login_system.login()
                elif choice == '3':
                    self.login_system.forgot_password()
                elif choice == '4':
                    break
                else:
                    print("Invalid choice. Please try again.")
            else:
                self.display_personal_information()
                self.display_switch_case_menu()
                choice = input("Enter your choice: ")
                if self.handle_menu_selection(choice):
                    break

            if msvcrt.kbhit():
                key = ord(msvcrt.getch())
                if key == 12:  # Ctrl+Shift+L
                    self.login_system.logout()
                    break

            time.sleep(0.1)  # Sleep to avoid high CPU usage

class LoginSystem:
    def __init__(self, db_name='credentials.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()
        self.additional_info_collector = AdditionalInfoCollector(self.conn)
        self.logged_in = False
        self.user_id = None
        self.additional_info_provided = False  # Flag to indicate if additional info is provided
        self.user_info = None
        self.calculation = Calculation(self.conn)

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                        (id INTEGER PRIMARY KEY, username TEXT, password TEXT,
                        name TEXT, birth_date TEXT, gender TEXT, height REAL, weight REAL, additional_info_provided INTEGER DEFAULT 0)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS weight_history
                        (id INTEGER PRIMARY KEY, user_id INTEGER, weight REAL, timestamp TEXT)''')  # Create weight_history table
        self.conn.commit()


    def clear_terminal(self):
        # Add a 1 second delay before clearing the terminal
        time.sleep(0.5)
        # Clear terminal screen depending on OS
        os.system('cls' if os.name == 'nt' else 'clear')

    def create_account(self):
        # Prompt user for username and password
        self.clear_terminal()
        print("\n------Creating New Account---\n\n")
        username = input("Enter username: ")
        password = input("Enter password: ")

        # Check if the username already exists
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        if cursor.fetchone():
            print("Account already exists!")
        else:
            # Insert new account into database
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            print("Account created successfully!")


    def login(self):
        # Prompt user for username and password
        username = input("Enter username: ")
        password = input("Enter password: ")

        # Check if credentials match any records in the database
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        if user:
            print("Login successful!")
            self.logged_in = True
            self.user_id = user[0]  # Store the user ID for the current session
            if len(user) >= 9:
                self.additional_info_provided = user[8] == 1  # Check if additional info is provided 
            else:
                self.additional_info_provided = False
            self.user_info = list(user[3:8])  # Store user's additional information as a list
            # Check if additional information is already provided
            if not self.additional_info_provided:
                self.additional_info_collector.collect_additional_info(self.user_id)  # Collect additional info if not provided
            print("Welcome back, {}!".format(user[3]))  # Display a welcome message
            result = pyfiglet.figlet_format(f"Welcome back, {(user[3])}", font = "slant"  ) 
            print(result)
            time.sleep(1)
        else:
            print("Invalid username or password")
            
    def calculate_age(self, birth_date):
        if birth_date is None:
            return None
        today = datetime.today()
        try:
            birth_date = datetime.strptime(birth_date, '%d-%m-%Y')
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            return age
        except ValueError:
            return None

    
    
    
    def logout(self):
        self.logged_in = False
        self.user_id = None
        self.user_info = None
        print("Logged out successfully!")

    def forgot_password(self):
        # Prompt user for username
        username = input("Enter username: ")

        # Check if the username exists in the database
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        if user:
            # Prompt the user to enter a new password
            new_password = input("Enter your new password: ")
            # Update the password in the database
            cursor.execute("UPDATE users SET password=? WHERE id=?", (new_password, user[0]))
            self.conn.commit()
            print("Password updated successfully!")
        else:
            print("Username not found. Please create an account first.")


    def close(self):
        self.conn.close()

class Calculation:
    def __init__(self, conn):
        self.conn = conn
        self.create_weight_history_table()  # Ensure weight_history table exists

    def create_weight_history_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS weight_history
                        (id INTEGER PRIMARY KEY, user_id INTEGER, weight REAL, timestamp TEXT)''')
        self.conn.commit()
        
    def update_weight(self, user_id):
        current_weight = float(input("Enter your current weight (in kg): "))
        
        # Store updated weight
        cursor = self.conn.cursor()
        cursor.execute("UPDATE users SET weight=? WHERE id=?", (current_weight, user_id))
        self.conn.commit()
        
        # Store previous weight and timestamp in history
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO weight_history (user_id, weight, timestamp) VALUES (?, ?, ?)", (user_id, current_weight, timestamp))
        self.conn.commit()
        
        # Return updated weight for display
        print("Successfully Weight is Updated...")
        time.sleep(0.2)
        return current_weight
    
    def get_heart_rate_status(self, age, gender, heart_rate):
        heart_rate_ranges = {
            'male': {
                (18, 25): {'Excellent': (49, 55), 'Good': (56, 61), 'Average': (61, 65), 'Poor': (70, 73), 'Critical': (82, float('inf'))},
                # Add other age ranges for males
            },
            'female': {
                (18, 25): {'Excellent': (54, 60), 'Good': (61, 65), 'Average': (66, 69), 'Poor': (74, 78), 'Critical': (85, float('inf'))},
            }
        }
        gender_lower = gender.lower()
        for age_range, status_ranges in heart_rate_ranges[gender_lower].items():
            if age >= age_range[0] and age <= age_range[1]:
                for status, rate_range in status_ranges.items():
                    if heart_rate >= rate_range[0] and heart_rate <= rate_range[1]:
                        return status

        return "Unknown"
    
    
    def fitness_plan(self, current_bmi, current_weight_kg, target_bmi, daily_calorie_burn, diet_preference):
            ideal_weight_kg = float(input("Enter Your Ideal Weight(Kg): "))

            def calculate_ideal_weight(current_bmi, current_weight_kg, target_bmi):
                height_m = ((current_weight_kg / current_bmi) ** 0.5)
                return target_bmi * height_m ** 2

            def calculate_weeks_to_reach_normal(current_weight_kg, ideal_weight_kg, daily_calorie_burn):
                weight_loss_kg = current_weight_kg - ideal_weight_kg
                if daily_calorie_burn > 0:
                    return weight_loss_kg * 7700 / daily_calorie_burn
                else:
                    return None

            def generate_meal_plan(diet_preference):
                if diet_preference.lower() == 'yes':
                    meal_plan = {
                        'breakfast': 'Avocado toast with tomatoes and spinach',
                        'snack1': 'Mixed nuts and seeds',
                        'lunch': 'Chickpea salad with quinoa and roasted vegetables',
                        'snack2': 'Hummus with carrot sticks',
                        'dinner': 'Vegetable stir-fry with tofu and brown rice'
                    }
                else:
                    meal_plan = {
                        'breakfast': 'Whole grain oatmeal with fruit and nuts',
                        'snack1': 'Greek yogurt with berries',
                        'lunch': 'Grilled chicken salad with mixed greens and vinaigrette dressing',
                        'snack2': 'Carrot sticks with hummus',
                        'dinner': 'Baked salmon with quinoa and steamed vegetables'
                    }
                return meal_plan

            ideal_weight_kg = calculate_ideal_weight(current_bmi, current_weight_kg, target_bmi)
            weeks_required = calculate_weeks_to_reach_normal(current_weight_kg, ideal_weight_kg, daily_calorie_burn)
            meal_plan = generate_meal_plan(diet_preference)

            print(f"\nFor a daily calorie burn of {daily_calorie_burn} calories:")
            if weeks_required is not None:
                print("Estimated Weeks to Reach Normal Weight:", round(weeks_required, 1))
            else:
                print("Cannot estimate weeks required with zero or negative daily calorie burn.")
            print("Ideal Weight (kg):", round(ideal_weight_kg, 2))
            print("Recommended Meal Plan:")
            for meal, description in meal_plan.items():
                print(f"{meal.capitalize()}: {description}")
            
            time.sleep(10)
            value_t=int(input("Enter 0 For Exit Fitnessss Plan: "))
            if value_t==0:
                time.sleep(0)
            else:
                time.sleep(10)
                
    def bmi(self,weight_kg, height_m):
        height_m= (height_m/100)
        bmi = weight_kg / (height_m ** 2)
        return bmi

class health_monitor:
    def __init__(self) -> None:
        pass
        

def main():
    login_system = LoginSystem()
    menu = Menu(login_system)
    menu.run()

if __name__ == "__main__":
    main()
