import pytest
from pytest_exercise5_from_week6 import counter

def test_empty_string():
    assert counter("") == (0, 0)

def test_all_uppercase():
    assert counter("ABCD") == (4, 0)

def test_all_lowercase():
    assert counter("abcd") == (0, 4)

    