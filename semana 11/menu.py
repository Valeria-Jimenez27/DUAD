from actions import Calculator
from data import CSVManage

class Menu:
    def __init__(self):
        self.calculate = Calculator()
        self.csv = CSVManage()

    def show_menu(self):
        while True:
            print("1. Add student")
            print("2. Show students")
            print("3. Top 3 by average")
            print("4. Class average")
            print("5. Export CSV")
            print("6. Import CSV")
            print("0. Exit")

            choice = input("Select an option: ").strip()
            if choice == "0":
                print("Exit")
                break
            self.execute(choice)

    def execute(self, choice):
        if choice == "1":
            self.calculate.add_student()
        elif choice == "2":
            self.calculate.show_students()
        elif choice == "3":
            self.calculate.show_top_3()
        elif choice == "4":
            self.calculate.get_general_average()
        elif choice == "5":
            self.csv.export_csv("students.csv", self.calculate.students)
        elif choice == "6":
            self.calculate.students = self.csv.import_csv("students.csv")
        else:
            print("Invalid option.")
