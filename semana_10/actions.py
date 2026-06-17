def request_grade(subject):
    while True:
        try:
            grade = float(input(f"Enter grade for {subject}: "))
            if 0 <= grade <= 100:
                return grade
            else:
                print("Grade must be between 0 and 100.")
        except ValueError:
            print("Please enter a valid number.")

def collect_student_data():
    print("Enter student information:")
    full_name = input("Full name: ")
    classroom = input("Classroom: ")
    spanish = request_grade("Spanish")
    english = request_grade("English")
    history = request_grade("History")
    science = request_grade("Science")
    avg = (spanish + english + history + science) / 4

    return {
        "Name": full_name,
        "Classroom": classroom,
        "Spanish grade": spanish,
        "English grade": english,
        "History grade": history,
        "Science grade": science,
        "Total Average": avg
    }

def add_student(student_list):
    student = collect_student_data()
    student_list.append(student)
    print(f"Student '{student['Name']}' added successfully.")

def show_students(student_list):
    if not student_list:
        print("No students to display.")
        return

    for index, s in enumerate(student_list, 1):
        print(f"\nStudent {index}:")
        print(f"Name: {s['Name']}")
        print(f"Classroom: {s['Classroom']}")
        print(f"Spanish: {s['Spanish grade']}")
        print(f"English: {s['English grade']}")
        print(f"History: {s['History grade']}")
        print(f"Science: {s['Science grade']}")
        print(f"Total Average: {s['Total Average']:.2f}")

def show_top_3(student_list):
    if len(student_list) < 3:
        print("Fewer than 3 students registered.")
        return

    top = sorted(student_list, key=lambda s: s["Total Average"], reverse=True)[:3]
    print("Top 3 Students by Average:")
    for i, s in enumerate(top, 1):
        print(f"{i}. {s['Name']} - {s['Total Average']:.2f}")

def get_general_average(student_list):
    if not student_list:
        print("No students registered.")
        return

    avg = sum(s['Total Average'] for s in student_list) / len(student_list)
    print(f"Class Average: {avg:.2f}")
