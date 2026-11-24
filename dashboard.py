
import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

from database import connect_db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def open_module(filename):
    file_path = os.path.join(BASE_DIR, filename)

    if not os.path.exists(file_path):
        messagebox.showerror(
            "File Not Found",
            filename + " file not found!"
        )
        return

    try:
        subprocess.Popen([sys.executable, file_path])
    except Exception as error:
        messagebox.showerror("Error", str(error))

def get_statistics():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM rooms")
    total_rooms = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM allocations")
    total_allocations = cursor.fetchone()[0]

    conn.close()

    return total_students, total_rooms, total_allocations

def refresh_dashboard():
    try:
        students, rooms, allocations = get_statistics()

        student_number.config(text=str(students))
        room_number.config(text=str(rooms))
        allocation_number.config(text=str(allocations))

    except Exception as error:
        messagebox.showerror("Database Error", str(error))

def logout():
    answer = messagebox.askyesno(
        "Logout",
        "Are you sure you want to logout?"
    )

    if answer:
        root.destroy()

root = tk.Tk()
root.title("Exam Seat Allocation System - Dashboard")
root.geometry("1100x700")
root.configure(bg="#F1F5F9")
root.resizable(False, False)

header = tk.Frame(root, bg="#172554", height=90)
header.pack(fill="x")

tk.Label(
    header,
    text="EXAM SEAT ALLOCATION SYSTEM",
    font=("Arial", 22, "bold"),
    bg="#172554",
    fg="white"
).pack(pady=25)

sidebar = tk.Frame(root, bg="#1E293B", width=230)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

tk.Label(
    sidebar,
    text="ADMIN PANEL",
    font=("Arial", 16, "bold"),
    bg="#1E293B",
    fg="white"
).pack(pady=25)

def create_button(name, filename=None):

    if name == "Logout":
        command = logout

    elif name == "Dashboard":
        command = refresh_dashboard

    else:
        command = lambda: open_module(filename)

    tk.Button(
        sidebar,
        text=name,
        font=("Arial", 11, "bold"),
        bg="#334155",
        fg="white",
        activebackground="#2563EB",
        activeforeground="white",
        relief="flat",
        width=22,
        height=2,
        command=command
    ).pack(pady=5)


create_button("Dashboard")
create_button("Add Student", "student.py")
create_button("View Student", "student.py")
create_button("Add Exam Room", "room.py")
create_button("Seat Allocation", "allocation.py")
create_button("Search Student", "search.py")
create_button("View Allocation", "allocation.py")

def generate_report():
    open_module("report.py")


tk.Button(
    sidebar,
    text="Generate Report",
    font=("Arial", 11, "bold"),
    bg="#334155",
    fg="white",
    activebackground="#2563EB",
    relief="flat",
    width=22,
    height=2,
    command=generate_report
).pack(pady=5)

create_button("Logout")

content = tk.Frame(root, bg="#F1F5F9")
content.pack(side="left", fill="both", expand=True)


tk.Label(
    content,
    text="Welcome, Admin!",
    font=("Arial", 25, "bold"),
    bg="#F1F5F9",
    fg="#172554"
).pack(anchor="w", padx=40, pady=(40, 5))


tk.Label(
    content,
    text="Manage your examination seating activities here.",
    font=("Arial", 12),
    bg="#F1F5F9",
    fg="#64748B"
).pack(anchor="w", padx=40)

card_frame = tk.Frame(content, bg="#F1F5F9")
card_frame.pack(pady=65, padx=20)

card_data = [
    ("TOTAL STUDENTS", "#2563EB"),
    ("EXAM ROOMS", "#16A34A"),
    ("ALLOCATED SEATS", "#EA580C")
]

number_labels = []

for i, (title, color) in enumerate(card_data):

    card = tk.Frame(
        card_frame,
        bg="white",
        width=210,
        height=150,
        highlightbackground="#CBD5E1",
        highlightthickness=1
    )

    card.grid(row=0, column=i, padx=12)
    card.pack_propagate(False)

    tk.Label(
        card,
        text=title,
        font=("Arial", 11, "bold"),
        bg="white",
        fg="#64748B"
    ).pack(pady=(30, 10))

    number_label = tk.Label(
        card,
        text="0",
        font=("Arial", 28, "bold"),
        bg="white",
        fg=color
    )

    number_label.pack()

    number_labels.append(number_label)


student_number = number_labels[0]
room_number = number_labels[1]
allocation_number = number_labels[2]


tk.Button(
    content,
    text="REFRESH DASHBOARD",
    font=("Arial", 11, "bold"),
    bg="#2563EB",
    fg="white",
    width=22,
    height=2,
    command=refresh_dashboard
).pack(pady=10)

tk.Label(
    content,
    text="Exam Seat Allocation System | Python Project",
    font=("Arial", 10),
    bg="#F1F5F9",
    fg="#64748B"
).pack(side="bottom", pady=20)

refresh_dashboard()

root.mainloop()