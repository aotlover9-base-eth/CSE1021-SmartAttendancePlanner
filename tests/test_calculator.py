"""
test_calculator.py - Simple unit tests for math formulas.
"""

import unittest
from attendance_tracker.calculator import (
    calculate_percentage,
    calculate_bunks,
    calculate_recovery,
    get_status
)


class TestCalculator(unittest.TestCase):

    def test_percentage_normal(self):
        # 15 out of 20 = 75%
        self.assertEqual(calculate_percentage(15, 20), 75.0)
        # 20 out of 25 = 80%
        self.assertEqual(calculate_percentage(20, 25), 80.0)

    def test_percentage_zero_classes(self):
        # At start of semester, 0 classes conducted = 100%
        self.assertEqual(calculate_percentage(0, 0), 100.0)

    def test_bunk_allowance(self):
        # If attended 24 out of 30, target 75%:
        # 24 / 32 = 75%, so can miss 2 classes
        bunks = calculate_bunks(24, 30, target=75.0)
        self.assertEqual(bunks, 2)

    def test_bunk_allowance_when_low(self):
        # If attendance is already 70% < 75%, bunks should be 0
        bunks = calculate_bunks(14, 20, target=75.0)
        self.assertEqual(bunks, 0)

    def test_recovery_needed(self):
        # 14 attended out of 20 (70%). Target 75%.
        # Needs 4 classes in a row (18/24 = 75%)
        needed = calculate_recovery(14, 20, target=75.0)
        self.assertEqual(needed, 4)

    def test_status_categories(self):
        self.assertEqual(get_status(85.0, 75.0), "SAFE")
        self.assertEqual(get_status(72.0, 75.0), "WARNING")
        self.assertEqual(get_status(60.0, 75.0), "CRITICAL")


if __name__ == "__main__":
    unittest.main()
