my_list= [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
index= 0
while (index<len(my_list)):
    if my_list[index] %2:
        del my_list[index]
    else:
        index +=1
print(my_list)