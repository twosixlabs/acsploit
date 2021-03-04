from input import IntGenerator
import pytest


def get_generator(min_value, max_value):
    ig = IntGenerator()
    ig.options['min_value'] = min_value
    ig.options['max_value'] = max_value
    ig.prepare()
    return ig


@pytest.mark.parametrize("min_value", [-1000, -200, -1, 0, 1, 3, 5, 50, 50000])
def test_get_min_value(min_value):
    ig = get_generator(min_value, 50000)
    assert ig.get_min_value() == min_value


@pytest.mark.parametrize("max_value", [-1000, -200, -1, 0, 1, 3, 5, 50, 50000])
def test_get_min_value(max_value):
    ig = get_generator(-1000, max_value)
    assert ig.get_max_value() == max_value


@pytest.mark.parametrize("min_value, max_value, num, expected", [
    (1, 10, 5, [1, 2, 3, 4, 5]),  # all positive
    (-10, -1, 4, [-10, -9, -8, -7]),  # all negative
    (-3, 3, 5, [-3, -2, -1, 0, 1]),  # negative to positive
    (100, 102, 3, [100, 101, 102]),  # all values from min to max
    (0, 5, 1, [0])  # one value
])
def test_get_list_of_values(min_value, max_value, num, expected):
    ig = get_generator(min_value, max_value)
    assert ig.get_list_of_values(num) == expected


def test_get_list_of_too_many_values():
    ig = get_generator(1, 5)
    with pytest.raises(ValueError):
        ig.get_list_of_values(6)


@pytest.mark.parametrize("min_value, max_value, value, expected", [
    (1, 100, 10, 11),  # greater than min
    (1, 100, 8.3, 9),  # float value
    (1, 100, 99, 100),  # value == max - 1
    (1, 100, 99.9, 100),  # max - 1 < value < max
    (-10, 100, -8, -7),  # negative min
    (-10, 100, -8.3, -8),  # negative float value
    (-10, 100, -0.3, 0),  # -1 < value < 0
    (-10, 100, 0.3, 1),  # 0 < value < 1
    (5, 100, 4, 5),  # value == min - 1
    (5, 100, 4.8, 5),  # min - 1 < value < min
    (5, 100, 2, 5),  # value < min - 1
    (-3, 0, -4, -3),  # negative min, value == min - 1
    (-3, 0, -3.5, -3),  # negative min, min - 1 < value < min
    (-3, 0, -10, -3)  # negative min, value < min - 1
])
def test_get_greater_than(min_value, max_value, value, expected):
    ig = get_generator(min_value, max_value)
    assert ig.get_greater_than(value) == expected


@pytest.mark.parametrize("min_value, max_value, too_large", [
    (1, 10, 12),  # greater than max
    (1, 10, 10),  # equal to max
    (1, 10, 10.1),  # max < value < max + 1
    (-10, -5, 3),  # greater than negative max
    (-10, -5, -5),  # equal to negative max
    (-10, -5, -4.9)  # negative max, max < value < max + 1
])
def test_get_greater_than_max(min_value, max_value, too_large):
    ig = get_generator(min_value, max_value)
    with pytest.raises(ValueError):
        ig.get_greater_than(too_large)


@pytest.mark.parametrize("min_value, max_value, value, expected", [
    (1, 100, 10, 9),  # less than max
    (1, 100, 8.3, 8),  # float value
    (1, 100, 2, 1),  # value == min + 1
    (1, 100, 1.1, 1),  # min < value < min + 1
    (-100, -10, -18, -19),  # negative max
    (-100, -10, -43.22, -44),  # negative float value
    (-10, 100, -0.3, -1),  # -1 < value < 0
    (-10, 100, 0.3, 0),  # 0 < value < 1
    (5, 10, 11, 10),  # value == max + 1
    (5, 10, 10.9, 10),  # max < value < max + 1
    (5, 100, 123, 100),  # value > max + 1
    (-30, -5, -4, -5),  # negative max, value == max + 1
    (-30, -5, -4.5, -5),  # negative max, max < value < max + 1
    (-30, -5, -1.4, -5)  # negative min, value > max + 1
])
def test_get_less_than(min_value, max_value, value, expected):
    ig = get_generator(min_value, max_value)
    assert ig.get_less_than(value) == expected


@pytest.mark.parametrize("min_value, max_value, too_small", [
    (5, 10, 3),  # less than min
    (5, 10, 5),  # equal to min
    (5, 10, 4.3),  # min - 1 < value < min
    (-10, -5, -15),  # less than negative min
    (-10, -5, -10),  # equal to negative min
    (-10, -5, -10.01)  # negative min, min - 1 < value < min
])
def test_get_less_than_min(min_value, max_value, too_small):
    ig = get_generator(min_value, max_value)
    with pytest.raises(ValueError):
        ig.get_less_than(too_small)


@pytest.mark.parametrize("min_value, max_value, valid_values", [
    (1, 10, list(range(1, 11))),  # positive min, max
    (-10, -1, list(range(-10, 0))),  # negative min, max
    (-100, 1000, list(range(-100, 1001)))  # negative min, positive max
])
def test_valid_values(min_value, max_value, valid_values):
    ig = get_generator(min_value, max_value)
    for value in valid_values:
        assert ig.is_valid(value)


@pytest.mark.parametrize("min_value, max_value, invalid_values", [
    (1, 10, [-2, -.5, 1.2, 10.2, 11]),  # positive min, max
    (-10, -1, [-15, -14.2, -9.5, 0, 0.4]),  # negative min, max
    (-100, 1000, [-101, -100.2, -3.3, 100.5, 1000.4, 1007])  # negative min, positive max
])
def test_invalid_values(min_value, max_value, invalid_values):
    ig = get_generator(min_value, max_value)
    for value in invalid_values:
        assert not ig.is_valid(value)
