VALUE = 'value'
DESCRIPTION = 'description'
VALUES = 'values'
CUSTOM = 'custom'


class Options(object):
    """Options class"""
    TRUE_VALUES = [True, 'True', 'true', 'Yes', 'yes', 'Y', 'y']

    def __init__(self):
        self._options = {}

    def __getitem__(self, key):
        return self.get_value(key)

    def __setitem__(self, key, value):
        if key not in self._options:
            raise KeyError('add_option() must be used to add new options')
        self.set_value(key, value)

    def add_option(self, name, default_value, description, values=list(), supports_custom=False):
        """Adds an option."""
        if type(name) is not str:
            raise TypeError('Option name must be a string, not a %s' % str(type(name)))
        if name in self._options:
            raise KeyError('Cannot add duplicate option %s' % name)
        self._options[name] = {VALUE: default_value,
                               DESCRIPTION: description,
                               CUSTOM: supports_custom}
        if len(values) > 0:
            self._options[name][VALUES] = values

    def get_option_names(self):
        """Returns a list of all option names."""
        return list(self._options.keys())

    def get_value(self, name):
        """Returns the value of an option."""
        return self._options[name][VALUE]

    def get_acceptable_values(self, name):
        """Returns the acceptable values for an option."""
        values = self._options[name][VALUES] if VALUES in self._options[name] else []
        if self._options[name][CUSTOM]:
            values.append(CUSTOM)
        return values if len(values) > 0 else None

    def is_acceptable_value(self, name, value):
        return ((VALUES not in self._options[name]) or
                (value in self._options[name][VALUES]) or
                (self._options[name][CUSTOM] and type(value) is str and value.startswith(CUSTOM + ' ')))

    def set_value(self, name, value):
        """Sets an option."""
        # type conversions for non-str values
        if type(self._options[name][VALUE]) is bool:
            value = value in Options.TRUE_VALUES
        if type(self._options[name][VALUE]) is int:
            value = int(value)
        if type(self._options[name][VALUE]) is float:
            value = float(value)
        if not self.is_acceptable_value(name, value):
            raise ValueError('%r is not an acceptable value for %s' % (value, name))
        self._options[name][VALUE] = value

    def get_description(self, name):
        """Returns a description of an option."""
        return self._options[name][DESCRIPTION]

    def supports_custom(self, name):
        return self._options[name][CUSTOM]
