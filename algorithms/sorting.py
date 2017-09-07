from input import Generator
from .base import Algorithm

class Sort(Algorithm):
	is_ascending = True  #This algorithm sorts in ascending order

	def exploit(self, generator, n_inputs):
		if self.is_ascending:
			# Worst case for ascending sorting algorithm is a descending list
			return self.descending_list(generator, n_inputs)
		else:
			return self.ascending_list(generator, n_inputs)

	def ascending_list(self, generator, n_inputs):
		return list(reversed(self.descending_list(generator, n_inputs)))

	def descending_list(self, generator, n_inputs):
		output = [generator.get_random()] # pick random value for now, need to check range in future

		for i in range(1,n_inputs):
			output.append(generator.get_less_than(output[i-1]))     

		return output
