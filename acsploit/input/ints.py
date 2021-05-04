import random
import math
from acsploit.options import Options


class IntGenerator:
    """Integer Generator"""

    INPUT_NAME = "int"

    def __init__(self):
        """Initialize the Integer Generator."""
        self.options = Options()
        self.options.add_option('min_value', 0, 'Minimum integer allowed')
        self.options.add_option('max_value', 255, 'Maximum integer allowed')

        self._min = 0
        self._max = 255

    def prepare(self):
        """Sets max, min based on _options; called before generator is used with an exploit."""
        self._min = self.options['min_value']
        self._max = self.options['max_value']

    def get_less_than(self, value):
        """Returns a integer less than the given value."""
        if value > self._max:
            return self._max
        if value <= self._min:
            raise ValueError('No valid values less than {}'.format(value))
        return int(math.ceil(value) - 1)

    def get_greater_than(self, value):
        """Returns an integer greater than the given value."""
        if value < self._min:
            return self._min
        if value >= self._max:
            raise ValueError('No valid values greater than {}'.format(value))
        return int(math.floor(value) + 1)

    def get_max_value(self):
        """Return the max character value."""
        return self._max

    def get_min_value(self):
        """Return the min character value."""
        return self._min

    def get_random(self):
        """Returns a random integer."""
        return random.randint(self._min, self._max)

    def is_valid(self, value):
        """Returns True if the integer is a valid value between the min and max values (inclusive)."""
        return self._min <= value <= self._max and type(value) is int

    def get_list_of_values(self, num_values):
        """Returns a list of ints."""
        if self._min + num_values - 1 > self._max:
            raise ValueError('Fewer than {} unique values'.format(num_values))
        return [self._min + i for i in range(num_values)]
