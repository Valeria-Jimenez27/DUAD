def sum_list(list):
    sum = 0
    for number in list:
        sum += number
    return sum

list=[20,100,55,34,5]
result=sum_list(list)
print(f"The result of the sum is:{result}")