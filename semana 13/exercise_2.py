def check_numbers(func):
    def wrapper(*args):
        valid_numbers= (int,float)
        for i, n in enumerate(args):
            if not isinstance(n,valid_numbers):
                raise ValueError(f"Invalid value {i+1}: '{n}' is not a number")

        return func(*args)
    return wrapper

@check_numbers
def sum_numbers(*args):
    return sum(args)

print(sum_numbers(100, "dos", 85))


