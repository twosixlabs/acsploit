from input import CharGenerator
import pytest


def get_generator(min_value, max_value, restrictions):
    cg = CharGenerator()
    cg.set_option('min_value', min_value)
    cg.set_option('max_value', max_value)
    cg.set_option('restrictions', restrictions)
    return cg


def test_options():
    cg = get_generator('a', 'c', 'b')
    options = cg.get_options()
    assert options['min_value'] == 'a'
    assert options['max_value'] == 'c'
    assert options['restrictions'] == 'b'
    cg.set_option('max_value', 'd')
    assert options['max_value'] == 'd'


@pytest.mark.parametrize("min_value, max_value, restrictions, expected", [
    ('a', 'c', 'b', 'a'),
    ('X', 'Z', '', 'X'),  # no restrictions
    ('w', 'w', '', 'w'),  # min == max
    ('l', 'z', 'l', 'm'),  # min restricted
    ('l', 'z', 'lmnop', 'q')  # min and successive values restricted
])
def test_get_min_value(min_value, max_value, restrictions, expected):
    cg = get_generator(min_value, max_value, restrictions)
    assert cg.get_min_value() == expected


@pytest.mark.parametrize("min_value, max_value, restrictions, expected", [
    ('a', 'c', 'b', 'c'),
    ('X', 'Z', '', 'Z'),  # no restrictions
    ('w', 'w', '', 'w'),  # min == max
    ('b', 'n', 'n', 'm'),  # max restricted
    ('D', 'V', 'RSTUV', 'Q')  # max and preceding values restricted
])
def test_get_max_value(min_value, max_value, restrictions, expected):
    cg = get_generator(min_value, max_value, restrictions)
    assert cg.get_max_value() == expected


@pytest.mark.parametrize("min_value, max_value, restrictions, num, expected", [
    ('a', 'z', '', 5, 'abcde'),  # no restrictions
    ('a', 'z', 'qrstu', 5, 'abcde'),  # restrictions not affecting result
    ('p', 'z', 'q', 5, 'prstu'),  # one restriction
    ('p', 'z', 'qrstu', 3, 'pvw'),  # multiple restrictions
    ('p', 'z', 'qru', 4, 'pstv'),  # multiple restrictions, non contiguous
    ('A', 'D', 'A', 3, 'BCD')  # excluding min_value, including max_value
])
def test_get_list_of_values(min_value, max_value, restrictions, num, expected):
    cg = get_generator(min_value, max_value, restrictions)
    assert cg.get_list_of_values(num) == list(expected)


def test_get_list_of_too_many_values():
    cg = get_generator('a', 'z', '')
    with pytest.raises(ValueError):
        cg.get_list_of_values(27)


@pytest.mark.parametrize("restrictions, value, expected", [
    ('', 'b', 'c'),  # no restrictions
    ('', 'a', 'b'),  # no restrictions, min_value
    ('x', 'w', 'y'),  # skip restricted char
    ('qrstu', 'p', 'v'),  # multiple restrictions
    ('p', 'p', 'q'),  # input value restricted
    ('', 'y', 'z'),  # expected response equal to max_value
    ('', '0', 'a')  # expect min_value if initial input is below min_value ('0' < 'a')
])
def test_get_greater_than(restrictions, value, expected):
    cg = get_generator('a', 'z', restrictions)
    assert cg.get_greater_than(value) == expected


@pytest.mark.parametrize("max_value, restrictions, too_large", [
    ('z', '', '~'),
    ('x', '', 'y'),
    ('z', '', 'z'),
    ('z', 'wxyz', 'w')
])
def test_get_greater_than_max(max_value, restrictions, too_large):
    cg = get_generator('a', max_value, restrictions)
    with pytest.raises(ValueError):
        cg.get_greater_than(too_large)


@pytest.mark.parametrize("restrictions, value, expected", [
    ('', 'c', 'b'),  # no restrictions
    ('', 'z', 'y'),  # no restrictions, max_value
    ('x', 'y', 'w'),  # skip restricted char
    ('qrstu', 'v', 'p'),  # multiple restrictions
    ('p', 'p', 'o'),  # input value restricted
    ('', 'b', 'a'),  # expected response equal to min_value
    ('', '~', 'z')  # expect max_value if initial input is above max_value ('~' > 'z')
])
def test_get_less_than(restrictions, value, expected):
    cg = get_generator('a', 'z', restrictions)
    assert cg.get_less_than(value) == expected


@pytest.mark.parametrize("min_value, restrictions, too_small", [
    ('a', '', 0),
    ('c', '', 'a'),
    ('a', '', 'a'),
    ('a', 'abcd', 'd')
])
def test_get_less_than_min(min_value, restrictions, too_small):
    cg = get_generator(min_value, 'z', restrictions)
    with pytest.raises(ValueError):
        cg.get_less_than(too_small)

@pytest.mark.parametrize("min_value, max_value, restrictions, valid", [
    ('a', 'j', '', 'abcdefghij'),
    ('D', 'K', 'KFI', 'DEGHJ'),
    (' ', '0', '#$%"', " !&'()*+,-./0"),
    ('9', 'B', '9:=K\x00B', ";<>?@A")
])
def test_is_valid(min_value, max_value, restrictions, valid):
    cg = get_generator(min_value, max_value, restrictions)
    invalid = [chr(i) for i in range(256) if chr(i) not in valid]
    for c in valid:
        assert cg.is_valid(c)
    for c in invalid:
        assert not cg.is_valid(c)
