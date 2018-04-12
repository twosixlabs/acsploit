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
import argparse

from options import Options


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


def set_option_complete(text, line, begidx, endidx, context):
    # text = line[begidx:endidx] is the word we want to complete
    # split the completed words, should either be ['set'], or ['set', <option_key>]
    split_line = line[:begidx].split()
    if len(split_line) == 1:
        return [option for option in context.get_option_names() if option.startswith(text) or '.' + text in option]

    if len(split_line) == 2:
        key = split_line[1]
        options = context.get_options(key)
        if options is not None:
            scoped_key = key.split('.')[1] if '.' in key else key
            values = options.get_acceptable_values(scoped_key)
            if values is not None:
                return [value for value in values if value.startswith(text)]

    return []


def get_exploits():
    results = {}
    for loader, name, ispkg in pkgutil.walk_packages(exploits.__path__):
        m = loader.find_module(name).load_module(name)

        if not ispkg and hasattr(m, 'options') and hasattr(m, 'run'):
            exploit = name.replace('.', '/')
            results[exploit] = m

    return results


def get_inputs():
    inputs = {}
    for obj in list(vars(input).values()):
        if hasattr(obj, 'INPUT_NAME'):
            inputs[obj.INPUT_NAME] = obj

    return inputs


def get_outputs():
    outputs = {}
    for obj in list(vars(output).values()):
        if hasattr(obj, 'OUTPUT_NAME'):
            outputs[obj.OUTPUT_NAME] = obj

    return outputs


