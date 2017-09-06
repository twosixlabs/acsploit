class Option():
	def __init__(self, key, value_type, default_value):
		self.key = key
		self.value = default_value
		self.value_type = value_type

	def set_value(self, value):
		typed_value = self.validate(value)
		if typed_value is None:
			print(self.key + " must be of type " + self.value_type)
		else:
			self.value = typed_value

	#gross
	def validate(self, input):
		if self.value_type is 'string':
			return input
		elif self.value_type is 'bool':
			if input.lower() == 'true' or input.lower() == 't':
				return True
			elif input.lower() == 'false' or input.lower() == 'f':
				return False
			else:
				return None
		elif self.value_type is 'int':
			try:
				return int(input)
			except ValueError:
				return None
		elif self.value_type is 'float':
			try:
				return float(input)
			except ValueError:
				return None

