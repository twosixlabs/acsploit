import random
import exrex
import re
from chars import CharGenerator
from options import Options


class StringGenerator(object):

    def __init__(self):
        self._options = Options()
        self._options.add_option('min_length', 1, 'Minimum string length')
        self._options.add_option('max_length', 10, 'Maximum string length')
        self._options.add_option('min_value', 'a', 'Minimum ASCII character to use')
        self._options.add_option('max_value', 'z', 'Maximum ASCII character to use')
        self._options.add_option('restrictions', '', 'String of characters to exclude')

        self.char_gen = CharGenerator()
        self.update('min_value', self._options['min_value'])
        self.update('max_value', self._options['max_value'])
        self.update('restrictions', self._options['restrictions'])

    def set_option(self, key, value):
        self._options[key] = value
        if key in ['min_value', 'max_value', 'restrictions']:
            self.update(key, value)

    def get_options(self):
        return self._options

    def update(self, key, value):
        self.char_gen.set_option(key, value)

    # returns the next lowest string, may be shorter than min_length
    def _reduce_last_char(self, value):
        c = value[-1]
        try:
            low_c = self.char_gen.get_less_than(c)
            return value[:-1] + low_c + self.char_gen.get_max_value() * (self._options['max_length'] - len(value))
        except ValueError:
            # the last character is min_value, strip it off
            return value[:-1]

    # returns the next greatest string of equal or lesser length than value
    def _increment_last_char(self, value):
        while len(value) > 0:
            c = value[-1]
            try:
                high_c = self.char_gen.get_greater_than(c)
                value = value[:-1] + high_c
                if len(value) < self._options['min_length']:
                    value += self.char_gen.get_min_value() * (self._options['min_length'] - len(value))
                return value

            except ValueError:
                value = value[:-1]

        # should never get here since we only call this function with value < max_value
        raise ValueError('No valid value exists greater than {}'.format(value))

    # returns the largest valid string less than value (lexicographical order)
    def get_less_than(self, value):
        # give up if value is not greater than min_value
        # all other cases should succeed, since there is at least one valid string (min_value) less than value
        if value <= self.get_min_value():
            raise ValueError('No valid value exists less than {}'.format(value))

        # strip all extra characters from the right if string is too long
        # the new value will be less than original, so return if valid, or continue
        max_len = self._options['max_length']
        if len(value) > max_len:
            value = value[:max_len]
            if self.is_valid(value):
                return value

        # strip all chars beyond the first invalid char in value
        # we will reduce the invalid char in the next step
        for i, c in enumerate(value):
            if not self.char_gen.is_valid(c):
                value = value[:i+1]

        value = self._reduce_last_char(value)
        while not self.is_valid(value):
            value = self._reduce_last_char(value)

        return value

    # returns the smallest valid string greater than value (lexicographical order)
    def get_greater_than(self, value):
        # give up if value is not smaller than max_value
        # all other cases should succeed, since there is at least one valid string (max_value) greater than value
        if value >= self.get_max_value():
            raise ValueError('No valid value exists greater than {}'.format(value))

        # strip all extra characters from the right if string is too long
        # the result will be less than original, but will have the same next greatest value
        max_len = self._options['max_length']
        if len(value) > max_len:
            value = value[:max_len]

        # deal with invalid chars
        # strip all chars right of the invalid char; increment the invalid char to a larger valid char
        for i, c in enumerate(value):
            if not self.char_gen.is_valid(c):
                value = value[:i+1]
                return self._increment_last_char(value)

        # no invalid chars
        min_len = self._options['min_length']
        if len(value) < min_len:
            # pad short value with min_value to min_length
            return value + self.char_gen.get_min_value() * (min_len - len(value))
        elif len(value) < max_len:
            # append one min_value character to value if not too long
            return value + self.char_gen.get_min_value()
        else:
            # can't extend length; increment last char to a larger char
            return self._increment_last_char(value)

    def get_max_value(self):
        return self.char_gen.get_max_value() * self._options['max_length']

    def get_min_value(self):
        return self.char_gen.get_min_value() * self._options['min_length']

    # Returns a random string
    # Length is chosen uniformly at random, so shorter strings appear equally as often as longer strings,
    # which means the distribution is not uniform, since any given short string is more likely to be chosen
    # than a given longer string
    def get_random(self):
        length = random.randint(self._options['min_length'], self._options['max_length'])
        return ''.join([self.char_gen.get_random() for _ in range(length)])

    def get_list_of_values(self, num_values):  # returns a list of valid numbers starting from min_value.
        values = []
        next = self.get_min_value()
        for _ in range(num_values):
            values.append(next)
            try:
                next = self.get_greater_than(next)
            except ValueError:
                raise ValueError('Fewer than {} unique values'.format(num_values))
        return values

    def is_valid(self, candidate):  # determine if candidate is valid
        length_is_valid = self._options['min_length'] <= len(candidate) <= self._options['max_length']
        chars_are_valid = all(self.char_gen.is_valid(c) for c in candidate)
        return length_is_valid and chars_are_valid