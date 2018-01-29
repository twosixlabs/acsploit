from abc import abstractmethod


class Generator(object):

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
