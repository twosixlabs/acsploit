import pytest
from strings import StringGenerator

def test_constructor():
    stringGen=StringGenerator()
    assert stringGen.get_min_value() <= stringGen.get_max_value()

def test_get_random():
    stringGen=StringGenerator()
    assert stringGen.is_valid(stringGen.get_random()) # generate a random character and see if it is valid

def test_get_list_of_values():
    stringGen=StringGenerator()
    for string in stringGen.get_list_of_values(10): # if we change the defaults, we may want to test more than 10
        assert stringGen.is_valid(string)

def test_get_greater_than(): # under the assumption that min and max are different, should we change this?
    stringGen=StringGenerator()
    assert stringGen.get_greater_than(stringGen.get_min_value()) > stringGen.get_min_value()

def test_get_less_than():   # under the assumption that min and max are different, should we change this?
    stringGen=StringGenerator()
    assert stringGen.get_less_than(stringGen.get_max_value()) < stringGen.get_max_value()

def test_default_min_value():
    stringGen=StringGenerator()
    assert stringGen.get_min_value()==chr(int(0x61))

def test_default_max_value():
    stringGen=StringGenerator()
    assert stringGen.get_max_value()=="zzzzzzzzzz"


