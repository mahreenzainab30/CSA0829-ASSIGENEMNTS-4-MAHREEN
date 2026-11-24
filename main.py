
from pathlib import Path
from reader import read_attendance
from report import write_reports

BASE = Path(__file__).resolve().parent.parent
INPUT = BASE / "attendance.csv"

if __name__ == "__main__":
    records = read_attendance(INPUT)
    write_reports(records)
