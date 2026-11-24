
from pathlib import Path

# All files are stored in the Task04 folder
BASE_FOLDER = Path(__file__).parent

# Original defective function
def save_returns_old(books):
    log = open(BASE_FOLDER / "old_returns.log", "w")

    for book in books:
        log.write(book)

    log.close()


def process_old(day_file):
    try:
        with open(day_file, "r", encoding="utf-8") as file:
            books = file.read().split("\n")

        save_returns_old(books)

    except FileNotFoundError:
        print("missing")


# Demonstrate the original problem
print("ORIGINAL PROGRAM TEST")

for day in ["day1.txt", "day2.txt", "day3.txt"]:
    process_old(BASE_FOLDER / day)

with open(BASE_FOLDER / "old_returns.log", "r", encoding="utf-8") as file:
    print("\nOriginal log:")
    print(repr(file.read()))


# Repaired program
def save_returns(books):
    with open(
        BASE_FOLDER / "returns.log",
        "a",
        encoding="utf-8"
    ) as log:

        for book in books:
            if book.strip():
                log.write(book.strip() + "\n")


def process(day_file):
    try:
        with open(day_file, "r", encoding="utf-8") as file:
            books = file.readlines()

        save_returns(books)
        print(f"Processed: {Path(day_file).name}")

    except FileNotFoundError as error:
        with open(
            BASE_FOLDER / "error.log",
            "a",
            encoding="utf-8"
        ) as error_file:
            error_file.write(
                f"Missing file: {day_file} | {error}\n"
            )

        print(f"Missing file: {Path(day_file).name}")

    except PermissionError as error:
        with open(
            BASE_FOLDER / "error.log",
            "a",
            encoding="utf-8"
        ) as error_file:
            error_file.write(f"Permission error: {error}\n")

        print("Permission denied.")


# Clear old demonstration logs before running
for filename in ["returns.log", "error.log", "old_returns.log"]:
    path = BASE_FOLDER / filename
    if path.exists():
        path.unlink()


print("\nREPAIRED PROGRAM TEST")

# Process three daily files
for day in ["day1.txt", "day2.txt", "day3.txt"]:
    process(BASE_FOLDER / day)

# Demonstrate missing-file error handling
process(BASE_FOLDER / "missing_day.txt")


# Display the repaired log
print("\nREPAIRED BOOK RETURN LOG")

with open(BASE_FOLDER / "returns.log", "r", encoding="utf-8") as file:
    print(file.read())

print("ERROR LOG")

with open(BASE_FOLDER / "error.log", "r", encoding="utf-8") as file:
    print(file.read())
