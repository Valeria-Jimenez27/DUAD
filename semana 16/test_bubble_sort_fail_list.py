import pytest
from bubble_sort_fail_list import bubble_sort_with_exeptions

def test_bubble_sort_fail_list():
    #arrange
    fail_list=[33,22,44,11,-1]
    #act
    bubble_sort_with_exeptions(fail_list)
    #assert     
    assert fail_list==[-1,11,22,33,44]

def test_bubble_sort_fail_list2():
    #arrange
    not_a_list="This is not a list"
    #act / assert
    with pytest.raises(TypeError):
        bubble_sort_with_exeptions(not_a_list)

def test_bubble_sort_fail_list3():
    #arrange
    empty_list=[]
    #act
    bubble_sort_with_exeptions(empty_list)          
    #assert     
    assert empty_list==[]