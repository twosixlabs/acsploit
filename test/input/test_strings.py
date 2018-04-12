from input import StringGenerator
import pytest


def get_generator(min_length, max_length, min_value, max_value, restrictions):
    sg = StringGenerator()
    sg.options['min_length'] = min_length
    sg.options['max_length'] = max_length
    sg.options['min_value'] = min_value
    sg.options['max_value'] = max_value
    sg.options['restrictions'] = restrictions
    sg.prepare()
    return sg


def get_generator_whitelist(min_length, max_length, whitelist):
    sg = StringGenerator()
    sg.options['min_length'] = min_length
    sg.options['max_length'] = max_length
    sg.options['use_whitelist'] = True
    sg.options['whitelist'] = whitelist
    sg.prepare()
    return sg


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


@pytest.mark.parametrize("min_length, whitelist, expected", [
    (1, 'abcde', 'a'),
    (2, 'edcba', 'aa'),
    (4, 'uibkjky', 'bbbb')
])
def test_get_min_value_whitelist(min_length, whitelist, expected):
    sg = get_generator_whitelist(min_length, 10, whitelist)
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


@pytest.mark.parametrize("max_length, whitelist, expected", [
    (1, 'abcde', 'e'),
    (2, 'edcba', 'ee'),
    (4, 'uibkjky', 'yyyy')
])
def test_get_max_value_whitelist(max_length, whitelist, expected):
    sg = get_generator_whitelist(1, max_length, whitelist)
    assert sg.get_max_value() == expected


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
    ('a', 'aa'),
    ('c', 'ca'),
    ('aaaaa', 'aaaab'),
    ('ddfff', 'de'),
    ('ZZZ', 'a')
])
def test_get_greater_than_whitelist(value, expected):
    sg = get_generator_whitelist(1, 5, 'abcdef')
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


@pytest.mark.parametrize("value, expected", [
    ('d', 'daa'),
    ('ddfff', 'dea'),
    ('dddddf', 'dddde')
])
def test_min_max_length_get_greater_than(value, expected):
    sg = get_generator_whitelist(3, 5, 'abcdef')
    assert sg.get_greater_than(value) == expected


@pytest.mark.parametrize("max_value, restrictions, too_large", [
    ('z', '', 'zzzzz'),  # equal to max_value * max_length
    ('f', '', 'g'),  # greater than max_value
    ('z', '', 'zzzzza'),  # greater than max_value
    ('z', 'wxyz', 'vvvvv'),  # nothing greater than value with restrictions
])
def test_get_greater_than_max(max_value, restrictions, too_large):
    sg = get_generator(1, 5, 'a', max_value, restrictions)
    with pytest.raises(ValueError):
        sg.get_greater_than(too_large)


@pytest.mark.parametrize("too_large", [
    'ggggg',
    'h',
    'ggggga'
])
def test_get_greater_than_max_whitelist(too_large):
    sg = get_generator_whitelist(1, 5, 'abcdefg')
    with pytest.raises(ValueError):
        sg.get_greater_than(too_large)


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
    ('aabbb', 'aabba'),
    ('bbaaa', 'bbaa'),
    ('be', 'bdfff'),
    ('ddfff', 'ddffd'),
    ('~', 'fffff')
])
def test_get_less_than_whitelist(value, expected):
    sg = get_generator_whitelist(1, 5, 'abcdf')
    assert sg.get_less_than(value) == expected


@pytest.mark.parametrize("value, expected", [
    ('xxxayyy', 'xxxay'),  # reduce length if input is beyond max_length
    ('cxa', 'cwzzz'),  # do not remove chars to drop below min_length
])
def test_min_max_length_get_less_than(value, expected):
    sg = get_generator(3, 5, 'a', 'z', 'bd')
    assert sg.get_less_than(value) == expected


@pytest.mark.parametrize("value, expected", [
    ('dddafff', 'dddaf'),  # reduce length if input is beyond max_length
    ('cda', 'ccfff'),  # do not remove chars to drop below min_length
])
def test_min_max_length_get_less_than_whitelist(value, expected):
    sg = get_generator_whitelist(3, 5, 'abcdef')
    assert sg.get_less_than(value) == expected


@pytest.mark.parametrize("min_value, restrictions, too_small", [
    ('a', '', 'aaa'),  # equal to min_value * max_length
    ('b', '', 'a'),  # less than min_value
    ('a', '', 'aa'),  # less than min_value
    ('b', 'bcd', 'e'),  # nothing less than value with restrictions
])
def test_get_less_than_min(min_value, restrictions, too_small):
    sg = get_generator(3, 5, min_value, 'z', restrictions)
    with pytest.raises(ValueError):
        sg.get_less_than(too_small)


@pytest.mark.parametrize("too_small", [
    'aaa',
    '`',
    'aa'
])
def test_get_less_than_min_whitelist(too_small):
    sg = get_generator_whitelist(3, 5, 'abcdefg')
    with pytest.raises(ValueError):
        sg.get_less_than(too_small)


def test_get_list_of_values():
    sg = get_generator(2, 4, 'a', 'e', 'bcd')
    values = ['aa', 'aaa', 'aaaa', 'aaae', 'aae', 'aaea', 'aaee', 'ae', 'aea', 'aeaa', 'aeae', 'aee', 'aeea', 'aeee',
              'ea', 'eaa', 'eaaa', 'eaae', 'eae', 'eaea', 'eaee', 'ee', 'eea', 'eeaa', 'eeae', 'eee', 'eeea', 'eeee']

    for i in range(1, 28):
        assert sg.get_list_of_values(i) == values[:i]


def test_get_list_of_values_whitelist():
    sg = get_generator_whitelist(2, 4, 'ae')
    values = ['aa', 'aaa', 'aaaa', 'aaae', 'aae', 'aaea', 'aaee', 'ae', 'aea', 'aeaa', 'aeae', 'aee', 'aeea', 'aeee',
              'ea', 'eaa', 'eaaa', 'eaae', 'eae', 'eaea', 'eaee', 'ee', 'eea', 'eeaa', 'eeae', 'eee', 'eeea', 'eeee']

    for i in range(1, 28):
        assert sg.get_list_of_values(i) == values[:i]


# Same options as test_get_list_of_values, which has 28 possible values
def test_get_list_of_too_many_values():
    sg = get_generator(2, 4, 'a', 'e', 'bcd')
    with pytest.raises(ValueError):
        sg.get_list_of_values(29)


def test_get_list_of_too_many_values_whitelist():
    sg = get_generator_whitelist(2, 4, 'ae')
    with pytest.raises(ValueError):
        sg.get_list_of_values(29)
