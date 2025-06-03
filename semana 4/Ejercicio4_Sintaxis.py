number1=int(input("Entry the first number"))
number2=int(input("Entry the second number"))
number3=int(input("Entry the third number"))

if (number1>=number2 and number1>=number3):
    highest_number=number1
elif(number2>=number1 and number2>=number3):
    highest_number=number2
elif(number3>=number1 and number3>=number2):
    highest_number=number3
print(f"Your highest number is:{highest_number}")
