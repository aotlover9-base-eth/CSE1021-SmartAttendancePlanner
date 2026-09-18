# Student Attendance & Bunk Planner CLI

A simple and easy Python terminal tool to keep track of college attendance and know exactly how many classes you can bunk or need to attend to stay above 75%.

---

## What Does This Project Do?
In college, we need 75% attendance to write exams. This program runs in the terminal and helps you:
1. Add your subjects (like `CSE1021`, `MAT1011`).
2. Mark if you were Present or Absent in class.
3. Calculate if you can safely bunk the next class.
4. Calculate how many classes you must attend if you are below 75%.
5. Save all your attendance records in a simple local database.

---

## How to Setup and Run

### Step 1: Requirements
You only need Python 3 installed on your computer. You don't need to install any external libraries!

Check your Python version:
```bash
python3 --version
```

### Step 2: Clone the Repository
```bash
git clone https://github.com/aotlover9-base-eth/CSE1021-SmartAttendancePlanner.git
cd CSE1021-SmartAttendancePlanner
```

### Step 3: Run the Program
Run this command in your terminal:
```bash
python3 main.py
```

---

## How It Works (Step-by-Step)
When you run `python3 main.py`, an easy menu appears:

```text
==================================================
     ACADEMIC ATTENDANCE & BUNK PLANNER CLI
==================================================
  1. Add a New Course
  2. Mark Attendance (Present / Absent)
  3. Check Bunk & Recovery Allowance
  4. View All Courses Table
  5. View Course History
  6. Load Sample College Demo Data
  7. Delete a Course
  8. Exit
--------------------------------------------------
Enter choice (1-8):
```

You just type a number and press **Enter**. The program asks for details one by one!

### Quick Demo Mode:
If you want to test the program quickly with pre-loaded college subjects:
```bash
python3 main.py --demo
```

---

## Screenshots
Output screenshots are provided in the `screenshots/` folder.

---

## How to Run Tests
We wrote 10 simple unit tests to verify the math calculations and database saving.

To run all tests:
```bash
python3 -m unittest discover tests -v
```

---

## Project Structure
```text
CSE1021-SmartAttendancePlanner/
├── attendance_tracker/
│   ├── calculator.py       # Simple formulas for percentage and bunks
│   ├── database.py         # SQLite database to save data
│   └── cli.py              # Interactive menu logic
├── tests/
│   ├── test_calculator.py  # Tests for math calculations
│   └── test_database.py    # Tests for database functions
├── docs/
│   └── PROJECT_REPORT.md   # Course submission report
├── screenshots/            # Output screenshots
├── Statement.md            # Simple problem statement
├── README.md               # How to run instructions
└── main.py                 # Main file to run
```

---

## License
MIT License - Free to use for college projects.
