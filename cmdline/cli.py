from cmd import Cmd
from .option import Option
from .base import OptionCommandLine, InputGeneratorCommandLine
import algorithms
import input
import configparser

class ExploitCommandLine(OptionCommandLine):
	def __init__(self):
		super(ExploitCommandLine, self).__init__()
		self.options['input'] = Option('input', 'string', '')

	def do_input(self, args):
		split_args = args.split()

		if len(split_args) != 2:
			self.help_input()
			return

		data_type = split_args[0]
		name = split_args[1]

		InputGeneratorCommandLine.start_instance(name, data_type)

		options = input.Generator.get(name)

		if options['data_type'] == 'string':
			self.input = input.StringGenerator(options)
		elif options['data_type'] == 'int':
			self.input = input.IntGenerator(options)

class SortCommandLine(ExploitCommandLine):
	algorithm = algorithms.Sort()

	def __init__(self):
		super(SortCommandLine, self).__init__()
		self.options['ascending'] = Option("ascending", 'bool', True)

	@staticmethod
	def start_instance():
		prompt = SortCommandLine()
		prompt.prompt = "exploit(sort)$ "
		prompt.cmdloop("Exploit Sorting Algorithms. Type \'help\' for available commands")

	def help_run(self):
		print("Prints the output of the exploit. Must have set a type first.")

	def do_run(self, args):
		self.algorithm.is_ascending = self.options['ascending'].value
		
		print(self.algorithm.exploit(self.input, 10))

