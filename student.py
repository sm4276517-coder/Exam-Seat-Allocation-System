import tkinter as tk
from tkinter import ttk, messagebox
from database import (
    add_student,
    get_students,
    update_student,
    delete_student
)

root = tk.Tk()
root.title("Student Management")
root.geometry("1000x700")
root.configure(bg="#F1F5F9")

selected_id = None

header = tk.Frame(root, bg="#172554", height=80)
header.pack(fill="x")

tk.Label(
    header,
    text="STUDENT MANAGEMENT",
    font=("Arial", 22, "bold"),
    bg="#172554",
    fg="white"
).pack(pady=20)

form = tk.LabelFrame(
    root,
    text="Student Registration",
    font=("Arial", 14, "bold"),
    bg="white",
    padx=20,
    pady=20
)
form.pack(fill="x", padx=30, pady=15)

tk.Label(form, text="Roll Number", bg="white").grid(
    row=0, column=0, padx=10, pady=10
)
roll_entry = tk.Entry(form, width=25, font=("Arial", 11))
roll_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(form, text="Student Name", bg="white").grid(
    row=0, column=2, padx=10, pady=10
)
name_entry = tk.Entry(form, width=25, font=("Arial", 11))
name_entry.grid(row=0, column=3, padx=10, pady=10)

tk.Label(form, text="Department", bg="white").grid(
    row=1, column=0, padx=10, pady=10
)
department_entry = tk.Entry(form, width=25, font=("Arial", 11))
department_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(form, text="Semester", bg="white").grid(
    row=1, column=2, padx=10, pady=10
)
semester_entry = ttk.Combobox(
    form,
    values=["1st", "2nd", "3rd", "4th",
            "5th", "6th", "7th", "8th"],
    width=22,
    state="readonly"
)
semester_entry.grid(row=1, column=3, padx=10, pady=10)

table_frame = tk.LabelFrame(
    root,
    text="Student Records",
    font=("Arial", 14, "bold"),
    bg="white",
    padx=10,
    pady=10
)
table_frame.pack(fill="both", expand=True, padx=30, pady=10)

columns = ("ID", "Roll", "Name", "Department", "Semester")

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=12
)

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=150, anchor="center")

table.pack(fill="both", expand=True)


def load_students():
    for item in table.get_children():
        table.delete(item)

    for student in get_students():
        table.insert("", "end", values=student)


def clear_fields():
    global selected_id
    selected_id = None

    roll_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    department_entry.delete(0, tk.END)
    semester_entry.set("")

    table.selection_remove(table.selection())


def select_student(event):
    global selected_id

    selected = table.selection()

    if not selected:
        return

    values = table.item(selected[0], "values")

    selected_id = int(values[0])

    clear_entries_only()

    roll_entry.insert(0, values[1])
    name_entry.insert(0, values[2])
    department_entry.insert(0, values[3])
    semester_entry.set(values[4])


def clear_entries_only():
    roll_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    department_entry.delete(0, tk.END)
    semester_entry.set("")


def save_student():
    roll = roll_entry.get().strip()
    name = name_entry.get().strip()
    department = department_entry.get().strip()
    semester = semester_entry.get()

    if not roll or not name or not department or not semester:
        messagebox.showwarning("Warning", "Please fill all fields!")
        return

    if add_student(roll, name, department, semester):
        messagebox.showinfo("Success", "Student Added Successfully!")
        clear_fields()
        load_students()
    else:
        messagebox.showerror("Error", "This Roll Number already exists!")


def edit_student():
    if selected_id is None:
        messagebox.showwarning("Warning", "Please select a student first!")
        return

    roll = roll_entry.get().strip()
    name = name_entry.get().strip()
    department = department_entry.get().strip()
    semester = semester_entry.get()

    if not roll or not name or not department or not semester:
        messagebox.showwarning("Warning", "Please fill all fields!")
        return

    confirm = messagebox.askyesno(
        "Confirm Update",
        "Do you want to update this student?"
    )

    if confirm:
        result = update_student(
            selected_id, roll, name, department, semester
        )

        if result:
            messagebox.showinfo("Success", "Student Updated Successfully!")
            clear_fields()
            load_students()
        else:
            messagebox.showerror(
                "Error",
                "Update failed! Roll Number may already exist."
            )


def remove_student():
    if selected_id is None:
        messagebox.showwarning("Warning", "Please select a student first!")
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this student?\n"
        "Their seat allocation will also be deleted."
    )

    if confirm:
        if delete_student(selected_id):
            messagebox.showinfo("Success", "Student Deleted Successfully!")
            clear_fields()
            load_students()
        else:
            messagebox.showerror("Error", "Unable to delete student!")


table.bind("<<TreeviewSelect>>", select_student)

button_frame = tk.Frame(root, bg="#F1F5F9")
button_frame.pack(pady=12)

tk.Button(
    button_frame,
    text="ADD STUDENT",
    bg="#2563EB",
    fg="white",
    width=16,
    command=save_student
).grid(row=0, column=0, padx=6)

tk.Button(
    button_frame,
    text="UPDATE STUDENT",
    bg="#D97706",
    fg="white",
    width=16,
    command=edit_student
).grid(row=0, column=1, padx=6)

tk.Button(
    button_frame,
    text="DELETE STUDENT",
    bg="#DC2626",
    fg="white",
    width=16,
    command=remove_student
).grid(row=0, column=2, padx=6)

tk.Button(
    button_frame,
    text="CLEAR",
    bg="#64748B",
    fg="white",
    width=12,
    command=clear_fields
).grid(row=0, column=3, padx=6)

tk.Button(
    button_frame,
    text="REFRESH",
    bg="#16A34A",
    fg="white",
    width=12,
    command=load_students
).grid(row=0, column=4, padx=6)

load_students()
root.mainloop()