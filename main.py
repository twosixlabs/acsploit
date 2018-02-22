import exploits
import inspect
import re
import cmd
import input

BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'


class cmdline(cmd.Cmd):
    # intro = colored("\n**********ACsploit**********\n", 'red')
    intro = "\n**********ACsploit**********\n"
    prompt = BLUE + "(acsploit) " + ENDC
    origpromptlen = len(prompt)
    options = {"input": 'string'}
    descriptions = {"input": "One of int, char, str."}
    currexp = None
    currinputgen = input.StringGenerator()
    availexps = {}
    
    def init(self):
        d = dict()
        d = self.recurse(exploits, d)
        for name in d:
            obj = d[name]
            try:
                path = inspect.getfile(obj).split("/")
                i = path.index('exploits')
                fullname = '/'.join(path[i+1:]).split('.')[0]
                self.availexps[fullname] = obj
            except TypeError:
                pass

    def recurse(self, module, d):
        if module.__file__.split('/')[-1] == "__init__.py":
            for name, obj in inspect.getmembers(module, inspect.ismodule):
                self.recurse(obj, d)
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if str(type(obj)) == "<type 'classobj'>":
                d[name] = obj
        return d
            

    def do_exit(self, args):
        """Exits ACsploit."""
        return True

    def do_options(self, args):
        """Displays current options, more of which appear after 'input' and 'exploit' are set. Use 'options describe' to see descriptions of each."""
        if len(args.split()) == 0:
            print("")
            for key, option in self.options.items():
                print GREEN + "  " + key + ": " + ENDC + str(option)
            if self.currexp is not None:
                print GREEN + "\n  Exploit options" + ENDC
                for key, option in self.currexp.options.items():
                    print GREEN + "    " + key + ": " + ENDC + str(option)
            if self.currinputgen is not None:
                print GREEN + "\n  Input options" + ENDC
                for key, option in self.currinputgen.options.items():
                    print GREEN + "    " + key + ": " + ENDC + str(option)
            print("")
        else:
            if args.split()[0] == "describe":
                print("")
                for key, desc in self.descriptions.items():
                    print GREEN + "  " + key + ": " + ENDC + str(desc)
                if self.currexp is not None:
                    print GREEN + "\n  Exploit options" + ENDC
                    for key, desc in self.currexp.descriptions.items():
                        print GREEN + "    " + key + ": " + ENDC + str(desc)
                if self.currinputgen is not None:
                    print GREEN + "\n  Input options" + ENDC
                    for key, desc in self.currinputgen.descriptions.items():
                        print GREEN + "    " + key + ": " + ENDC + str(desc)
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
                print RED + "Input " + val + " does not exist." + ENDC
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
                print RED + "No " + val + " attack exists." + ENDC
        else:
            print(RED + "Option "+ key+ " does not exist." + ENDC)

    def do_use(self, args):
        """Sets the current exploit. Usage: use [exploit_name]"""
        args = args.split()
        self.update_exploit(args[0])

    def do_show(self, args):
        """Lists all available exploits."""
        print GREEN + "\nAvailable exploits:" + ENDC
        for key in sorted(self.availexps):
            print GREEN + "    " + key + ENDC
        print("")

    def update_exploit(self, expname):
        if expname in self.availexps:
            self.prompt = self.prompt[:self.origpromptlen - 6] + " : "+expname+") " + '\033[0m'
            self.currexp = self.availexps[expname]
        else:
            print(RED + "Exploit " + expname + " does not exist." + ENDC)
            pass

    def do_run(self, args):
        """Runs exploit with given options."""
        if self.currexp is None:
            print RED + "No exploit set, nothing to do. See options." + ENDC
        elif self.currinputgen is None:
            print RED + "No input specified, nothing to do. See options." + ENDC
        else:
            self.currexp().run(self.currinputgen) 

if __name__ == '__main__':
    cmdlineobj = cmdline()
    cmdlineobj.init()
    cmdline().cmdloop()
