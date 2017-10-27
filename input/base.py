from abc import abstractmethod
import configparser

class Generator(object):
	@staticmethod
	def create(name, data_type, options):
		config = configparser.RawConfigParser()

		if (config.has_section(name)):
			raise ValueError("Input generator with name " + name + " already exists!")

		config.add_section(name)

		config.set(name, 'data_type', data_type)

		for option in options.values():
			config.set(name, option.key, option.value)

		with open('.input.cfg', 'a') as configfile:
			config.write(configfile)

	@staticmethod
	def get(name):
		config = configparser.RawConfigParser()
		config.read('.input.cfg')

		saved_config = {}

		if not config.has_section(name):
			return None

		options = dict(config.items(name))

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
