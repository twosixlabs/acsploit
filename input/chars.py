from .base import Generator
import cmdline

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
			'min_value' : cmdline.Option('min_value', 'int', 0x61),
			'max_value' : cmdline.Option('max_value', 'int', 0x71)
		})

	def add_restrictions(self, restrictions):
		for restriction in restrictions:
			try:
				self.characters.remove(restriction)
			except ValueError:
				pass  # Error doesn't need to be dealt with
