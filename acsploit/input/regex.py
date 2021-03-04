import exrex
import re
from acsploit.options import Options


class RegexMatchGenerator:
    """Regex Generator"""

    INPUT_NAME = 'regex'

    def __init__(self):
        """Initialize the Regex Generator."""
        self.options = Options()
        self.options.add_option('regex', '.*', 'Generated strings will match this regex')

    def get_random(self):
        """Returns a random string matching the regex"""
        return exrex.getone(self.options['regex'])

    def get_random_list(self, num_values):
        """Returns a list of num_values random strings matching regex; note that matches may be repeated"""
        return [exrex.getone(self.options['regex']) for _ in range(num_values)]

    def get_list_of_values(self, num_values):
        """Returns a list of num_values strings matching regex; note that strings that match in
        multiple ways may be repeated (e.g. regex 'a|a|a' would yield 'a' as a match three times)"""
        regex_gen = exrex.generate(self.options['regex'])
        try:
            return [next(regex_gen) for _ in range(num_values)]
        except StopIteration:
            raise ValueError('Fewer than {} regex matches could be generated'.format(num_values))

    def is_valid(self, candidate):
        """Returns true if valid."""
        return re.match(self.options['regex'], candidate) is not None

    def get_max_value(self):
        raise NotImplementedError('Regex input generator cannot generate maximum values')

    def get_min_value(self):
        raise NotImplementedError('Regex input generator cannot generate minimum values')

    def get_greater_than(self, value):
        raise NotImplementedError('Regex input generator cannot generate relative values')

    def get_less_than(self, value):
        raise NotImplementedError('Regex input generator cannot generate relative values')
