import sys
import os
from options import Options


class Stdout(object):

    OUTPUT_NAME = "stdout" #exploits can use this internally to whitelist/blacklist supported output formats
    #TODO - have an option for decimal, hex, etc

    def __init__(self):
        self.options = Options()

    def output(self, output_list):
        for element in output_list:
            sys.stdout.write(str(element))
            sys.stdout.write(os.linesep)
