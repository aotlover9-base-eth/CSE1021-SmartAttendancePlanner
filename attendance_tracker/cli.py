"""
cli.py - Simple interactive terminal menu for the attendance planner.
Asks for inputs one at a time with simple validations.
"""

import sys
from datetime import date
from .database import AttendanceDB
from .calculator import calculate_percentage, calculate_bunks, calculate_recovery, get_status


class SimpleCLI:
    def __init__(self, db_file="attendance.db"):
        self.db = AttendanceDB(db_file)

    def print_menu(self):
        print("\n" + "=" * 50)
        print("     ACADEMIC ATTENDANCE & BUNK PLANNER CLI")
        print("=" * 50)
        print("  1. Add a New Course")
        print("  2. Mark Attendance (Present / Absent)")
        print("  3. Check Bunk & Recovery Allowance")
        print("  4. View All Courses Table")
        print("  5. View Course History")
        print("  6. Load Sample College Demo Data")
        print("  7. Delete a Course")
        print("  8. Exit")
        print("-" * 50)

    def run(self):
        while True:
            self.print_menu()
            choice = input("Enter choice (1-8): ").strip()

            if choice == "1":
                self.add_course()
            elif choice == "2":
                self.mark_attendance()
            elif choice == "3":
                self.check_bunks()
            elif choice == "4":
                self.view_table()
            elif choice == "5":
                self.view_history()
            elif choice == "6":
                self.db.seed_demo_data()
                print("\n[+] Demo data loaded! Choose option 4 to see courses.")
            elif choice == "7":
                self.delete_course()
            elif choice == "8":
                print("\nGoodbye! Keep your attendance above 75%! 👋\n")
                break
            else:
                print("\n[!] Invalid option, please enter a number from 1 to 8.")

            input("\nPress Enter to return to menu...")

    def add_course(self):
        print("\n--- Add New Course ---")
        code = input("Enter course code (e.g. CSE1021): ").strip().upper()
        if not code:
            print("[!] Course code cannot be empty.")
            return

        name = input("Enter course name (e.g. Python Programming): ").strip()
        if not name:
            print("[!] Course name cannot be empty.")
            return

        target_input = input("Enter required attendance % [default: 75]: ").strip()
        target = float(target_input) if target_input else 75.0

        total_input = input("Enter total planned classes [default: 45]: ").strip()
        total_classes = int(total_input) if total_input else 45

        course_id = self.db.add_course(code, name, target, total_classes)
        if course_id:
            print(f"\n[✓] Course '{code} - {name}' added successfully!")
        else:
            print(f"\n[!] Course with code '{code}' already exists!")

    def select_course(self):
        courses = self.db.get_all_courses()
        if not courses:
            print("\n[!] No courses found! Please add a course first.")
            return None

        print("\nAvailable Courses:")
        for idx, c in enumerate(courses, 1):
            print(f"  {idx}. {c['code']} - {c['name']}")

        try:
            choice = int(input(f"Select course (1-{len(courses)}): ").strip())
            if 1 <= choice <= len(courses):
                return courses[choice - 1]
            print("[!] Selection out of range.")
            return None
        except ValueError:
            print("[!] Please enter a valid number.")
            return None

    def mark_attendance(self):
        print("\n--- Mark Attendance ---")
        course = self.select_course()
        if not course:
            return

        print(f"\nSelected: {course['code']} - {course['name']}")
        print("Options: [P] Present  [A] Absent  [M] Medical  [C] Cancelled")
        status_input = input("Enter status (P/A/M/C) [default: P]: ").strip().upper()
        if not status_input:
            status_input = "P"

        status_map = {"P": "PRESENT", "A": "ABSENT", "M": "MEDICAL", "C": "CANCELLED"}
        if status_input not in status_map:
            print("[!] Invalid status choice.")
            return

        status = status_map[status_input]
        today = date.today().isoformat()
        date_str = input(f"Enter date (YYYY-MM-DD) [default: {today}]: ").strip()
        if not date_str:
            date_str = today

        note = input("Enter optional note: ").strip()

        self.db.mark_attendance(course["id"], status, date_str, note)
        print(f"\n[✓] Logged '{status}' for {course['code']} on {date_str}!")

    def check_bunks(self):
        print("\n--- Check Bunk & Recovery Status ---")
        course = self.select_course()
        if not course:
            return

        attended, conducted = self.db.get_attendance_count(course["id"])
        target = course["target"]
        pct = calculate_percentage(attended, conducted)
        bunks = calculate_bunks(attended, conducted, target)
        recovery = calculate_recovery(attended, conducted, target)
        status = get_status(pct, target)

        print("\n" + "-" * 50)
        print(f"Course: {course['code']} - {course['name']}")
        print(f"Attended: {attended} / {conducted} held")
        print(f"Current Percentage : {pct}% (Target: {target}%)")
        print(f"Status Category    : [{status}]")

        if bunks > 0:
            print(f"\n[✓] YOU CAN BUNK: You can miss {bunks} more class(es) safely!")
        elif recovery > 0:
            print(f"\n[!] WARNING: Must attend {recovery} consecutive class(es) to recover!")
        else:
            print(f"\n[!] BORDERLINE: Exactly on track. Do not miss any upcoming class!")
        print("-" * 50)

    def view_table(self):
        courses = self.db.get_all_courses()
        if not courses:
            print("\n[!] No courses found! Please add a course first.")
            return

        print("\n" + "=" * 70)
        print(f"{'Code':<10} | {'Course Name':<22} | {'Att/Cond':<10} | {'Current %':<10} | {'Status':<10}")
        print("-" * 70)

        for c in courses:
            att, cond = self.db.get_attendance_count(c["id"])
            pct = calculate_percentage(att, cond)
            status = get_status(pct, c["target"])
            bunks = calculate_bunks(att, cond, c["target"])
            rec = calculate_recovery(att, cond, c["target"])

            if bunks > 0:
                status_display = f"SAFE (+{bunks})"
            elif rec > 0:
                status_display = f"WARN (-{rec})"
            else:
                status_display = "EXACT (0)"

            name = c["name"] if len(c["name"]) <= 22 else c["name"][:19] + "..."
            ratio = f"{att}/{cond}"
            print(f"{c['code']:<10} | {name:<22} | {ratio:<10} | {pct:<9}% | {status_display:<10}")

        print("=" * 70)

    def view_history(self):
        print("\n--- View Course History ---")
        course = self.select_course()
        if not course:
            return

        history = self.db.get_course_history(course["id"])
        if not history:
            print(f"\n[!] No attendance records logged yet for {course['code']}.")
            return

        print(f"\nRecent Attendance for {course['code']}:")
        print(f"{'Date':<12} | {'Status':<10} | {'Note'}")
        print("-" * 45)
        for h in history:
            print(f"{h['date']:<12} | {h['status']:<10} | {h['note']}")
        print("-" * 45)

    def delete_course(self):
        print("\n--- Delete Course ---")
        course = self.select_course()
        if not course:
            return

        confirm = input(f"Are you sure you want to delete {course['code']}? (y/n): ").strip().lower()
        if confirm == "y":
            self.db.delete_course(course["id"])
            print(f"[✓] Deleted {course['code']} successfully.")
        else:
            print("Cancelled.")
