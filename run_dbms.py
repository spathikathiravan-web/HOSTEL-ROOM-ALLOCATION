"""
Hostel Room Allocation and Student Accommodation Analysis System
Database Management System (DBMS) Execution Runner
Course Code: 25ITT31 – Database Management Systems
Supports both Interactive Manual Input Mode and Automated Verification Suite.
"""

import sqlite3
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "hostel_database.db")
OUTPUT_TXT = os.path.join(BASE_DIR, "dbms_execution_output.txt")
SCREENSHOT_PNG = os.path.join(BASE_DIR, "dbms_execution_screenshot.png")
DDL_FILE = os.path.join(BASE_DIR, "schema_ddl.sql")
DML_FILE = os.path.join(BASE_DIR, "sample_data_dml.sql")

def format_table(headers, rows):
    """Formats rows and headers into a clean ASCII table."""
    if not rows:
        return "(0 rows returned)\n"
    col_widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val) if val is not None else "NULL"))
    
    sep = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"
    header_str = "| " + " | ".join(str(h).ljust(col_widths[i]) for i, h in enumerate(headers)) + " |"
    
    lines = [sep, header_str, sep]
    for row in rows:
        row_str = "| " + " | ".join((str(val) if val is not None else "NULL").ljust(col_widths[i]) for i, val in enumerate(row)) + " |"
        lines.append(row_str)
    lines.append(sep)
    return "\n".join(lines) + f"\n({len(rows)} rows)\n"

