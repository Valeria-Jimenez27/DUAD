class Grades:
    def __init__(self, spanish, english, history, science):
        self.spanish = spanish
        self.english = english
        self.history = history
        self.science = science

    def get_average(self):
        return (self.spanish+self.english+self.history+self.science) / 4

class Student:
    def __init__(self, full_name, classroom, grades):
        self.full_name = full_name
        self.classroom = classroom
        self.grades = grades

class Calculator:
    def __init__(self):
        self.students = []

    def request_grade(self, subject):
        while True:
            try:
                grade = float(input(f"Enter grade for {subject}: "))
                if 0 <= grade <= 100:
                    return grade
                else:
                    print("Grade must be between 0 and 100.")
            except ValueError:
                print("Please enter a valid number.")

    def collect_student_data(self):
        print("Enter student information:")
        full_name = input("Full name: ")
        classroom = input("Classroom: ")
        spanish = self.request_grade("Spanish")
        english = self.request_grade("English")
        history = self.request_grade("History")
        science = self.request_grade("Science")
        grades = Grades(spanish, english, history, science)
        return Student(full_name, classroom, grades)

    def add_student(self):
        student = self.collect_student_data()
        self.students.append(student)
        print(f"Student '{student.full_name}' added successfully.")

    def show_students(self):
        if not self.students:
            print("No students to display.")
            return
        for index, student in enumerate(self.students, 1):
            g = student.grades
            print(f"Student {index}:")
            print(f"Name: {student.full_name}")
            print(f"Classroom: {student.classroom}")
            print(f"Spanish: {g.spanish}")
            print(f"English: {g.english}")
            print(f"History: {g.history}")
            print(f"Science: {g.science}")
            print(f"Total Average: {g.get_average()}")

    def show_top_3(self):
        if len(self.students) < 3:
            print("There are fewer than 3 students registered.")
            return
        top = sorted(self.students, key=lambda s: s.grades.get_average(), reverse=True)[:3]
        print("Top 3 Students by Average:")
        for i, student in enumerate(top, 1):
            print(f"{i}. {student.full_name} - {student.grades.get_average()}")

    def get_general_average(self):
        if not self.students:
            print("No students registered.")
            return
        total = sum(s.grades.get_average() for s in self.students)
        avg = total / len(self.students)
        print(f"Class Average: {avg}")

