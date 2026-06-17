def bubble_sort_with_exeptions(list_of_sort):
    if not isinstance(list_of_sort, list):
        raise TypeError("The provided argument is not a list")
    
    if not list_of_sort:
        return list_of_sort

    for outer_index in range(0,len(list_of_sort)-1):
        changes_made=False
        for index in range(0, len(list_of_sort) - 1 -outer_index):
            current_number=list_of_sort[index]
            next_number=list_of_sort[index+1]
            print(f"Iteration {outer_index},current number {current_number}, next number {next_number}")
            
            if current_number > next_number:
                print("Swapping numbers")
                list_of_sort[index]=next_number
                list_of_sort[index+1]=current_number
                changes_made=True
            
            
        if not changes_made:
            return

testing_list=[1,5,10,2,13,22]
bubble_sort_with_exeptions(testing_list)


print(f"Result: {testing_list}")