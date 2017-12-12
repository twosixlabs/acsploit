import exploits
import inspect
import re
import cmd
import input
#from termcolor import colored

BLUE = '\033[94m'
GREEN = '\033[92m'
RED = '\033[93m'
ENDC = '\033[0m'

class cmdline(cmd.Cmd):
    #intro = colored("\n**********ACsploit**********\n", 'red')
    intro = "\n**********ACsploit**********\n"
    prompt = BLUE + "(acsploit) " + ENDC
    origpromptlen = len(prompt)
    options = dict({"exploit" : "", "input" : "", "attack" : "time"})
    descriptions = dict({"exploit" : "Type of exploit to use. Use 'list' to view." , "input" : "One of int, char, str." , "attack" : "One of time or memory."})
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

    def do_list(self, args):
        """Lists available exploits."""
        print "Available exploits:"
        for key in self.availexps:
            print "  " + key

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

        if key == "exploit":
            self.update_exploit(val)
        elif key == "input":
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
                print "Input " + val + " does not exist."
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
                print "No " + val + " attack exists."
        else:
            print("Option "+ key+ " does not exist.")

    def update_exploit(self, expname):
        if expname in self.availexps:
            self.prompt = self.prompt[:self.origpromptlen - 6] + ":"+expname+") " + '\033[0m'
            self.currexp = self.availexps[expname]
            self.options["exploit"] = expname
        else:
            print("Exploit " + expname + " does not exist.")
            pass

    def do_run(self, args):
        """Runs exploit with given options."""
        if self.currexp == None:
            print "No exploit set, nothing to do."
        elif self.currinputgen == None:
            print "No input specified, nothing to do."
        else:
            self.currexp().run(self.currinputgen) 

if __name__ == '__main__':
    cmdlineobj = cmdline()
    cmdlineobj.init()
    cmdline().cmdloop()
