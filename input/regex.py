import exrex
import re
from options import Options


class RegexMatchGenerator(object):

    def __init__(self):
        self._options = Options()
        self._options.add_option('regex', '.*', 'Regular expression to match strings against')

    def set_option(self, key, value):
        self._options[key] = value

    def get_options(self):
        return self._options

    # Returns a random string matching the regex
    def get_random(self):
        return exrex.getone(self._options['regex'])

    # Returns a list of num_values random strings matching regex; note that matches may be repeated
    def get_random_list(self, num_values):
        return [exrex.getone(self._options['regex']) for _ in range(num_values)]

    # Returns a list of num_values strings matching regex; note that strings that match in
    # multiple ways may be repeated (e.g. regex 'a|a|a' would yield 'a' as a match three times)
    def get_list_of_values(self, num_values):
        regex_gen = exrex.generate(self._options['regex'])
        try:
            return [next(regex_gen) for _ in range(num_values)]
        except StopIteration:
            raise ValueError('Fewer than {} regex matches could be generated'.format(num_values))

    def is_valid(self, candidate):  # determine if candidate is valid
        return re.match(self._options['regex'], candidate) is not None
