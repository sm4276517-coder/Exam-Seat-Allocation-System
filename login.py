import tkinter as tk
from tkinter import messagebox

def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "admin" and password == "1234":
        messagebox.showinfo("Success", "Login Successful!")
    else:
        messagebox.showerror("Error", "Invalid Username or Password!")

root = tk.Tk()
root.title("Exam Seat Allocation System")
root.geometry("500x400")
root.configure(bg="blue")

title = tk.Label(root, text="EXAM SEAT ALLOCATION",
                 font=("Arial", 20, "bold"),
                 bg="blue", fg="white")
title.pack(pady=30)

tk.Label(root, text="Username").pack()
username_entry = tk.Entry(root)
username_entry.pack(pady=5)

tk.Label(root, text="Password").pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=5)

tk.Button(root, text="LOGIN", command=login).pack(pady=20)

root.mainloop()