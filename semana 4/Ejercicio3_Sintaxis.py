import random
secret_number=random.randint(1, 10)

while True:
    random_number=int(input("Entry your number"))
    if (random_number==secret_number):
        print("Congratulations! You have guessed the secret number")
    else:
        print("Good luck next time, try again")


