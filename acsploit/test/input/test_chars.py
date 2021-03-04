from input import CharGenerator
import pytest


def get_generator(min_value, max_value, restrictions):
    cg = CharGenerator()
    cg.options['min_value'] = min_value
    cg.options['max_value'] = max_value
    cg.options['restrictions'] = restrictions
    cg.prepare()
    return cg


def get_whitelist_generator(whitelist):
    cg = CharGenerator()
    cg.options['use_whitelist'] = True
    cg.options['whitelist'] = whitelist
    cg.prepare()
    return cg


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


def test_get_min_value_whitelist():
    cg = get_whitelist_generator('zxv!q~')
    assert cg.get_min_value() == '!'


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


def test_get_max_value_whitelist():
    cg = get_whitelist_generator('zxv!q~')
    assert cg.get_max_value() == '~'


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


def test_get_list_of_values_whitelist():
    cg = get_whitelist_generator('adhyto')
    assert cg.get_list_of_values(3) == ['a', 'd', 'h']


def test_get_list_of_too_many_values():
    cg = get_generator('a', 'z', '')
    with pytest.raises(ValueError):
        cg.get_list_of_values(27)


def test_get_list_of_too_many_values_whitelist():
    cg = get_whitelist_generator('adhyto')
    with pytest.raises(ValueError):
        cg.get_list_of_values(7)


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


def test_get_greater_than_whitelist():
    whitelist = 'abcdefg'
    cg = get_whitelist_generator(whitelist)
    for i, c in enumerate(whitelist[:-1]):
        assert cg.get_greater_than(c) == whitelist[i+1]


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


def test_get_greater_than_max_whitelist():
    cg = get_whitelist_generator('abdcefgh')
    with pytest.raises(ValueError):
        cg.get_greater_than('h')
    with pytest.raises(ValueError):
        cg.get_greater_than('z')


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


def test_get_less_than_whitelist():
    whitelist = 'abcdefg'
    cg = get_whitelist_generator(whitelist)
    for i, c in enumerate(whitelist[1:]):
        assert cg.get_less_than(c) == whitelist[i]


@pytest.mark.parametrize("min_value, restrictions, too_small", [
    ('a', '', chr(0)),
    ('c', '', 'a'),
    ('a', '', 'a'),
    ('a', 'abcd', 'd')
])
def test_get_less_than_min(min_value, restrictions, too_small):
    cg = get_generator(min_value, 'z', restrictions)
    with pytest.raises(ValueError):
        cg.get_less_than(too_small)


def test_get_less_than_min_whitelist():
    cg = get_whitelist_generator('abdcefgh')
    with pytest.raises(ValueError):
        cg.get_less_than('a')
    with pytest.raises(ValueError):
        cg.get_less_than('!')


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


@pytest.mark.parametrize("whitelist, valid", [
    ('aeiou', 'aeiou'),
    ('uioae', 'aeiou')
])
def test_is_valid_whitelist(whitelist, valid):
    cg = get_whitelist_generator(whitelist)
    invalid = [chr(i) for i in range(256) if chr(i) not in valid]
    for c in valid:
        assert cg.is_valid(c)
    for c in invalid:
        assert not cg.is_valid(c)
