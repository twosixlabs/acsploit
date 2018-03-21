import random
import string
from options import Options


class CharGenerator(object):

    INPUT_NAME = "char"

    # min cannot equal max
    def __init__(self):
        self._options = Options()
        self._options.add_option('min_value', 'a', 'Minimum ASCII character to use')
        self._options.add_option('max_value', 'z', 'Maximum ASCII character to use')
        self._options.add_option('restrictions', '', 'String of characters to exclude')

        self.char_set = []  # char_set will be a sorted valid set of characters given the constraints set in _options
        self.update()

    def set_option(self, key, value):
        self._options[key] = value
        self.update()

    def get_options(self):
        return self._options

    def get_min_value(self):
        return self.char_set[0]  # options[min_value] could be in restrictions, so we don't just return that

    def get_max_value(self):
        return self.char_set[-1]  # options[max_value] could be in restrictions, so we don't just return that

    def is_valid(self, candidate):
        min_val = self._options['min_value']
        max_val = self._options['max_value']
        restrictions = self._options['restrictions']
        return min_val <= candidate <= max_val and candidate not in restrictions

    def update(self):
        self.char_set = [c for c in string.printable if self.is_valid(c)]
        self.char_set.sort()

    def get_less_than(self, value):
        result = None
        for c in self.char_set:
            if c >= value:
                break
            result = c
        if result is None:
            raise ValueError('No valid value exists less than {}'.format(value))
        return result

    def get_greater_than(self, value):
        for c in self.char_set:
            if c > value:
                return c

        raise ValueError('No valid value exists greater than {}'.format(value))

    def get_random(self):
        return random.choice(self.char_set)

    def get_char_set(self):
        return self.char_set

    def get_list_of_values(self, num_values):  # returns a string with length num_values starting from min_value
        if num_values > len(self.char_set):
            raise ValueError('Fewer than {} unique values'.format(num_values))

        return self.char_set[:num_values]
