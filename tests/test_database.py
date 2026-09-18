"""
test_database.py - Simple unit tests for database saving and loading.
"""

import os
import unittest
from attendance_tracker.database import AttendanceDB


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db_file = "test_attendance.db"
        self.db = AttendanceDB(self.db_file)

    def tearDown(self):
        if os.path.exists(self.db_file):
            os.remove(self.db_file)

    def test_add_and_get_course(self):
        course_id = self.db.add_course("CSE1021", "Python Essentials", 75.0, 45)
        self.assertIsNotNone(course_id)

        course = self.db.get_course_by_code("CSE1021")
        self.assertEqual(course["code"], "CSE1021")
        self.assertEqual(course["name"], "Python Essentials")

    def test_duplicate_course_rejected(self):
        self.db.add_course("CSE1021", "Python 1")
        duplicate = self.db.add_course("CSE1021", "Python 2")
        self.assertIsNone(duplicate)

    def test_mark_attendance_and_count(self):
        c_id = self.db.add_course("MAT1011", "Calculus", 75.0, 45)
        self.db.mark_attendance(c_id, "PRESENT", "2026-09-01")
        self.db.mark_attendance(c_id, "PRESENT", "2026-09-02")
        self.db.mark_attendance(c_id, "ABSENT", "2026-09-03")

        attended, conducted = self.db.get_attendance_count(c_id)
        self.assertEqual(attended, 2)
        self.assertEqual(conducted, 3)

    def test_delete_course(self):
        c_id = self.db.add_course("PHY1001", "Physics")
        self.db.delete_course(c_id)
        self.assertIsNone(self.db.get_course_by_code("PHY1001"))


if __name__ == "__main__":
    unittest.main()
