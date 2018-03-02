import exploits
import inspect
import cmd2
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
            values = options.get_acceptable_values(key)
            if values is not None:
                line += ' (Acceptable Values: ' + str(values) + ')'
        print indent + line


class ACsploit(cmd2.Cmd):
    intro = r"""
                             .__         .__  __
_____    ____   ____________ |  |   ____ |__|/  |_
\__  \ _/ ___\ /  ___/\____ \|  |  /  _ \|  \   __\
 / __ \\  \___ \___ \ |  |_> >  |_(  <_> )  ||  |
(____  /\___  >____  >|   __/|____/\____/|__||__|
     \/     \/     \/ |__|

"""

    prompt = color('(acsploit) ', 'blue')
    origpromptlen = len(prompt)
    options = Options()
    options.add_option('input', 'string', 'Input generator to use with exploits', ['int', 'char', 'string', 'regex'])
    options.add_option('output', 'stdout', 'Output generator to use with exploits', ['stdout', 'file'])

    currexp = None
    currinputgen = input.StringGenerator()
    curroutput = output.Stdout()
    availexps = {}

    def __init__(self):
        #delete unused commands that are baked-into cmd2
        del cmd2.Cmd.do_py
        del cmd2.Cmd.do_edit
        del cmd2.Cmd.do_load
        del cmd2.Cmd.do_shortcuts
        #del cmd2.Cmd.do_shell # we still include it to get !-style bash execution
        del cmd2.Cmd.do_pyscript
        del cmd2.Cmd.do_set
        cmd2.Cmd.abbrev = True
        self.exclude_from_help.append('do_shell')
        self.shortcuts.update({"sh": "show"}) # don't want "sh" to trigger the hidden "shell" command
        cmd2.Cmd.__init__(self)

    def init(self):
        self.availexps = self.get_exploits()

    def get_exploits(self):
        results = {}
        for loader, name, ispkg in pkgutil.walk_packages(exploits.__path__):
            m = loader.find_module(name).load_module(name)

            if not ispkg and hasattr(m, 'options') and hasattr(m, 'run'):
                exploit = m.exploit_name if hasattr(m, 'exploit_name') else name
                #TODO - if we were using "name" above, we'd require exploit contributors to have "name" be the *full* path...
                exploit = exploit.replace('.', '/')
                results[exploit] = m

        return results

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
            print_options(self.currinputgen.get_options(), describe, indent_level=2)
        if self.curroutput is not None:
            print color("\n  Output options", "green")
            print_options(self.curroutput.options, describe, indent_level=2)
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
                'string': input.StringGenerator(),
                'regex': input.RegexMatchGenerator()
            }

            if val not in input_map:
                print color("Input " + val + " does not exist.", 'red')
                return

            self.currinputgen = input_map[val]
            self.options[key] = val

        elif key == "output":
            output_map = {
                'stdout': output.Stdout(),
                'file': output.File()
            }

            if val not in output_map:
                print color("Output " + val + " does not exist.", 'red')
                return

            self.curroutput = output_map[val]
            self.options[key] = val

        elif self.currexp is not None and key in self.currexp.options.get_option_names():
            # TODO check input type is what is expected
            self.currexp.options[key] = val

        elif self.currinputgen is not None and key in self.currinputgen.get_options().get_option_names():
            # TODO check input type is what is expected
            self.currinputgen.set_option(key, val)

        elif self.curroutput is not None and key in self.curroutput.options.get_option_names():
            self.curroutput.options[key] = val

        else:
            print color("Option " + key + " does not exist.", 'red')

    def do_use(self, args):
        """Sets the current exploit. Usage: use [exploit_name]"""
        if len(args) > 0:
            self.update_exploit(args.split()[0])
        else:
            print color("Usage: use [exploit_name]", 'red')
            return

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

    history_file = '~/.acsploit.history'

    #cmdlineobj = ACsploit(hist_file=history_file) #TODO - Wait for cmd2 version 0.8.1 to be on pip for this...
    cmdlineobj = ACsploit()
    cmdlineobj.debug = True #TODO - eventually not have this
    cmdlineobj.init()
    cmdlineobj.cmdloop()
