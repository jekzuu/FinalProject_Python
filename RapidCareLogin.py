import tkinter as tk
from tkinter import messagebox
import subprocess
import mysql.connector
from hashlib import sha256

# Database connection
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="rapidcare"
    )

# Function to handle login
def login():
    username = username_entry.get()
    password = password_entry.get()
    
    if username == "" or password == "":
        messagebox.showerror("Error", "Username and Password are required")
        return
    
    # Hash the password for comparison
    hashed_password = sha256(password.encode()).hexdigest()
    
    try:
        connection = create_connection()
        cursor = connection.cursor()
        # Check if the user exists
        cursor.execute("SELECT role FROM users WHERE username = %s AND password = %s", (username, hashed_password))
        result = cursor.fetchone()
        
        if result:
            role = result[0]
            messagebox.showinfo("Success", f"Login Successful! Role: {role}")
            open_application()
        else:
            messagebox.showerror("Error", "Invalid Username or Password")
        
        connection.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# Function to open the application (launch the application.py file)
def open_application():
    try:
        root.destroy()
        subprocess.Popen(["python", "D:/PROGRAMMING PROJECTS/Python Projects/Edwin/Rapid Care/application.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open the application: {e}")

    password_var = tk.StringVar()

    # Create a password entry
    password_var = tk.StringVar()

    # Create a password entry
    password_entry = tk.Entry(
        login_frame,
        textvariable=password_var,
        show="*",
        font=("antom", 10)
    )
    password_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.BooleanVar()

def toggle_password():
    if show_password_var.get():
        password_entry.config(show="")  # Show password
        root.after(1000, lambda: password_entry.config(show="*"))
        # Reset the checkbox state after showing the password
        root.after(1000, lambda: show_password_var.set(False))
    else:
        password_entry.config(show="*")  # Hide password immediately
def exit_program():
    root.quit()

root = tk.Tk()
root.title("Rapid Care: Login")

icon = tk.PhotoImage(file="D:/PROGRAMMING PROJECTS/Python Projects/Edwin/Rapid Care/RapidCareLogo.png")
root.iconphoto(True, icon)

height = 600
width = 1000
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f'{width}x{height}+{x}+{y}')
root.resizable(False, False)

bg_image = tk.PhotoImage(file="D:/PROGRAMMING PROJECTS/Python Projects/Edwin/Rapid Care/1.png")
canvas = tk.Canvas(root, width=width, height=height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_image, anchor="nw")

login_frame = tk.Frame(root, width=800, height=500, bg="black")
login_frame.place(x=320, y=250)

# Title label with white text
title_label = tk.Label(login_frame, text="Login", font=("Arial", 20, "bold"), bg="black", fg="white")
title_label.grid(row=1, column=0, columnspan=2, pady=10)

# Username label and entry with white text
username_label = tk.Label(login_frame, text="Username:", bg="black", fg="white", font=("antom", 15, "bold"))
username_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
username_entry = tk.Entry(login_frame, width=30)
username_entry.grid(row=2, column=1, padx=10, pady=10)

# Password label and entry with white text
password_label = tk.Label(login_frame, text="Password:", bg="black", fg="white", font=("antom", 15, "bold"))
password_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
password_entry = tk.Entry(login_frame, width=30, show="*")
password_entry.grid(row=3, column=1, padx=10, pady=5)

# Show password checkbox with white text
show_password_var = tk.BooleanVar()
show_password_check = tk.Checkbutton(login_frame,text="Show Password",variable=show_password_var,bg="black",fg="white",command=toggle_password,font=("antom", 10, "bold"))
show_password_check.grid(row=4, column=1, padx=10, pady=5, sticky="e")

# Login and Exit buttons
login_button = tk.Button(login_frame, text="Login", width=20, height=2, command=login, bg="blue", fg="white", font=("antom", 10, "bold"))
login_button.grid(row=5, column=0, padx=5, pady=10)

exit_button = tk.Button(login_frame, text="Exit", width=20, height=2, command=exit_program, bg="red", fg="white", font=("antom", 10, "bold"))
exit_button.grid(row=5, column=1, padx=5, pady=10)

root.mainloop()
