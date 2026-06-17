def bubble_sort(list_of_sort):
    n= len(list_of_sort)
    for outer_index in range (0, n - 1):
        print(f"Swapping: {outer_index +1}")
        changes_made=False
        
        for index in range(n - 1, outer_index, -1):
            current_number = list_of_sort[index - 1]
            next_number = list_of_sort[index]
            if next_number > current_number:
                print(f"Swapping numbers")
                list_of_sort[index - 1], list_of_sort[index] = next_number, current_number
                changes_made = True
            else:
                print("No exchange of numbers")

        print(f"Iteration {outer_index + 1}: {list_of_sort}")

        if not changes_made:
            break

testing_list=[1,2,3,4]
bubble_sort(testing_list)


print(f"Sorted in descending order: {testing_list}")