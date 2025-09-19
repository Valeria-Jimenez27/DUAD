from pytest_exercise4_from_week6 import my_string
def test_my_tring():
    #arrange
    expected_result="I focus on what really matters"
    #act
    result=my_string()
    #assert
    assert result== expected_result[::-1]   