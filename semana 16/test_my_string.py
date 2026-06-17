from pytest_exercise4_from_week6 import my_string
def test_my_string():
    #arrange
    expected_result="I focus on what really matters"
    #act
    result=my_string()
    #assert
    assert result== expected_result[::-1]   


def test_my_string_empty_info():
    #arrange
    expected_result=""
    #act        
    result=my_string("")
    #assert     
    assert result== expected_result


def test_my_srting_with_numbers():
    #arrange
    expected_result= "12345"
    #act        
    result= my_string("54321")
    #assert 
    assert result== expected_result 
