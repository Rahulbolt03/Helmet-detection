import mysql.connector
import tkinter as tk
from tkinter import messagebox

# Function to handle button click event
def save_to_database():
    # Get values from input fields
    name = entry_name.get()
    reg_num = entry_reg_num.get()
    department = entry_department.get()
    bike_no = entry_bike_no.get()
    email = entry_email.get()  # Get email value

    # Check if any field is empty
    if not name or not reg_num or not department or not bike_no or not email:
        messagebox.showerror("Error", "Please fill in all fields")
        return

    # Connect to MySQL database
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Why2change-_-",
            database="student"
        )
        print("Connected to the database")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        messagebox.showerror("Database Error", "Failed to connect to the database")
        return

    # Insert data into the database
    try:
        cursor = connection.cursor()
        query = "INSERT INTO student_info (Name, RegisterNum, Department, Bikeno, Email) VALUES (%s, %s, %s, %s, %s)"  # Modified query
        data = (name, reg_num, department, bike_no, email)  # Include email in data tuple
        cursor.execute(query, data)
        connection.commit()
        print("Data inserted into the database")
        messagebox.showinfo("Success", "Data saved successfully")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        messagebox.showerror("Database Error", "Failed to save data to the database")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if connection.is_connected():
            connection.close()
            print("Database connection closed")

# Create main window
root = tk.Tk()
root.title("Student Information")

# Create labels
label_name = tk.Label(root, text="Name:")
label_name.grid(row=0, column=0, padx=10, pady=5)
label_reg_num = tk.Label(root, text="Register Number:")
label_reg_num.grid(row=1, column=0, padx=10, pady=5)
label_department = tk.Label(root, text="Department:")
label_department.grid(row=2, column=0, padx=10, pady=5)
label_bike_no = tk.Label(root, text="Bike Number:")
label_bike_no.grid(row=3, column=0, padx=10, pady=5)
label_email = tk.Label(root, text="Email:")  # Add label for email
label_email.grid(row=4, column=0, padx=10, pady=5)  # Place label for email

# Create entry fields
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1, padx=10, pady=5)
entry_reg_num = tk.Entry(root)
entry_reg_num.grid(row=1, column=1, padx=10, pady=5)
entry_department = tk.Entry(root)
entry_department.grid(row=2, column=1, padx=10, pady=5)
entry_bike_no = tk.Entry(root)
entry_bike_no.grid(row=3, column=1, padx=10, pady=5)
entry_email = tk.Entry(root)  # Add entry field for email
entry_email.grid(row=4, column=1, padx=10, pady=5)  # Place entry field for email

# Create save button
save_button = tk.Button(root, text="Save", command=save_to_database)
save_button.grid(row=5, column=0, columnspan=2, pady=10)

# Run the Tkinter event loop
root.mainloop()
