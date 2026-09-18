"""
database.py - Simple SQLite database operations for saving courses and attendance.
Uses standard sqlite3 with simple helper functions.
"""

import sqlite3
from datetime import datetime


class AttendanceDB:
    def __init__(self, db_file="attendance.db"):
        self.db_file = db_file
        self.init_tables()

    def get_conn(self):
        """Connects to SQLite database."""
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        return conn

    def init_tables(self):
        """Creates courses and attendance tables if they don't exist."""
        conn = self.get_conn()
        cursor = conn.cursor()

        # Table for storing courses
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                target REAL DEFAULT 75.0,
                total_classes INTEGER DEFAULT 45
            );
        """)

        # Table for storing daily attendance logs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER,
                status TEXT NOT NULL,
                date TEXT NOT NULL,
                note TEXT,
                FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE
            );
        """)

        conn.commit()
        conn.close()

    def add_course(self, code, name, target=75.0, total_classes=45):
        """Adds a new course."""
        code = code.strip().upper()
        name = name.strip()
        conn = self.get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO courses (code, name, target, total_classes) VALUES (?, ?, ?, ?)",
                (code, name, target, total_classes)
            )
            conn.commit()
            course_id = cursor.lastrowid
            conn.close()
            return course_id
        except sqlite3.IntegrityError:
            conn.close()
            return None  # Course code already exists

    def get_all_courses(self):
        """Returns list of all courses."""
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT id, code, name, target, total_classes FROM courses ORDER BY code")
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    def get_course_by_code(self, code):
        """Finds a single course by its code."""
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT id, code, name, target, total_classes FROM courses WHERE UPPER(code) = ?", (code.strip().upper(),))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def mark_attendance(self, course_id, status, date_str, note=""):
        """Marks attendance for a class session (PRESENT, ABSENT, MEDICAL, CANCELLED)."""
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO attendance (course_id, status, date, note) VALUES (?, ?, ?, ?)",
            (course_id, status.upper(), date_str, note)
        )
        conn.commit()
        conn.close()

    def get_attendance_count(self, course_id):
        """Returns (attended, conducted) count for a course."""
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN status = 'PRESENT' THEN 1 ELSE 0 END) AS attended,
                SUM(CASE WHEN status IN ('PRESENT', 'ABSENT') THEN 1 ELSE 0 END) AS conducted
            FROM attendance
            WHERE course_id = ?
        """, (course_id,))
        row = cursor.fetchone()
        conn.close()
        attended = row["attended"] or 0
        conducted = row["conducted"] or 0
        return int(attended), int(conducted)

    def get_course_history(self, course_id, limit=20):
        """Returns recent attendance records for a course."""
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT status, date, note FROM attendance WHERE course_id = ? ORDER BY id DESC LIMIT ?",
            (course_id, limit)
        )
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    def delete_course(self, course_id):
        """Deletes a course and its attendance logs."""
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM attendance WHERE course_id = ?", (course_id,))
        cursor.execute("DELETE FROM courses WHERE id = ?", (course_id,))
        conn.commit()
        conn.close()

    def seed_demo_data(self):
        """Fills database with 4 college courses and attendance data for easy testing."""
        courses = [
            ("CSE1021", "Python Essentials", 75.0, 45),
            ("MAT1011", "Calculus for Engineers", 75.0, 45),
            ("PHY1001", "Engineering Physics", 75.0, 40),
            ("CSE2005", "Data Structures", 80.0, 50),
        ]
        for code, name, target, total in courses:
            c_id = self.add_course(code, name, target, total)
            if not c_id:
                continue
            if code == "CSE1021":
                # 18 present out of 20 -> 90% (Can bunk 4 classes)
                for i in range(1, 19):
                    self.mark_attendance(c_id, "PRESENT", f"2026-08-{i:02d}", "Attended")
                for i in range(19, 21):
                    self.mark_attendance(c_id, "ABSENT", f"2026-08-{i:02d}", "Absent")
            elif code == "MAT1011":
                # 14 present out of 20 -> 70% (Needs 4 classes to recover)
                for i in range(1, 15):
                    self.mark_attendance(c_id, "PRESENT", f"2026-08-{i:02d}", "Attended")
                for i in range(15, 21):
                    self.mark_attendance(c_id, "ABSENT", f"2026-08-{i:02d}", "Absent")
            elif code == "PHY1001":
                # 15 present out of 20 -> 75% exact
                for i in range(1, 16):
                    self.mark_attendance(c_id, "PRESENT", f"2026-08-{i:02d}", "Attended")
                for i in range(16, 21):
                    self.mark_attendance(c_id, "ABSENT", f"2026-08-{i:02d}", "Absent")
