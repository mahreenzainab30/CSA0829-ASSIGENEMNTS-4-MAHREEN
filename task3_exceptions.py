
import os
import tempfile


class InvalidRecord(Exception):
    """Raised when an attendance record is invalid."""


def parse_line(line):
    """Convert one attendance line into a tuple."""

    parts = line.strip().split(",")

    try:
        if len(parts) != 3:
            raise ValueError(
                f"expected 3 fields, found {len(parts)}"
            )

        register_number = parts[0].strip()
        date = parts[1].strip()
        status = parts[2].strip().upper()

        if not register_number or not date:
            raise ValueError("register number or date is missing")

        if status not in ("P", "A"):
            raise ValueError(f"invalid status '{status}'")

        return register_number, date, status

    except ValueError as error:
        raise InvalidRecord(str(error)) from error


def summarise(path):
    present = 0
    absent = 0
    errors = []

    try:
        with open(path, "r", encoding="utf-8") as file:

            for line_number, line in enumerate(file, start=1):

                if not line.strip():
                    continue

                try:
                    register_number, date, status = parse_line(line)

                except InvalidRecord as error:
                    errors.append((line_number, str(error)))

                else:
                    if status == "P":
                        present += 1
                    elif status == "A":
                        absent += 1

    except FileNotFoundError:
        errors.append((0, f"file not found: {path}"))

    except PermissionError:
        errors.append((0, f"permission denied: {path}"))

    except UnicodeDecodeError:
        errors.append((0, f"wrong file encoding: {path}"))

    else:
        print("File processing completed.")

    finally:
        print("Processing attempt finished.")

    return present, absent, errors


# Sample attendance data provided in the assignment
data = (
    "192311001,2026-10-08,P\n"
    "192311002,2026-10-08,A\n"
    "192311003,2026-10-08\n"
    "192311004,2026-10-08,L\n"
)

# Create a temporary sample file
with tempfile.NamedTemporaryFile(
    "w",
    suffix=".csv",
    delete=False,
    encoding="utf-8"
) as tmp:
    tmp.write(data)
    temporary_filename = tmp.name

# Process the sample file
print("VALIDATION RESULT:")
print(summarise(temporary_filename))

# Test a file that does not exist
print("\nMISSING FILE TEST:")
print(summarise("missing_attendance.csv"))

# Delete temporary file after testing
os.remove(temporary_filename)
