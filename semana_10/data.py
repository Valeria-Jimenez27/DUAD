import csv

def export_csv(file_name, student_list):
    headers = [
        "Name", "Classroom", "Spanish grade", "English grade",
        "History grade", "Science grade", "Total Average"
    ]
    try:
        with open(file_name, "w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(student_list)
        print("Data exported successfully.")
    except Exception as e:
        print(f"Error exporting data: {e}")

def import_csv(file_name, student_list):
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["Spanish grade"] = float(row["Spanish grade"])
                row["English grade"] = float(row["English grade"])
                row["History grade"] = float(row["History grade"])
                row["Science grade"] = float(row["Science grade"])
                row["Total Average"] = float(row["Total Average"])
                student_list.append(row)
        print("Data imported successfully.")
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
    except Exception as e:
        print(f"Error importing data: {e}")
