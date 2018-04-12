import random
import math
from options import Options


class IntGenerator(object):

    INPUT_NAME = "int"

    def __init__(self):
        self.options = Options()
        self.options.add_option('min_value', 0, 'Minimum integer allowed')
        self.options.add_option('max_value', 255, 'Maximum integer allowed')

        self.min = 0
        self.max = 255

    # sets max, min based on _options; called before generator is used with an exploit
    def prepare(self):
        self.min = self.options['min_value']
        self.max = self.options['max_value']

    def get_less_than(self, value):
        # return closest int less than value
        # this can be simplified if we know value is an int
        if value > self.max:
            return self.max
        if value <= self.min:
            raise ValueError('No valid values less than {}'.format(value))
        return int(math.ceil(value) - 1)

    def get_greater_than(self, value):
        # return closest int greater than value
        # this can be simplified if we know value is an int
        if value < self.min:
            return self.min
        if value >= self.max:
            raise ValueError('No valid values greater than {}'.format(value))
        return int(math.floor(value) + 1)

    def get_max_value(self):
        return self.max

    def get_min_value(self):
        return self.min

    def get_random(self):
        return random.randint(self.min, self.max)

    def is_valid(self, value):  # Checks if a candidate value is valid, can be made stronger in the future
        return self.min <= value <= self.max and int(value) == value

    def get_list_of_values(self, num_values):  # returns a list of valid numbers starting from min_value
        if self.min + num_values - 1 > self.max:
            raise ValueError('Fewer than {} unique values'.format(num_values))
        return [self.min + i for i in range(num_values)]
