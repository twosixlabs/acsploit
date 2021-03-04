import random
from acsploit.options import Options


class FloatGenerator:

    INPUT_NAME = "float"

    def __init__(self):
        """Initialize the Float Generator."""
        self.options = Options()
        self.options.add_option('min_value', 0.0, 'Minimum floating point value allowed')
        self.options.add_option('max_value', 255.0, 'Maximum floating point value allowed')

        self._min = 0.0
        self._max = 255.0

    def prepare(self):
        """Sets max, min based on _options; called before generator is used with an exploit."""
        self._min = self.options['min_value']
        self._max = self.options['max_value']

    def get_less_than(self, value):
        """Returns a float less than the given value."""
        if value > self._max:
            return self._max
        if value <= self._min:
            raise ValueError('No valid values less than {}'.format(value))
        # return average of _min and value
        return self._min / 2 + value / 2

    def get_greater_than(self, value):
        """Returns a float greater than the given value."""
        if value < self._min:
            return self._min
        if value >= self._max:
            raise ValueError('No valid values greater than {}'.format(value))
        # return average of _max and value
        return self._max / 2 + value / 2

    def get_max_value(self):
        """Return the max character value."""
        return self._max

    def get_min_value(self):
        """Return the min character value."""
        return self._min

    def get_random(self):
        """Returns a random float."""
        return random.uniform(self._min, self._max)

    def is_valid(self, value):
        """Returns True if the float is a valid value between the min and max values (inclusive)."""
        return self._min <= value <= self._max and type(value) is float

    def get_list_of_values(self, num_values):
        """Returns a list of floats."""
        # not technically guaranteed to be unique, but collisions are highly unlikely
        return [random.uniform(self._min, self._max) for _ in range(num_values)]
