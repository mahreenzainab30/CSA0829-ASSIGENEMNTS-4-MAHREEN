
def read_attendance(filename):
    records = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) == 3 and parts[2] in ("P", "A"):
                records.append((parts[0], parts[1], parts[2]))
    return records
