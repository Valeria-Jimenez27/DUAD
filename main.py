from menu import show_menu_and_execute

def main():
    student_list = []

    while True:
        if not show_menu_and_execute(student_list):
            break

if __name__ == "__main__":
    main()
