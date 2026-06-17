numbers =[]
for index in range(10):
    list_of_numbers= int(input(f"Entry your number {index+1}:"))
    numbers.append(list_of_numbers)

highest_number= max(numbers)
print(f"Your list of numbers is:{numbers}")
print(f"Your hightest number is:{highest_number}")
