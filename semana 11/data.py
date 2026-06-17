from actions import Student, Grades
import csv

class CSVManage:
    def export_csv(self, file_name, students):
        headers = [
            "Name", "Classroom", "Spanish grade", "English grade",
            "History grade", "Science grade", "Total Average"
        ]
        try:
            with open(file_name, "w", encoding="utf-8", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()
                for student in students:
                    g = student.grades
                    writer.writerow({
                        "Name": student.full_name,
                        "Classroom": student.classroom,
                        "Spanish grade": g.spanish,
                        "English grade": g.english,
                        "History grade": g.history,
                        "Science grade": g.science,
                        "Total Average": g.get_average()
                    })
            print("Data exported successfully.")
        except Exception as e:
            print(f"Error exporting data: {e}")

    def import_csv(self, file_name):
        students = []
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    grades = Grades(
                        float(row["Spanish grade"]),
                        float(row["English grade"]),
                        float(row["History grade"]),
                        float(row["Science grade"])
                    )
                    student = Student(row["Name"], row["Classroom"], grades)
                    students.append(student)
            print("Data imported successfully.")
        except FileNotFoundError:
            print(f"File '{file_name}' not found.")
        except Exception as e:
            print(f"Error importing data: {e}")
        return students
