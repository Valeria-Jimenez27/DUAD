def bubble_sort(list_of_sort): # O(n)
    for outer_index in range(0,len(list_of_sort)-1): # O(n)
        changes_made=False # O(1)
        for index in range(0, len(list_of_sort) - 1 -outer_index): # O(n)
            current_number=list_of_sort[index] # O(n)
            next_number=list_of_sort[index+1] # O(n)
            print(f"Iteration {outer_index},current number {current_number}, next number {next_number}") # O(1)
            
            if current_number > next_number: # O(n)
                print("Swapping numbers")# O(1)
                list_of_sort[index]=next_number # O(n)
                list_of_sort[index+1]=current_number # O(n)
                changes_made=True # O(1)
            
            
        if not changes_made:# O(1)
            return # O(1)

testing_list=[23,97,2,80,10,73.2,-100] # O(1)
bubble_sort(testing_list) # O(1)


print(f"Sorted in ascending order: {testing_list}") # O(1)