import exploits
import inspect
import cmd
import input
import os
import sys


def color(s, c):
    endc = '\033[0m'
    colors = {
        'blue': '\033[94m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'red': '\033[91m'
    }

    if c not in colors:
        print(colors['red'] + "{} is not a supported color".format(c) + endc)
        return s

    return colors[c] + s + endc


class CmdLine(cmd.Cmd):
    intro = "\n**********ACsploit**********\n"
    prompt = color('(acsploit) ', 'blue')
    origpromptlen = len(prompt)
    options = {"input": 'string'}
    descriptions = {"input": "One of int, char, str."}
    currexp = None
    currinputgen = input.StringGenerator()
    availexps = {}
    
    def init(self):
        d = self.get_exploits()
        for name in d:
            obj = d[name]
            try:
                path = inspect.getfile(obj).split("/")
                i = path.index('exploits')
                fullname = '/'.join(path[i+1:]).split('.')[0]
                self.availexps[fullname] = obj
            except TypeError:
                pass

    def get_exploits(self):
        d = dict()
        for dirname, subdirlist, filelist in os.walk('exploits'):
            for f in filelist:
                if f != "__init__.py" and os.path.splitext(f)[1] == ".py":
                    f = os.path.join(dirname, f).replace(os.path.sep, '.')[:-3]  # -3 to strip '.py' extension
                    try:  # test for existence of `options` and `descriptions` in the file before adding
                        f_compound = f + '.' + f.split('.')[-1]
                        eval(f_compound + '.options')
                        # eval(f_compound + '.descriptions')
                        d[f.split('.')[-1]] = eval(f_compound)
                    except AttributeError:
                        print("Found .py in exploits/ that does not satisfy requirements, exiting.")
                        # TODO - in the future we probably want to handle this appropriately, rather than exit
                        sys.exit(1)
        return d

    def do_exit(self, args):
        """Exits ACsploit."""
        return True

    def do_options(self, args):
        """Displays current options, more of which appear after 'input' and 'exploit' are set. Use 'options describe' to see descriptions of each."""
        if len(args.split()) == 0:
            print("")
            for key, option in self.options.items():
                print color("  " + key + ": ", 'green') + str(option)
            if self.currexp is not None:
                print color("\n  Exploit options", 'green')
                for key, option in self.currexp.options.items():
                    print color("    " + key + ": ", 'green') + str(option)
            if self.currinputgen is not None:
                print color("\n  Input options", 'green')
                for key, option in self.currinputgen.options.items():
                    print color("    " + key + ": ", 'green') + str(option)
            print("")
        else:
            if args.split()[0] == "describe":
                print("")
                for key, desc in self.descriptions.items():
                    print color("  " + key + ": ", 'green') + str(desc)
                if self.currexp is not None:
                    print color("\n  Exploit options", 'green')
                    for key, desc in self.currexp.descriptions.items():
                        print color("    " + key + ": ", 'green') + str(desc)
                if self.currinputgen is not None:
                    print color("\n  Input options", 'green')
                    for key, desc in self.currinputgen.descriptions.items():
                        print color("    " + key + ": ", 'green') + str(desc)
                print("")

    def do_set(self, args):
        """Sets an option. Usage: set [option_name] [value]"""
        args = args.split()
        if len(args) != 2:
            print "Usage: set [option_name] [value]"
            return

        key = args[0]
        val = args[1]

        if key == "input":
            if val == "int":
                self.currinputgen = input.IntGenerator()
                self.options["input"] = val
            elif val == "char":
                self.currinputgen = input.CharGenerator()
                self.options["input"] = val
            elif val == "string":
                self.currinputgen = input.StringGenerator()
                self.options["input"] = val
            else:
                print color("Input " + val + " does not exist.", 'red')
                return
        elif self.currexp is not None and key in self.currexp.options:
            # TODO check input type is what is expected
            self.currexp.options[key] = val
        elif self.currinputgen is not None and key in self.currinputgen.options:
            # TODO check input type is what is expected
            self.currinputgen.options[key] = val
        elif key == "attack":
            if val == "time" or val == "memory":
                self.options["attack"] = val
            else:
                print color("No " + val + " attack exists.", 'red')
        else:
            print(color("Option "+ key+ " does not exist.", 'red'))

    def do_use(self, args):
        """Sets the current exploit. Usage: use [exploit_name]"""
        self.update_exploit(args.split[0])

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
            self.currexp().run(self.currinputgen) 


if __name__ == '__main__':
    cmdlineobj = CmdLine()
    cmdlineobj.init()
    cmdlineobj.cmdloop()
