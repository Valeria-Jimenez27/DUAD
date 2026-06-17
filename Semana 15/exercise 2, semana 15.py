def bubble_sort(list_of_sort):
    n= len(list_of_sort)
    for outer in range (0, n - 1):
        changes_made=False
        for index in range(n - 1,outer, -1):
            if list_of_sort[index] < list_of_sort[index - 1]:
                list_of_sort[index], list_of_sort[index - 1] = list_of_sort[index - 1], list_of_sort[index]
                changes_made=True
                
            if not changes_made:
                return

testing_list=[1,2,3,4]
bubble_sort(testing_list)


print(f"Sorted in descending order: {testing_list}")