def my_first_decorator(func):
    def wrapper(*args):
        print("Hello Roberto")
        func(*args)
        print("This is my first decorator!")

    return wrapper

@my_first_decorator
def vale_decorator():
    print("I never get the idea of decorators in python, but now I am")	

vale_decorator()

