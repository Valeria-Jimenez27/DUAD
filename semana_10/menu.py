from actions import (
    add_student,
    show_students,
    show_top_3,
    get_general_average
)
from data import export_csv, import_csv

def show_menu_and_execute(student_list):
    print("Main Menu:")
    print("1. Add a new student")
    print("2. Show all students")
    print("3. Show top 3 averages")
    print("4. Show class average")
    print("5. Export data to CSV")
    print("6. Import data from CSV")
    print("7. Exit")

    option = input("Choose an option (1-7): ")

    if option == "1":
        add_student(student_list)
    elif option == "2":
        show_students(student_list)
    elif option == "3":
        show_top_3(student_list)
    elif option == "4":
        get_general_average(student_list)
    elif option == "5":
        export_csv("students.csv", student_list)
    elif option == "6":
        import_csv("students.csv", student_list)
    elif option == "7":
        print("Exit")
        return False
    else:
        print("Invalid option. Please choose a number between 1 and 7.")
    return True
