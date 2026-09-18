#!/usr/bin/env python3
"""
main.py - Entry point for the Attendance & Bunk Planner project.
Run with:
    python3 main.py
"""

import sys
from attendance_tracker.cli import SimpleCLI
from attendance_tracker.database import AttendanceDB


def main():
    # If run with --demo flag, load sample data and show table directly
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        db = AttendanceDB()
        db.seed_demo_data()
        cli = SimpleCLI()
        print("\n[+] Demo data loaded successfully!\n")
        cli.view_table()
        return

    # If run with --dashboard flag, show courses table
    if len(sys.argv) > 1 and sys.argv[1] == "--dashboard":
        cli = SimpleCLI()
        cli.view_table()
        return

    # Default: Start interactive step-by-step menu
    cli = SimpleCLI()
    cli.run()


if __name__ == "__main__":
    main()
