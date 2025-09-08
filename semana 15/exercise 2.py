def bubble_sort(list_of_sort):
    for outer_index in range(0,len(list_of_sort) - 1):
        changes_made=False
        for index in range(0, len(list_of_sort)- 1 -outer_index):
            current_number=list_of_sort[index]
            next_number=list_of_sort[index+1]
            print(f"Iteration {outer_index},current number {current_number}, next number {next_number}")
            
            if current_number < next_number:
                print("Swapping numbers")
                list_of_sort[index]=next_number
                list_of_sort[index+1]=current_number
                changes_made=True
            
            
        if not changes_made:
            return

testing_list=[23,97,2,80,10,73.2,-100]
bubble_sort(testing_list)


print(f"Sorted in descending order: {testing_list}")