class ACsploit(cmd2.Cmd):
    intro = r"""
                             .__         .__  __
_____    ____   ____________ |  |   ____ |__|/  |_
\__  \ _/ ___\ /  ___/\____ \|  |  /  _ \|  \   __\
 / __ \\  \___ \___ \ |  |_> >  |_(  <_> )  ||  |
(____  /\___  >____  >|   __/|____/\____/|__||__|
     \/     \/     \/ |__|

"""

    # find all inputs, outputs, exploits
    inputs = get_inputs()
    outputs = get_outputs()
    availexps = get_exploits()

    def __init__(self, hist_file):
        self.setup_cmd2(hist_file)

        # Register tab-completion functions
        self.complete_use = functools.partial(exploit_path_complete, match_against=ACsploit.availexps)
        self.complete_set = functools.partial(set_option_complete, context=self)

        self.prompt = self.make_prompt()

        self.currexp = None
        self.currexpname = ''
        self.currinput = None
        self.curroutput = None
        self.curroptions = Options()
        self.defaulted_options = []

    def setup_cmd2(self, hist_file):
        # delete unused commands that are baked-into cmd2 and set some options
        del cmd2.Cmd.do_py
        del cmd2.Cmd.do_edit
        del cmd2.Cmd.do_shortcuts
        del cmd2.Cmd.do_pyscript
        del cmd2.Cmd.do_set
        del cmd2.Cmd.do_alias
        del cmd2.Cmd.do_unalias
        cmd2.Cmd.abbrev = True
        self.allow_cli_args = False  # disable parsing of command-line args by cmd2
        self.shortcuts.update({"sh": "show"})  # don't want "sh" to trigger the hidden "shell" command

        # init cmd2 and the history file
        cmd2.Cmd.__init__(self, persistent_history_file=hist_file, persistent_history_length=200)

        # disable help on builtins
        self.exclude_from_help.append('do_shell')  # TODO: this is still in the help menu
        self.exclude_from_help.append('do_load')  # TODO: this is still in the help menu
        self.exclude_from_help.append('do_exit')  # TODO: come back to this?

    def make_prompt(self, location=None):
        prompt = '(acsploit : %s) ' % location if location is not None else '(acsploit) '
        return self.colorize(prompt, 'blue')

    # returns the names of all options within current exploit, input , and output options
    def get_option_names(self):
        # There are no options until the current exploit is set
        if self.currexp is None:
            return []

        option_names = self.curroptions.get_option_names()

        if self.currinput is not None:
            option_names += ['input.' + option for option in self.currinput.get_options().get_option_names()]

        if self.curroutput is not None:
            option_names += ['output.' + option for option in self.curroutput.options.get_option_names()]

        if self.currexp is not None:
            option_names += ['exploit.' + option for option in self.currexp.options.get_option_names()]

        return option_names

    # returns the options object containing the given key
    def get_options(self, key):
        if key in self.curroptions.get_option_names():
            return self.curroptions

        try:
            scope, scoped_key = key.split('.')
        except ValueError:
            return None

        if scope == 'input' and scoped_key in self.currinput.get_options().get_option_names():
            return self.currinput.get_options()
        elif scope == 'output' and scoped_key in self.curroutput.options.get_option_names():
            return self.curroutput.options
        elif scope == 'exploit' and scoped_key in self.currexp.options.get_option_names():
            return self.currexp.options
        else:
            return None

    def print_options(self, options, describe=False, indent_level=0):
        indent = '  ' * indent_level
        for option in options.get_option_names():
            line = self.colorize(option + ': ', 'green') + str(options[option])
            if describe:
                line += ' (' + options.get_description(option) + ')'
                values = options.get_acceptable_values(option)
                if values is not None:
                    line += ' (Acceptable Values: ' + str(values) + ')'
            print(indent + line)

    def do_info(self, args):
        """Displays the description of the set exploit."""
        if self.currexp is None:
            print(self.colorize('No exploit set; nothing to describe. See options.', 'red'))
        else:
            print(self.colorize('\n  ' + self.currexp.DESCRIPTION + '\n', 'green'))

    def do_options(self, args):
        """Displays current options, more of which appear after 'input' and 'exploit' are set. Use 'options describe' to see descriptions of each."""
        if args not in ['', 'describe']:
            print(self.colorize('Unsupported argument to options', 'red'))
            self.do_help('options')
            return

        if self.currexp is None:
            print(self.colorize("No options available. Select an exploit with the 'use' command", "cyan"))
            return

        describe = args == 'describe'

        print()
        self.print_options(self.curroptions, describe, indent_level=1)
        if self.currinput is not None:
            print(self.colorize("\n  Input options", 'green'))
            self.print_options(self.currinput.get_options(), describe, indent_level=2)
        if self.curroutput is not None:
            print(self.colorize("\n  Output options", "green"))
            self.print_options(self.curroutput.options, describe, indent_level=2)
        if self.currexp is not None:
            print(self.colorize("\n  Exploit options", 'green'))
            self.print_options(self.currexp.options, describe, indent_level=2)
        print()

    def do_exit(self, args):
        self._should_quit = True
        return self._STOP_AND_EXIT

    def do_set(self, args):
        """Sets an option. Usage: set [option_name] [value]"""
        try:
            key, value = args.split(maxsplit=1)
        except ValueError:
            print("Usage: set [option_name] [value]")
            return

        error_msg = self.colorize('No options set', 'cyan')

        if key not in self.get_option_names():
            print(self.colorize('Option {} does not exist'.format(key), 'red'))
            print(error_msg)
            return

        options = self.get_options(key)  # This call should always succeed due to the check above
        scoped_key = key.split('.')[1] if '.' in key else key
        values = options.get_acceptable_values(scoped_key)
        if values is not None and value not in values:
            print(self.colorize('{} is not an acceptable option for {}'.format(value, key), 'red'))
            print(error_msg)
            return

        if key in self.defaulted_options:
            confirm_prompt = 'Changing this option may result in degraded exploit performance or failure.'
            confirmation = __builtins__.input(self.colorize(confirm_prompt + '\nDo you want to continue? [y|N] ',
                                                            'yellow'))
            if confirmation.lower() in ['yes', 'y']:
                self.defaulted_options.remove(key)  # only warn the first time overwriting the defaulted option
            else:
                print(error_msg)
                return

        if key == 'input':
            self.currinput = ACsploit.inputs[value]()
        elif key == 'output':
            self.curroutput = ACsploit.outputs[value]()

        options[scoped_key] = value
        print(self.colorize('%s => %s' % (key, value), 'cyan'))

    def do_use(self, args):
        """Sets the current exploit. Usage: use [exploit_name]"""
        if len(args) > 0:
            self.update_exploit(args.split()[0])
        else:
            print(self.colorize("Usage: use [exploit_name]", 'red'))
            return

    def do_show(self, args):
        """Lists all available exploits."""
        print(self.colorize("\nAvailable exploits:", 'green'))
        for key in sorted(ACsploit.availexps):
            print(self.colorize("    " + key, 'green'))
        print("")

    def update_exploit(self, expname):
        if expname not in ACsploit.availexps:
            print((self.colorize("Exploit " + expname + " does not exist.", 'red')))
            return

        # save current input/output and  to current exploit in private variables
        # this allows restoration of the current settings f the exploit is used again
        if self.currexp is not None:
            self.currexp._ACsploit_exploit_settings = {
                'input': self.currinput,
                'output': self.curroutput,
                'options': self.curroptions,
                'defaulted_options': self.defaulted_options,
            }

        # set the new exploit; restore previous input/output
        self.currexpname = expname
        self.currexp = ACsploit.availexps[expname]
        self.prompt = self.make_prompt(expname)

        if hasattr(self.currexp, '_ACsploit_exploit_settings'):
            self.currinput = self.currexp._ACsploit_exploit_settings['input']
            self.curroutput = self.currexp._ACsploit_exploit_settings['output']
            self.curroptions = self.currexp._ACsploit_exploit_settings['options']
            self.defaulted_options = self.currexp._ACsploit_exploit_settings['defaulted_options']

        else:
            input_desc = 'Input generator to use with exploits'
            output_desc = 'Output generator to use with exploits'
            self.defaulted_options = []
            self.curroptions = Options()

            # set default input and output for new exploit, if any
            if hasattr(self.currexp, 'NO_INPUT') and self.currexp.NO_INPUT:
                self.currinput = None
            elif hasattr(self.currexp, 'DEFAULT_INPUT'):
                self.curroptions.add_option('input', self.currexp.DEFAULT_INPUT, input_desc,
                                            list(ACsploit.inputs.keys()))
                self.defaulted_options.append('input')
                self.currinput = ACsploit.inputs[self.currexp.DEFAULT_INPUT]()
            else:
                # We set string as the default input, but do not warn if this option is changed
                self.curroptions.add_option('input', 'string', input_desc, list(ACsploit.inputs.keys()))
                self.currinput = ACsploit.inputs['string']()

            if hasattr(self.currexp, 'DEFAULT_OUTPUT'):
                self.curroptions.add_option('output', self.currexp.DEFAULT_OUTPUT, output_desc,
                                            list(ACsploit.outputs.keys()))
                self.defaulted_options.append('output')
                self.curroutput = ACsploit.outputs[self.currexp.DEFAULT_OUTPUT]()
            else:
                # We set stdout as the default output, but do not warn if this option is changed
                self.curroptions.add_option('output', 'stdout', output_desc, list(ACsploit.outputs.keys()))
                self.curroutput = ACsploit.outputs['stdout']()

            # set defaults for input and output settings for new exploit, if any
            if hasattr(self.currexp, 'DEFAULT_INPUT_OPTIONS'):
                for option, value in self.currexp.DEFAULT_INPUT_OPTIONS.items():
                    self.currinput.set_option(option, value)
                    self.defaulted_options.append('input.%s' % option)
            if hasattr(self.currexp, 'DEFAULT_OUTPUT_OPTIONS'):
                for option, value in self.currexp.DEFAULT_OUTPUT_OPTIONS.items():
                    self.curroutput.options.set_value(option, value)
                    self.defaulted_options.append('output.%s' % option)

    def do_run(self, args):
        """Runs exploit with given options."""
        if self.currexp is None:
            print(self.colorize("No exploit set; nothing to do. See options.", 'red'))
        else:
            if self.currinput is None:
                self.currexp.run(self.curroutput)
            else:
                self.currexp.run(self.currinput, self.curroutput)


if __name__ == '__main__':

    history_file = os.path.join(os.path.expanduser("~"), ".acsploit_history")
    if not os.path.isfile(history_file):
        with open(history_file, 'w') as f:
            f.write('_HiStOrY_V2_\n\n')

    parser = argparse.ArgumentParser(description='A tool for generating worst-case inputs for algorithms')
    parser.add_argument('--debug', action='store_true', help='show debug stack traces')

    args = parser.parse_args()

    cmdlineobj = ACsploit(hist_file=history_file)
    cmdlineobj.debug = args.debug
    cmdlineobj.cmdloop()
