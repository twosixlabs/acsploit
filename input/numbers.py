from .base import Generator
import acsploit
import random

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
			'min_value' : acsploit.Option('min_value', 'int', 0),
			'max_value' : acsploit.Option('max_value', 'int', 255),
		})

