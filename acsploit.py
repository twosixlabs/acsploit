#! /usr/bin/env python

import sys
if sys.hexversion < 0x03050000:
    raise Exception('ACsploit requires Python 3.5 or higher')

import exploits
import cmd2
import input
import output
import os
import pkgutil
import functools

from cmd2 import index_based_complete
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
    for option in options.get_option_names():
        line = color(option + ': ', 'green') + str(options[option])
        if describe:
            line += ' (' + options.get_description(option) + ')'
            values = options.get_acceptable_values(option)
            if values is not None:
                line += ' (Acceptable Values: ' + str(values) + ')'
        print(indent + line)


def exploit_path_complete(text, line, begidx, endidx, match_against):
    split_line = line.split(maxsplit=1)
    full_text = split_line[1] if len(split_line) == 2 else ''
    match_begidx = len(full_text) - len(text)
    result_set = set()
    for match in match_against:
        if match.startswith(full_text):
            match_endidx = match.find('/', match_begidx)
            if match_endidx != -1:
                result_set.add(match[match_begidx:match_endidx+1])
            else:
                result_set.add(match[match_begidx:])

    return sorted(result_set)


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

    # find all inputs imported in input
    inputs = {}
    for obj in list(vars(input).values()):
        try:
            inputs[obj.INPUT_NAME] = obj
        except AttributeError:
            continue
    input_options = list(inputs.keys())
    input_options.append('none')  # add in None as an option so we don't get errors when not using an input
    options.add_option('input', 'string', 'Input generator to use with exploits', input_options)

    # find all outputs imported in output
    outputs = {}
    for obj in list(vars(output).values()):
        try:
            outputs[obj.OUTPUT_NAME] = obj
        except AttributeError:
            continue
    options.add_option('output', 'stdout', 'Output generator to use with exploits', list(outputs.keys()))

    currexp = None
    currinput = None
    curroutput = None

    def __init__(self, hist_file):
        # delete unused commands that are baked-into cmd2
        del cmd2.Cmd.do_py
        del cmd2.Cmd.do_edit
        del cmd2.Cmd.do_shortcuts
        # del cmd2.Cmd.do_shell # we still include it to get !-style bash execution
        del cmd2.Cmd.do_pyscript
        del cmd2.Cmd.do_set
        del cmd2.Cmd.do_alias
        del cmd2.Cmd.do_unalias
        cmd2.Cmd.abbrev = True
        self.shortcuts.update({"sh": "show"})  # don't want "sh" to trigger the hidden "shell" command
        cmd2.Cmd.__init__(self, persistent_history_file=hist_file, persistent_history_length=200)
        self.exclude_from_help.append('do_shell')
        self.exclude_from_help.append('do_load')
        self.exclude_from_help.append('do_exit')
        self.availexps = self.get_exploits()
        self.complete_use = functools.partial(exploit_path_complete, match_against=self.availexps)
        self.option_list = []
        self.complete_set = functools.partial(index_based_complete, index_dict={1: self.option_list})
        self.currexp = None
        self.currexpname = None

    def get_exploits(self):
        results = {}
        for loader, name, ispkg in pkgutil.walk_packages(exploits.__path__):
            m = loader.find_module(name).load_module(name)

            if not ispkg and hasattr(m, 'options') and hasattr(m, 'run'):
                exploit = m.exploit_name if hasattr(m, 'exploit_name') else name
                # TODO - if we used "name" above, we'd require exploit contributors to have "name" be the *full* path...
                exploit = exploit.replace('.', '/')
                results[exploit] = m

        return results

    # Update self.option_list in place so that complete_set will always have the current set of options
    def update_options(self, old_options, new_options, scope):
        for old_option in old_options:
            self.option_list.remove(scope + '.' + old_option)
        for new_option in new_options:
            self.option_list.append(scope + '.' + new_option)

    # TODO: if someone could figure out a good way to combine the following two functions
    # TODO:  that's not unreadably abstract, that'd be cool
    def update_input(self, new_input):
        old_options = self.currinput.get_options().get_option_names() if self.currinput is not None else []
        if new_input is not None:
            self.currinput = ACsploit.inputs[new_input]()
            self.options['input'] = new_input
        else:
            self.currinput = None
            self.options['input'] = 'none'
        new_options = self.currinput.get_options().get_option_names() if self.currinput is not None else []
        self.update_options(old_options, new_options, scope='input')

    def update_output(self, new_output):
        old_options = self.curroutput.options.get_option_names() if self.curroutput is not None else []
        self.curroutput = ACsploit.outputs[new_output]()
        self.options['output'] = new_output
        new_options = self.curroutput.options.get_option_names()
        self.update_options(old_options, new_options, scope='output')

    def do_info(self, args):
        """Displays the description of the set exploit."""
        if self.currexp is None:
            print(color('No exploit set; nothing to describe. See options.', 'red'))
        else:
            print(color('\n  ' + self.currexp.DESCRIPTION + '\n', 'green'))

    def do_options(self, args):
        """Displays current options, more of which appear after 'input' and 'exploit' are set. Use 'options describe' to see descriptions of each."""
        if args not in ['', 'describe']:
            print(color('Unsupported argument to options', 'red'))
            self.do_help('options')
            return

        describe = args == 'describe'

        print()
        # TODO: suppress printing of input here if None
        print_options(self.options, describe, indent_level=1)
        if self.currinput is not None:
            print(color("\n  Input options", 'green'))
            print_options(self.currinput.get_options(), describe, indent_level=2)
        if self.curroutput is not None:
            print(color("\n  Output options", "green"))
            print_options(self.curroutput.options, describe, indent_level=2)
        if self.currexp is not None:
            print(color("\n  Exploit options", 'green'))
            print_options(self.currexp.options, describe, indent_level=2)
        print()

    def do_exit(self,args):
        self._should_quit = True
        return self._STOP_AND_EXIT

    def do_set(self, args):
        """Sets an option. Usage: set [option_name] [value]"""
        # TODO: warning on default overwrite

        try:
            key, val = args.split(' ', 1)
        except ValueError:
            print("Usage: set [option_name] [value]")
            return

        if key == "input":
            if val not in ACsploit.inputs:
                print(color("Input " + val + " does not exist.", 'red'))
                return
            self.update_input(val)

        elif key == "output":
            if val not in ACsploit.outputs:
                print(color("Output " + val + " does not exist.", 'red'))
                return
            self.update_output(val)

        elif '.' in key:
            scope, scoped_key = key.split('.', 1)
            if scope == 'input':
                if self.currinput is None:
                    print(color('No input set; cannot set input options', 'red'))
                elif scoped_key in self.currinput.get_options().get_option_names():
                    self.currinput.set_option(scoped_key, val)
                else:
                    print(color("Option " + scoped_key + " does not exist for input " + self.currinput.INPUT_NAME,
                                'red'))
            elif scope == 'output':
                if self.curroutput is None:
                    print(color('No output set; cannot set output options', 'red'))
                elif scoped_key in self.curroutput.options.get_option_names():
                    self.curroutput.options[scoped_key] = val
                else:
                    print(color("Option " + scoped_key + " does not exist for output " + self.curroutput.OUTPUT_NAME,
                                'red'))
            elif scope == 'exploit':
                if self.currexp is None:
                    print(color('No exploit set; cannot set exploit options', 'red'))
                elif scoped_key in self.currexp.options.get_option_names():
                    self.currexp.options[scoped_key] = val
                else:
                    print(color("Option " + scoped_key + " does not exist for exploit " + self.currexpname, 'red'))

        elif self.currexp is not None and key in self.currexp.options.get_option_names():
            self.currexp.options[key] = val

        elif self.currinput is not None and key in self.currinput.get_options().get_option_names():
            self.currinput.set_option(key, val)

        elif self.curroutput is not None and key in self.curroutput.options.get_option_names():
            self.curroutput.options[key] = val

        else:
            print(color("Option " + key + " does not exist.", 'red'))

    def do_use(self, args):
        """Sets the current exploit. Usage: use [exploit_name]"""
        if len(args) > 0:
            self.update_exploit(args.split()[0])
        else:
            print(color("Usage: use [exploit_name]", 'red'))
            return

    def do_show(self, args):
        """Lists all available exploits."""
        print(color("\nAvailable exploits:", 'green'))
        for key in sorted(self.availexps):
            print(color("    " + key, 'green'))
        print("")

    def update_exploit(self, expname):
        if expname not in self.availexps:
            print((color("Exploit " + expname + " does not exist.", 'red')))
            return

        self.prompt = self.prompt[:self.origpromptlen - 6] + " : " + expname + ") " + '\033[0m'
        self.currexpname = expname

        old_options = [] if self.currexp is None else self.currexp.options.get_option_names()

        self.currexp = self.availexps[expname]

        new_options = self.currexp.options.get_option_names()
        self.update_options(old_options, new_options, scope='exploit')

        # set default input and output for new exploit, if any
        if hasattr(self.currexp, 'NO_INPUT') and self.currexp.NO_INPUT:
            self.update_input(None)
        else:
            # thus we have an invariant that self.currexp.NO_INPUT always exists!
            self.currexp.NO_INPUT = False

        if hasattr(self.currexp, 'DEFAULT_INPUT') and self.currexp.DEFAULT_INPUT:
            # TODO: try to validate this or error handle if it's bad?
            self.update_input(self.currexp.DEFAULT_INPUT)
        if hasattr(self.currexp, 'DEFAULT_OUTPUT') and self.currexp.DEFAULT_OUTPUT:
            self.update_output(self.currexp.DEFAULT_OUTPUT)

        # set defaults for input and output settings for new exploit, if any
        if hasattr(self.currexp, 'DEFAULT_INPUT_OPTIONS'):
            for option, value in self.currexp.DEFAULT_INPUT_OPTIONS.items():
                self.currinput.set_option(option, value)
        if hasattr(self.currexp, 'DEFAULT_OUTPUT_OPTIONS'):
            for option, value in self.currexp.DEFAULT_OUTPUT_OPTIONS.items():
                self.curroutput.options.set_value(option, value)

    def do_run(self, args):
        """Runs exploit with given options."""
        if self.currexp is None:
            print(color("No exploit set; nothing to do. See options.", 'red'))
        elif not self.currexp.NO_INPUT and self.currinput is None:  # only warn about lack of input if exploit cares
            print(color("No input specified; nothing to do. See options.", 'red'))
        else:
            if self.currexp.NO_INPUT:
                self.currexp.run(self.curroutput)
            else:
                self.currexp.run(self.currinput, self.curroutput)


if __name__ == '__main__':

    history_file = os.path.join(os.path.expanduser("~"), ".acsploit_history")
    if not os.path.isfile(history_file):
        with open(history_file, 'w') as f:
            f.write('_HiStOrY_V2_\n\n')

    cmdlineobj = ACsploit(hist_file=history_file)
    cmdlineobj.debug = True  # TODO - eventually not have this or do it based on command-line flag?
    cmdlineobj.cmdloop()
