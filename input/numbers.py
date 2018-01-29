import random


class IntGenerator(object):

    options = {
        'max_value': 255,
        'min_value': 0}
    descriptions = {
        'max_value': 'Maximum integer allowed.',
        'min_value': 'Minimum integer allowed.'}

    def __init__(self):
        self.max = int(self.options['max_value'])
        self.min = int(self.options['min_value'])

    def get_less_than(self, value):
        if value == int(self.options['min_value']):
            return int(self.options['min_value'])
        return value - 1

    def get_greater_than(self, value):
        if value == int(self.options['max_value']):
            return int(self.options['max_value'])
        return value + 1

    def get_max_value(self):
        return int(self.options['max_value'])

    def get_min_value(self):
        return int(self.options['min_value'])

    def get_random(self):
        return random.randint(int(self.options['min_value']), int(self.options['max_value']))
