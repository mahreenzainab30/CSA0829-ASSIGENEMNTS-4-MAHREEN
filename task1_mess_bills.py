
from decimal import Decimal, InvalidOperation
from pathlib import Path


def process_mess_bills(filename):
    total = Decimal("0.00")
    report = []
    rejected_lines = []

    try:
        # Open and read the file one line at a time
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):

                # Ignore empty lines
                if not line.strip():
                    continue

                try:
                    parts = line.strip().split(",")

                    # Check whether exactly 3 fields are present
                    if len(parts) != 3:
                        raise ValueError("Expected 3 fields")

                    register_number = parts[0].strip()
                    name = parts[1].strip()
                    amount_text = parts[2].strip()

                    if not register_number or not name:
                        raise ValueError("Register number or name is missing")

                    # Decimal correctly handles amounts with paise
                    amount = Decimal(amount_text)

                    report.append(f"{name} - Rs. {amount:.2f}")
                    total += amount

                except (ValueError, InvalidOperation) as error:
                    rejected_lines.append(
                        (line_number, line.strip(), str(error))
                    )

        print("MESS BILL REPORT")
        print("----------------")
        for item in report:
            print(item)

        print("----------------")
        print("Total Mess Bill: Rs.", f"{total:.2f}")

        print("\nREJECTED LINES")
        print("--------------")
        if rejected_lines:
            for item in rejected_lines:
                print(
                    f"Line {item[0]}: {item[1]} | Reason: {item[2]}"
                )
        else:
            print("No rejected lines.")

    except FileNotFoundError:
        print("Error: The input file was not found.")

    except PermissionError:
        print("Error: Permission denied while opening the file.")

    except OSError as error:
        print("File processing error:", error)


# Main program
if __name__ == "__main__":
    file_path = Path(__file__).parent / "mess_oct.txt"
    process_mess_bills(file_path)
