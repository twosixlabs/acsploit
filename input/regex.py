import exrex
import re
from options import Options


class RegexMatchGenerator:

    INPUT_NAME = 'regex'

    def __init__(self):
        self.options = Options()
        self.options.add_option('regex', '.*', 'Generated strings will match this regex')

    # returns a random string matching the regex
    def get_random(self):
        return exrex.getone(self.options['regex'])

    # returns a list of num_values random strings matching regex; note that matches may be repeated
    def get_random_list(self, num_values):
        return [exrex.getone(self.options['regex']) for _ in range(num_values)]

    # returns a list of num_values strings matching regex; note that strings that match in
    # multiple ways may be repeated (e.g. regex 'a|a|a' would yield 'a' as a match three times)
    def get_list_of_values(self, num_values):
        regex_gen = exrex.generate(self.options['regex'])
        try:
            return [next(regex_gen) for _ in range(num_values)]
        except StopIteration:
            raise ValueError('Fewer than {} regex matches could be generated'.format(num_values))

    def is_valid(self, candidate):
        return re.match(self.options['regex'], candidate) is not None

    def get_max_value(self):
        raise NotImplementedError('Regex input generator cannot generate maximum values')

    def get_min_value(self):
        raise NotImplementedError('Regex input generator cannot generate minimum values')

    def get_greater_than(self, value):
        raise NotImplementedError('Regex input generator cannot generate relative values')

    def get_less_than(self, value):
        raise NotImplementedError('Regex input generator cannot generate relative values')
