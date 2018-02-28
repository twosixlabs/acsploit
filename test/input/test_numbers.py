from input import IntGenerator

def test_constructor():
    ig = IntGenerator()
    assert ig.get_min_value() <= ig.get_max_value()


def test_get_random():
    ig = IntGenerator()
    assert ig.is_valid(ig.get_random())  # generate a random integer and see if it is valid


def test_get_list_of_values():
    ig = IntGenerator()
    for value in ig.get_list_of_values(10):  # if we change the defaults, we may want to test more than 10
        assert ig.is_valid(value)


def test_get_greater_than():  # under the assumption that min and max are different, should we change this?
    ig = IntGenerator()
    assert ig.get_greater_than(ig.get_min_value()) > ig.get_min_value()


def test_get_less_than():  # under the assumption that min and max are different, should we change this?
    ig = IntGenerator()
    assert ig.get_less_than(ig.get_max_value()) < ig.get_max_value()


def test_default_min_value():
    ig = IntGenerator()
    assert ig.get_min_value() == 0


def test_default_max_value():
    ig = IntGenerator()
    assert ig.get_max_value() == 255
