import tkinter as tk
from tkinter import ttk, messagebox
from database import add_room, get_rooms, delete_room

root = tk.Tk()
root.title("Exam Room Management")
root.geometry("900x600")
root.configure(bg="#F1F5F9")
root.resizable(False, False)

header = tk.Frame(root, bg="#172554", height=80)
header.pack(fill="x")

tk.Label(
    header,
    text="EXAM ROOM MANAGEMENT",
    font=("Arial", 22, "bold"),
    bg="#172554",
    fg="white"
).pack(pady=20)

form = tk.LabelFrame(
    root,
    text="Add New Exam Room",
    font=("Arial", 14, "bold"),
    bg="white",
    padx=25,
    pady=25
)
form.pack(fill="x", padx=30, pady=25)

tk.Label(
    form,
    text="Room Name",
    font=("Arial", 12),
    bg="white"
).grid(row=0, column=0, padx=15, pady=15)

room_entry = tk.Entry(form, font=("Arial", 12), width=25)
room_entry.grid(row=0, column=1, padx=15, pady=15)

tk.Label(
    form,
    text="Room Capacity",
    font=("Arial", 12),
    bg="white"
).grid(row=0, column=2, padx=15, pady=15)

capacity_entry = tk.Entry(form, font=("Arial", 12), width=25)
capacity_entry.grid(row=0, column=3, padx=15, pady=15)

table_frame = tk.LabelFrame(
    root,
    text="Available Exam Rooms",
    font=("Arial", 14, "bold"),
    bg="white",
    padx=15,
    pady=15
)
table_frame.pack(fill="both", expand=True, padx=30, pady=10)

columns = ("ID", "Room Name", "Capacity")

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=200, anchor="center")

table.pack(fill="both", expand=True)


def load_rooms():
    for item in table.get_children():
        table.delete(item)

    rooms = get_rooms()

    for room in rooms:
        table.insert("", "end", values=room)


def save_room():
    room_name = room_entry.get().strip()
    capacity = capacity_entry.get().strip()

    if not room_name or not capacity:
        messagebox.showwarning(
            "Warning", "Please fill all fields!"
        )
        return

    try:
        capacity = int(capacity)

        if capacity <= 0:
            messagebox.showwarning(
                "Warning",
                "Capacity must be greater than zero!"
            )
            return

    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter a valid number for capacity!"
        )
        return

    result = add_room(room_name, capacity)

    if result:
        messagebox.showinfo(
            "Success",
            "Exam Room Added Successfully!"
        )

        room_entry.delete(0, tk.END)
        capacity_entry.delete(0, tk.END)
        load_rooms()

    else:
        messagebox.showerror(
            "Error",
            "This Room Name already exists!"
        )


def remove_room():
    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a room first!"
        )
        return

    room_data = table.item(selected[0], "values")
    room_id = room_data[0]
    room_name = room_data[1]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete {room_name}?\n\n"
        "Its seat allocations will also be deleted."
    )

    if confirm:
        result = delete_room(room_id)

        if result:
            messagebox.showinfo(
                "Success",
                "Room Deleted Successfully!"
            )
            load_rooms()
        else:
            messagebox.showerror(
                "Error",
                "Unable to delete room!"
            )


button_frame = tk.Frame(root, bg="#F1F5F9")
button_frame.pack(pady=15)

tk.Button(
    button_frame,
    text="ADD ROOM",
    font=("Arial", 11, "bold"),
    bg="#2563EB",
    fg="white",
    width=18,
    command=save_room
).grid(row=0, column=0, padx=10)

tk.Button(
    button_frame,
    text="DELETE ROOM",
    font=("Arial", 11, "bold"),
    bg="#DC2626",
    fg="white",
    width=18,
    command=remove_room
).grid(row=0, column=1, padx=10)

tk.Button(
    button_frame,
    text="REFRESH",
    font=("Arial", 11, "bold"),
    bg="#16A34A",
    fg="white",
    width=18,
    command=load_rooms
).grid(row=0, column=2, padx=10)

load_rooms()

root.mainloop()