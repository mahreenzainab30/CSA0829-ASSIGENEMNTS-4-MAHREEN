
from datetime import datetime, timedelta

def read_attendance(filename):
    records = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) == 3 and parts[2] in ("P", "A"):
                records.append((parts[0], parts[1], parts[2]))
    return records

def calculate_percentage(records):
    totals = {}
    for reg, date, status in records:
        totals.setdefault(reg, [0, 0])
        totals[reg][1] += 1
        if status == "P":
            totals[reg][0] += 1
    return {
        reg: round(present / total * 100, 2)
        for reg, (present, total) in totals.items()
    }

def absent_three_days(records):
    dates = {}
    for reg, date, status in records:
        dates.setdefault(reg, {})[date] = status

    result = []
    for reg, attendance in dates.items():
        absent_dates = sorted(
            date for date, status in attendance.items()
            if status == "A"
        )
        for i in range(len(absent_dates) - 2):
            d1 = datetime.strptime(absent_dates[i], "%Y-%m-%d").date()
            d2 = datetime.strptime(absent_dates[i + 1], "%Y-%m-%d").date()
            d3 = datetime.strptime(absent_dates[i + 2], "%Y-%m-%d").date()
            if d2 - d1 == timedelta(days=1) and d3 - d2 == timedelta(days=1):
                result.append(reg)
                break
    return result

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
