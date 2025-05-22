global_function = int(input("Enter a number"))

def print_variable():
  if(global_function>10):
    print(f'Local function: {global_function}')
  else:
    print("This is an error")


print_variable()
print(f'Global function: {global_function}')