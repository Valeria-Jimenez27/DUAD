from bubble_sort_empty_list import bubble_sort_without_numbers
def test_bubble_sort_empty_list():
    #arrange
    empty_list=[]
    #act    
    bubble_sort_without_numbers(empty_list)
    #assert     
    assert empty_list==[]
    