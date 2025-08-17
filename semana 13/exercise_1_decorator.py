def my_first_decorator(func):
    def wrapper(*args,**kwargs):
        print("Hello Roberto")
        print("positional parameters:",*args)
        print("keyword parameters:",**kwargs)
        
        result= func(*args,**kwargs)
        print("result of the function:",result)
        
        print("This is my first decorator!")
        return result
    return wrapper

@my_first_decorator
def vale_decorator():
    print("I had never understood the concept of decorators in Python, but now I do.")	

vale_decorator()