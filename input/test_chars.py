import pytest
from chars import CharGenerator

def test_constructor():
    characterGen=CharGenerator()
    assert characterGen.get_min_value() in characterGen.characters # check if minimum and maximum characters are in
    assert characterGen.get_max_value() in characterGen.characters # the character set

def test_get_random():
    characterGen=CharGenerator()
    assert characterGen.is_valid(characterGen.get_random()) # generate a random character and see if it is valid
    assert characterGen.get_random() in characterGen.characters # generate a random character and test if in char set

def test_get_list_of_values():
    characterGen=CharGenerator()
    for char in characterGen.get_list_of_values(10): # if we change the defaults, we may want to test more than 10
        assert char in characterGen.characters
        assert characterGen.is_valid(char)

def test_get_greater_than(): # under the assumption that min and max are different, should we change this?
    characterGen=CharGenerator()
    assert characterGen.get_greater_than(characterGen.get_min_value()) > characterGen.get_min_value()

def test_get_less_than():   # under the assumption that min and max are different, should we change this?
    characterGen=CharGenerator()
    assert characterGen.get_less_than(characterGen.get_max_value()) < characterGen.get_max_value()

def test_default_min_value():
    characterGen=CharGenerator()
    assert characterGen.get_min_value()==chr(int(0x61))

def test_default_max_value():
    characterGen=CharGenerator()
    assert characterGen.get_max_value()==chr(int(0x7A))


