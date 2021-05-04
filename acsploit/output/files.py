import os
from acsploit.options import Options
from . import output_common


class File:
    """File class."""

    OUTPUT_NAME = 'file'

    _SEPARATORS = {
        'newline': '\n',
        'comma': ',',
        'space': ' ',
        'tab': '\t',
        'os_newline': os.linesep
    }

    def __init__(self):
        """Initialize the File class."""
        self.options = Options()
        self.options.add_option('filename', 'acsploit_output.dat', 'The name of the file to write to')
        # TODO: add more formats
        self.options.add_option('separator', 'newline', 'Separator between elements',
                                list(self._SEPARATORS.keys()), True)
        self.options.add_option('format', 'plaintext', 'The format to write output in', ['plaintext', 'binary', 'sv', 'template'])
        self.options.add_option('final_newline', True, 'Whether to end the file with a newline')
        self.options.add_option('number_format', 'decimal', 'Format for numbers', ['decimal', 'hexadecimal', 'octal'])
        self.options.add_option('template_file', None, 'Template file to use when "format" is "template"')
        self.options.add_option('template_pattern', '<ACSPLOIT>',
                                'Replacement pattern in template file, marks where the payload will be copied')
        self.options.add_option('replace_first_only', False,
                                'Whether to replace only the first occurrence of template_pattern or all occurrences')

    def output(self, output_list):
        """Create file output."""
        output_path = os.path.expanduser(self.options['filename'])
        separator = output_common.get_separator(self.options['separator'], self._SEPARATORS)
        if self.options['format'] == 'binary':
            with open(output_path, 'wb') as output_file:
                self.write_binary_file(output_list, output_file)
        else:
            with open(output_path, 'w') as output_file:
                if self.options['format'] == 'plaintext':
                    self.write_plaintext_file(output_list, output_file, separator)
                elif self.options['format'] == 'sv':
                    self.write_sv_file(output_list, output_file, separator)
                elif self.options['format'] == 'template':
                    if self.options['template_file'] is None:
                        raise ValueError('Must set "template_file" to use "template" format')
                    self.write_template_file(output_list, output_file, separator, self.options['template_file'],
                                             self.options['template_pattern'])

                if self.options['final_newline'] and self.options['format'] != 'template':
                    output_file.write(os.linesep)

    def write_plaintext_file(self, output_list, output_file, separator):
        """Write plaintext payload data to output file."""
        output_file.write(separator.join([self.convert_item(item) for item in output_list]))

    def write_template_file(self, output_list, output_file, separator, template, pattern):
        output = separator.join([self.convert_item(item) for item in output_list])
        final_output = output_common.process_template(template, output, pattern, self.options['replace_first_only'])
        output_file.write(final_output)

    def write_binary_file(self, output_list, output_file):
        """Write binary payload data to output file."""
        # for a binary file, we don't want to be adding in our own lineseps
        for item in output_list:
            output_file.write(item)

    def write_sv_file(self, output_list, output_file, separator):
        """Write sv file."""
        # treat lists of lists as rows x cols
        if all(type(item) is list for item in output_list):
            # take each inner list, glue it together with the separator, then glue these together with os.linesep
            lines = [separator.join(self.convert_item(subitem) for subitem in item) for item in output_list]
            output_file.write(os.linesep.join(lines))

        else:
            output_file.write(separator.join([self.convert_item(item) for item in output_list]))

    def convert_item(self, item):
        """Convert output to hexadecimal or octal."""
        # NB: this doesn't recurse onto lists
        if type(item) is int:
            if self.options['number_format'] == 'hexadecimal':
                item = hex(item)
            elif self.options['number_format'] == 'octal':
                item = oct(item)
        return str(item)
