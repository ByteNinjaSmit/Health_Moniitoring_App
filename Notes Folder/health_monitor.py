import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import zscore

# Sample health data (replace this with your actual data)
health_data = {
    'Date': ['2024-03-01', '2024-03-02', '2024-03-03', '2024-03-04', '2024-03-05'],
    'HeartRate': [75, 78, 80, 82, 79],  # BPM
    'BloodPressure': [120, 122, 118, 124, 121],  # Systolic BP
    'SleepDuration': [7, 6.5, 7.2, 6.8, 7.5],  # Hours
    'ExerciseDuration': [30, 45, 60, 40, 50],  # Minutes
    'CalorieIntake': [2000, 1900, 2100, 1800, 1950]  # Calories
}


# You Can also Ask Value's From user by Using Below Code but then you need above code comment either below code comment

# def get_health_data():
#     date = input("Enter the date (YYYY-MM-DD): ")
#     heart_rate = float(input("Enter the heart rate (BPM): "))
#     blood_pressure = float(input("Enter the systolic blood pressure: "))
#     sleep_duration = float(input("Enter the sleep duration (Hours): "))
#     exercise_duration = float(input("Enter the exercise duration (Minutes): "))
#     calorie_intake = float(input("Enter the calorie intake (Calories): "))
    
#     return {'Date': date, 'HeartRate': heart_rate, 'BloodPressure': blood_pressure,
#             'SleepDuration': sleep_duration, 'ExerciseDuration': exercise_duration,
#             'CalorieIntake': calorie_intake}

# # Sample health data (replace this with your actual data)
# health_data = []



# Convert data to pandas DataFrame
df = pd.DataFrame(health_data)
df['Date'] = pd.to_datetime(df['Date'])  # Convert 'Date' column to datetime

# Plot heart rate over time
plt.figure(figsize=(10, 5))
plt.plot(df['Date'], df['HeartRate'], marker='o', color='b')
plt.title('Heart Rate Over Time')
plt.xlabel('Date')
plt.ylabel('Heart Rate (BPM)')
plt.grid(True)
plt.show()

# Plot blood pressure over time
plt.figure(figsize=(10, 5))
plt.plot(df['Date'], df['BloodPressure'], marker='o', color='r')
plt.title('Blood Pressure Over Time')
plt.xlabel('Date')
plt.ylabel('Systolic Blood Pressure')
plt.grid(True)
plt.show()

# Plot sleep duration over time
plt.figure(figsize=(10, 5))
plt.plot(df['Date'], df['SleepDuration'], marker='o', color='g')
plt.title('Sleep Duration Over Time')
plt.xlabel('Date')
plt.ylabel('Sleep Duration (Hours)')
plt.grid(True)
plt.show()

# Plot exercise duration over time
plt.figure(figsize=(10, 5))
plt.plot(df['Date'], df['ExerciseDuration'], marker='o', color='m')
plt.title('Exercise Duration Over Time')
plt.xlabel('Date')
plt.ylabel('Exercise Duration (Minutes)')
plt.grid(True)
plt.show()

# Plot calorie intake over time
plt.figure(figsize=(10, 5))
plt.plot(df['Date'], df['CalorieIntake'], marker='o', color='y')
plt.title('Calorie Intake Over Time')
plt.xlabel('Date')
plt.ylabel('Calorie Intake (Calories)')
plt.grid(True)
plt.show()

# Basic statistics
print("Basic Statistics:")
print(df.describe())

# Anomaly detection using Z-score
df['HeartRate_Zscore'] = zscore(df['HeartRate'])
df['BloodPressure_Zscore'] = zscore(df['BloodPressure'])
df['SleepDuration_Zscore'] = zscore(df['SleepDuration'])
df['ExerciseDuration_Zscore'] = zscore(df['ExerciseDuration'])
df['CalorieIntake_Zscore'] = zscore(df['CalorieIntake'])

# Threshold for anomaly detection
threshold = 3

# Detecting anomalies
anomalies_heart_rate = df[df['HeartRate_Zscore'].abs() > threshold]
anomalies_blood_pressure = df[df['BloodPressure_Zscore'].abs() > threshold]
anomalies_sleep_duration = df[df['SleepDuration_Zscore'].abs() > threshold]
anomalies_exercise_duration = df[df['ExerciseDuration_Zscore'].abs() > threshold]
anomalies_calorie_intake = df[df['CalorieIntake_Zscore'].abs() > threshold]

print("\nAnomalies in Heart Rate:")
print(anomalies_heart_rate)

print("\nAnomalies in Blood Pressure:")
print(anomalies_blood_pressure)

print("\nAnomalies in Sleep Duration:")
print(anomalies_sleep_duration)

print("\nAnomalies in Exercise Duration:")
print(anomalies_exercise_duration)

print("\nAnomalies in Calorie Intake:")
print(anomalies_calorie_intake)
