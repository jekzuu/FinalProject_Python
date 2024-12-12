import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import subprocess
from mysql.connector import Error
import json

def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="rapidcare" 
        )
        if conn.is_connected():
            return conn
    except Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return None

def open_guardian_form():
    # Hide the patient form
    patient_frame.pack_forget()
    
    # Show the guardian form
    guardian_frame.pack(fill="both", expand=True)


def back_to_patient_form():
    # Hide the guardian form
    guardian_frame.pack_forget()
    
    # Show the patient form
    patient_frame.pack(fill="both", expand=True)

def submit_form():
    # Collect all input data as you already did
    room_number = room_var.get()
    full_name = entries["Full Name:"].get()
    age = entries["Age:"].get()
    gender = entries["Gender:"].get()
    address = entries["Address:"].get()
    contact_number = entries["Contact Number:"].get()
    condition = entries["Condition:"].get()

    guardian_name = guardian_name_entry.get()
    guardian_address = guardian_address_entry.get()
    guardian_contact = guardian_contact_entry.get()
    guardian_relation = guardian_relation_entry.get()
    beneficiary = beneficiary_entry.get()
    type_of_case = type_var.get()

    if not full_name or not guardian_name or not beneficiary:
        messagebox.showerror("Validation Error", "Please fill in all the required fields.")
        return

    confirm = messagebox.askyesno("Confirm Submission", "Are you sure you want to submit the form?")
    if not confirm:
        return

    # Connect to the database
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()

            # Insert data into the patients table
            cursor.execute("""
                INSERT INTO patients (room_number, full_name, age, gender, address, contact_number, `condition`)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (room_number, full_name, age, gender, address, contact_number, condition))

            # Get the id of the newly inserted patient
            patient_id = cursor.lastrowid

            # Insert data into the guardians table with the patient_id
            cursor.execute("""
                INSERT INTO guardians (patient_id, full_name, address, contact_number, relation, beneficiary, type_of_case)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (patient_id, guardian_name, guardian_address, guardian_contact, guardian_relation, beneficiary, type_of_case))

            conn.commit()
            messagebox.showinfo("Success", "Form submitted successfully!")

            # Save the data for the table view (optional)
            new_entry = {
                "room_number": room_number,
                "full_name": full_name,
                "age": age,
                "gender": gender,
                "address": address,
                "contact_number": contact_number,
                "condition": condition,
                "guardian_name": guardian_name,
                "guardian_address": guardian_address,
                "guardian_contact": guardian_contact,
                "guardian_relation": guardian_relation,
                "beneficiary": beneficiary,
                "type_of_case": type_of_case
            }

            # Save to a JSON file (optional, depends on your use case)
            with open("patient_data.json", "a") as f:
                json.dump(new_entry, f)
                f.write("\n")

            # Optionally, open the table view directly after submission
            subprocess.Popen(["python", "D:/PROGRAMMING PROJECTS/Python Projects/Edwin/Rapid Care/table.py"])

            # Close the current window
            root.quit()  # or root.destroy()

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to insert data into the database: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        messagebox.showerror("Database Error", "Failed to connect to the database.")


def cancel_application():
    try:
        subprocess.run(["python", "D:/PROGRAMMING PROJECTS/Python Projects/Edwin/Rapid Care/.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open login form: {e}")
    root.destroy()


root = tk.Tk()
root.title("Rapid Care: Application")

icon = tk.PhotoImage(file="D:/PROGRAMMING PROJECTS/Python Projects/Edwin/Rapid Care/RapidCareLogo.png")
root.iconphoto(True, icon)

height = 600
width = 1000
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f'{width}x{height}+{x}+{y}')
root.resizable(False, False)

bg_image = tk.PhotoImage(file="D:/PROGRAMMING PROJECTS/Python Projects/Edwin/Rapid Care/2.png")

patient_frame = tk.Frame(root, bg="black")
guardian_frame = tk.Frame(root, bg="black")

style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=6)
style.configure("TCombobox", font=("Arial", 12), background="#D3D3D3", relief="flat", padding=5)

canvas = tk.Canvas(patient_frame, width=width, height=height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_image, anchor="nw")

patient_title = tk.Label(patient_frame, text="Patient Details", font=("Arial", 18, "bold"), bg="black", fg="white")
canvas.create_window(500, 100, window=patient_title)

