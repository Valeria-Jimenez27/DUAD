def list_of_numbers():
    numbers =[]
    for index in range(5):
        number= int(input(f"Enter your number {index+1}:"))
        numbers.append(number)
    return numbers


def prime_number(n):
    if n<2:
        return False
    for index in range(2,int(n**0.5)+1):
        if n%index==0:
            return False
    return True


def main():
    numbers=list_of_numbers()
    print("The list of prime numbers is:")
    for number in numbers:
        if prime_number(number):
            print(number)


main()