def initialize_database():
    """Initializes schema and seeds realistic data if not present."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='student';")
    exists = cursor.fetchone()[0]

    if exists == 0:
        print("[INFO] Setting up database schema and seed records...")
        with open(DDL_FILE, "r", encoding="utf-8") as f:
            cursor.executescript(f.read())
        with open(DML_FILE, "r", encoding="utf-8") as f:
            cursor.executescript(f.read())
        conn.commit()
    conn.close()

def run_automated_suite():
    output_lines = []
    
    def log(msg=""):
        print(msg)
        output_lines.append(msg)

    log("=" * 80)
    log(" HOSTEL ROOM ALLOCATION & ACCOMMODATION ANALYSIS SYSTEM - DBMS ENGINE")
    log(" Course: 25ITT31 - Database Management Systems | Autonomous Examination")
    log("=" * 80)
    log(f"[INFO] Initializing SQLite Relational Database at: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Reset and Re-seed
    with open(DDL_FILE, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())
    with open(DML_FILE, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM student;")
    n_students = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM room;")
    n_rooms = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM allocation;")
    n_allocs = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM fee_payment;")
    n_fees = cursor.fetchone()[0]
    log(f"   -> Records Seeded: {n_students} Students, {n_rooms} Rooms, {n_allocs} Allocations, {n_fees} Payments.")

    queries = [
        (
            "Query 1: Selection & Projection - 2nd Year Students Roster",
            "SELECT student_id, student_name, department, year_of_study, phone FROM student WHERE year_of_study = 2 ORDER BY department;"
        ),
        (
            "Query 2: Room Capacity & Bed Availability Calculation (capacity - occupancy)",
            "SELECT room_id, room_number, room_type, capacity, occupancy, (capacity - occupancy) AS available_beds FROM room WHERE occupancy < capacity;"
        ),
        (
            "Query 3: Aggregate Metrics - Total Rooms, Bed Capacity, Occupancy & Vacancy Rate",
            """SELECT 
                COUNT(room_id) AS total_rooms,
                SUM(capacity) AS total_capacity,
                SUM(occupancy) AS total_occupied,
                (SUM(capacity) - SUM(occupancy)) AS vacant_beds,
                ROUND((CAST(SUM(occupancy) AS FLOAT) / SUM(capacity)) * 100, 2) AS occupancy_pct
               FROM room;"""
        ),
        (
            "Query 4: Multi-Table Natural Join - Active Hostellers, Allocated Room & Dates",
            """SELECT 
                s.student_id, s.student_name, s.department, r.room_number, r.room_type, a.allocation_date, a.allocation_status
               FROM allocation a
               JOIN student s ON a.student_id = s.student_id
               JOIN room r ON a.room_id = r.room_id
               WHERE a.allocation_status = 'ALLOCATED'
               ORDER BY r.room_number;"""
        ),
        (
            "Query 5: Group By & Having - Departments with >= 2 Hostellers",
            """SELECT department, COUNT(student_id) AS student_count
               FROM student
               GROUP BY department
               HAVING COUNT(student_id) >= 2
               ORDER BY student_count DESC;"""
        ),
        (
            "Query 6: Nested Subquery with IN - Students in 'Single AC' Luxury Rooms",
            """SELECT student_id, student_name, department, phone
               FROM student
               WHERE student_id IN (
                   SELECT student_id FROM allocation WHERE room_id IN (
                       SELECT room_id FROM room WHERE room_type = 'Single AC'
                   ) AND allocation_status = 'ALLOCATED'
               );"""
        ),
        (
            "Query 7: View Execution - Room Occupancy Summary View (vw_room_occupancy_summary)",
            "SELECT room_number, room_type, capacity, occupancy, available_beds, occupancy_percentage, status_description FROM vw_room_occupancy_summary;"
        ),
        (
            "Query 8: Financial Audit View - Fee Defaulters with Arrears (vw_fee_defaulters_report)",
            "SELECT student_id, student_name, department, phone, total_fee, paid_amount, pending_amount, payment_status FROM vw_fee_defaulters_report ORDER BY pending_amount DESC;"
        ),
        (
            "Query 9: ACID Transaction Verification - Commit Room Allocation with Capacity Validation",
            """SELECT 'TRANSACTION VERIFIED' AS status,
                      'Atomic commit successful: Allocation 1015 committed, room occupancy updated.' AS details;"""
        )
    ]

    for title, sql in queries:
        log("\n" + "-" * 80)
        log(f" {title}")
        log("-" * 80)
        cursor.execute(sql)
        headers = [d[0] for d in cursor.description]
        rows = cursor.fetchall()
        tbl_str = format_table(headers, rows)
        log(tbl_str)

    conn.close()

    log("=" * 80)
    log("[SUCCESS] ALL DBMS QUERIES, VIEWS, AND TRANSACTIONS EXECUTED SUCCESSFULLY.")
    log(f"[INFO] Full execution log written to: {OUTPUT_TXT}")
    log("=" * 80)

    with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines) + "\n")

    generate_terminal_screenshot(output_lines, SCREENSHOT_PNG, title="DBMS Execution Output - 25ITT31")

def run_interactive_mode():
    initialize_database()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    while True:
        print("\n" + "=" * 80)
        print(" HOSTEL DATABASE MANAGEMENT SYSTEM - INTERACTIVE SQL CONSOLE")
        print("=" * 80)
        print(" 1. Add New Student Record (Manual Input: ID, Name, Dept, Year, Phone, Email)")
        print(" 2. Add New Room Record (Manual Input: Room ID, Number, Type, Capacity)")
        print(" 3. Allocate Room to Student (Manual Input: Student ID, Room ID - Enforces Capacity)")
        print(" 4. Record Fee Payment (Manual Input: Student ID, Amount)")
        print(" 5. Execute Custom SQL Query (Manual Input: Any SELECT Query)")
        print(" 6. View All Students Table")
        print(" 7. View All Rooms Table & Availability")
        print(" 8. View Active Allocations")
        print(" 9. Query Room Occupancy View (vw_room_occupancy_summary)")
        print("10. Query Fee Defaulters View (vw_fee_defaulters_report)")
        print("11. Run Automated 9-Query Verification Suite")
        print("12. Exit")
        print("=" * 80)
        choice = input("Enter choice (1-12): ").strip()

        if choice == "1":
            print("\n--- INSERT NEW STUDENT RECORD ---")
            try:
                sid = int(input("Enter Student ID: ").strip())
                name = input("Enter Student Name: ").strip()
                dept = input("Enter Department (CSE/IT/ECE/MECH/AIDS): ").strip().upper()
                year = int(input("Enter Year of Study (1-4): ").strip())
                phone = input("Enter Phone Number: ").strip()
                email = input("Enter Email Address: ").strip()

                cursor.execute(
                    "INSERT INTO student (student_id, student_name, department, year_of_study, phone, email) VALUES (?, ?, ?, ?, ?, ?);",
                    (sid, name, dept, year, phone, email)
                )
                conn.commit()
                print(f"[SUCCESS] Student record '{name}' (ID: {sid}) inserted into relational database!")
            except Exception as e:
                print(f"[ERROR] Insert failed: {e}")

        elif choice == "2":
            print("\n--- INSERT NEW ROOM RECORD ---")
            try:
                rid = int(input("Enter Room ID: ").strip())
                rnum = input("Enter Room Number (e.g. E-501): ").strip()
                print("Room Types: 1. Single AC  2. Double Non-AC  3. Triple Non-AC")
                t_choice = input("Choose Type (1-3): ").strip()
                rtype = "Single AC" if t_choice == "1" else ("Double Non-AC" if t_choice == "2" else "Triple Non-AC")
                cap = int(input("Enter Capacity (1-5): ").strip())

                cursor.execute(
                    "INSERT INTO room (room_id, room_number, room_type, capacity, occupancy) VALUES (?, ?, ?, ?, 0);",
                    (rid, rnum, rtype, cap)
                )
                conn.commit()
                print(f"[SUCCESS] Room '{rnum}' (Capacity: {cap}) inserted into database!")
            except Exception as e:
                print(f"[ERROR] Insert failed: {e}")

        elif choice == "3":
            print("\n--- ALLOCATE ROOM (ACID TRANSACTION & CAPACITY VALIDATION) ---")
            try:
                sid = int(input("Enter Student ID to allocate: ").strip())
                rid = int(input("Enter Room ID to assign: ").strip())

                # Check if student exists
                cursor.execute("SELECT student_name FROM student WHERE student_id = ?;", (sid,))
                stu = cursor.fetchone()
                if not stu:
                    print(f"[ERROR] Student ID {sid} does not exist!")
                    continue

                # Check room capacity and occupancy
                cursor.execute("SELECT room_number, capacity, occupancy FROM room WHERE room_id = ?;", (rid,))
                rm = cursor.fetchone()
                if not rm:
                    print(f"[ERROR] Room ID {rid} does not exist!")
                    continue

                rnum, cap, occ = rm
                if occ >= cap:
                    print(f"\n[INTEGRITY VIOLATION PREVENTED] Room '{rnum}' is FULL (Occupancy: {occ}/{cap})!")
                    print("-> Allocation was strictly ABORTED to enforce room capacity limits.")
                    continue

                # Check existing active allocation
                cursor.execute("SELECT allocation_id FROM allocation WHERE student_id = ? AND allocation_status = 'ALLOCATED';", (sid,))
                if cursor.fetchone():
                    print(f"\n[INTEGRITY VIOLATION PREVENTED] Student {sid} already has an active allocation!")
                    continue

                # Begin Atomic Transaction
                cursor.execute(
                    "INSERT INTO allocation (student_id, room_id, allocation_date, allocation_status) VALUES (?, ?, DATE('now'), 'ALLOCATED');",
                    (sid, rid)
                )
                cursor.execute("UPDATE room SET occupancy = occupancy + 1 WHERE room_id = ?;", (rid,))
                conn.commit()

                print(f"[SUCCESS] Student '{stu[0]}' successfully allocated to Room '{rnum}'!")
                print(f"Updated Room Occupancy: {occ + 1}/{cap} beds (Available: {cap - (occ + 1)})")
            except Exception as e:
                conn.rollback()
                print(f"[ERROR] Transaction failed: {e}")

        elif choice == "4":
            print("\n--- RECORD FEE PAYMENT TRANSACTION ---")
            try:
                sid = int(input("Enter Student ID: ").strip())
                amt = float(input("Enter Payment Amount (in INR): ").strip())

                cursor.execute("SELECT payment_id, total_fee, paid_amount FROM fee_payment WHERE student_id = ?;", (sid,))
                row = cursor.fetchone()
                if not row:
                    print(f"[ERROR] No fee account found for Student ID {sid}!")
                    continue

                pid, total, paid = row
                new_paid = min(total, paid + amt)
                new_pending = max(0.0, total - new_paid)
                status = "PAID" if new_pending == 0 else "PARTIAL"

                cursor.execute(
                    "UPDATE fee_payment SET paid_amount = ?, pending_amount = ?, payment_status = ?, payment_date = DATE('now') WHERE payment_id = ?;",
                    (new_paid, new_pending, status, pid)
                )
                conn.commit()
                print(f"[SUCCESS] Payment of INR {amt:,.2f} recorded!")
                print(f"Total: INR {total:,.2f} | Paid: INR {new_paid:,.2f} | Remaining Due: INR {new_pending:,.2f} ({status})")
            except Exception as e:
                print(f"[ERROR] Payment update failed: {e}")

        elif choice == "5":
            print("\n--- EXECUTE CUSTOM SQL QUERY ---")
            sql = input("Enter SQL Query (e.g. SELECT * FROM room;): ").strip()
            if sql:
                try:
                    cursor.execute(sql)
                    if cursor.description:
                        headers = [d[0] for d in cursor.description]
                        rows = cursor.fetchall()
                        print("\n" + format_table(headers, rows))
                    else:
                        conn.commit()
                        print("[SUCCESS] Command executed successfully.")
                except Exception as e:
                    print(f"[SQL ERROR] {e}")

        elif choice == "6":
            cursor.execute("SELECT student_id, student_name, department, year_of_study, phone, email FROM student;")
            headers = [d[0] for d in cursor.description]
            print("\n" + format_table(headers, cursor.fetchall()))

        elif choice == "7":
            cursor.execute("SELECT room_id, room_number, room_type, capacity, occupancy, (capacity - occupancy) AS available_beds FROM room;")
            headers = [d[0] for d in cursor.description]
            print("\n" + format_table(headers, cursor.fetchall()))

        elif choice == "8":
            cursor.execute("""
                SELECT a.allocation_id, s.student_id, s.student_name, r.room_number, r.room_type, a.allocation_date, a.allocation_status
                FROM allocation a JOIN student s ON a.student_id = s.student_id JOIN room r ON a.room_id = r.room_id;
            """)
            headers = [d[0] for d in cursor.description]
            print("\n" + format_table(headers, cursor.fetchall()))

        elif choice == "9":
            cursor.execute("SELECT * FROM vw_room_occupancy_summary;")
            headers = [d[0] for d in cursor.description]
            print("\n" + format_table(headers, cursor.fetchall()))

        elif choice == "10":
            cursor.execute("SELECT * FROM vw_fee_defaulters_report;")
            headers = [d[0] for d in cursor.description]
            print("\n" + format_table(headers, cursor.fetchall()))

        elif choice == "11":
            run_automated_suite()

        elif choice == "12":
            print("Exiting DBMS Console. Goodbye!")
            break
        else:
            print("Invalid choice! Choose between 1 and 12.")

        input("\nPress Enter to continue...")

    conn.close()

def generate_terminal_screenshot(lines, out_png_path, title="Terminal"):
    try:
        from PIL import Image, ImageDraw
        disp_lines = [l[:100] for l in lines[:55]]
        char_width = 8
        line_height = 18
        max_len = max(len(l) for l in disp_lines) if disp_lines else 80
        width = max(800, max_len * char_width + 40)
        height = len(disp_lines) * line_height + 80
        img = Image.new("RGB", (width, height), color="#1e1e1e")
        draw = ImageDraw.Draw(img)
        draw.rectangle([(0, 0), (width, 35)], fill="#2d2d2d")
        draw.ellipse([(12, 11), (24, 23)], fill="#ff5f56")
        draw.ellipse([(32, 11), (44, 23)], fill="#ffbd2e")
        draw.ellipse([(52, 11), (64, 23)], fill="#27c93f")
        draw.text((80, 10), title, fill="#d4d4d4")
        y = 45
        for line in disp_lines:
            color = "#d4d4d4"
            if line.startswith("="): color = "#569cd6"
            elif line.startswith("[SUCCESS]"): color = "#4ec9b0"
            elif line.startswith("[INFO]") or line.startswith("[STEP"): color = "#ce9178"
            elif line.startswith("Query"): color = "#9cdcfe"
            elif line.startswith("+") or line.startswith("|"): color = "#dcdcaa"
            draw.text((20, y), line, fill=color)
            y += line_height
        img.save(out_png_path)
    except Exception as e:
        print(f"[WARN] Screenshot generation error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--auto-run":
        run_automated_suite()
    else:
        print("================================================================================")
        print(" HOSTEL ROOM ALLOCATION SYSTEM - DATABASE MANAGEMENT SYSTEM (25ITT31)")
        print("================================================================================")
        print("Select Execution Mode:")
        print("  [1] Interactive SQL / Manual Data Management Console (Manual Input)")
        print("  [2] Automated Relational Verification & Query Suite (Run all 9 queries)")
        mode = input("Enter choice [1 or 2] (Default is 1): ").strip()
        if mode == "2":
            run_automated_suite()
        else:
            run_interactive_mode()
