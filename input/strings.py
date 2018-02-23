import random
import exrex
import re
from chars import CharGenerator
from options import Options


class StringGenerator(object):

    options = Options()
    options.add_option('min_length', 1, 'Minimum string length')
    options.add_option('max_length', 10, 'Maximum string length')
    options.add_option('min_value', 0x61, 'Minimum ASCII character to use')
    options.add_option('max_value', 0x7A, 'Maximum ASCII character to use')
    options.add_option('restrictions', '', 'String of characters to exclude')

    def __init__(self):
        self.char_gen = CharGenerator()
        self.init_char_gen()

    def init_char_gen(self):
        char_opts = {
            'min_value': self.options['min_value'],
            'max_value': self.options['max_value'],
            'restrictions': self.options['restrictions']}
        self.char_gen.options = char_opts

    def get_less_than(self, value):
        char_list = list(value)
        for i in range(len(char_list) - 1, 0, -1):  # iterate backwards through list. e.g. replace zzz with zzy
            c = char_list[i]
            if c != self.char_gen.get_min_value():
                char_list[i] = self.char_gen.get_less_than(c)
                return ''.join(char_list)

        return value

    def get_greater_than(self, value):
        char_list = list(value)
        for i in range(len(char_list)):
            c = char_list[i]
            if c != self.char_gen.get_max_value():
                char_list[i] = self.char_gen.get_greater_than(c)
                return ''.join(char_list)

        return value

    def get_max_value(self):
        value = ''
        for i in range(int(self.options['max_length'])):
            value = value + self.char_gen.get_max_value()

        return value

    def get_min_value(self):
        value = ''
        for i in range(int(self.options['min_length'])):
            value = value + self.char_gen.get_min_value()

        return value

    def get_random(self):
        self.init_char_gen()
        length = int(self.options['min_length'])
        
        if int(self.options['min_length']) != int(self.options['max_length']):
            length = random.randint(int(self.options['min_length']), int(self.options['max_length']))

        value = []
        for i in range(length):
            value.append(self.char_gen.get_random())
            
        return ''.join(value)

    def get_random_regex(self,regex):
        y=str(exrex.getone(regex))
        while self.is_valid(y)==False or re.match(regex,y)==False: #infinite loop, bad
            y=str(exrex.getone(regex))
        return y

    def get_random_regex_list(self,regex,numvalues):
        regex_matches=[]
        while len(regex_matches)<numvalues:  #infinite loop, bad
            candidate=self.get_random_regex(regex)
            if candidate not in regex_matches:
                regex_matches.append(candidate)
        return regex_matches

    def get_list_of_values(self, numvalues):  # returns a list of valid numbers starting from min_value.
        list_of_values = []
        if (numvalues > 0):
            candidate = self.options['min_value']
            while len(list_of_values) < numvalues:
                if self.is_valid(candidate):
                    list_of_values.append(candidate)
                if candidate > self.get_max_value():
                    print "Candidate larger than maximum, aborting"
                    break
                candidate = self.get_greater_than(candidate)
            return list_of_values

    def is_valid(self, candidate):  # determine if candidate is valid
        if (len(candidate) >= int(self.options['min_length'])) & (len(candidate) <= int(self.options['max_length'])):
            for character in candidate:
                if character <= self.char_gen.get_min_value() or character >= self.char_gen.get_max_value():
                    return False
                if character in self.options['restrictions']:
                    return False
            return True
        else:
            return False
