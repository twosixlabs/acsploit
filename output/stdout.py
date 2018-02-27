import sys
import os
from options import Options


class Stdout(object):

    OUTPUT_NAME = "stdout"  # exploits can use this internally to whitelist/blacklist supported output formats

    _SEPARATORS = {
        'newline': '\n',
        'comma': ',',
        'space': ' ',
        'tab': '\t',
        'os_newline': os.linesep
    }

    def __init__(self):
        self.options = Options()
        self.options.add_option('separator', 'newline', 'Separator between elements', ['newline', 'comma', 'space',
                                                                                       'tab', 'os_newline'])
        self.options.add_option('number_format', 'decimal', 'Format for numbers', ['decimal', 'hexadecimal', 'octal'])

    def output(self, output_list):
        separator = Stdout._SEPARATORS[self.options['separator']]
        line = separator.join([self.convert_item(item) for item in output_list])
        sys.stdout.write(line)
        sys.stdout.write(os.linesep)

    def convert_item(self, item):
        if type(item) is int:
            if self.options['number_format'] == 'hexdecimal':
                item = hex(item)
            elif self.options['number_format'] == 'octal':
                item = oct(item)

        return str(item)
