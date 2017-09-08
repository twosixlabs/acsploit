# from abc import ABC
from abc import abstractmethod
import random

class Generator(object):
    @abstractmethod
    def get_less_than(self, value):
        pass

    @abstractmethod
    def get_greater_than(self, value):
        pass

    @abstractmethod
    def get_max_value(self):
        pass

    @abstractmethod
    def get_min_value(self):
        pass

    @abstractmethod
    def get_random(self):
        pass

class IntGenerator(Generator):
    def __init__(self, min, max):
        super(IntGenerator, self).__init__()
        self.min = min
        self.max = max

    def get_less_than(self, value):
        if value == self.min:
            return self.min
        return value - 1

    def get_greater_than(self, value):
        if value == self.max:
            return self.max
        return value + 1

    def get_max_value(self):
        return self.max

    def get_min_value(self):
        return self.min

    def get_random(self):
        return random.randint(self.min, self.max)

class StringGenerator(Generator):
    def __init__(self, char_gen, min_length, max_length):
        super(StringGenerator, self).__init__()
        self.char_gen = char_gen
        self.min_length = min_length
        self.max_length = max_length

    def get_less_than(self, value):
        char_list = list(value)
        for i in range(len(char_list) - 1, 0, -1): #iterate backwards through list. e.g. replace zzz with zzy
            c = char_list[i]
            if (c != self.char_gen.get_min_value()):
                char_list[i] = self.char_gen.get_less_than(c)
                return ''.join(char_list)

        return value

    def get_greater_than(self, value):
        char_list = list(value)
        for i in range(len(char_list)):
            c = char_list[i]
            if (c != self.char_gen.get_max_value()):
                char_list[i] = self.char_gen.get_greater_than(c)
                return ''.join(char_list)

        return value

    def get_max_value(self):
        value = ""
        for i in range(self.max_length):
            value = value + self.char_gen.get_max_value()

        return value

    def get_min_value(self):
        value = ""
        for i in range(self.min_length):
            value = value + self.char_gen.get_min_value()

        return value

    def get_random(self):
        length = self.min_length

        if (self.min_length != self.max_length):
            length = random.randint(self.min_length, self.max_length)

        value = []
        for i in range(length):
            value.append(self.char_gen.get_random())

        return ''.join(value)

class CharGenerator(Generator):
    # min cannot equal max
    def __init__(self, min, max):
        super(CharGenerator, self).__init__()

        self.min = min
        self.max = max
        self.characters = []
        self.init_characters()

    def init_characters(self):
        chars = []
        for i in range(int(self.min), int(self.max) + 1):
            chars.append(chr(i))
        self.characters = chars
        print(self.characters)

    def get_less_than(self, value):
        if ord(value) == self.min:
            return self.min
        value = chr(ord(value) - 1)
        while chr(ord(value)) not in self.characters:
            value = chr(ord(value) - 1)
        return value

    def get_greater_than(self, value):
        if ord(value) == self.max:
            return value
        value = chr(ord(value) + 1)
        while chr(ord(value)) not in self.characters:
            value = chr(ord(value) + 1)
        return value


    def get_max_value(self):
        return chr(self.max)

    def get_min_value(self):
        return chr(self.min)

    def get_random(self):
        return random.choice(self.characters)

    def add_restrictions(self, restrictions):
        for restriction in restrictions:
            try:
                self.characters.remove(restriction)
            except ValueError:
                pass  # Error doesn't need to be dealt with
