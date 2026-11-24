
from stats import calculate_percentage, absent_three_days

def write_reports(records):
    percentages = calculate_percentage(records)
    absentees = absent_three_days(records)

    with open("attendance_summary.txt", "w", encoding="utf-8") as file:
        for reg, percentage in percentages.items():
            file.write(f"{reg}: {percentage}%\n")

    with open("three_day_absentees.txt", "w", encoding="utf-8") as file:
        for reg in absentees:
            file.write(reg + "\n")

    print("Attendance summary:", percentages)
    print("Absent for three consecutive days:", absentees)
