from .base import Generator
import random

class CharGenerator(Generator):

    options = dict({"min_value":0x61, "max_value":0x7A, "restrictions":""})

    # min cannot equal max
    def __init__(self):
        super(CharGenerator, self).__init__()
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
        if ord(value) == int(self.options['min_value']):
            return value
        value = chr(ord(value) - 1)
        while chr(ord(value)) not in self.characters:
            if ord(value) - 1 < 0:
                return value
            value = chr(ord(value) - 1)
        return value

    def get_greater_than(self, value):
        if (ord(value) == int(self.options['max_value'])):
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
        self.init_characters() #in case options have been changed
        return random.choice(self.characters)

    def add_restrictions(self, restrictions):
        for restriction in restrictions:
            try:
                self.characters.remove(restriction)
            except ValueError:
                pass  # Error doesn't need to be dealt with
