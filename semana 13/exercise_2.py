def check_numbers(func):
    def wrapper(*args,**kwargs):
        valid_numbers= (int,float)
        for i, n in enumerate(args):
            if not isinstance(n,valid_numbers):
                raise ValueError(f"Invalid value {i+1}: '{n}' is not a number")
            
        for key, value in kwargs.items():
            if not isinstance(value,valid_numbers):
                raise ValueError(f"Invalid Value for {key}: '{value}' is not a number")
            
        return func(*args,**kwargs)
    return wrapper

@check_numbers
def sum_numbers(*args,**kwargs):
    return sum(*args) + sum(kwargs.value())

print(sum_numbers(a=2, b="dos", c=5))


