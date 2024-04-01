import re
import tkinter as tk
from tkinter import messagebox
import sqlite3

DATABASE_FILE = "user_database.db"

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
        return None

def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        print("Table created successfully")
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def insert_user(conn, email, password):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        print("User inserted successfully.")
    except sqlite3.IntegrityError:
        print("Email already exists. Please choose another email.")
    except sqlite3.Error as e:
        print(e)

def validate_email(email):
    pattern = r'^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$'
    return re.match(pattern, email)

def submit_form(email_entry, password_entry, confirm_password_entry):
    email = email_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    if not validate_email(email):
        messagebox.showerror("Error", "Invalid email format.")
        return

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match.")
        return

    conn = create_connection(DATABASE_FILE)
    if conn:
        create_table(conn)
        insert_user(conn, email, password)
        conn.close()
        messagebox.showinfo("Success", "User successfully added to the database.")

def main():
    window = tk.Tk()
    window.title("Sign Up")

    tk.Label(window, text="Email:").grid(row=0, column=0, padx=10, pady=5)
    email_entry = tk.Entry(window)
    email_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(window, text="Password:").grid(row=1, column=0, padx=10, pady=5)
    password_entry = tk.Entry(window, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(window, text="Confirm Password:").grid(row=2, column=0, padx=10, pady=5)
    confirm_password_entry = tk.Entry(window, show="*")
    confirm_password_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Button(window, text="Submit", command=lambda: submit_form(email_entry, password_entry, confirm_password_entry)).grid(row=3, column=0, columnspan=2, pady=10)

    window.mainloop()

if __name__ == "__main__":
    main()
