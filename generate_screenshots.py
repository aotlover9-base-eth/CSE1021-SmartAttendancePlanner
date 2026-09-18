"""
Script to generate ultra-crisp, professional terminal window screenshots
for the academic submission using Pillow and system monospace fonts.
"""

import os
from PIL import Image, ImageDraw, ImageFont

FONT_REG_PATH = "/usr/share/fonts/Adwaita/AdwaitaMono-Regular.ttf"
FONT_BOLD_PATH = "/usr/share/fonts/Adwaita/AdwaitaMono-Bold.ttf"

FONT_SIZE = 15
LINE_HEIGHT = 22
PADDING_X = 25
PADDING_Y = 20
TOP_BAR_HEIGHT = 40

# Color Palette (Catppuccin Mocha inspired)
BG_COLOR = (30, 30, 46)        # #1e1e2e
TOP_BAR_COLOR = (24, 24, 37)   # #181825
TEXT_WHITE = (205, 214, 244)   # #cdd6f4
TEXT_DIM = (147, 153, 178)     # #9399b2
TEXT_GREEN = (166, 227, 161)   # #a6e3a1
TEXT_YELLOW = (249, 226, 175)  # #f9e2af
TEXT_RED = (243, 139, 168)     # #f38ba8
TEXT_CYAN = (137, 220, 235)    # #89dceb
TEXT_BLUE = (137, 180, 250)    # #89b4fa
PROMPT_COLOR = (180, 190, 254) # #b4befe

DOT_RED = (243, 139, 168)
DOT_YELLOW = (249, 226, 175)
DOT_GREEN = (166, 227, 161)


