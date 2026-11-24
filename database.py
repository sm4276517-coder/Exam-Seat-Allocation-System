import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "exam.db")


def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            semester TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_name TEXT UNIQUE NOT NULL,
            capacity INTEGER NOT NULL CHECK(capacity > 0)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS allocations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_roll TEXT NOT NULL UNIQUE,
            room_name TEXT NOT NULL,
            seat_number TEXT NOT NULL,
            UNIQUE(room_name, seat_number)
        )
    """)

    conn.commit()
    conn.close()


def add_student(roll, name, department, semester):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO students
            (roll, name, department, semester)
            VALUES (?, ?, ?, ?)
        """, (roll, name, department, semester))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    except sqlite3.Error as error:
        print("Student Error:", error)
        return False
    finally:
        conn.close()


def get_students():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students ORDER BY id")
    data = cursor.fetchall()
    conn.close()
    return data


def update_student(student_id, roll, name, department, semester):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT roll FROM students WHERE id = ?",
            (student_id,)
        )
        old_student = cursor.fetchone()

        if old_student is None:
            return False

        old_roll = old_student[0]

        cursor.execute("""
            UPDATE students
            SET roll = ?, name = ?, department = ?, semester = ?
            WHERE id = ?
        """, (roll, name, department, semester, student_id))

        if old_roll != roll:
            cursor.execute("""
                UPDATE allocations
                SET student_roll = ?
                WHERE student_roll = ?
            """, (roll, old_roll))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        conn.rollback()
        return False
    except sqlite3.Error as error:
        conn.rollback()
        print("Update Error:", error)
        return False
    finally:
        conn.close()


def delete_student(student_id):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT roll FROM students WHERE id = ?",
            (student_id,)
        )
        student = cursor.fetchone()

        if student is None:
            return False

        roll = student[0]

        cursor.execute(
            "DELETE FROM allocations WHERE student_roll = ?",
            (roll,)
        )
        cursor.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

        conn.commit()
        return True

    except sqlite3.Error as error:
        conn.rollback()
        print("Delete Error:", error)
        return False
    finally:
        conn.close()


def add_room(room_name, capacity):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO rooms (room_name, capacity)
            VALUES (?, ?)
        """, (room_name, capacity))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    except sqlite3.Error as error:
        print("Room Error:", error)
        return False
    finally:
        conn.close()


def get_rooms():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rooms ORDER BY id")
    data = cursor.fetchall()
    conn.close()
    return data


def delete_room(room_id):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT room_name FROM rooms WHERE id = ?",
            (room_id,)
        )
        room = cursor.fetchone()

        if room is None:
            return False

        room_name = room[0]

        cursor.execute(
            "DELETE FROM allocations WHERE room_name = ?",
            (room_name,)
        )
        cursor.execute(
            "DELETE FROM rooms WHERE id = ?",
            (room_id,)
        )

        conn.commit()
        return True

    except sqlite3.Error as error:
        conn.rollback()
        print("Room Delete Error:", error)
        return False
    finally:
        conn.close()


def get_allocations():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM allocations ORDER BY id")
    data = cursor.fetchall()
    conn.close()
    return data


create_tables()


if __name__ == "__main__":
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM rooms")
    total_rooms = cursor.fetchone()[0]

    print("--------------------------------")
    print("DATABASE CONNECTED SUCCESSFULLY")
    print("--------------------------------")
    print("Total Students:", total_students)
    print("Total Rooms:", total_rooms)

    conn.close()