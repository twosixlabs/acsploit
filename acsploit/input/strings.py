import random
from .chars import CharGenerator
from acsploit.options import Options


class StringGenerator:
    """String Generator"""

    INPUT_NAME = "string"

    def __init__(self):
        """Initialize the String Generator."""
        self.options = Options()
        self.options.add_option('min_length', 1, 'Minimum string length')
        self.options.add_option('max_length', 10, 'Maximum string length')
        self.options.add_option('min_value', 'a', 'Minimum ASCII character to use')
        self.options.add_option('max_value', 'z', 'Maximum ASCII character to use')
        self.options.add_option('restrictions', '', 'String of characters to exclude')
        self.options.add_option('use_whitelist', False, 'If True, only generate characters from the whitelist')
        self.options.add_option('whitelist', '', 'String of characters to generate from if use_whitelist is True')

        self.char_gen = CharGenerator()
        self.prepare()

    def prepare(self):
        """Updates the string generator options."""
        self.char_gen.options['min_value'] = self.options['min_value']
        self.char_gen.options['max_value'] = self.options['max_value']
        self.char_gen.options['restrictions'] = self.options['restrictions']
        self.char_gen.options['use_whitelist'] = self.options['use_whitelist']
        self.char_gen.options['whitelist'] = self.options['whitelist']
        self.char_gen.prepare()

    def _reduce_last_char(self, value):
        """Returns the next lowest string, may be shorter than min_length"""
        c = value[-1]
        try:
            low_c = self.char_gen.get_less_than(c)
            return value[:-1] + low_c + self.char_gen.get_max_value() * (self.options['max_length'] - len(value))
        except ValueError:
            # the last character is min_value, strip it off
            return value[:-1]

    def _increment_last_char(self, value):
        """Returns the next greatest string of equal or lesser length than value"""
        while len(value) > 0:
            c = value[-1]
            try:
                high_c = self.char_gen.get_greater_than(c)
                value = value[:-1] + high_c
                if len(value) < self.options['min_length']:
                    value += self.char_gen.get_min_value() * (self.options['min_length'] - len(value))
                return value

            except ValueError:
                value = value[:-1]

        # should never get here since we only call this function with value < max_value
        raise ValueError('No valid value exists greater than {}'.format(value))

    def get_less_than(self, value):
        """Returns the largest valid string less than value (lexicographical order)"""
        # give up if value is not greater than min_value
        # all other cases should succeed, since there is at least one valid string (min_value) less than value
        if value <= self.get_min_value():
            raise ValueError('No valid value exists less than {}'.format(value))

        # strip all extra characters from the right if string is too long
        # the new value will be less than original, so return if valid, or continue
        max_len = self.options['max_length']
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

    def get_greater_than(self, value):
        """Returns the smallest valid string greater than value (lexicographical order)"""
        # give up if value is not smaller than max_value
        # all other cases should succeed, since there is at least one valid string (max_value) greater than value
        if value >= self.get_max_value():
            raise ValueError('No valid value exists greater than {}'.format(value))

        # strip all extra characters from the right if string is too long
        # the result will be less than original, but will have the same next greatest value
        max_len = self.options['max_length']
        if len(value) > max_len:
            value = value[:max_len]

        # deal with invalid chars
        # strip all chars right of the invalid char; increment the invalid char to a larger valid char
        for i, c in enumerate(value):
            if not self.char_gen.is_valid(c):
                value = value[:i+1]
                return self._increment_last_char(value)

        # no invalid chars
        min_len = self.options['min_length']
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
        """Returns the max value."""
        return self.char_gen.get_max_value() * self.options['max_length']

    def get_min_value(self):
        """Returns the min value."""
        return self.char_gen.get_min_value() * self.options['min_length']

    def get_random(self):
        """Returns a random string
        Length is chosen uniformly at random, so shorter strings appear equally as often as longer strings,
        which means the distribution is not uniform, since any given short string is more likely to be chosen
        than a given longer string"""
        length = random.randint(self.options['min_length'], self.options['max_length'])
        return ''.join([self.char_gen.get_random() for _ in range(length)])

    def get_list_of_values(self, num_values):
        """Returns a list of valid numbers starting from min_value."""
        values = []
        next = self.get_min_value()
        for _ in range(num_values):
            values.append(next)
            try:
                next = self.get_greater_than(next)
            except ValueError:
                raise ValueError('Fewer than {} unique values'.format(num_values))
        return values

    def is_valid(self, candidate):
        """Returns true if the string has valid characters and meets min and max length constraints."""
        length_is_valid = self.options['min_length'] <= len(candidate) <= self.options['max_length']
        chars_are_valid = all(self.char_gen.is_valid(c) for c in candidate)
        return length_is_valid and chars_are_valid
