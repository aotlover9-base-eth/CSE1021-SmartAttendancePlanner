"""
calculator.py - Super simple math functions for attendance and bunks.
No complicated logic, just simple formulas every college student uses.
"""

import math


def calculate_percentage(attended, conducted):
    """Calculates attendance percentage (attended / conducted * 100)."""
    if conducted == 0:
        return 100.0  # Semester just started
    if attended < 0 or conducted < 0:
        raise ValueError("Attendance cannot be negative numbers!")
    if attended > conducted:
        raise ValueError("Attended cannot be more than total classes conducted!")
    
    return round((attended / conducted) * 100, 2)


def calculate_bunks(attended, conducted, target=75.0):
    """
    Calculates how many future classes you can safely miss (bunk)
    while keeping your attendance at or above target percentage.
    """
    if conducted == 0:
        return 0
    
    current_pct = (attended / conducted) * 100
    if current_pct < target:
        return 0  # Already below target, cannot bunk!

    # Math: attended / (conducted + bunks) >= target / 100
    # bunks <= (attended * 100 / target) - conducted
    max_bunks = int((attended * 100 / target) - conducted)
    return max(0, max_bunks)


def calculate_recovery(attended, conducted, target=75.0):
    """
    Calculates how many classes in a row you MUST attend
    to get back up to the target percentage if you are below it.
    """
    if conducted == 0:
        return 0
    
    current_pct = (attended / conducted) * 100
    if current_pct >= target:
        return 0  # Already safe!

    # Math: (attended + x) / (conducted + x) >= target / 100
    target_ratio = target / 100.0
    needed = math.ceil(((target_ratio * conducted) - attended) / (1.0 - target_ratio))
    return max(0, needed)


def get_status(current_pct, target=75.0):
    """Returns a simple status string."""
    if current_pct >= target:
        return "SAFE"
    elif current_pct >= (target - 5.0):
        return "WARNING"
    else:
        return "CRITICAL"
