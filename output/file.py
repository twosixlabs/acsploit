import os
from options import Options


class File(object):

    OUTPUT_NAME = 'file'

    def __init__(self):
        self.options = Options()
        self.options.add_option('filename', 'acsploit_output.txt', 'The name of the file to write to')

    def output(self, output_list):
        with open(self.options['filename'], 'w') as output_file:
            for item in output_list:
                output_file.write(str(item))
                output_file.write(os.linesep)
