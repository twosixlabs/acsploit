from input import FloatGenerator
import pytest


def get_generator(min_value, max_value):
    fg = FloatGenerator()
    fg.options['min_value'] = min_value
    fg.options['max_value'] = max_value
    fg.prepare()
    return fg


@pytest.mark.parametrize("min_value", [-1020.3, -200.2555, -1.1, 0.0, 0.6667, 1.0, 5.755, 57.8, 50000.555])
def test_get_min_value(min_value):
    fg = get_generator(min_value, 50000.555)
    assert fg.get_min_value() == min_value


@pytest.mark.parametrize("max_value", [-1020.3, -200.2555, -1.1, 0.0, 0.6667, 1.0, 5.755, 57.8, 50000.555])
def test_get_min_value(max_value):
    fg = get_generator(-1020.3, max_value)
    assert fg.get_max_value() == max_value


@pytest.mark.parametrize("min_value, max_value, num", [
    (1.15, 10.0, 5),  # all positive
    (-10.0, -1.15, 4),  # all negative
    (-3.33, 3.44, 5),  # negative to positive
    (100.0, 102.09, 3),  # all values from min to max
    (0.0, 5.5, 1)  # one value
])
def test_get_list_of_values(min_value, max_value, num):
    fg = get_generator(min_value, max_value)
    l = fg.get_list_of_values(num)
    assert len(l) == num
    assert all(min_value <= x <= max_value for x in l)


@pytest.mark.parametrize("min_value, max_value, value, expected", [
    (1.0, 100.5, 10.5, 55.5),  # greater than min
    (1.0, 100.5, 8, 54.25),  # int value
    (-10.0, 100.5, -8.3, 46.1),  # negative min
    (-10.0, 100.5, -8, 46.25),  # negative int value
    (5.0, 100.5, 4.0, 5.0),  # value < min
    (5.0, 100.5, 5.0, 52.75),  # value = min
    (-3.0, 0.5, -4.0, -3.0),  # negative min, value < min
    (5.0, 100.5, 5.0, 52.75),  # negative min, value = min
])
def test_get_greater_than(min_value, max_value, value, expected):
    fg = get_generator(min_value, max_value)
    assert fg.get_greater_than(value) == expected


@pytest.mark.parametrize("min_value, max_value, too_large", [
    (1, 10, 12),  # greater than max
    (1, 10, 10),  # equal to max
    (-10, -5, 3),  # greater than negative max
    (-10, -5, -5.0),  # equal to negative max
])
def test_get_greater_than_max(min_value, max_value, too_large):
    fg = get_generator(min_value, max_value)
    with pytest.raises(ValueError):
        fg.get_greater_than(too_large)


@pytest.mark.parametrize("min_value, max_value, value, expected", [
    (1, 100.5, 10.5, 5.75),  # less than max
    (1, 100.5, 8, 4.5),  # int value
    (-100, -10, -18.5, -59.25),  # negative max
    (-100, -10, -43, -71.5),  # negative int value
    (5, 10.1, 11.0, 10.1),  # value > max
    (5, 10.1, 10.1, 7.55),  # value = max
    (-30, -5.3, -4, -5.3),  # negative max, value > max
    (-30, -5.3, -5.3, -17.65),  # negative max, value == max
])
def test_get_less_than(min_value, max_value, value, expected):
    fg = get_generator(min_value, max_value)
    assert fg.get_less_than(value) == expected


@pytest.mark.parametrize("min_value, max_value, too_small", [
    (5.4, 10, 3),  # less than min
    (5.4, 10, 5.4),  # equal to min
    (-10.1, -5, -15.0),  # less than negative min
    (-10.1, -5, -10.1),  # equal to negative min
])
def test_get_less_than_min(min_value, max_value, too_small):
    fg = get_generator(min_value, max_value)
    with pytest.raises(ValueError):
        fg.get_less_than(too_small)


@pytest.mark.parametrize("min_value, max_value, valid_values", [
    (1.1, 10.4, [1.1, 4.9, 5.5, 10.4]),  # positive min, max
    (-10.4, -1.1, [-1.1, -4.9, -5.5, -10.4]),  # negative min, max
    (-100.3, 1000.15, [-100.3, -23.2, 0.0, 135.0, 430.3, 1000.0, 1000.15])  # negative min, positive max
])
def test_valid_values(min_value, max_value, valid_values):
    fg = get_generator(min_value, max_value)
    for value in valid_values:
        assert fg.is_valid(value)


@pytest.mark.parametrize("min_value, max_value, invalid_values", [
    (1.1, 10.4, [-2, -1, 0.2, 1, 1.0, 10, 11.0]),  # positive min, max
    (-10.4, -1.1, [-15, -14.2, -9, -2, -1, -1.0, 0, 0.4]),  # negative min, max
    (-100.3, 1000.15, [-101, -100.31, -3, 100, 1000.4, 1007])  # negative min, positive max
])
def test_invalid_values(min_value, max_value, invalid_values):
    fg = get_generator(min_value, max_value)
    for value in invalid_values:
        assert not fg.is_valid(value)
