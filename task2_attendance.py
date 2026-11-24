
from pathlib import Path

# Find the input and output folders
BASE_FOLDER = Path(__file__).parent
INPUT_FOLDER = BASE_FOLDER / "input"
OUTPUT_FOLDER = BASE_FOLDER / "output"

# Create output folder if it does not exist
OUTPUT_FOLDER.mkdir(exist_ok=True)

# Store attendance counts for every student
attendance = {}

# Store damaged records
damaged_lines = []

# Find all daily attendance files
daily_files = sorted(INPUT_FOLDER.glob("*.txt"))

# Process each daily file
for file_path in daily_files:

    with open(file_path, "r", encoding="utf-8") as file:

        for line_number, line in enumerate(file, start=1):

            if not line.strip():
                continue

            parts = line.strip().split(",")

            # Validate the record
            if len(parts) != 3:
                damaged_lines.append(
                    (file_path.name, line_number, line.strip())
                )
                continue

            register_number = parts[0].strip()
            date = parts[1].strip()
            status = parts[2].strip().upper()

            if not register_number or not date or status not in ("P", "A"):
                damaged_lines.append(
                    (file_path.name, line_number, line.strip())
                )
                continue

            # Create a record for a new student
            if register_number not in attendance:
                attendance[register_number] = {
                    "present": 0,
                    "absent": 0
                }

            # Update attendance count
            if status == "P":
                attendance[register_number]["present"] += 1
            else:
                attendance[register_number]["absent"] += 1


# Prepare the summary report
summary_path = OUTPUT_FOLDER / "attendance_summary.csv"
below_path = OUTPUT_FOLDER / "below_75_percent.csv"
error_path = OUTPUT_FOLDER / "damaged_lines.log"

with open(summary_path, "w", encoding="utf-8") as summary_file:
    summary_file.write(
        "Register Number,Present,Absent,Total,Percentage\n"
    )

    for register_number, counts in sorted(attendance.items()):

        present = counts["present"]
        absent = counts["absent"]
        total = present + absent

        percentage = (present / total) * 100 if total else 0

        summary_file.write(
            f"{register_number},{present},{absent},"
            f"{total},{percentage:.2f}\n"
        )


# Prepare the list of students below 75%
with open(below_path, "w", encoding="utf-8") as below_file:
    below_file.write("Register Number,Attendance Percentage\n")

    for register_number, counts in sorted(attendance.items()):

        total = counts["present"] + counts["absent"]

        percentage = (
            counts["present"] / total
        ) * 100 if total else 0

        if percentage < 75:
            below_file.write(
                f"{register_number},{percentage:.2f}\n"
            )


# Prepare the damaged-line log
with open(error_path, "w", encoding="utf-8") as error_file:

    for filename, line_number, content in damaged_lines:
        error_file.write(
            f"{filename}, Line {line_number}: {content}\n"
        )


# Display the result
print("MONTHLY ATTENDANCE PROCESSING COMPLETED")
print("---------------------------------------")

for register_number, counts in sorted(attendance.items()):

    total = counts["present"] + counts["absent"]
    percentage = counts["present"] / total * 100

    print(
        f"{register_number}: "
        f"{percentage:.2f}% attendance"
    )

print("\nStudents below 75%:")

for register_number, counts in sorted(attendance.items()):

    total = counts["present"] + counts["absent"]
    percentage = counts["present"] / total * 100

    if percentage < 75:
        print(f"{register_number}: {percentage:.2f}%")

print("\nDamaged records:", len(damaged_lines))
print("Reports saved in the output folder.")
