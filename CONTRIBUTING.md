Contributing to ACsploit
------------------------
We welcome community contributions to all aspects of ACsploit!

### General Code Style

- Follow [PEP8](http://pep8.org)
- Throw exceptions to indicate errors and failure conditions
  - These will be caught by the ACsploit framework and any `string` message included in the error presented to the user
- Use `_private` names for module-internal functions
- Use [`pytest`](https://docs.pytest.org/en/latest/) for tests
- If you add a module that requires additional dependencies, add them to `requirements.txt`
- ACsploit aims for compatibility with Python 3.5 or greater; do not add features which rely on later Python versions


### Contributing Exploits

Exploits must follow the rules below and implement the given API:

- Each exploit must be implemented in its own module in the appropriate directory. You may create new directories if your exploit does not fit anywhere in the existing hierarchy.
  - Use a lower case, underscore-separated filename for your exploit's module. Make it descriptive, yet brief.
  - Create an empty `__init__.py` file in each new directory you create.

##### API:
- Your module must have an `Options` object. Use the `add_option` method to add exploit-specific options. (See below for the options API)
- Your module must have a `DESCRIPTION` string which briefly describes what the module does and provides a description of the algorithm or approach used by the module.
  - The algorithm description should be separated from the brief module description by a newline and may contain internal newlines. 
  - You are strongly encouraged to follow the format of the existing exploits in your description.
- Your module must have a method `run(generator, output)`. This method will be called when your exploit is used.
  - `generator` is an input generator object (see below for the input generator API).
  - `output` is an output generator object (see below for the output generator API).
  - Your `run` method will typically end with `output.output(exploit_results)`, where `exploit_results` is a `list`.

###### Optional Configuration:
- If your exploit only works with a certain input generator you must include a module-level constant `DEFAULT_INPUT` which specifies the name of that generator.
  - If specifying a `DEFAULT_INPUT`, you may also include a `dict` of `DEFAULT_INPUT_OPTIONS`. The keys of this `dict` must be options on the `DEFAULT_INPUT` input generator and values the values your exploit requires for those options.
- You may include `DEFAULT_OUTPUT` and `DEFAULT_OUTPUT_OPTIONS` constants, which work analogously to `DEFAULT_INPUT` and `DEFAULT_INPUT_OPTIONS` for output formatters.
- If your exploit does not use an input generator, you may add a module-level constant `NO_INPUT = True`.
  - If you set `NO_INPUT = True` your exploit's  `run()` method must have the signature `run(output)`, where `output` is an output generator object.

##### Tests:
- It is strongly recommended that you implement a test suite for your exploit.
- If your exploit is in a file called `exploits/star/twinkle/shiny.py`, you should put its tests in `test/exploits/star/twinkle/shiny.py`.

Beyond the above requirements, your exploit can be written however you'd like.

### Contributing Input Generators

Input generators must follow the rules below and implement the given API:

- Your generator must have its own file in the `input/` directory.
  - When adding a new generator you must add its class to the list in `input/__init__.py`.
  - Use a lower case, underscore-separated filename for your generator's module. Make it descriptive, yet brief.
- Your generator must be a class inheriting from `object` (ie a new-style python class).

##### API:
- Your input generator class must have a class-level `OUTPUT_NAME`, a string identifying the input generator.
  - This string should be lower case and underscore-separated.
- Your input generator class must have an `__init__(self)` method that creates and configures an `Options` object as the `options` member of instances of the class.
  - eg:

```
	def __init__(self):
   		self.options = Options()
   		self.options.add_options(…)
   		…
```
- Your input generator may have a `prepare()` method, which will be called by ACsploit before any exploit using your input generator runs but after all configuration of your input generator by the user.
  - The `prepare()` method should be used to perform any internal synchronization or manipulations of state needed before generating values. (See `/inputs/strings.py` for an example of this.)
- Your input generator class must have the following methods, each of which should return as indicated or raise a `NotImplementedError` if no meaningful value can be returned. (eg, the `regex` generator cannot meaningfully return anything for `get_max_value()`, as the 'maximum' value for a given regex is not a universally meaningful concept.)
  - `get_max_value(self)`/`get_min_value(self)`: return the greatest/smallest values that the generator could generate given its current option configuration.
  - `get_greater_than(self, value)`/`get_less_than(self, value)`: return a value greater or lesser than `value`, if these is one given the current option configuration. If no such value exists, these methods should raise a `ValueError`.
  - `get_random(self)`: return a random value within the restrictions of the current option configuration.
  - `get_list_of_values(self, num_values)`: return `num_values` values from within the restrictions of the current option configuration as a `list`. If that many values cannot be generated, this method should raise a `ValueError`.
  - `is_valid(self, value)`: return `True` if `value` could be generated by the generator given its current option configuration and `False` otherwise.

##### Tests:
- It is strongly recommended that you implement a test suite for your input generator.
- If your input generator is in a file called `input/shiny.py`, you should put its tests in `test/input/shiny.py`.

### Contributing Output Formatters

Output formatters must follow the rules below and implement the given API:

- Your formatter must have its own file in the `output/` directory.
  - When adding a new formatter you must add its class to the list in `output/__init__.py`.
  - Use a lower case, underscore-separated filename for your formatter's module. Make it descriptive, yet brief.
- Your formatter must be a class inheriting from `object` (ie a new-style python class).

##### API:
- Your output formatter class must have a class-level `OUTPUT_NAME`, a string identifying the output formatter.
  - This string should be lower case and underscore-separated.
- Your output formatter class must have a `__init__(self)` that creates and configures an `Options` object as the `options` member of instances of the class.
  - eg:

```
	def __init__(self):
   		self.options = Options()
   		self.options.add_options(…)
   		…
```
- Your output formatter class must have a `output(self, output_list)` method that formats and outputs each item in `output_list` (a `list`). This method must NOT return any values.

##### Tests:
- It is strongly recommended that you implement a test suite for your output formatter.
- If your output formatter is in a file called `output/shiny.py`, you should put its tests in `test/output/shiny.py`.

### Using Options

The `Options` module is used throughout ACsploit for configuration management.

Each configurable component (eg, an exploit, input generator, output formatter, etc) should create an `Options` object and expose it to consumers.

To add options call `options.add_option(option_name, default_value, description, acceptable_values=[])`.

- `option_name` should be in `snake_case`
- `Options` infers the type of the value from the type of `default_value` and coerces new values to that type.
  - eg, if `default_value` is `True`, calling `set_value()` with `'false'` will set the option to `False`.
  - coercion is implemented for `bool`, `int`, and `float`.
- `description` should be a human-readable description of the option.
- `acceptable_values` is an optional `list` of values. If provided, attempts to set the option to values not in `acceptable_values` will be rejected.

To get the current value of an option use `options.get_value(option_name)` or `options[option_name]`.

To set the value of an option call `options.set_value(option_name, value)`. If `value` is not in the `acceptable_values` for that option `set_value()` will raise a `ValueError`.

Example:

```
	from acsploit.options import Options
	…
	class ExampleOutputFormatter(object):
		…
		def __init__(self):
			self.options = Options()
			self.options.add_option('this_is_the_option_name', 'this_is_the_default_value', 'This is the description of the option', ['this', 'is', 'a', 'list', 'of', 'acceptable', 'values'])
			self.options.add_option('verbosity', 0, 'How verbose to be')
			self.options.add_option('encabulate', False, 'Encabulate output')
			…
```