my_list=['1','3','5','7','9',]
if len(my_list) > 1:
        my_list[0], my_list[-1] = my_list[-1], my_list[0]
for index in range(len(my_list)):
    print(my_list[index])

