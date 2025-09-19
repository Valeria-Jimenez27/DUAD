import random
def bubble_sort_random_numbers(list_of_sort):
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

testing_list=[random.randint(1,200) for _ in range(150)]
bubble_sort_random_numbers(testing_list)


print(f"Sorted in ascending order: {testing_list}")
