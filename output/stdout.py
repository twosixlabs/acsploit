import sys
import os


class Stdout(object):

    OUTPUT_NAME = "stdout" #exploits can use this internally to whitelist/blacklist supported output formats

    def output(self, output_list):
        for element in output_list:
            sys.stdout.write(str(element))
            sys.stdout.write(os.linesep)