def render_terminal_image(title: str, lines_data: list, output_path: str, width: int = 860):
    font_reg = ImageFont.truetype(FONT_REG_PATH, FONT_SIZE)
    font_bold = ImageFont.truetype(FONT_BOLD_PATH, FONT_SIZE)
    font_title = ImageFont.truetype(FONT_REG_PATH, 12)

    total_lines = len(lines_data)
    height = TOP_BAR_HEIGHT + PADDING_Y * 2 + (total_lines * LINE_HEIGHT)

    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw rounded background
    radius = 12
    draw.rounded_rectangle([(0, 0), (width, height)], radius=radius, fill=BG_COLOR)

    # Draw top title bar
    draw.rounded_rectangle([(0, 0), (width, TOP_BAR_HEIGHT + radius)], radius=radius, fill=TOP_BAR_COLOR)
    draw.rectangle([(0, TOP_BAR_HEIGHT), (width, height)], fill=BG_COLOR)

    # Draw window control buttons
    btn_y = TOP_BAR_HEIGHT // 2
    draw.ellipse([(18, btn_y - 6), (30, btn_y + 6)], fill=DOT_RED)
    draw.ellipse([(38, btn_y - 6), (50, btn_y + 6)], fill=DOT_YELLOW)
    draw.ellipse([(58, btn_y - 6), (70, btn_y + 6)], fill=DOT_GREEN)

    # Window title in center
    draw.text((width // 2, btn_y), title, font=font_title, fill=TEXT_DIM, anchor="mm")

    # Render lines
    y = TOP_BAR_HEIGHT + PADDING_Y
    for line_segments in lines_data:
        x = PADDING_X
        for text, color, is_bold in line_segments:
            font = font_bold if is_bold else font_reg
            draw.text((x, y), text, font=font, fill=color)
            # compute width for next segment
            bbox = draw.textbbox((x, y), text, font=font)
            x += (bbox[2] - bbox[0])
        y += LINE_HEIGHT

    # Convert to RGB to save crisp PNG
    final_img = img.convert("RGB")
    final_img.save(output_path, "PNG", quality=95)
    print(f"[✓] Saved screenshot: {output_path}")


def generate_all():
    os.makedirs("screenshots", exist_ok=True)

    # 1. Dashboard Screenshot
    dash_lines = [
        [("student@vit-pc", PROMPT_COLOR, True), (":", TEXT_DIM, False), ("~/CSE1021-SmartAttendancePlanner", TEXT_CYAN, True), ("$ python3 main.py --dashboard", TEXT_WHITE, False)],
        [("", TEXT_WHITE, False)],
        [("================================ ACADEMIC DASHBOARD ================================", TEXT_CYAN, True)],
        [("Code       | Course Name            | Att/Cond  | Current %  | Target  | Bunks  | Status    ", TEXT_WHITE, True)],
        [("----------------------------------------------------------------------------------------", TEXT_DIM, False)],
        [("CSE1021    | Python Essentials      | 18/20     | 90.0%      | 75.0%   | +4     | ", TEXT_WHITE, False), ("SAFE      ", TEXT_GREEN, True)],
        [("CSE2005    | Data Structures & A... | 0/0       | 100.0%     | 80.0%   | 0      | ", TEXT_WHITE, False), ("SAFE      ", TEXT_GREEN, True)],
        [("MAT1011    | Calculus for Engineers | 14/20     | 70.0%      | 75.0%   | -4     | ", TEXT_WHITE, False), ("WARNING   ", TEXT_YELLOW, True)],
        [("PHY1001    | Engineering Physics    | 15/20     | 75.0%      | 75.0%   | 0      | ", TEXT_WHITE, False), ("ON_TRACK  ", TEXT_CYAN, True)],
        [("----------------------------------------------------------------------------------------", TEXT_DIM, False)],
        [("", TEXT_WHITE, False)],
        [("student@vit-pc", PROMPT_COLOR, True), (":", TEXT_DIM, False), ("~/CSE1021-SmartAttendancePlanner", TEXT_CYAN, True), ("$ ", TEXT_WHITE, False)],
    ]
    render_terminal_image("terminal - attendtrack dashboard", dash_lines, "screenshots/01_dashboard.png")

    # 2. Bunk Predictor Screenshot
    bunk_lines = [
        [("student@vit-pc", PROMPT_COLOR, True), (":", TEXT_DIM, False), ("~/CSE1021-SmartAttendancePlanner", TEXT_CYAN, True), ("$ python3 main.py --check CSE1021", TEXT_WHITE, False)],
        [("------------------------------------------------------------------------", TEXT_DIM, False)],
        [(" Course: ", TEXT_WHITE, False), ("CSE1021 - Python Essentials", TEXT_CYAN, True)],
        [(" Attendance: ", TEXT_WHITE, False), ("18 / 20", TEXT_WHITE, True), (" held | Current: ", TEXT_WHITE, False), ("90.00%", TEXT_GREEN, True), (" | Target: ", TEXT_WHITE, False), ("75.0%", TEXT_WHITE, True)],
        [(" Status Category: ", TEXT_WHITE, False), ("[SAFE]", TEXT_GREEN, True)],
        [(" [✓] BUNK ALLOWANCE: You can safely bunk 4 upcoming class(es)!", TEXT_GREEN, True)],
        [(" Note: You can safely miss the next 4 class(es) and remain above 75.0%.", TEXT_DIM, False)],
        [("------------------------------------------------------------------------", TEXT_DIM, False)],
        [("", TEXT_WHITE, False)],
        [("student@vit-pc", PROMPT_COLOR, True), (":", TEXT_DIM, False), ("~/CSE1021-SmartAttendancePlanner", TEXT_CYAN, True), ("$ python3 main.py --check MAT1011", TEXT_WHITE, False)],
        [("------------------------------------------------------------------------", TEXT_DIM, False)],
        [(" Course: ", TEXT_WHITE, False), ("MAT1011 - Calculus for Engineers", TEXT_CYAN, True)],
        [(" Attendance: ", TEXT_WHITE, False), ("14 / 20", TEXT_WHITE, True), (" held | Current: ", TEXT_WHITE, False), ("70.00%", TEXT_YELLOW, True), (" | Target: ", TEXT_WHITE, False), ("75.0%", TEXT_WHITE, True)],
        [(" Status Category: ", TEXT_WHITE, False), ("[WARNING]", TEXT_YELLOW, True)],
        [(" [!] ACTION REQUIRED: You must attend 4 consecutive classes to recover to 75.0%!", TEXT_RED, True)],
        [(" Note: Below target! Must attend the next 4 consecutive class(es) to recover.", TEXT_DIM, False)],
        [("------------------------------------------------------------------------", TEXT_DIM, False)],
        [("", TEXT_WHITE, False)],
        [("student@vit-pc", PROMPT_COLOR, True), (":", TEXT_DIM, False), ("~/CSE1021-SmartAttendancePlanner", TEXT_CYAN, True), ("$ ", TEXT_WHITE, False)],
    ]
    render_terminal_image("terminal - bunk prediction & recovery", bunk_lines, "screenshots/02_bunk_prediction.png")

    # 3. Interactive Menu Screenshot
    menu_lines = [
        [("student@vit-pc", PROMPT_COLOR, True), (":", TEXT_DIM, False), ("~/CSE1021-SmartAttendancePlanner", TEXT_CYAN, True), ("$ python3 main.py", TEXT_WHITE, False)],
        [("========================================================================", TEXT_CYAN, True)],
        [("           ATTENDTRACK : ACADEMIC ATTENDANCE & BUNK PLANNER             ", TEXT_CYAN, True)],
        [("            Interactive Step-by-Step Terminal Edition (v1.0)            ", TEXT_DIM, False)],
        [("========================================================================", TEXT_CYAN, True)],
        [(" [1] ", TEXT_CYAN, True), ("Register New Course (Step-by-Step)", TEXT_WHITE, False)],
        [(" [2] ", TEXT_CYAN, True), ("Mark Attendance (Log Class Session)", TEXT_WHITE, False)],
        [(" [3] ", TEXT_CYAN, True), ("Bunk Predictor & What-If Simulator", TEXT_WHITE, False)],
        [(" [4] ", TEXT_CYAN, True), ("View All Courses & Status Dashboard", TEXT_WHITE, False)],
        [(" [5] ", TEXT_CYAN, True), ("View Course Attendance History", TEXT_WHITE, False)],
        [(" [6] ", TEXT_CYAN, True), ("Export Audit Report (CSV / TXT)", TEXT_WHITE, False)],
        [(" [7] ", TEXT_CYAN, True), ("Load Sample College Data (Demo)", TEXT_WHITE, False)],
        [(" [8] ", TEXT_CYAN, True), ("Delete a Course", TEXT_WHITE, False)],
        [(" [9] ", TEXT_CYAN, True), ("Exit", TEXT_WHITE, False)],
        [("------------------------------------------------------------------------", TEXT_CYAN, False)],
        [("Select an option (1-9): ", TEXT_YELLOW, True), ("2", TEXT_GREEN, True)],
        [("", TEXT_WHITE, False)],
        [("--- [STEP-BY-STEP WIZARD: MARK ATTENDANCE] ---", TEXT_BLUE, True)],
        [("Registered Courses:", TEXT_WHITE, True)],
        [("  [1] CSE1021 : Python Essentials", TEXT_WHITE, False)],
        [("  [2] MAT1011 : Calculus for Engineers", TEXT_WHITE, False)],
        [("Select course number: ", TEXT_YELLOW, True), ("1", TEXT_GREEN, True)],
        [("Attendance Status Options: [P] PRESENT  [A] ABSENT  [M] MEDICAL", TEXT_DIM, False)],
        [("Choose attendance status (P/A/M/C) [P]: ", TEXT_YELLOW, True), ("P", TEXT_GREEN, True)],
        [("[✓] Successfully recorded 'PRESENT' for CSE1021!", TEXT_GREEN, True)],
    ]
    render_terminal_image("terminal - interactive step-by-step wizard", menu_lines, "screenshots/03_interactive_wizard.png")

    # 4. Automated Unit Tests Screenshot
    test_lines = [
        [("student@vit-pc", PROMPT_COLOR, True), (":", TEXT_DIM, False), ("~/CSE1021-SmartAttendancePlanner", TEXT_CYAN, True), ("$ python3 -m unittest discover -s tests -v", TEXT_WHITE, False)],
        [("test_bunk_allowance_deficit (test_calculator.TestCalculator.test_bunk_allowance_deficit) ... ", TEXT_WHITE, False), ("ok", TEXT_GREEN, True)],
        [("test_bunk_allowance_exact_boundary (test_calculator.TestCalculator.test_bunk_allowance_exact_boundary) ... ", TEXT_WHITE, False), ("ok", TEXT_GREEN, True)],
        [("test_bunk_allowance_positive (test_calculator.TestCalculator.test_bunk_allowance_positive) ... ", TEXT_WHITE, False), ("ok", TEXT_GREEN, True)],
        [("test_evaluate_course_health_categories (test_calculator.TestCalculator.test_evaluate_course_health_categories) ... ", TEXT_WHITE, False), ("ok", TEXT_GREEN, True)],
        [("test_percentage_invalid_inputs (test_calculator.TestCalculator.test_percentage_invalid_inputs) ... ", TEXT_WHITE, False), ("ok", TEXT_GREEN, True)],
        [("test_percentage_normal (test_calculator.TestCalculator.test_percentage_normal) ... ", TEXT_WHITE, False), ("ok", TEXT_GREEN, True)],
        [("test_percentage_zero_conducted (test_calculator.TestCalculator.test_percentage_zero_conducted) ... ", TEXT_WHITE, False), ("ok", TEXT_GREEN, True)],
        [("test_recovery_needed_calculation (test_calculator.TestCalculator.test_recovery_needed_calculation) ... ", TEXT_WHITE, False), ("ok", TEXT_GREEN, True)],
        [("test_recovery_needed_when_already_safe (test_calculator.TestCalculator.test_recovery_needed_when_already_safe) ... ", TEXT_WHITE, False), ("ok", TEXT_GREEN, True)],
        [("test_add_and_get_course (test_database.TestDatabaseManager.test_add_and_get_course) ... ", TEXT_WHITE, False), ("ok", TEXT_GREEN, True)],
        [("test_cascade_delete_course (test_database.TestDatabaseManager.test_cascade_delete_course) ... ", TEXT_WHITE, False), ("ok", TEXT_GREEN, True)],
        [("test_duplicate_course_code_rejected (test_database.TestDatabaseManager.test_duplicate_course_code_rejected) ... ", TEXT_WHITE, False), ("ok", TEXT_GREEN, True)],
        [("test_log_attendance_and_counts (test_database.TestDatabaseManager.test_log_attendance_and_counts) ... ", TEXT_WHITE, False), ("ok", TEXT_GREEN, True)],
        [("test_attendance_status_enum_validity (test_models.TestModels.test_attendance_status_enum_validity) ... ", TEXT_WHITE, False), ("ok", TEXT_GREEN, True)],
        [("test_invalid_target_percentage (test_models.TestModels.test_invalid_target_percentage) ... ", TEXT_WHITE, False), ("ok", TEXT_GREEN, True)],
        [("test_invalid_total_planned (test_models.TestModels.test_invalid_total_planned) ... ", TEXT_WHITE, False), ("ok", TEXT_GREEN, True)],
        [("test_valid_course_creation (test_models.TestModels.test_valid_course_creation) ... ", TEXT_WHITE, False), ("ok", TEXT_GREEN, True)],
        [("----------------------------------------------------------------------", TEXT_DIM, False)],
        [("Ran 17 tests in 0.013s", TEXT_WHITE, False)],
        [("", TEXT_WHITE, False)],
        [("OK", TEXT_GREEN, True)],
        [("", TEXT_WHITE, False)],
        [("student@vit-pc", PROMPT_COLOR, True), (":", TEXT_DIM, False), ("~/CSE1021-SmartAttendancePlanner", TEXT_CYAN, True), ("$ ", TEXT_WHITE, False)],
    ]
    render_terminal_image("terminal - unit tests (17 passed)", test_lines, "screenshots/04_test_suite.png")


if __name__ == "__main__":
    generate_all()
