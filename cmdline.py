from cmd import Cmd
from abc import ABC, abstractmethod
import algorithms
import input

class BaseCmd(Cmd):
	def do_EOF(self, args):
		self.do_exit(args)

	def do_exit(self, args):
		return True

class AcsploitCommandLine(BaseCmd):
	@staticmethod
	def start_instance():
		prompt = AcsploitCommandLine()
		prompt.prompt = "> "
		prompt.cmdloop('***************Acsploit***************\nSelect an algorithm to being. Type \'help\' for available commands')

	def do_select(self, args):
		algorithm_name = args.split()[0]
		
		prompt = {
			'sort': SortCommandLine,
		}.get(algorithm_name, '')

		prompt.start_instance()

class ExploitCommandLine(BaseCmd):
	def help_type(self):
		print("Set data type. Must be of type int, string, or char")

	def do_type(self, args):
		split_args = args.split()

		if len(split_args) != 1:
			self.help_type()
			return

		if split_args[0] == 'int':
			self.generator = input.IntGenerator(0, 10)
		elif split_args[0] == 'string':
			self.generator = input.StringGenerator(input.CharGenerator(0x61, 0x7a), 10,10)
		elif split_args[0] == 'char':
			self.generator = input.CharGenerator(0x61, 0x7a)
		else:
			self.help_type()

	def do_exit(self, args):
		'''Exits the current shell'''
		return True


class SortCommandLine(ExploitCommandLine):
	isDescending = True

	@staticmethod
	def start_instance():
		prompt = SortCommandLine()
		prompt.prompt = "exploit(sort)$ "
		prompt.cmdloop("Exploit Sorting Algorithms. Type \'help\' for available commands")

	def help_descending(self):
		print("Usage: descending true OR descending false. Sets the output to be in descending order or not. Descending is the default")

	def do_descending(self, args):
		split_args = args.split()

		if len(split_args) != 1:
			self.help_descending()
			return

		if split_args[0].lower() == "true":
			self.isDescending = True
		elif split_args[0].lower() == "false":
			self.isDescending = False

	def help_exploit(self):
		print("Prints the output of the exploit. Must have set a type first.")

	def do_exploit(self, args):
		if self.generator == '':
			self.help_exploit()

		print(algorithms.Sort().exploit(self.generator, 10))


