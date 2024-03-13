import tkinter as tk
import sqlite3
from tkinter import messagebox
import hashlib
import customtkinter as ctk 
import tkinter.messagebox as tkmb 

class LoggedInScreen:
    def __init__(self, root, username, login_system_instance):
        self.root = root
        self.username = username
        self.login_system_instance = login_system_instance
        self.root.title("Logged In")
        self.welcome_label = tk.Label(self.root, text=f"Welcome {self.username}", font=("Helvetica", 36))
        self.welcome_label.pack(pady=50)
        self.logout_button = tk.Button(self.root, text="Logout", command=self.logout)
        self.logout_button.pack(side=tk.TOP, padx=20, pady=20, anchor='ne')

    def logout(self):
        self.root.destroy()
        self.login_system_instance.home_screen()

class LoginSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("HOME Window")
        self.root.attributes('-fullscreen', True)

        self.conn = sqlite3.connect('main.db')
        self.cursor = self.conn.cursor()

        self.create_table()

        self.home_screen()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
              (id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT NOT NULL,
              password TEXT NOT NULL)''')
        self.conn.commit()

    def home_screen(self):
        self.clear_screen()

        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Create buttons
        self.create_account_button = tk.Button(self.root, text="Create Account", command=self.create_account, height=5, width=20)
        self.create_account_button.grid(row=0, column=0, padx=20, pady=20)

        self.login_button = tk.Button(self.root, text="Login Account", command=self.login, height=5, width=20)
        self.login_button.grid(row=0, column=1, padx=20, pady=20)

        self.forgot_password_button = tk.Button(self.root, text="Forgot Password", command=self.forgot_password, height=5, width=20)
        self.forgot_password_button.grid(row=1, column=0, padx=20, pady=20)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit_app, height=5, width=20)
        self.exit_button.grid(row=1, column=1, padx=20, pady=20)

        # Set row and column weights to center the buttons
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_account(self):
        def submit_account():
            username = self.username_entry.get()
            password = self.encrypt_password(self.password_entry.get())
            try:
                self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                self.conn.commit()
                messagebox.showinfo("Success", "Account created successfully!")
                create_account_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        create_account_window = tk.Toplevel(self.root)
        create_account_window.title("Create Account")
        create_account_window.attributes('-fullscreen', True)

        self.username_label = tk.Label(create_account_window, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(create_account_window)
        self.username_entry.pack()

        self.password_label = tk.Label(create_account_window, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(create_account_window, show="*")
        self.password_entry.pack()

        self.submit_button = tk.Button(create_account_window, text="Submit", command=submit_account)
        self.submit_button.pack()

    def login(self):
        def submit_login():
            username = user_entry.get()
            password = self.encrypt_password(user_pass.get())  # Hash the provided password
            self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            user = self.cursor.fetchone()
            if user:
                stored_password = user[2]  # Assuming password is stored in the third column
                if stored_password == password:
                    messagebox.showinfo("Success", f"Welcome {username}!")
                    self.logged_in_screen(username)
                else:
                    messagebox.showerror(title="Login Failed", message="Invalid Username or password")
                    self.home_screen()  # Go back to home screen
            else:
                messagebox.showerror(title="Login Failed", message="Invalid Username or password")
                self.home_screen()  # Go back to home screen

        self.clear_screen()

        label = ctk.CTkLabel(self.root, text="This is the main UI page")
        label.pack(pady=20)

        frame = ctk.CTkFrame(master=self.root)
        frame.pack(pady=20, padx=40, fill='both', expand=True)

        label = ctk.CTkLabel(master=frame, text='Modern Login System UI')
        label.pack(pady=12, padx=10)

        user_entry = ctk.CTkEntry(master=frame, placeholder_text="Username")
        user_entry.pack(pady=12, padx=10)

        user_pass = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
        user_pass.pack(pady=12, padx=10)

        button = ctk.CTkButton(master=frame, text='Login', command=submit_login)
        button.pack(pady=12, padx=10)

        checkbox = ctk.CTkCheckBox(master=frame, text='Remember Me')
        checkbox.pack(pady=12, padx=10)

    def forgot_password(self):
        def submit_username():
            entered_username = username_entry.get()
            # Check if the username exists in the database
            self.cursor.execute("SELECT * FROM users WHERE username=?", (entered_username,))
            user = self.cursor.fetchone()
            if user:
                # Prompt the user to enter a new password
                reset_password(user[0])  # Pass user id to reset_password function
            else:
                tkmb.showerror("Error", "Username not found")
                # Send the user back to the home screen
                self.home_screen()

        def reset_password(user_id):
            def submit_password():
                new_password = new_password_entry.get()
                confirm_password = confirm_password_entry.get()
                if new_password == confirm_password:
                    # Update the password in the database
                    hashed_password = self.encrypt_password(new_password)
                    self.cursor.execute("UPDATE users SET password=? WHERE id=?", (hashed_password, user_id))
                    self.conn.commit()
                    tkmb.showinfo("Success", "Password updated successfully")
                    # Return to home screen
                    self.home_screen()
                else:
                    tkmb.showerror("Error", "Passwords do not match")

            # Clear the existing screen content
            self.clear_screen()

            # Create the forgot password window
            new_password_label = tk.Label(self.root, text="New Password:")
            new_password_label.pack()
            new_password_entry = tk.Entry(self.root, show="*")
            new_password_entry.pack()

            confirm_password_label = tk.Label(self.root, text="Confirm Password:")
            confirm_password_label.pack()
            confirm_password_entry = tk.Entry(self.root, show="*")
            confirm_password_entry.pack()

            submit_button = tk.Button(self.root, text="Submit", command=submit_password)
            submit_button.pack()

        # Clear the existing screen content
        self.clear_screen()

        # Create the forgot password window
        username_label = tk.Label(self.root, text="Enter Username:")
        username_label.pack()

        username_entry = tk.Entry(self.root)
        username_entry.pack()

        submit_button = tk.Button(self.root, text="Submit", command=submit_username)
        submit_button.pack()

    def exit_app(self):
        self.root.destroy()

    def encrypt_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def logged_in_screen(self, username):
        logged_in_root = tk.Toplevel(self.root)
        logged_in_root.title("Logged In")
        logged_in_root.attributes('-fullscreen', True)
        logged_in_screen_instance = LoggedInScreen(logged_in_root, username, self)


# Main window
root = tk.Tk()
app = LoginSystem(root)
root.mainloop()