room_label = tk.Label(patient_frame, text="Room Number:", font=("Arial", 12, "bold"), bg="black", fg="white", anchor="w")
canvas.create_window(250, 150, window=room_label)
room_options = ["Room 1", "Room 2", "Room 3", "Room 4", "Room 5", "ER1", "ER2", "ER3"]
room_var = tk.StringVar(value="Room 1")
room_menu = ttk.Combobox(patient_frame, textvariable=room_var, values=room_options, state="readonly")
room_menu.config(style="TCombobox")
canvas.create_window(400, 150, window=room_menu)

fields = ["Full Name:", "Age:", "Gender:", "Birthdate:", "Address:", "Contact Number:", "Condition:"]
entries = {}
y_position = 200
for field in fields:
    label = tk.Label(patient_frame, text=field, font=("Arial", 12, "bold"), bg="black", fg="white", anchor="w")
    canvas.create_window(250, y_position, window=label)

    if field == "Gender:":
        gender_var = tk.StringVar(value="Male")
        gender_menu = ttk.Combobox(patient_frame, textvariable=gender_var, values=["Male", "Female", "LGBTQIA+"], state="readonly")
        gender_menu.config(style="TCombobox")
        canvas.create_window(400, y_position, window=gender_menu)
        entries[field] = gender_var
    elif field == "Birthdate:":
        day_var = tk.StringVar(value="1")
        month_var = tk.StringVar(value="January")
        year_var = tk.StringVar(value="2000")

        days = [str(i) for i in range(1, 32)]
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        years = [str(i) for i in range(1900, 2024)]

        day_spinbox = ttk.Spinbox(patient_frame, values=days, width=10, textvariable=day_var)
        month_spinbox = ttk.Spinbox(patient_frame, values=months, width=10, textvariable=month_var)
        year_spinbox = ttk.Spinbox(patient_frame, values=years, width=10, textvariable=year_var)

        canvas.create_window(390, y_position, window=day_spinbox)
        canvas.create_window(480, y_position, window=month_spinbox)
        canvas.create_window(570, y_position, window=year_spinbox)

        entries[field] = (day_var, month_var, year_var)
    else:
        entry = tk.Entry(patient_frame, font=("courier new", 12, "bold"), width=30)
        canvas.create_window(480, y_position, window=entry)
        entries[field] = entry

    y_position += 50

button_done = tk.Button(patient_frame, text="Done", command=open_guardian_form, font=("Arial", 12), bg="green", fg="white")
button_cancel = tk.Button(patient_frame, text="Cancel", command=cancel_application, font=("Arial", 12), bg="red", fg="white")
canvas.create_window(800, y_position, window=button_done)
canvas.create_window(900, y_position, window=button_cancel)

canvas_g = tk.Canvas(guardian_frame, width=width, height=height)
canvas_g.pack(fill="both", expand=True)
canvas_g.create_image(0, 0, image=bg_image, anchor="nw")

guardian_title = tk.Label(guardian_frame, text="Guardian Details", font=("Arial", 18, "bold"), bg="black", fg="white")
canvas_g.create_window(500, 130, window=guardian_title)

fields_g = ["Full Name:", "Address:", "Contact Number:", "Relation:", "Beneficiary:", "Type:"]
entries_g = {}
y_position = 200

type_options = ["Check-up", "Emergency"]
type_var = tk.StringVar(value="Check-up")

for field in fields_g:
    label = tk.Label(guardian_frame, text=field, font=("Arial", 12, "bold"), bg="black", fg="white", anchor="w")
    canvas_g.create_window(250, y_position, window=label)

    if field == "Type:":
        type_menu = ttk.Combobox(guardian_frame, textvariable=type_var, values=type_options, state="readonly")
        type_menu.config(style="TCombobox")
        canvas_g.create_window(450, y_position, window=type_menu)
    else:
        entry = tk.Entry(guardian_frame, font=("Arial", 12), width=30)
        canvas_g.create_window(480, y_position, window=entry)
        entries_g[field] = entry

    y_position += 50

guardian_name_entry = entries_g["Full Name:"]
guardian_address_entry = entries_g["Address:"]
guardian_contact_entry = entries_g["Contact Number:"]
guardian_relation_entry = entries_g["Relation:"]
beneficiary_entry = entries_g["Beneficiary:"]

button_submit = tk.Button(guardian_frame, text="Submit", command=submit_form, font=("Arial", 12), bg="green", fg="white")
button_back = tk.Button(guardian_frame, text="Back", command=back_to_patient_form, font=("Arial", 12), bg="orange", fg="white")
canvas_g.create_window(800, y_position, window=button_submit)
canvas_g.create_window(900, y_position, window=button_back)

patient_frame.pack(fill="both", expand=True)

root.mainloop()
