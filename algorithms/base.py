from abc import abstractmethod

class Algorithm(object):
	@abstractmethod
	def exploit(self, generator):
		pass


