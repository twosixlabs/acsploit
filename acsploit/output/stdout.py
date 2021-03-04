import os
import sys
from acsploit.options import Options
from . import output_common


class Stdout:
    """Stdout class."""

    OUTPUT_NAME = 'stdout'  # exploits can use this internally to whitelist/blacklist supported output formats

    _SEPARATORS = {
        'newline': '\n',
        'comma': ',',
        'space': ' ',
        'tab': '\t',
        'os_newline': os.linesep
    }

    def __init__(self):
        """Initialize the Stdout class."""
        self.options = Options()
        self.options.add_option('separator', 'newline', 'Separator between elements',
                                list(self._SEPARATORS.keys()), True)
        self.options.add_option('number_format', 'decimal', 'Format for numbers', ['decimal', 'hexadecimal', 'octal'])

    def output(self, output_list):
        """Output to stdout."""
        separator = output_common.get_separator(self.options['separator'], self._SEPARATORS)
        line = separator.join([self.convert_item(item) for item in output_list])
        line += os.linesep
        sys.stdout.write(line)

    def convert_item(self, item):
        """Convert output to hexadecimal or octal."""
        # NB: this doesn't recurse onto lists
        if type(item) is int:
            if self.options['number_format'] == 'hexadecimal':
                item = hex(item)
            elif self.options['number_format'] == 'octal':
                item = oct(item)

        return str(item)
