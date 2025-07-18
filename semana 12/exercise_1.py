class BankAccount:
    def __init__(self):
        self.balance = 0 


    def deposit_money(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited: ${amount}")
        else:
            print("Try again with another number")


    def withdraw_money(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew: ${amount}")
        else:
            print("Insufficient funds")


    def show_total_balance(self):
        print(f"Your current balance is ${self.balance}")

class SavingsAccount(BankAccount):
    def __init__(self,min_balance):
        super().__init__()
        self.min_balance=min_balance
    

    def withdraw_money(self, amount):
        if self.balance-amount >= self.min_balance:
            self.balance-= amount
            print(f"Withdrew: ${amount}")
        else:
            print(f"Inssuficient funds, the Minimum balance must be: ${self.min_balance}")


min_balance=int(input("Enter the minimum balance for your account:"))
savings=SavingsAccount(min_balance)

deposit=int(input("How much would you like to deposit?"))
savings.deposit_money(deposit)

withdraw=int(input("How much would you like to withdraw?"))
savings.withdraw_money(withdraw)

savings.show_total_balance()

