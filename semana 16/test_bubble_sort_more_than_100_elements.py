from bubble_sort_more_than_100_elements import bubble_sort_random_numbers

def test_bubble_sort_more_than_100_elements():
    #arrange
    large_list=[i for i in range(150,0,-1)]
    #act
    bubble_sort_random_numbers(large_list)
    #assert     
    assert large_list==[i for i in range(1,151)]