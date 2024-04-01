import tkinter as tk
from tkinter import messagebox
import sqlite3

DATABASE_FILE = "user_database.db"

def validate_login(email, password):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def sign_in(email_entry, password_entry):
    email = email_entry.get()
    password = password_entry.get()

    if validate_login(email, password):
        messagebox.showinfo("Success", "Log in successful", icon="info")
    else:
        messagebox.showerror("Error", "Email or password incorrect", icon="error")

def main():
    window = tk.Tk()
    window.title("Sign In")

    tk.Label(window, text="Email:").grid(row=0, column=0, padx=10, pady=5)
    email_entry = tk.Entry(window)
    email_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(window, text="Password:").grid(row=1, column=0, padx=10, pady=5)
    password_entry = tk.Entry(window, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Button(window, text="Sign In", command=lambda: sign_in(email_entry, password_entry)).grid(row=2, column=0, columnspan=2, pady=10)

    window.mainloop()

if __name__ == "__main__":
    main()
