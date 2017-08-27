from cmd import Cmd
from abc import ABC, abstractmethod
import algorithms
import input

class BaseCmd(Cmd):
	def do_EOF(self, args):
		self.do_exit(args)

	def do_exit(self, args):
		return True

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
	algorithm = algorithms.Sort()
	generator = ''
	
	@staticmethod
	def start_instance():
		prompt = SortCommandLine()
		prompt.prompt = "exploit(sort)$ "
		prompt.cmdloop("Exploit Sorting Algorithms. Type \'help\' for available commands")

	def help_ascending(self):
		print("Usage: ascending true OR ascending false. " +
			"Sets the output to be worst case for an algorithm that sorts in ascending order (true)  or not (false). Ascending=true is the default")

	def do_ascending(self, args):
		split_args = args.split()

		if len(split_args) != 1:
			self.help_ascending()
			return

		if split_args[0].lower() == "true":
			self.algorithm.is_ascending = True
		elif split_args[0].lower() == "false":
			self.algorithm.is_ascending = False

	def help_exploit(self):
		print("Prints the output of the exploit. Must have set a type first.")

	def do_exploit(self, args):
		if self.generator == '':
			self.help_exploit()
			return
		
		print(self.algorithm.exploit(self.generator, 10))


