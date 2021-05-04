# this is necessary so python2 doesn't throw a syntax error over the definition of eprint()
#  and can thus pass through syntax checking to actually running this file, at which point
#  it will properly bail out on the system version check
from __future__ import print_function

import sys
if sys.hexversion < 0x03050000:
    raise Exception('ACsploit requires Python 3.5 or higher')

import acsploit.exploits
import acsploit.input
import acsploit.output
import cmd2
import os
import pkgutil
import functools
import argparse
import importlib
import time
from colorama import Fore

from acsploit.options import Options

FG_COLORS = {
    'black': Fore.BLACK,
    'red': Fore.RED,
    'green': Fore.GREEN,
    'yellow': Fore.YELLOW,
    'blue': Fore.BLUE,
    'magenta': Fore.MAGENTA,
    'cyan': Fore.CYAN,
    'white': Fore.WHITE,
}


def colorize(string, colorname):
    return FG_COLORS[colorname] + string + Fore.RESET


def eprint(*args, **kwargs):
    """Print helper to stderr."""
    print(*args, file=sys.stderr, **kwargs)


def get_exploits():
    """Find and load all exploit modules."""
    results = {}
    for loader, name, ispkg in pkgutil.walk_packages(acsploit.exploits.__path__):
        m = loader.find_module(name).load_module(name)

        if not ispkg and hasattr(m, 'options') and hasattr(m, 'run'):
            exploit = name.replace('.', '/')
            results[exploit] = m

    return results


def get_inputs():
    """Get all input modules."""
    inputs = {}
    for obj in vars(acsploit.input).values():
        if hasattr(obj, 'INPUT_NAME'):
            inputs[obj.INPUT_NAME] = obj

    return inputs


def get_outputs():
    """Get all output modules."""
    outputs = {}
    for obj in vars(acsploit.output).values():
        if hasattr(obj, 'OUTPUT_NAME'):
            outputs[obj.OUTPUT_NAME] = obj

    return outputs


