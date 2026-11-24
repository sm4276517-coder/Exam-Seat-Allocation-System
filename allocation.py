
import tkinter as tk
from tkinter import ttk, messagebox
from database import connect_db


def load_allocations():
    for item in table.get_children():
        table.delete(item)

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT students.roll, students.name,
               allocations.room_name, allocations.seat_number
        FROM allocations
        JOIN students
        ON students.roll = allocations.student_roll
        ORDER BY students.roll
    """)

    records = cursor.fetchall()

    for record in records:
        table.insert("", "end", values=record)

    conn.close()


def allocate_seats():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT roll, name FROM students ORDER BY roll")
    students = cursor.fetchall()

    cursor.execute("SELECT room_name, capacity FROM rooms ORDER BY room_name")
    rooms = cursor.fetchall()

    if len(students) == 0:
        messagebox.showwarning("Warning", "Please add students first!")
        conn.close()
        return

    if len(rooms) == 0:
        messagebox.showwarning("Warning", "Please add rooms first!")
        conn.close()
        return

    cursor.execute("SELECT student_roll FROM allocations")
    allocated = [row[0] for row in cursor.fetchall()]

    remaining = [s for s in students if s[0] not in allocated]

    if len(remaining) == 0:
        messagebox.showinfo("Info", "All students are already allocated!")
        conn.close()
        return

    count = 0

    for room_name, capacity in rooms:

        cursor.execute(
            "SELECT seat_number FROM allocations WHERE room_name = ?",
            (room_name,)
        )

        used_seats = [row[0] for row in cursor.fetchall()]

        for seat in range(1, capacity + 1):

            if len(remaining) == 0:
                break

            seat_number = "S" + str(seat).zfill(2)

            if seat_number in used_seats:
                continue

            student = remaining.pop(0)

            cursor.execute("""
                INSERT INTO allocations
                (student_roll, room_name, seat_number)
                VALUES (?, ?, ?)
            """, (student[0], room_name, seat_number))

            count += 1

        if len(remaining) == 0:
            break

    conn.commit()
    conn.close()

    load_allocations()

    messagebox.showinfo(
        "Success",
        str(count) + " Students Allocated Successfully!"
    )

root = tk.Tk()
root.title("Automatic Seat Allocation")
root.geometry("1000x650")
root.configure(bg="#F1F5F9")
root.resizable(False, False)
header = tk.Frame(root, bg="#172554", height=80)
header.pack(fill="x")

tk.Label(
    header,
    text="AUTOMATIC SEAT ALLOCATION",
    font=("Arial", 22, "bold"),
    bg="#172554",
    fg="white"
).pack(pady=20)

tk.Label(
    root,
    text="Automatically assign exam rooms and seat numbers to students.",
    font=("Arial", 12),
    bg="#F1F5F9"
).pack(pady=20)

button_frame = tk.Frame(root, bg="#F1F5F9")
button_frame.pack(pady=15)

tk.Button(
    button_frame,
    text="ALLOCATE SEATS",
    font=("Arial", 12, "bold"),
    bg="#2563EB",
    fg="white",
    width=20,
    height=2,
    command=allocate_seats
).grid(row=0, column=0, padx=10)

tk.Button(
    button_frame,
    text="REFRESH",
    font=("Arial", 12, "bold"),
    bg="#16A34A",
    fg="white",
    width=20,
    height=2,
    command=load_allocations
).grid(row=0, column=1, padx=10)
table_frame = tk.LabelFrame(
    root,
    text="Student Seat Allocation Records",
    font=("Arial", 14, "bold"),
    bg="white",
    padx=15,
    pady=15
)
table_frame.pack(fill="both", expand=True, padx=30, pady=20)

columns = ("Roll Number", "Student Name", "Room Name", "Seat Number")

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=200, anchor="center")

table.pack(fill="both", expand=True)

load_allocations()

root.mainloop()