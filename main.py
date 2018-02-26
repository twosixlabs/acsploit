import exploits
import inspect
import cmd
import input
import output
import os
import sys
import logging
import pkgutil

from options import Options


def color(s, c):
    endc = '\033[0m'
    colors = {
        'blue': '\033[94m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'red': '\033[91m'
    }

    if c not in colors:
        return s

    return colors[c] + s + endc


def print_options(options, describe=False, indent_level=0):
    indent = '  ' * indent_level
    for key in options.get_option_names():
        line = color(str(key) + ': ', 'green') + str(options[key])
        if describe:
            line += ' (' + options.get_description(key) + ')'
        print indent + line


class CmdLine(cmd.Cmd):
    intro = "\n**********ACsploit**********\n"
    prompt = color('(acsploit) ', 'blue')
    origpromptlen = len(prompt)
    options = Options()
    options.add_option('input', 'string', 'One of int, char, string')
    options.add_option('output', 'stdout', 'file', 'TBD')

    currexp = None
    currinputgen = input.StringGenerator()
    curroutput = output.Stdout()
    availexps = {}
    
    def init(self):
        self.availexps = self.get_exploits()

    def get_exploits(self):
        results = {}
        for loader, name, ispkg in pkgutil.walk_packages(exploits.__path__):
            m = loader.find_module(name).load_module(name)

            if not ispkg and hasattr(m, 'options') and hasattr(m, 'run'):
                exploit = m.exploit_name if hasattr(m, 'exploit_name') else name
                results[exploit] = m

        return results

    def do_exit(self, args):
        """Exits ACsploit."""
        return True

    def do_options(self, args):
        """Displays current options, more of which appear after 'input' and 'exploit' are set. Use 'options describe' to see descriptions of each."""
        if args not in ['', 'describe']:
            print color('Unsupported argument to options', 'red')
            self.do_help('options')
            return

        describe = args == 'describe'

        print
        print_options(self.options, describe, indent_level=1)
        if self.currinputgen is not None:
            print color("\n  Input options", 'green')
            print_options(self.currinputgen.options, describe, indent_level=2)
        if self.currexp is not None:
            print color("\n  Exploit options", 'green')
            print_options(self.currexp.options, describe, indent_level=2)
        print

    def do_set(self, args):
        """Sets an option. Usage: set [option_name] [value]"""
        try:
            key, val = args.split(' ', 1)
        except ValueError:
            print "Usage: set [option_name] [value]"
            return

        if key == "input":
            input_map = {
                'int': input.IntGenerator(),
                'char': input.CharGenerator(),
                'string': input.StringGenerator()
            }

            if val not in input_map:
                print color("Input " + val + " does not exist.", 'red')
                return

            self.currinputgen = input_map[val]
            self.options[key] = val

        elif key == "output":
            #TODO
            print color("Changing output type is not yet supported", 'red')

        elif self.currexp is not None and key in self.currexp.options.get_option_names():
            # TODO check input type is what is expected
            self.currexp.options[key] = val

        elif self.currinputgen is not None and key in self.currinputgen.options.get_option_names():
            # TODO check input type is what is expected
            self.currinputgen.options[key] = val

        else:
            print color("Option " + key + " does not exist.", 'red')

    def do_use(self, args):
        """Sets the current exploit. Usage: use [exploit_name]"""
        self.update_exploit(args.split()[0])

    def do_show(self, args):
        """Lists all available exploits."""
        print color("\nAvailable exploits:", 'green')
        for key in sorted(self.availexps):
            print color("    " + key, 'green')
        print("")

    def update_exploit(self, expname):
        if expname in self.availexps:
            self.prompt = self.prompt[:self.origpromptlen - 6] + " : "+expname+") " + '\033[0m'
            self.currexp = self.availexps[expname]
        else:
            print(color("Exploit " + expname + " does not exist.", 'red'))
            pass

    def do_run(self, args):
        """Runs exploit with given options."""
        if self.currexp is None:
            print color("No exploit set, nothing to do. See options.", 'red')
        elif self.currinputgen is None:
            print color("No input specified, nothing to do. See options.", 'red')
        else:
            self.currexp.run(self.currinputgen, self.curroutput)


if __name__ == '__main__':
    cmdlineobj = CmdLine()
    cmdlineobj.init()
    cmdlineobj.cmdloop()
