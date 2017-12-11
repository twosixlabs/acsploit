from .chars import CharGenerator
from .base import Generator
import random

class StringGenerator(Generator):

    options = dict({"min_length":1, "max_length":10, "min_value":0x61, "max_value":0x7A, "restrictions":""})

    def __init__(self):
        super(StringGenerator, self).__init__()
        self.char_gen = CharGenerator()
        self.init_char_gen()

    def init_char_gen(self):
        char_opts = dict({"min_value":self.options["min_value"] , "max_value":self.options["max_value"] , "restrictions":self.options["restrictions"]})
        self.char_gen.options = char_opts

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
        for i in range(int(self.options['max_length'])):
            value = value + self.char_gen.get_max_value()

        return value

    def get_min_value(self):
        value = ""
        for i in range(int(self.options['min_length'])):
            value = value + self.char_gen.get_min_value()

        return value

    def get_random(self):
        self.init_char_gen()
        length = int(self.options['min_length'])
        
        if (int(self.options['min_length']) != int(self.options['max_length'])):
            length = random.randint(int(self.options['min_length']), int(self.options['max_length']))

        value = []
        for i in range(length):
            value.append(self.char_gen.get_random())
            
        return ''.join(value)

