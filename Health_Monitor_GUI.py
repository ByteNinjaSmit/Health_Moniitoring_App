import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.font_manager import FontProperties


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
        
        # Make it fullscreen
        self.num_days_window.attributes('-fullscreen', True)
        
        # Calculate the position for centering the window
        screen_width = self.num_days_window.winfo_screenwidth()
        screen_height = self.num_days_window.winfo_screenheight()
        
        tk.Label(self.num_days_window, text="Enter the number of days:").pack()
        self.entry_num_days = tk.Entry(self.num_days_window)
        self.entry_num_days.pack()
        tk.Button(self.num_days_window, text="Submit", command=self.set_num_days).pack()

        # Center the window after widgets are added
        self.num_days_window.geometry('+{}+{}'.format((screen_width - self.num_days_window.winfo_reqwidth()) // 2,
                                                    (screen_height - self.num_days_window.winfo_reqheight()) // 2))

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
        # bold_font = mfont.Font(weight="bold")
        bold_font = FontProperties(weight="bold")  # Use FontProperties instead of font

        # Plot heart rate over time
        axs[0, 0].plot(df['Date'], df['HeartRate'], marker='o', color='b')
        axs[0,0].axhline(y=80, linestyle="--", color='r', label='80 BPM')
        axs[0,0].axhline(y=60, linestyle="--", color='g', label='60 BPM')
        axs[0, 0].set_title('Heart Rate Over Time')
        axs[0, 0].set_xlabel('Date') 
        axs[0, 0].set_ylabel('Heart Rate (BPM)')
        axs[0, 0].set_ylim(54, 90)  # Setting y-axis limits
        axs[0, 0].grid(True)
        axs[0, 0].legend()  # Show legend for the dashed lines
        # bold_font = font.Font(weight="bold")
        # Determine health status based on heart rate
        #  (18, 25): {'Excellent': (54, 60), 'Good': (61, 65), 'Average': (66, 69), 'Poor': (74, 78), 'Critical': (85, float('inf'))},
        # Define health status categories based on heart rate
        if max(df['HeartRate']) <= 54:
            health_status = 'Excellent'
            color = 'green'
        elif 54 < max(df['HeartRate']) <= 60:
            health_status = 'Very Good'
            color = 'green'
        elif 60 < max(df['HeartRate']) <= 65:
            health_status = 'Good'
            color = 'green'
        elif 65 < max(df['HeartRate']) <= 69:
            health_status = 'Above Average'
            color = 'orange'
        elif 69 < max(df['HeartRate']) <= 74:
            health_status = 'Average'
            color = 'orange'
        elif 74 < max(df['HeartRate']) <= 78:
            health_status = 'Below Average'
            color = 'orange'
        elif 78 < max(df['HeartRate']) <= 85:
            health_status = 'Poor'
            color = 'red'
        else:
            health_status = 'Critical'
            color = 'red'
        # Add health status to x-axis label
        axs[0, 0].set_xlabel('Your Heart Rate Health Status: (' + health_status + ')', fontsize=14, color=color, fontproperties=bold_font)  # Use fontproperties instead of font
        
        
        # Noramal : 80 , At Risk: 120 , High BP: 140
        # Plot blood pressure over time
        bp_plot = axs[0, 1].plot(df['Date'], df['BloodPressure'], marker='o', color='r')
        axs[0, 1].set_title('Blood Pressure Over Time')
        axs[0, 1].set_xlabel('Date')
        axs[0, 1].set_ylabel('Systolic Blood Pressure')
        axs[0, 1].grid(True)
        axs[0, 1].axhline(y=100, linestyle='--', color='b', label='100 mmHg')
        axs[0, 1].axhline(y=130, linestyle='--', color='g', label='130 mmHg')
        axs[0, 1].legend()

        # Determine blood pressure health status based on systolic blood pressure
        # Define blood pressure health status categories
        bp_status = ''  # Initialize bp_status with a default value

        # Determine blood pressure health status based on systolic blood pressure
        # Define blood pressure health status categories
        if max(df['BloodPressure']) <= 100:
            bp_status = 'Normal'
            color = 'green'
        elif 100 < max(df['BloodPressure']) <= 120:
            bp_status = 'Elevated'
            color = 'orange'
        elif 120 < max(df['BloodPressure']) <= 129:
            bp_status = 'High Blood Pressure (Hypertension Stage 1)'
            color = 'red'
        elif 130 < max(df['BloodPressure']) <= 139:
            bp_status = 'High Blood Pressure (Hypertension Stage 2)'
            color = 'red'
        elif max(df['BloodPressure']) >= 140:
            bp_status = 'Hypertensive Crisis (Consult your doctor immediately)'
            color = 'red'


        # Add health status to x-axis label
        # bold_font = font.Font(weight="bold")
        axs[0, 1].set_xlabel('Your Blood Pressure Health Status: (' + bp_status + ')', fontsize=12, color=color, fontproperties=bold_font)  # Use fontproperties instead of font


        # Plot sleep duration over time
        axs[1, 0].plot(df['Date'], df['SleepDuration'], marker='o', color='g')
        axs[1, 0].set_title('Sleep Duration Over Time')
        axs[1, 0].set_xlabel('Date')
        axs[1, 0].set_ylabel('Sleep Duration (Hours)')
        axs[1, 0].grid(True)

        # Determine sleep duration health status
        # Define sleep duration health status categories
        if max(df['SleepDuration']) >= 7:
            sleep_status = 'Adequate'
            color = 'green'
        elif 6 < max(df['SleepDuration']) < 7:
            sleep_status = 'Slightly Inadequate'
            color = 'orange'
        else:
            sleep_status = 'Inadequate'
            color = 'red'

        # Add health status to x-axis label
        axs[1, 0].set_xlabel('Your Sleep Duration Health Status: (' + sleep_status + ')', fontsize=12, color=color, fontproperties=bold_font)  # Use fontproperties instead of font

        # Plot exercise duration over time
        axs[1, 1].plot(df['Date'], df['ExerciseDuration'], marker='o', color='m')
        axs[1, 1].set_title('Exercise Duration Over Time')
        axs[1, 1].set_xlabel('Date')
        axs[1, 1].set_ylabel('Exercise Duration (Minutes)')
        axs[1, 1].grid(True)

        # Determine exercise duration health status
        # Define exercise duration health status categories
        if max(df['ExerciseDuration']) >= 150:
            exercise_status = 'Excellent'
            color = 'green'
        elif 120 <= max(df['ExerciseDuration']) < 150:
            exercise_status = 'Good'
            color = 'green'
        elif 90 <= max(df['ExerciseDuration']) < 120:
            exercise_status = 'Average'
            color = 'orange'
        elif 60 <= max(df['ExerciseDuration']) < 90:
            exercise_status = 'Below Average'
            color = 'orange'
        else:
            exercise_status = 'Poor'
            color = 'red'

        # Add health status to x-axis label
        axs[1, 1].set_xlabel('Your Exercise Duration Health Status: (' + exercise_status + ')', fontsize=12, color=color, fontproperties=bold_font)  # Use fontproperties instead of font

        # Plot calorie intake over time
        axs[2, 0].plot(df['Date'], df['CalorieIntake'], marker='o', color='y')
        axs[2, 0].set_title('Calorie Intake Over Time')
        axs[2, 0].set_xlabel('Date')
        axs[2, 0].set_ylabel('Calorie Intake (Calories)')
        axs[2, 0].grid(True)

        # Determine calorie intake health status
        # Define calorie intake health status categories
        if max(df['CalorieIntake']) <= 2000:
            calorie_status = 'Low'
            color = 'red'
        elif 2000 < max(df['CalorieIntake']) < 2500:
            calorie_status = 'Normal'
            color = 'green'
        else:
            calorie_status = 'High'
            color = 'orange'

        # Add health status to x-axis label
        axs[2, 0].set_xlabel('Your Calorie Intake Health Status: (' + calorie_status + ')', fontsize=12, color=color, fontproperties=bold_font)  # Use fontproperties instead of font


        # # Basic statistics
        axs[2, 1].axis('off')
        stats_table = df.describe().to_string()
        axs[2, 1].text(0.5, 0.5, stats_table, ha='center', va='center', fontsize=8)

        overall_health_avg = df.mean(numeric_only=True).mean()
        overall_status_categories = {
            'Excellent': 'You are in excellent health condition. Keep up the good work!',
            'Good': 'Your overall health condition is good. Maintain your healthy habits.',
            'Average': 'Your overall health condition is average. Consider improving your lifestyle.',
            'Poor': 'Your overall health condition is poor. Consult a healthcare professional for guidance.'
        }

        if overall_health_avg >= 6:
            overall_status = 'Excellent'
        elif 3 <= overall_health_avg < 6:
            overall_status = 'Good'
        elif 0 <= overall_health_avg < 3:
            overall_status = 'Average'
        else:
            overall_status = 'Poor'

        overall_status_description = overall_status_categories.get(overall_status, 'Undefined')

        # Display overall health status report
        report_window = tk.Toplevel()
        report_window.title("Overall Health Report")

        tk.Label(report_window, text="Overall Health Status", font=('Helvetica', 16, 'bold')).pack(pady=10)
        
        tk.Label(report_window, text=f"Brief Summary: {overall_status}", font=('Helvetica', 12)).pack(pady=5)
        tk.Label(report_window, text=f"Details: {overall_status_description}", font=('Helvetica', 12)).pack(pady=5)

        tk.Button(report_window, text="Close", command=report_window.destroy).pack(pady=10)


        # Adjust layout
        plt.tight_layout()

        # Open graphs in a new window with full-screen mode
        graphs_window = tk.Toplevel()
        graphs_window.attributes('-fullscreen', True)
        canvas = FigureCanvasTkAgg(fig, master=graphs_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        graphs_window.bind("<Escape>", lambda event: close_window(graphs_window, self.root))

        # Bind the window closing event
        graphs_window.protocol("WM_DELETE_WINDOW", lambda: close_window(graphs_window, self.root))

def close_window(window, root):
    window.destroy()
    root.quit()  # Terminate the program

def run_health_data_entry():
    root = tk.Tk()
    app = HealthDataEntry(root)
    root.mainloop()

if __name__ == "__main__":
    run_health_data_entry()