class ACsploit(cmd2.Cmd):
    """An interactive command-line utility to generate worst-case inputs to commonly used algorithms."""

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
    exploits = get_exploits()

    def __init__(self, hist_file):
        """Initialization and setup of ACsploit."""
        self.setup_cmd2(hist_file)

        self.prompt = self.make_prompt()

        self.exploit = None
        self.exploit_name = ''
        self.input = None
        self.output = None
        self.options = Options()
        self.defaulted_options = []

        self.script_mode = False
        self.shortcuts = cmd2.DEFAULT_SHORTCUTS

    def setup_cmd2(self, hist_file):
        """"Set up interactive command line interface."""
        # delete unused commands that are baked-into cmd2 and set some options
        del cmd2.Cmd.do_py
        del cmd2.Cmd.do_edit
        del cmd2.Cmd.do_shortcuts
        del cmd2.Cmd.do_run_pyscript
        del cmd2.Cmd.do_set
        del cmd2.Cmd.do_run_script
        cmd2.Cmd.abbrev = True
        self.allow_cli_args = False  # disable parsing of command-line args by cmd2
        self.allow_redirection = False  # disable redirection to enable right shift (>>) in custom_hash to work
        self.redirector = '\xff'  # disable redirection in the parser as well

        # init cmd2 and the history file
        cmd2.Cmd.__init__(self, persistent_history_file=hist_file, persistent_history_length=200)

        # disable help on builtins
        self.hidden_commands.append('shell')
        self.hidden_commands.append('exit')

    def make_prompt(self, location=None):
        """Create the command line prompt."""
        prompt = '(acsploit : %s) ' % location if location is not None else '(acsploit) '
        return colorize(prompt, "blue")

    def complete_set(self, text, line, begidx, endidx):
        """Provide tab completion for the "set" option."""
        # text = line[begidx:endidx] is the word we want to complete
        # split the completed words, should either be ['set'], or ['set', <option_key>]
        split_line = line[:begidx].split()
        if len(split_line) == 1:
            return [option for option in self.get_option_names() if option.startswith(text) or '.' + text in option]

        if len(split_line) == 2:
            key = split_line[1]
            options = self.get_options(key)
            if options is not None:
                scoped_key = key.split('.')[1] if '.' in key else key
                values = options.get_acceptable_values(scoped_key)
                if values is not None:
                    return [value for value in values if value.startswith(text)]

        return []

    def complete_use(self, text, line, begidx, endidx):
        """Provide tab completion for the "use" option."""
        return self.delimiter_complete(text, line, begidx, endidx, ACsploit.exploits, '/')

    def get_option_names(self):
        """Returns the names of all options within current exploit, input , and output options."""
        # There are no options until the current exploit is set
        if self.exploit is None:
            return []

        option_names = self.options.get_option_names()

        if self.input is not None:
            option_names += ['input.' + option for option in self.input.options.get_option_names()]

        if self.output is not None:
            option_names += ['output.' + option for option in self.output.options.get_option_names()]

        if self.exploit is not None:
            option_names += ['exploit.' + option for option in self.exploit.options.get_option_names()]

        return option_names

    def get_options(self, key):
        """Returns the options object containing the given key."""
        if key in self.options.get_option_names():
            return self.options

        try:
            scope, scoped_key = key.split('.')
        except ValueError:
            return None

        if scope == 'input' and scoped_key in self.input.options.get_option_names():
            return self.input.options
        elif scope == 'output' and scoped_key in self.output.options.get_option_names():
            return self.output.options
        elif scope == 'exploit' and scoped_key in self.exploit.options.get_option_names():
            return self.exploit.options
        else:
            return None

    def print_options(self, options, describe=False, indent_level=0):
        """Print available options and current values."""
        indent = '  ' * indent_level
        for option in options.get_option_names():
            line = colorize(option + ': ', 'green') + str(options[option])
            if describe:
                line += ' (' + options.get_description(option) + ')'
                values = options.get_acceptable_values(option)
                if values is not None:
                    line += ' (Acceptable Values: ' + str(values) + ')'
            eprint(indent + line)

    def fuzzy_equals(self, lhs, rhs):
        """Type-coerce to the type of rhs and then compare, Returns True if equals."""
        t = type(rhs)
        if t is bool:  # special case bool because bool() treats all strings as True
            return rhs is (lhs in Options.TRUE_VALUES)
        try:
            if rhs is None:
                return lhs is None
            return t(lhs) == rhs
        except ValueError:
            return False

    def do_info(self, args):
        """Displays the description of the selected exploit."""
        if self.exploit is None:
            eprint(colorize('No exploit set; nothing to describe. Select an exploit with the \'use\' command',
                                 'cyan'))
        else:
            eprint(colorize('\n  ' + self.exploit.DESCRIPTION + '\n', 'green'))

    def do_options(self, args):
        """Displays options for the selected exploit. Use 'options describe' to see descriptions"""
        if args not in ['', 'describe']:
            eprint(colorize('Unsupported argument to options', 'red'))
            self.do_help('options')
            return

        if self.exploit is None:
            eprint(colorize('No exploit set; no options to show. Select an exploit with the \'use\' command',
                                 'cyan'))
            return

        describe = args == 'describe'

        eprint()
        self.print_options(self.options, describe, indent_level=1)
        if self.input is not None:
            eprint(colorize('\n  Input options', 'green'))
            self.print_options(self.input.options, describe, indent_level=2)
        if self.output is not None:
            eprint(colorize('\n  Output options', 'green'))
            self.print_options(self.output.options, describe, indent_level=2)
        if self.exploit is not None:
            eprint(colorize('\n  Exploit options', 'green'))
            self.print_options(self.exploit.options, describe, indent_level=2)
        eprint()

    def do_exit(self, args):
        """Exit ACsploit."""
        self._should_quit = True
        return self._STOP_AND_EXIT

    def do_set(self, args):
        """Sets an option. Usage: set [option_name] [value]"""
        try:
            key, value = args.split(maxsplit=1)
        except ValueError:
            eprint('Usage: set [option_name] [value]')
            return

        no_option_msg = colorize('No option set', 'cyan')

        if key == 'debug':
            if value.lower() == 'true':
                self.debug = True
                eprint(colorize('debug => true', 'cyan'))
            elif value.lower() == 'false':
                self.debug = False
                eprint(colorize('debug => false', 'cyan'))
            else:
                eprint(colorize('{} is not an acceptable value for option {}'.format(value, key), 'red'))
                eprint(no_option_msg)
            return

        if key not in self.get_option_names():
            eprint(colorize('Option {} does not exist'.format(key), 'red'))
            eprint(no_option_msg)
            return

        options = self.get_options(key)  # this call should always succeed due to the check above
        scoped_key = key.split('.')[1] if '.' in key else key
        if not options.is_acceptable_value(scoped_key, value):
            if options.supports_custom(scoped_key) and value == 'custom':
                eprint(colorize('value must be specified after \"custom\"', 'red'))
            else:
                eprint(colorize('{} is not an acceptable value for option {}'.format(value, key), 'red'))
            eprint(no_option_msg)
            return

        if self.fuzzy_equals(value, options[scoped_key]):
            eprint(colorize('Option {} is already set to {}'.format(key, value), 'cyan'))
            return

        if key in self.defaulted_options:
            if self.script_mode:  # in script mode, warn and continue
                eprint(colorize('The following change may result in degraded exploit performance or failure',
                                     'yellow'))
                self.defaulted_options.remove(key)  # only warn the first time overwriting the defaulted option
            else:  # in interactive mode, prompt for confirmation
                confirm_prompt = 'Changing this option may result in degraded exploit performance or failure'
                confirmation = __builtins__.input(colorize(confirm_prompt + '\nDo you want to continue? [y|N] ',
                                                                'yellow'))
                if confirmation.lower() in ['yes', 'y']:
                    self.defaulted_options.remove(key)  # only warn the first time overwriting the defaulted option
                else:
                    eprint(no_option_msg)
                    return

        if key == 'input':
            self.input = ACsploit.inputs[value]()
        elif key == 'output':
            self.output = ACsploit.outputs[value]()

        options[scoped_key] = value
        eprint(colorize('%s => %s' % (key, value), 'cyan'))

    def do_reset(self, args):
        """Resets the current exploit to default options"""
        if self.exploit is None:
            eprint(colorize('No exploit set; nothing to reset. Select an exploit with the \'use\' command',
                                 'cyan'))
            return

        # delete the stored settings and reset the options in the current module
        if hasattr(self.exploit, '_ACsploit_exploit_settings'):
            del self.exploit._ACsploit_exploit_settings

        importlib.reload(self.exploit)  # we need to do this to reset currexp.options back to original values

        self.exploit = None
        self.update_exploit(self.exploit_name)

    def do_use(self, args):
        """Sets the current exploit. Usage: use [exploit_name]"""
        if len(args) > 0:
            self.update_exploit(args.split()[0])
        else:
            eprint(colorize('Usage: use [exploit_name]', 'red'))
            return

    def do_show(self, args):
        """Lists all available exploits."""
        eprint(colorize('\nAvailable exploits:', 'green'))
        for key in sorted(ACsploit.exploits):
            eprint(colorize('    ' + key, 'green'))
        eprint()

    def do_clear(self, args):
        """Clears the screen"""
        # 'cls' on windows, otherwise 'clear'
        os.system('cls' if os.name == 'nt' else 'clear')

    def update_exploit(self, exploit_name):
        """Sets the exploit name as the current exploit and restores saved settings or sets default values."""
        if exploit_name not in ACsploit.exploits:
            eprint((colorize('Exploit ' + exploit_name + ' does not exist', 'red')))
            return

        # save current input/output and  to current exploit in private variables
        # this allows restoration of the current settings if the exploit is used again
        if self.exploit is not None:
            self.exploit._ACsploit_exploit_settings = {
                'input': self.input,
                'output': self.output,
                'options': self.options,
                'defaulted_options': self.defaulted_options,
            }

        # set the new exploit; restore previous input/output
        self.exploit_name = exploit_name
        self.exploit = ACsploit.exploits[exploit_name]
        self.prompt = self.make_prompt(exploit_name)

        eprint(colorize('exploit => %s' % exploit_name, 'cyan'))

        if hasattr(self.exploit, '_ACsploit_exploit_settings'):
            self.input = self.exploit._ACsploit_exploit_settings['input']
            self.output = self.exploit._ACsploit_exploit_settings['output']
            self.options = self.exploit._ACsploit_exploit_settings['options']
            self.defaulted_options = self.exploit._ACsploit_exploit_settings['defaulted_options']

        else:
            input_desc = 'Input generator to use with exploits'
            output_desc = 'Output generator to use with exploits'
            self.defaulted_options = []
            self.options = Options()

            # set default input and output for new exploit, if any
            if hasattr(self.exploit, 'NO_INPUT') and self.exploit.NO_INPUT:
                self.input = None
            elif hasattr(self.exploit, 'DEFAULT_INPUT'):
                self.options.add_option('input', self.exploit.DEFAULT_INPUT, input_desc,
                                        list(ACsploit.inputs.keys()))
                self.defaulted_options.append('input')
                self.input = ACsploit.inputs[self.exploit.DEFAULT_INPUT]()
            else:
                # We set string as the default input, but do not warn if this option is changed
                self.options.add_option('input', 'string', input_desc, list(ACsploit.inputs.keys()))
                self.input = ACsploit.inputs['string']()

            if hasattr(self.exploit, 'NO_OUTPUT') and self.exploit.NO_OUTPUT:
                self.output = None
            elif hasattr(self.exploit, 'DEFAULT_OUTPUT'):
                self.options.add_option('output', self.exploit.DEFAULT_OUTPUT, output_desc,
                                        list(ACsploit.outputs.keys()))
                self.defaulted_options.append('output')
                self.output = ACsploit.outputs[self.exploit.DEFAULT_OUTPUT]()
            else:
                # We set stdout as the default output, but do not warn if this option is changed
                self.options.add_option('output', 'stdout', output_desc, list(ACsploit.outputs.keys()))
                self.output = ACsploit.outputs['stdout']()

            # set defaults for input and output settings for new exploit, if any
            if hasattr(self.exploit, 'DEFAULT_INPUT_OPTIONS'):
                for option, value in self.exploit.DEFAULT_INPUT_OPTIONS.items():
                    self.input.set_option(option, value)
                    self.defaulted_options.append('input.%s' % option)
            if hasattr(self.exploit, 'DEFAULT_OUTPUT_OPTIONS'):
                for option, value in self.exploit.DEFAULT_OUTPUT_OPTIONS.items():
                    self.output.options.set_value(option, value)
                    self.defaulted_options.append('output.%s' % option)

    def do_run(self, args):
        """Runs the current exploit"""
        if self.exploit is None:
            eprint(colorize('No exploit set; nothing to do. Select an exploit with the \'use\' command', 'cyan'))
        else:
            eprint(colorize('Running %s...' % self.exploit_name, 'cyan'))
            start = time.perf_counter()
            if self.input is None:
                if self.output is None:
                    self.exploit.run()
                else:
                    self.exploit.run(self.output)
            else:
                # prepare is used to update internal state of input generators prior to running
                if hasattr(self.input, 'prepare'):
                    self.input.prepare()
                if self.output is None:
                    self.exploit.run(self.input)
                else:
                    self.exploit.run(self.input, self.output)
            end = time.perf_counter()
            eprint(colorize('Finished running %s (%.2f seconds)' % (self.exploit_name, end - start), 'cyan'))


def main() -> None:
    history_file = os.path.join(os.path.expanduser('~'), '.acsploit_history')
    if not os.path.isfile(history_file):
        with open(history_file, 'w') as f:
            f.write('')

    parser = argparse.ArgumentParser(description='A tool for generating worst-case inputs for algorithms')
    parser.add_argument('--debug', action='store_true', help='show debug stack traces')
    parser.add_argument('--load-file', metavar='FILE', default=None, help='load commands from file and then exit')

    args = parser.parse_args()

    cmdlineobj = ACsploit(hist_file=history_file)
    cmdlineobj.debug = args.debug

    if args.load_file is not None:
        try:
            with open(args.load_file) as script:
                lines = [line.strip().split('#', 1)[0] for line in script]  # `#` is a comment in scripts
                cmdlineobj.script_mode = True
                cmdlineobj.runcmds_plus_hooks(lines)
        except OSError:
            eprint(cmdlineobj.colorize('Could not open file %s' % args.load_file, 'red'))
    else:
        cmdlineobj.cmdloop()


if __name__ == '__main__':
    main()
    
