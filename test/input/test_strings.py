from input import StringGenerator
import pytest


def get_generator(min_length, max_length, min_value, max_value, restrictions):
    sg = StringGenerator()
    sg.set_option('min_length', min_length)
    sg.set_option('max_length', max_length)
    sg.set_option('min_value', min_value)
    sg.set_option('max_value', max_value)
    sg.set_option('restrictions', restrictions)
    return sg


def test_options():
    sg = get_generator(1, 5, 'a', 'c', 'b')
    options = sg.get_options()
    assert options['min_length'] == 1
    assert options['max_length'] == 5
    assert options['min_value'] == 'a'
    assert options['max_value'] == 'c'
    assert options['restrictions'] == 'b'
    sg.set_option('max_length', 10)
    assert options['max_length'] == 10


@pytest.mark.parametrize("min_length, min_value, restrictions, expected", [
    (1, 'a', '', 'a'),
    (2, '#', '', '##'),
    (3, 'W', '', 'WWW'),
    (2, 'a', 'a', 'bb'),  # min_value restricted
    (4, 'f', 'fghi', 'jjjj')  # min_value and successive chars restricted
])
def test_get_min_value(min_length, min_value, restrictions, expected):
    sg = get_generator(min_length, 10, min_value, 'z', restrictions)
    assert sg.get_min_value() == expected


@pytest.mark.parametrize("max_length, max_value, restrictions, expected", [
    (1, 'z', '', 'z'),
    (2, '#', '', '##'),
    (3, 'W', '', 'WWW'),
    (2, 'b', 'b', 'aa'),  # max_value restricted
    (4, 'F', 'CDEF', 'BBBB')  # max_value and preceding chars restricted
])
def test_get_max_value(max_length, max_value, restrictions, expected):
    sg = get_generator(1, max_length, '!', max_value, restrictions)
    assert sg.get_max_value() == expected


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


@pytest.mark.parametrize("value, expected", [
    ('a', 'aa'),  # append min_char if not at max_length
    ('cc', 'cca'),  # append min_char if not at max_length
    ('aaaax', 'aaaay'),  # increment last char if at max_length
    ('aaaac', 'aaaae'),  # increment last char if at max_length, skip restricted chars
    ('cxzzz', 'cy'),  # increment first non max_value char
    ('b', 'c'),  # jump to non-restricted value
    ('aadsf', 'aae'),  # jump to non-restricted value
    ('ZZZ', 'a'),  # jump to min_value if value < min
])
def test_get_greater_than(value, expected):
    sg = get_generator(1, 5, 'a', 'z', 'bd')
    assert sg.get_greater_than(value) == expected

@pytest.mark.parametrize("value, expected", [
    ('x', 'xaa'),  # append min_chars until at min_length
    ('cxzzz', 'cya'),  # increment first non max_value char, pad to min_length
    ('b', 'caa'),  # jump to non-restricted value
    ('adsf', 'aea'),  # jump to non-restricted value with min_length
    ('ZZZ', 'aaa'),  # jump to min_value if value < min
    ('aaaaxf', 'aaaay')  # reduce length if input is beyond max_length
])
def test_min_max_length_get_greater_than(value, expected):
    sg = get_generator(3, 5, 'a', 'z', 'bd')
    assert sg.get_greater_than(value) == expected


@pytest.mark.parametrize("max_value, restrictions, too_large", [
    ('z', '', 'zzzzz'),  # equal to max_value * max_length
    ('f', '', 'g'),  # greater than max_value
    ('z', '', 'zzzzza'),  # greater than max_value
    ('z', 'wxyz', 'vvvvv'),  # nothing greater than value with restrictions
])
def test_get_greater_than_max(max_value, restrictions, too_large):
    cg = get_generator(1, 5, 'a', max_value, restrictions)
    with pytest.raises(ValueError):
        cg.get_greater_than(too_large)


@pytest.mark.parametrize("value, expected", [
    ('aazzz', 'aazzy'),  # decrement last_char if at max_length
    ('xxxaa', 'xxxa'),  # remove last char if equal to min_value
    ('qf', 'qezzz'),  # decrement last char and pad to max_length if not at max_length
    ('xxe', 'xxczz'),  # decrement last char and pad to max_length if not at max_length, skip restricted chars
    ('bbc', 'azzzz'),  # jump to non-restricted value
    ('aadsf', 'aaczz'),  # jump to non-restricted value
    ('~', 'zzzzz'),  # jump to max_value if value > max
])
def test_get_less_than(value, expected):
    sg = get_generator(1, 5, 'a', 'z', 'bd')
    assert sg.get_less_than(value) == expected


@pytest.mark.parametrize("value, expected", [
    ('xxxayyy', 'xxxay'),  # reduce length if input is beyond max_length
    ('cxa', 'cwzzz'),  # do not remove chars to drop below min_length
])
def test_min_max_length_get_less_than(value, expected):
    sg = get_generator(3, 5, 'a', 'z', 'bd')
    assert sg.get_less_than(value) == expected


@pytest.mark.parametrize("min_value, restrictions, too_small", [
    ('a', '', 'aaa'),  # equal to min_value * max_length
    ('b', '', 'a'),  # less than min_value
    ('a', '', 'aa'),  # less than min_value
    ('b', 'bcd', 'e'),  # nothing less than value with restrictions
])
def test_get_less_than_min(min_value, restrictions, too_small):
    cg = get_generator(3, 5, min_value, 'z', restrictions)
    with pytest.raises(ValueError):
        cg.get_less_than(too_small)


def test_get_list_of_values():
    sg = get_generator(2, 4, 'a', 'e', 'bcd')
    values = ['aa', 'aaa', 'aaaa', 'aaae', 'aae', 'aaea', 'aaee', 'ae', 'aea', 'aeaa', 'aeae', 'aee', 'aeea', 'aeee',
              'ea', 'eaa', 'eaaa', 'eaae', 'eae', 'eaea', 'eaee', 'ee', 'eea', 'eeaa', 'eeae', 'eee', 'eeea', 'eeee']

    for i in range(1, 28):
        assert sg.get_list_of_values(i) == values[:i]


# Same options as test_get_list_of_values, which has 28 possible values
def test_get_list_of_too_many_values():
    sg = get_generator(2, 4, 'a', 'e', 'bcd')
    with pytest.raises(ValueError):
        sg.get_list_of_values(29)
