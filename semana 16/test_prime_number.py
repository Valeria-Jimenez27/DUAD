import pytest
from pytest_exercise7_week6 import prime_number

def test_prime_number_True():
    #arrange
    number=13
    expected_result=True
    #act
    result=prime_number(number)
    #assert
    assert result==expected_result

def test_prime_number_False():
    #arrange
    number=10
    expected_result=False
    #act
    result=prime_number(number)
    #assert
    assert result==expected_result