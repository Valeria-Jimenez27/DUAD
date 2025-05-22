def show_menu():
    print("Which operation do you want to perform?")
    print("1. Sum")
    print("2. Rest")
    print("3. Multiplication")
    print("4. Division")
    print("5. Delete result")
    print("0. Exit")


def enter_number():
    try:
        return int(input("Enter a number: "))
    except ValueError:
        print("Error, be sure to enter a valid number.")


def calculator():
    current_number = 0
    print(f"Calculator started. Current number: {current_number}")
    while True:
        show_menu()
        option = input("Enter a number from 0-5: ")
        if option == "0":
            print("Exiting calculator.")
            break
        if option not in ["1", "2", "3", "4", "5"]:
            print("Invalid option. Please choose between 1 to 5")
            continue
        if option == "5":
            current_number = 0
            print(f"Result deleted. Current number:",{current_number})
            continue
        
        new_number = enter_number()
        
        if option == "1":
            current_number += new_number
        elif option == "2":
            current_number -= new_number
        elif option == "3":
            current_number *= new_number
        elif option == "4":
            if new_number == 0:
                print("Error: Cannot divide by zero")
                continue
            current_number /= new_number
        print("Result:",current_number)


def main():
    show_menu()
    enter_number()
    calculator()


main()
