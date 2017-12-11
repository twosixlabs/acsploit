from cmd import Cmd
import input
from .option import Option

class BaseCmd(Cmd):
    def do_EOF(self, args):
        self.do_exit(args)

    def do_exit(self, args):
        return True

class OptionCommandLine(BaseCmd):
    def __init__(self):
        super(OptionCommandLine, self).__init__()
        self.options = dict({})

    def help_set(self):
        print("implement dis")

    def do_set(self, args):
        split_args = args.split()

        if len(split_args) < 2:
            self.help_set()
            return

        key = split_args[0]
        value = split_args[1]

        if key not in self.options:
            self.help_set()
            return
        else:
            self.options[key].set_value(value)

    def do_options(self, args):
        for key, option in self.options.items():
            print(key + " " + str(option.value))

class InputGeneratorCommandLine(OptionCommandLine):
    @staticmethod
    def start_instance(name, data_type):
        prompt = InputGeneratorCommandLine()
        prompt.prompt = "> "

        if data_type == 'string':
            prompt.options = input.StringGenerator.get_options()
        elif data_type == 'int':
            prompt.options = input.IntGenerator.get_options()

        prompt.name = name
        prompt.data_type = data_type
        prompt.cmdloop()

    def do_save(self, args):
        input.Generator.create(self.name, self.data_type, self.options)

        return True

