import os
from options import Options


class File(object):

    OUTPUT_NAME = 'file'

    def __init__(self):
        self.options = Options()
        self.options.add_option('filename', 'acsploit_output.dat', 'The name of the file to write to')
        # TODO: add more formats
        self.options.add_option('format', 'plaintext', 'The format to write output in', ['plaintext', 'csv', 'tsv'])
        self.options.add_option('final_newline', True, 'Whether to end the file with a newline')

    def output(self, output_list):
        with open(self.options['filename'], 'w') as output_file:
            if self.options['format'] == 'plaintext':
                self.write_plaintext_file(output_list, output_file)
            elif self.options['format'] == 'csv':
                self.write_sv_file(output_list, output_file, ',')
            elif self.options['format'] == 'tsv':
                self.write_sv_file(output_list, output_file, '\t')

            if self.options['final_newline']:
                output_file.write(os.linesep)

    def write_plaintext_file(self, output_list, output_file):
        output_file.write(os.linesep.join([str(item) for item in output_list]))

    def write_sv_file(self, output_list, output_file, separator):
        # treat lists of lists as rows x cols
        list_of_lists = True
        for item in output_list:
            if type(item) is not list:
                list_of_lists = False
                break

        if list_of_lists:
            # take each inner list, glue it together with the separator, then glue these together with os.linesep
            output_file.write(os.linesep.join([separator.join([str(subitem) for subitem in item])
                                               for item in output_list]))
        else:
            output_file.write(separator.join([str(item) for item in output_list]))
