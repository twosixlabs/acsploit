import sys
import os

class Stdout(object):

    def output(self, output_list):
        for element in output_list:
            sys.stdout.write(element)
            sys.stdout.write(os.linesep)