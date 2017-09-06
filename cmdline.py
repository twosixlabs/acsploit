from cmd import Cmd
from abc import ABC, abstractmethod
from option import Option
import algorithms
import input
import configparser

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

	def do_create(self, args):
		input.Generator.create(self.name, self.data_type, self.options)

		return True

class ExploitCommandLine(OptionCommandLine):
	def __init__(self):
		super(ExploitCommandLine, self).__init__()
		self.options['input'] = Option('input', 'string', '')

	def do_input(self, args):
		split_args = args.split()

		if len(split_args) != 2:
			self.help_input()
			return

		name = split_args[0]
		data_type = split_args[1]

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

