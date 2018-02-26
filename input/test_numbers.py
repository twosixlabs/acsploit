import pytest
from numbers import IntGenerator

def test_constructor():
    intGen=IntGenerator()
    assert intGen.get_min_value()<= intGen.get_max_value()

def test_get_random():
    intGen=IntGenerator()
    assert intGen.is_valid(intGen.get_random()) # generate a random integer and see if it is valid

def test_get_list_of_values():
    intGen=IntGenerator()
    for int in intGen.get_list_of_values(10): # if we change the defaults, we may want to test more than 10
        assert intGen.is_valid(int)

def test_get_greater_than(): # under the assumption that min and max are different, should we change this?
    intGen=IntGenerator()
    assert intGen.get_greater_than(intGen.get_min_value()) > intGen.get_min_value()

def test_get_less_than():   # under the assumption that min and max are different, should we change this?
    intGen=IntGenerator()
    assert intGen.get_less_than(intGen.get_max_value()) < intGen.get_max_value()

def test_default_min_value():
    intGen=IntGenerator()
    assert intGen.get_min_value()==0

def test_default_max_value():
    intGen=IntGenerator()
    assert intGen.get_max_value()==255
