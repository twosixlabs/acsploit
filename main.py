import exploits
import inspect
import re
import cmd
import input
#from termcolor import colored

BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'

class cmdline(cmd.Cmd):
    #intro = colored("\n**********ACsploit**********\n", 'red')
    intro = "\n**********ACsploit**********\n"
    prompt = BLUE + "(acsploit) " + ENDC
    origpromptlen = len(prompt)
    options = dict({"input" : "", "attack" : "time"})
    descriptions = dict({"input" : "One of int, char, str." , "attack" : "One of time or memory."})
    currexp = None
    currinputgen = None
    availexps = {}
    
    def init(self):
        for name, obj in inspect.getmembers(exploits, inspect.isclass):
            try:
                arg_name = re.sub("Exploit", '', name).lower()
                self.availexps[arg_name] = obj
            except TypeError:
                pass

    def do_exit(self, args):
        """Exits ACsploit."""
        return True

    def do_options(self, args):
        """Displays current options, more of which appear after 'input' and 'exploit' are set. Use 'options describe' to see descriptions of each."""
        if len(args.split()) == 0:
            print("")
            for key, option in self.options.items():
                print GREEN + "  " + key + ": " + ENDC +  str(option)
            if self.currexp != None:
                print GREEN + "\n  Exploit options" + ENDC
                for key, option in self.currexp.options.items():
                    print GREEN + "    " + key + ": " + ENDC +  str(option)
            if self.currinputgen != None:
                print GREEN + "\n  Input options" + ENDC
                for key, option in self.currinputgen.options.items():
                    print GREEN + "    " + key + ": " + ENDC +  str(option)
            print("")
        else:
            if args.split()[0] == "describe":
                print("")
                for key, desc in self.descriptions.items():
                    print GREEN + "  " + key + ": " + ENDC +  str(desc)
                if self.currexp != None:
                    print GREEN + "\n  Exploit options" + ENDC
                    for key, desc in self.currexp.descriptions.items():
                        print GREEN + "    " + key + ": " + ENDC + str(desc)
                if self.currinputgen != None:
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
            #TODO list options with help or something else
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
        elif (self.currexp != None) and (key in self.currexp.options):
            #TODO check input type is what is expected
            self.currexp.options[key] = val
        elif (self.currinputgen != None) and (key in self.currinputgen.options):
            #TODO check input type is what is expected
            self.currinputgen.options[key] = val
        elif key == "attack":
            if val == "time" or val == "memory":
                self.options["attack"] = val
            else:
                print RED + "No " + val + " attack exists." + ENDC
        else:
            print(RED + "Option "+ key+ " does not exist." + ENDC)

    def do_use(self, args):
        """Lists all available exploits, and sets the current exploit. Usage: use [optional exploit to set]"""
        args = args.split()
        if len(args) == 0:
            print GREEN + "Use this command to set an exploit by typing:\n\n    exploit <exploit name>\n\nAvailable exploits:" + ENDC
            for key in self.availexps:
                print GREEN + "    " + key + ENDC
        else:
            self.update_exploit(args[0])

    def update_exploit(self, expname):
        if expname in self.availexps:
            self.prompt = self.prompt[:self.origpromptlen - 6] + ":"+expname+") " + '\033[0m'
            self.currexp = self.availexps[expname]
        else:
            print(RED + "Exploit " + expname + " does not exist." + ENDC)
            pass

    def do_exploit(self, args):
        """Runs exploit with given options."""
        if self.currexp == None:
            print RED + "No exploit set, nothing to do. See options." + ENDC
        elif self.currinputgen == None:
            print RED + "No input specified, nothing to do. See options." + ENDC
        else:
            self.currexp().run(self.currinputgen) 

if __name__ == '__main__':
    cmdlineobj = cmdline()
    cmdlineobj.init()
    cmdline().cmdloop()
