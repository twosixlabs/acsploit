import acsploit
import exploits
import inspect
import cmd

class cmdline(cmd.Cmd):

    intro = "\n--Welcome--\n"
    prompt = "(acsploit) "
    origpromptlen = len(prompt)
    options = dict({"exploit" : "", "input" : ""})
    currexp = None

    def do_EOF(self, args):
        return True

    def do_options(self, args):
        for key, option in self.options.items():
            print "  " + key + ": " +  str(option)
        if self.currexp != None:
            for key, option in self.currexp.options.items():
                print "  " + key + ": " +  str(option)

    def do_set(self, args):
        args = args.split()
        if len(args) < 2:
            return

        key = args[0]
        val = args[1]

        if key == "exploit":
            self.set_exploit(val)
        elif (self.currexp != None) and (key in self.currexp.options):
            self.currexp.options[key] = val
        else:
            self.options[key] = val

    def set_exploit(self, expname):
        self.prompt = self.prompt[:self.origpromptlen - 2] + ":"+expname+") "
        if expname == "sort":
            self.currexp = sort()
        if expname == "tree":
            self.currexp = tree()
        self.options["exploit"] = expname

class sort():
    options = dict({"numtries": "", "blah": ""})

class tree():
    options = dict({"abcd": "", "1234": ""})

if __name__ == '__main__':
    cmdline().cmdloop()
