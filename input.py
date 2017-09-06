from abc import ABC, abstractmethod
import random
from option import Option
import configparser

class Generator(object):
	@staticmethod
	def create(name, data_type, options):
		config = configparser.RawConfigParser()
		config.add_section(name)

		config.set(name, 'data_type', data_type)

		for option in options.values():
			config.set(name, option.key, option.value)

		with open('.input.cfg', 'w') as configfile:
			config.write(configfile)

	@staticmethod
	def get(name):
		config = configparser.RawConfigParser()
		config.read('.input.cfg')

		saved_config = {}

		options = dict(config.items(name))

		print(options)
		for key in options.keys():
			saved_config[key] = options[key]

		return saved_config

	@abstractmethod
	def get_less_than(self, value):
		pass

	@abstractmethod
	def get_greater_than(self, value):
		pass

	@abstractmethod
	def get_max_value(self):
		pass

	@abstractmethod
	def get_min_value(self):
		pass

	@abstractmethod
	def get_random(self):
		pass

	@staticmethod
	def get_options():
		pass

class IntGenerator(Generator):
	def __init__(self, options):
		super(IntGenerator, self).__init__()
		self.options = options
		self.max = int(options['max_value'])
		self.min = int(options['min_value'])

	def get_less_than(self, value):
		if value == self.min:
			return self.min
		return value - 1

	def get_greater_than(self, value):
		if value == self.max:
			return self.max
		return value + 1

	def get_max_value(self):
		return self.max

	def get_min_value(self):
		return self.min

	def get_random(self):
		return random.randint(self.min, self.max)

	def get_options():
		return dict({
			'min_value' : Option('min_value', 'int', 0),
			'max_value' : Option('max_value', 'int', 255),
		})

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
		return dict({
			'min_length' : Option('min_length', 'int', 0),
			'max_length' : Option('max_length', 'int', 10)
		}).update(self.char_gen.get_options())

class CharGenerator(Generator):
	# min cannot equal max
	def __init__(self, options):
		super(CharGenerator, self).__init__()

		self.min = int(options['min_value'])
		self.max = int(options['max_value'])
		self.characters = []
		self.init_characters()

	def init_characters(self):
		chars = []
		for i in range(int(self.min), int(self.max) + 1):
			chars.append(chr(i))
		self.characters = chars

	def get_less_than(self, value):
		if ord(value) == self.min:
			return self.min
		value = chr(ord(value) - 1)
		while chr(ord(value)) not in self.characters:
			value = chr(ord(value) - 1)
		return value

	def get_greater_than(self, value):
		if (ord(value) == self.max):
			return value
		value = chr(ord(value) + 1)
		while chr(ord(value)) not in self.characters:
			value = chr(ord(value) + 1)
		return value


	def get_max_value(self):
		return chr(self.max)

	def get_min_value(self):
		return chr(self.min)

	def get_random(self):
		return random.choice(self.characters)

	def get_options():
		return dict({
			'min_value' : Option('min_value', 'int', 0x61),
			'max_value' : Option('max_value', 'int', 0x71)
		})

	def add_restrictions(self, restrictions):
		for restriction in restrictions:
			try:
				self.characters.remove(restriction)
			except ValueError:
				pass  # Error doesn't need to be dealt with
