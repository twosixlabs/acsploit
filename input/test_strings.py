from strings import StringGenerator


def test_constructor():
    sg = StringGenerator()
    assert sg.get_min_value() <= sg.get_max_value()


def test_get_random():
    sg = StringGenerator()
    assert sg.is_valid(sg.get_random())  # generate a random character and see if it is valid


def test_get_list_of_values():
    sg = StringGenerator()
    for string in sg.get_list_of_values(10):  # if we change the defaults, we may want to test more than 10
        assert sg.is_valid(string)


def test_get_greater_than():  # under the assumption that min and max are different, should we change this?
    sg = StringGenerator()
    assert sg.get_greater_than(sg.get_min_value()) > sg.get_min_value()


def test_get_less_than():  # under the assumption that min and max are different, should we change this?
    sg = StringGenerator()
    assert sg.get_less_than(sg.get_max_value()) < sg.get_max_value()


def test_default_min_value():
    sg = StringGenerator()
    assert sg.get_min_value() == chr(int(0x61))


def test_default_max_value():
    sg = StringGenerator()
    assert sg.get_max_value() == "zzzzzzzzzz"


