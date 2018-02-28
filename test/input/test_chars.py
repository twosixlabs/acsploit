from input import CharGenerator


def test_constructor():
    cg = CharGenerator()
    assert cg.get_min_value() in cg.char_set  # check if minimum and maximum characters are in
    assert cg.get_max_value() in cg.char_set # the character set


def test_get_random():
    cg = CharGenerator()
    assert cg.is_valid(cg.get_random())  # generate a random character and see if it is valid
    assert cg.get_random() in cg.char_set  # generate a random character and test if in char set


def test_get_list_of_values():
    cg = CharGenerator()
    for char in cg.get_list_of_values(10):  # if we change the defaults, we may want to test more than 10
        assert char in cg.char_set
        assert cg.is_valid(char)


def test_get_greater_than():  # under the assumption that min and max are different, should we change this?
    cg = CharGenerator()
    assert cg.get_greater_than(cg.get_min_value()) > cg.get_min_value()


def test_get_less_than():  # under the assumption that min and max are different, should we change this?
    cg = CharGenerator()
    assert cg.get_less_than(cg.get_max_value()) < cg.get_max_value()


def test_default_min_value():
    cg = CharGenerator()
    assert cg.get_min_value() == chr(int(0x61))


def test_default_max_value():
    cg = CharGenerator()
    assert cg.get_max_value() == chr(int(0x7A))


