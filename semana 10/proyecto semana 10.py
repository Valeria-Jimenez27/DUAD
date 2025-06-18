import csv

students = []

def show_menu():
    print("1. Entry a new student")
    print("2. Display the full list of students")
    print("3. See top 3 averages")
    print("4. See total averages")
    print("5. Export data to CSV")
    print("6. Import data from CSV")
    print("7. Exit menu")


def request_grade(subject):
    while True:
        try:
            grade = float(input(f"Enter the grade for {subject}: "))
            if 0 <= grade <= 100:
                return grade
            else:
                print("The grade must be between 0 and 100.")
        except ValueError:
            print("Please, enter a valid number.")


def collect_student_data():
    print("Enter the info of the student:")
    full_name = input("Name ")
    classroom = input("Classroom")
    spanish_grade = request_grade("Spanish")
    english_grade = request_grade("English")
    history_grade = request_grade("History")
    science_grade = request_grade("Science")

    total_average = (spanish_grade + english_grade + history_grade + science_grade)/4

    student = {
        "Name": full_name,
        "Classroom": classroom,
        "Spanish grade": spanish_grade,
        "English grade": english_grade,
        "History grade": history_grade,
        "Science grade": science_grade,
        "Total Average": total_average
    }
    return student


def add_student():
    student = collect_student_data()
    students.append(student)
    print(f"Student '{student['Name']}' added successfully.")


def show_students():
    for index, s in enumerate(students, 1):
        print(f"Student {index}:")
        print(f"Name: {s['Name']}")
        print(f"Classroom: {s['Classroom']}")
        print(f"Spanish: {s['Spanish grade']}")
        print(f"English: {s['English grade']}")
        print(f"History: {s['History grade']}")
        print(f"Science: {s['Science grade']}")
        print(f"Total Average: {s['Total Average']:.2f}")


def show_top_3():
    if len(students) < 3:
        print("Less than 3 students registered")
        return
    top_3 = sorted(students, key=lambda s: s["Total Average"], reverse=True)[:3]
    print("Top 3 students by average:")
    for index, s in enumerate(top_3, 1):
        print(f"{index}. {s['Name']}, Total Average: {s['Total Average']:.2f}")


def get_general_average():
    general_average = sum(s['Total Average'] for s in students)/len(students)
    print(f"Overall average for all students {general_average:.2f}")


def export_csv(file_name, data, headers):
    with open(file_name, "w", encoding="utf-8") as file:
        writer = csv.DictWriter(file, headers)
        writer.writeheader()
        writer.writerows(data)
    print("Data successfully exported to CSV.")


def importar_csv(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["Spanish grade"] = float(row["Spanish grade"])
                row["English grade"] = float(row["English grade"])
                row["History grade"] = float(row["History grade"])
                row["Science grade"] = float(row["Science grade"])
                row["Total Average"] = float(row["Total Average"])
                students.append(row)
        print("Data successfully imported from CSV.")
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")


def main():
    while True:
        try:
            show_menu()
            option = input("Select an option (1-7): ")
            if option == "1":
                add_student()
            elif option == "2":
                show_students()
            elif option == "3":
                show_top_3()
            elif option == "4":
                get_general_average()
            elif option == "5":
                export_csv("students.csv", students, ["Name", "Classroom", "Spanish grade", "English grade", "History grade", "Science grade", "Total Average"])
            elif option == "6":
                importar_csv("students.csv")
            elif option == "7":
                print("Exit")
                break
            else:
                print("Invalid option, please select a number between 1 and 7.")
        except ValueError:
            print("Please, enter a valid number.")


main()
