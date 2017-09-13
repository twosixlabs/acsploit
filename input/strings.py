from .chars import CharGenerator
from .base import Generator
import acsploit
import random

class StringGenerator(Generator):
	def __init__(self, options):
		super(StringGenerator, self).__init__()
		self.min_length = int(options['min_length'])
		self.max_length = int(options['max_length'])
		self.char_gen = CharGenerator(options)

	def get_less_than(self, value):
		char_list = list(value)
		for i in range(len(char_list) - 1, 0, -1): #iterate backwards through list. e.g. replace zzz with zzy
			c = char_list[i]
			if (c != self.char_gen.get_min_value()):
				char_list[i] = self.char_gen.get_less_than(c)
				return ''.join(char_list)

		return value

	def get_greater_than(self, value):
		char_list = list(value)
		for i in range(len(char_list)):
			c = char_list[i]
			if (c != self.char_gen.get_max_value()):
				char_list[i] = self.char_gen.get_greater_than(c)
				return ''.join(char_list)

		return value

	def get_max_value(self):
		value = ""
		for i in range(self.max_length):
			value = value + self.char_gen.get_max_value()

		return value

	def get_min_value(self):
		value = ""
		for i in range(self.min_length):
			value = value + self.char_gen.get_min_value()

		return value

	def get_random(self):
		length = self.min_length
		
		if (self.min_length != self.max_length):
			length = random.randint(self.min_length, self.max_length)

		value = []
		for i in range(length):
			value.append(self.char_gen.get_random())
			
		return ''.join(value)
	
	def get_options():
		options = dict({
			'min_length' : acsploit.Option('min_length', 'int', 1),
			'max_length' : acsploit.Option('max_length', 'int', 10)
		})
		options.update(CharGenerator.get_options())
		return options

