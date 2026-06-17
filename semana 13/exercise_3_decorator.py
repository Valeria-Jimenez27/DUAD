from datetime import date

class User:
    def __init__(self, birthdate):
        self.birthdate = birthdate

    @property
    def age(self):
        today = date.today()
        return date.today().year - self.birthdate.year


def adult(func):
    def wrapper(user):
        if user.age < 18:
            raise PermissionError(f"{user.age}: Access denied, is not an adult")
        return func(user)
    return wrapper

@adult
def enter_a_bar(user):
    return f"{user.age}: You are allowed to enter"


try:
    print(enter_a_bar(User(date(1998, 1, 27))))
    print(enter_a_bar(User(date(2008, 10, 7))))
except PermissionError:
    print("Access denied")

