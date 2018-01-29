import random


class CharGenerator(object):

    options = {
        'min_value': 0x61,
        'max_value': 0x7A,
        'restrictions': ''}
    descriptions = {
        'min_value': 'Minimum ASCII value to use.',
        'max_value': 'Maximum ASCII value to use.',
        'restrictions': 'String of characters to exclude.'}

    # min cannot equal max
    def __init__(self):
        self.characters = []
        self.init_characters()
        # TODO: When there are a lot of restrictions, the char/string generators breaks - needs fix
        self.add_restrictions(self.options['restrictions'])

    def init_characters(self):
        chars = []
        for i in range(int(self.options['min_value']), int(self.options['max_value']) + 1):
            chars.append(chr(i))
        self.characters = chars

    def get_less_than(self, value):
        tempmin = int(self.options['min_value'])
        while chr(tempmin) not in self.characters:
            tempmin += 1

        if ord(value) == tempmin:
            return value
        value = chr(ord(value) - 1)
        while chr(ord(value)) not in self.characters:
            if ord(value) - 1 < 0:
                return value
            value = chr(ord(value) - 1)
        return value

    def get_greater_than(self, value):
        tempmax = int(self.options['max_value'])
        while chr(tempmax) not in self.characters:
            tempmax -= 1

        if ord(value) == tempmax:
            return value
        value = chr(ord(value) + 1)
        while chr(ord(value)) not in self.characters:
            value = chr(ord(value) + 1)
        return value

    def get_max_value(self):
        return chr(int(self.options['max_value']))

    def get_min_value(self):
        return chr(int(self.options['min_value']))

    def get_random(self):
        self.init_characters()  # in case options have been changed
        self.add_restrictions(self.options['restrictions'])
        return random.choice(self.characters)

    def add_restrictions(self, restrictions):
        for restriction in restrictions:
            try:
                self.characters.remove(restriction)
            except ValueError:
                pass  # Error doesn't need to be dealt with
