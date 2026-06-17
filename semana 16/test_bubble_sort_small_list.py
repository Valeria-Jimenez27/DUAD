from bubble_sort_small_list import bubble_sort

def test_bubble_sort_small_list():
    #arrange
    small_list=[5,3,1,4,2]
    #act
    bubble_sort(small_list)
    #assert
    assert small_list==[1,2,3,4,5]