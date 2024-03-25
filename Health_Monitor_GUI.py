import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class HealthDataEntry:
    def __init__(self, root):
        self.root = root
        self.root.title("Health Data Entry")
        self.num_days = 0
        self.current_day = 1
        self.data = []
        self.create_num_days_entry()
        
    def create_num_days_entry(self):
        self.num_days_window = tk.Toplevel(self.root)
        self.num_days_window.title("Enter Number of Days")
        tk.Label(self.num_days_window, text="Enter the number of days:").pack()
        self.entry_num_days = tk.Entry(self.num_days_window)
        self.entry_num_days.pack()
        tk.Button(self.num_days_window, text="Submit", command=self.set_num_days).pack()

    def set_num_days(self):
        self.num_days = int(self.entry_num_days.get())
        self.num_days_window.destroy()
        self.create_data_entry_fields()

  
    def create_data_entry_fields(self):
        tk.Label(self.root, text=f"Day {self.current_day}").grid(row=0, column=0, columnspan=2)
        tk.Label(self.root, text="Date:").grid(row=1, column=0)
        self.entry_date = DateEntry(self.root, width=12, background='darkblue',
                                    foreground='white', borderwidth=2)
        self.entry_date.grid(row=1, column=1)

        tk.Label(self.root, text="Heart Rate (BPM):").grid(row=2, column=0)
        self.entry_heart_rate = tk.Entry(self.root)
        self.entry_heart_rate.grid(row=2, column=1)

        tk.Label(self.root, text="Blood Pressure (Systolic BP):").grid(row=3, column=0)
        self.entry_blood_pressure = tk.Entry(self.root)
        self.entry_blood_pressure.grid(row=3, column=1)

        tk.Label(self.root, text="Sleep Duration (Hours):").grid(row=4, column=0)
        self.entry_sleep_duration = tk.Entry(self.root)
        self.entry_sleep_duration.grid(row=4, column=1)

        tk.Label(self.root, text="Exercise Duration (Minutes):").grid(row=5, column=0)
        self.entry_exercise_duration = tk.Entry(self.root)
        self.entry_exercise_duration.grid(row=5, column=1)

        tk.Label(self.root, text="Calorie Intake (Calories):").grid(row=6, column=0)
        self.entry_calorie_intake = tk.Entry(self.root)
        self.entry_calorie_intake.grid(row=6, column=1)

        tk.Button(self.root, text="Submit", command=self.submit_data).grid(row=7, columnspan=2)

    def submit_data(self):
        self.data.append({
            'Date': self.entry_date.get(),
            'HeartRate': float(self.entry_heart_rate.get()),
            'BloodPressure': float(self.entry_blood_pressure.get()),
            'SleepDuration': float(self.entry_sleep_duration.get()),
            'ExerciseDuration': float(self.entry_exercise_duration.get()),
            'CalorieIntake': float(self.entry_calorie_intake.get())
        })

        messagebox.showinfo("Success", f"Day {self.current_day} data submitted successfully")

        self.current_day += 1
        if self.current_day <= self.num_days:
            self.clear_entry_fields()
            tk.Label(self.root, text=f"Day {self.current_day}").grid(row=0, column=0, columnspan=2)
        else:
            self.display_graphs()
            self.root.withdraw()  # Hide the main window

    def clear_entry_fields(self):
        self.entry_date.delete(0, tk.END)
        self.entry_heart_rate.delete(0, tk.END)
        self.entry_blood_pressure.delete(0, tk.END)
        self.entry_sleep_duration.delete(0, tk.END)
        self.entry_exercise_duration.delete(0, tk.END)
        self.entry_calorie_intake.delete(0, tk.END)

    def display_graphs(self):
        if not self.data:
            messagebox.showwarning("No Data", "No data available to display.")
            return

        df = pd.DataFrame(self.data)
        df['Date'] = pd.to_datetime(df['Date'])

        plt.rcParams['figure.figsize'] = [10, 5]

        # Create figure
        fig, axs = plt.subplots(3, 2)

        # Plot heart rate over time
        axs[0, 0].plot(df['Date'], df['HeartRate'], marker='o', color='b')
        axs[0, 0].set_title('Heart Rate Over Time')
        axs[0, 0].set_xlabel('Date')
        axs[0, 0].set_ylabel('Heart Rate (BPM)')
        axs[0, 0].grid(True)

        # Plot blood pressure over time
        axs[0, 1].plot(df['Date'], df['BloodPressure'], marker='o', color='r')
        axs[0, 1].set_title('Blood Pressure Over Time')
        axs[0, 1].set_xlabel('Date')
        axs[0, 1].set_ylabel('Systolic Blood Pressure')
        axs[0, 1].grid(True)

        # Plot sleep duration over time
        axs[1, 0].plot(df['Date'], df['SleepDuration'], marker='o', color='g')
        axs[1, 0].set_title('Sleep Duration Over Time')
        axs[1, 0].set_xlabel('Date')
        axs[1, 0].set_ylabel('Sleep Duration (Hours)')
        axs[1, 0].grid(True)

        # Plot exercise duration over time
        axs[1, 1].plot(df['Date'], df['ExerciseDuration'], marker='o', color='m')
        axs[1, 1].set_title('Exercise Duration Over Time')
        axs[1, 1].set_xlabel('Date')
        axs[1, 1].set_ylabel('Exercise Duration (Minutes)')
        axs[1, 1].grid(True)

        # Plot calorie intake over time
        axs[2, 0].plot(df['Date'], df['CalorieIntake'], marker='o', color='y')
        axs[2, 0].set_title('Calorie Intake Over Time')
        axs[2, 0].set_xlabel('Date')
        axs[2, 0].set_ylabel('Calorie Intake (Calories)')
        axs[2, 0].grid(True)

        # Basic statistics
        axs[2, 1].axis('off')
        stats_table = df.describe().to_string()
        axs[2, 1].text(0.5, 0.5, stats_table, ha='center', va='center', fontsize=8)

        # Adjust layout
        plt.tight_layout()

        # Open graphs in a new window with full-screen mode
        graphs_window = tk.Toplevel()
        graphs_window.attributes('-fullscreen', True)
        canvas = FigureCanvasTkAgg(fig, master=graphs_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        graphs_window.bind("<Escape>", lambda event: close_window(graphs_window))

        # Bind the window closing event
        graphs_window.protocol("WM_DELETE_WINDOW", lambda: close_window(graphs_window))

def close_window(window):
    window.destroy()
    root.quit()  # Terminate the program

if __name__ == "__main__":
    root = tk.Tk()
    app = HealthDataEntry(root)
    root.mainloop()
