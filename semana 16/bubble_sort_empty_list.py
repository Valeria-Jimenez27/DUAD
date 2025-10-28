def bubble_sort_without_numbers(list_of_sort):
    if not list_of_sort:
        return
    
    for outer_index in range(0,len(list_of_sort)-1):
        changes_made=False
        for index in range(0, len(list_of_sort) - 1 -outer_index):
            current_number=list_of_sort[index]
            next_number=list_of_sort[index+1]
            
            if current_number > next_number:
                list_of_sort[index]=next_number
                list_of_sort[index+1]=current_number
                changes_made=True
            
            
        if not changes_made:
            return

testing_list=[]
bubble_sort_without_numbers(testing_list)


print(f"Sorted in ascending order: {testing_list}")