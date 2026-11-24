
import tkinter as tk
from tkinter import ttk, messagebox
from database import connect_db


def search_student():
    roll = roll_entry.get().strip()

    if roll == "":
        messagebox.showwarning("Warning", "Please enter Roll Number!")
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT students.roll,
               students.name,
               students.department,
               students.semester,
               allocations.room_name,
               allocations.seat_number
        FROM students
        LEFT JOIN allocations
        ON students.roll = allocations.student_roll
        WHERE students.roll = ?
    """, (roll,))

    result = cursor.fetchone()
    conn.close()

    for item in table.get_children():
        table.delete(item)

    if result:
        room = result[4] if result[4] else "Not Allocated"
        seat = result[5] if result[5] else "Not Allocated"

        table.insert(
            "",
            "end",
            values=(
                result[0],
                result[1],
                result[2],
                result[3],
                room,
                seat
            )
        )
    else:
        messagebox.showinfo("Not Found", "Student not found!")


def clear_data():
    roll_entry.delete(0, tk.END)

    for item in table.get_children():
        table.delete(item)

root = tk.Tk()
root.title("Search Student")
root.geometry("1000x600")
root.configure(bg="#F1F5F9")
root.resizable(False, False)

header = tk.Frame(root, bg="#172554", height=80)
header.pack(fill="x")

tk.Label(
    header,
    text="SEARCH STUDENT",
    font=("Arial", 22, "bold"),
    bg="#172554",
    fg="white"
).pack(pady=20)

search_frame = tk.Frame(root, bg="white", padx=30, pady=25)
search_frame.pack(pady=30)

tk.Label(
    search_frame,
    text="Enter Student Roll Number:",
    font=("Arial", 13, "bold"),
    bg="white"
).grid(row=0, column=0, padx=10)

roll_entry = tk.Entry(
    search_frame,
    font=("Arial", 13),
    width=25
)
roll_entry.grid(row=0, column=1, padx=10)

tk.Button(
    search_frame,
    text="SEARCH",
    font=("Arial", 11, "bold"),
    bg="#2563EB",
    fg="white",
    width=12,
    command=search_student
).grid(row=0, column=2, padx=10)

tk.Button(
    search_frame,
    text="CLEAR",
    font=("Arial", 11, "bold"),
    bg="#DC2626",
    fg="white",
    width=12,
    command=clear_data
).grid(row=0, column=3, padx=10)

table_frame = tk.LabelFrame(
    root,
    text="Student Details",
    font=("Arial", 14, "bold"),
    bg="white",
    padx=15,
    pady=15
)
table_frame.pack(fill="both", expand=True, padx=30, pady=20)

columns = (
    "Roll",
    "Name",
    "Department",
    "Semester",
    "Room",
    "Seat"
)

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=140, anchor="center")

table.pack(fill="both", expand=True)

root.mainloop()