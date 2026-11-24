
import tkinter as tk
from tkinter import messagebox, filedialog
import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, Image, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from database import connect_db

COLLEGE_NAME = "YOUR COLLEGE NAME"
COLLEGE_ADDRESS = "YOUR COLLEGE ADDRESS"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "college_logo.png")


def generate_report():

    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")],
        title="Save Exam Report"
    )

    if not file_path:
        return

    try:
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
            ORDER BY students.roll
        """)

        records = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) FROM students")
        total_students = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM rooms")
        total_rooms = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM allocations")
        total_allocations = cursor.fetchone()[0]

        conn.close()

    except Exception as error:
        try:
            conn.close()
        except:
            pass

        messagebox.showerror("Database Error", str(error))
        return

    try:
        document = SimpleDocTemplate(
            file_path,
            pagesize=landscape(A4),
            rightMargin=30,
            leftMargin=30,
            topMargin=25,
            bottomMargin=30
        )

        styles = getSampleStyleSheet()

        college_style = ParagraphStyle(
            "College",
            parent=styles["Title"],
            fontSize=20,
            textColor=colors.HexColor("#172554"),
            alignment=TA_CENTER,
            spaceAfter=5
        )

        address_style = ParagraphStyle(
            "Address",
            parent=styles["Normal"],
            fontSize=10,
            alignment=TA_CENTER
        )

        title_style = ParagraphStyle(
            "ReportTitle",
            parent=styles["Heading2"],
            fontSize=15,
            textColor=colors.HexColor("#2563EB"),
            alignment=TA_CENTER
        )

        elements = []

        if os.path.exists(LOGO_PATH):
            logo = Image(LOGO_PATH, width=75, height=75)
        else:
            logo = Paragraph("", styles["Normal"])

        college_info = [
            Paragraph(COLLEGE_NAME, college_style),
            Paragraph(COLLEGE_ADDRESS, address_style),
            Paragraph(
                "<b>EXAM SEAT ALLOCATION SYSTEM</b>",
                address_style
            )
        ]

        header_table = Table(
            [[logo, college_info]],
            colWidths=[100, 680]
        )

        header_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (0, 0), (0, 0), "CENTER"),
            ("LINEBELOW", (0, 0), (-1, -1), 2,
             colors.HexColor("#2563EB")),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12)
        ]))

        elements.append(header_table)
        elements.append(Spacer(1, 15))

        elements.append(
            Paragraph("STUDENT SEAT ALLOCATION REPORT", title_style)
        )

        elements.append(Spacer(1, 10))

        elements.append(
            Paragraph(
                "Report Date: " +
                datetime.now().strftime("%d-%m-%Y %H:%M"),
                styles["Normal"]
            )
        )

        elements.append(Spacer(1, 15))

        summary_data = [
            ["Total Students", "Total Exam Rooms", "Allocated Seats"],
            [
                str(total_students),
                str(total_rooms),
                str(total_allocations)
            ]
        ]

        summary_table = Table(
            summary_data,
            colWidths=[220, 220, 220]
        )

        summary_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0),
             colors.HexColor("#172554")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("BACKGROUND", (0, 1), (-1, 1),
             colors.HexColor("#E2E8F0")),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 11),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("GRID", (0, 0), (-1, -1), 1, colors.white)
        ]))

        elements.append(summary_table)
        elements.append(Spacer(1, 25))

        elements.append(
            Paragraph(
                "STUDENT ALLOCATION DETAILS",
                styles["Heading2"]
            )
        )

        elements.append(Spacer(1, 10))

        table_data = [[
            "Roll Number",
            "Student Name",
            "Department",
            "Semester",
            "Room Name",
            "Seat Number"
        ]]

        for record in records:

            room = record[4] if record[4] else "Not Allocated"
            seat = record[5] if record[5] else "Not Allocated"

            table_data.append([
                str(record[0]),
                str(record[1]),
                str(record[2]),
                str(record[3]),
                str(room),
                str(seat)
            ])

        report_table = Table(
            table_data,
            repeatRows=1,
            colWidths=[90, 130, 130, 80, 120, 100]
        )

        report_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0),
             colors.HexColor("#2563EB")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ("TOPPADDING", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
                colors.white,
                colors.HexColor("#F1F5F9")
            ])
        ]))

        elements.append(report_table)
        elements.append(Spacer(1, 45))

        # Signature Section
        signature_data = [
            ["____________________", "____________________"],
            ["Exam Controller", "Principal"],
            ["Date: ______________", "Date: ______________"]
        ]

        signature_table = Table(
            signature_data,
            colWidths=[350, 350],
            rowHeights=[25, 22, 22]
        )

        signature_table.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("TEXTCOLOR", (0, 1), (-1, 1),
             colors.HexColor("#172554")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
        ]))

        elements.append(KeepTogether([
            signature_table
        ]))

        document.build(elements)

        messagebox.showinfo(
            "Success",
            "Professional PDF Report Generated Successfully!\n\n"
            + file_path
        )

    except Exception as error:
        messagebox.showerror("Report Error", str(error))


# Run Application
if __name__ == "__main__":

    root = tk.Tk()
    root.title("Generate Exam Report")
    root.geometry("650x400")
    root.configure(bg="#F1F5F9")
    root.resizable(False, False)

    header = tk.Frame(root, bg="#172554", height=85)
    header.pack(fill="x")

    tk.Label(
        header,
        text="GENERATE EXAM REPORT",
        font=("Arial", 21, "bold"),
        bg="#172554",
        fg="white"
    ).pack(pady=22)

    tk.Label(
        root,
        text="Create a professional PDF report of student seat allocation.",
        font=("Arial", 11),
        bg="#F1F5F9",
        fg="#475569"
    ).pack(pady=35)

    tk.Button(
        root,
        text="GENERATE PDF REPORT",
        font=("Arial", 13, "bold"),
        bg="#2563EB",
        fg="white",
        width=25,
        height=2,
        command=generate_report
    ).pack(pady=15)

    tk.Label(
        root,
        text="Exam Seat Allocation System | Python Project",
        font=("Arial", 10),
        bg="#F1F5F9",
        fg="#64748B"
    ).pack(side="bottom", pady=20)

    root.mainloop()
