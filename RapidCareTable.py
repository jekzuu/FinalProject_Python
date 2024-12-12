import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
from datetime import datetime
import mysql.connector
import sys
from mysql.connector import Error

def connect_to_db():
    try:
        # Connect to your MySQL database
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

def add_entry():
    root.destroy()
    subprocess.Popen(["python", "D:/PROGRAMMING PROJECTS/Python Projects/Edwin/Rapid Care/application.py"])

def cancel_action():
    root.destroy()
    subprocess.Popen(["python", "D:/PROGRAMMING PROJECTS/Python Projects/Edwin/Rapid Care/table.py"])


def update_entry():
    selected = patient_table.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a record to update.")
        return

    # Get the selected record
    selected_item = patient_table.item(selected[0], "values")
    patient_id = selected_item[0]  # Assuming the first column is patient_id

    # Close the main window before opening the new one
    root.destroy()

    # Pass the patient_id to application.py to edit the record
    subprocess.Popen(["python", "D:/PROGRAMMING PROJECTS/Python Projects/Edwin/Rapid Care/application.py", str(patient_id)])

def delete_patient_entry():
    selected = patient_table.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a patient record to delete.")
        return

    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected patient record?")
    if confirm:
        for item in selected:
            patient_id = patient_table.item(item, "values")[0]  # Assuming the first column is patient_id
            conn = connect_to_db()
            if not conn:
                messagebox.showerror("Database Error", "Failed to connect to the database.")
                return
            try:
                cursor = conn.cursor()

                cursor.execute("DELETE FROM guardians WHERE patient_id = %s", (patient_id,))
                print(f"Guardians for Patient ID {patient_id} deleted")

                # Delete the patient record
                cursor.execute("DELETE FROM patients WHERE id = %s", (patient_id,))
                print(f"Patient with ID {patient_id} deleted")

                conn.commit() 
                patient_table.delete(item) 

                messagebox.showinfo("Deleted", "Patient and corresponding guardian records successfully deleted.")

                # Reload the data to reflect the changes
                reload_data()

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Failed to delete patient and guardian records: {err}")
                print(f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

def reload_data():
    """Reloads the patient and guardian data."""
    # Clear the existing data in Treeview
    for row in patient_table.get_children():
        patient_table.delete(row)
    for row in guardian_table.get_children():
        guardian_table.delete(row)

    # Load fresh data
    load_patients()
    load_guardians()

def load_patient_data(patient_id=None):
    if patient_id:
        # Query the database to load the patient's data for editing
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
                patient_data = cursor.fetchone()
                # Fill in the form with the existing data
            except Error as e:
                messagebox.showerror("Database Error", f"Failed to load patient data: {e}")
            finally:
                cursor.close()
                conn.close()
    else:
        # Create a new record (empty form)
        pass

# In your main code, get the patient_id from the arguments (if passed)
if len(sys.argv) > 1:
    patient_id = sys.argv[1]
    load_patient_data(patient_id)
else:
    # No patient_id passed, so create a new record
    load_patient_data()

def print_receipt():
    selected = patient_table.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a record to print.")
        return
    record = patient_table.item(selected[0], "values")
    receipt = f"""
    ---------------------------------
           Rapid Care Receipt       
    ---------------------------------
    Date: {datetime.now().strftime("%Y-%m-%d")}
    Time: {datetime.now().strftime("%H:%M:%S")}
    ---------------------------------
    Room No: {record[0]}
    Full Name: {record[1]}
    Age: {record[2]}
    Gender: {record[3]}
    Birthdate: {record[4]}
    Address: {record[5]}
    Contact No: {record[6]}
    Condition: {record[7]}
    ---------------------------------
    """
    
    receipt_window = tk.Toplevel(root)
    receipt_window.title("Receipt")
    
    receipt_window.geometry("400x350")
    
    receipt_text = tk.Text(receipt_window, wrap="word", height=25, width=40)
    receipt_text.pack(padx=10, pady=10)
    
    receipt_text.insert(tk.END, receipt)
    
    receipt_text.config(state=tk.DISABLED)



def load_patients():
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patients")
            records = cursor.fetchall()

            for record in records:
                patient_table.insert("", "end", values=record)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load patient data: {e}")
        finally:
            cursor.close()
            conn.close()

def load_guardians():
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM guardians") 
            records = cursor.fetchall()

            for record in records:
                guardian_table.insert("", "end", values=record)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load guardian data: {e}")
        finally:
            cursor.close()
            conn.close()

root = tk.Tk()
root.title("Rapid Care: Patient Information")

icon = tk.PhotoImage(file="D:/PROGRAMMING PROJECTS/Python Projects/Edwin/Rapid Care/RapidCareLogo.png")
root.iconphoto(True, icon)

height = 600
width = 1000
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f'{width}x{height}+{x}+{y}')
root.resizable(False, False)

bg_image = tk.PhotoImage(file="D:/PROGRAMMING PROJECTS/Python Projects/Edwin/Rapid Care/2.png")
canvas = tk.Canvas(root, width=width, height=height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_image, anchor="nw")

table_width = width - 100
table_column_width = table_width // 8
guardian_column_width = table_width // 6

patient_label = tk.Label(
    root, text="Patient Details", font=("Arial", 14, "bold"),
    bg="black", fg="white", padx=10, pady=5
)
patient_label.place(x=(width // 2) - (table_width // 2), y=80, width=table_width)

patient_columns = (
    "Room No", "Full Name", "Age", "Gender", 
    "Birthdate", "Address", "Contact No", "Condition"
)
patient_table = ttk.Treeview(root, columns=patient_columns, show="headings", height=7)

for col in patient_columns:
    patient_table.heading(col, text=col)
    patient_table.column(col, width=table_column_width, anchor="center")

patient_table.place(x=(width // 2) - (table_width // 2), y=120)

guardian_label = tk.Label(
    root, text="Guardian Details", font=("Arial", 14, "bold"),
    bg="black", fg="white", padx=10, pady=5
)
guardian_label.place(x=(width // 2) - (table_width // 2), y=300, width=table_width)

guardian_columns = (
    "Full Name", "Address", "Contact No", "Relation", 
    "Beneficiary", "Type"
)
guardian_table = ttk.Treeview(root, columns=guardian_columns, show="headings", height=7)

for col in guardian_columns:
    guardian_table.heading(col, text=col)
    guardian_table.column(col, width=guardian_column_width, anchor="center")

guardian_table.place(x=(width // 2) - (table_width // 2), y=340)

button_frame = tk.Frame(root, bg="black")
button_frame.place(x=450, y=520, width=500, height=40)

buttons = [
    {"text": "Add", "bg": "#6eb8b5", "command": add_entry},
    {"text": "Update", "bg": "#34825b", "command": update_entry},
    {"text": "Delete", "bg": "#7a3328", "command": delete_patient_entry},
    {"text": "Print", "bg": "#8c6949", "command": print_receipt},
    {"text": "Exit", "bg": "#4d229c", "command": root.quit}
]


for i, btn in enumerate(buttons):
    tk.Button(
        button_frame, text=btn["text"], font=("Arial", 10, "bold"),
        bg=btn["bg"], fg="white", width=10, command=btn["command"]
    ).grid(row=0, column=i, padx=5, pady=10)

# Load patient and guardian data when the app starts
load_patients()
load_guardians()

root.mainloop()
