ACsploit: a tool for generating worst-case inputs for algorithms
=======================================================================

TODO: write description.

[![Screenshot](acsploit.png)](gitlab.labs/stac/acsploit/awesomebranch/acsploit.png)

Usage
-----

TODO: write usage.

Contributing Exploits
---------------------

Requirements for exploit contribution:

- Create a python module for your exploit in the appropriate directory. New directories may be created so long as an empty `__init__.py` files is created for each new directory.
  - Use lower case, underscore-separated filenames for your exploit. Make it descriptive, yet brief.

- Your module must have an `Options` object. Use the `add_option` method to add exploit-specific options.

- Your module must have a method `run(generator, output)`. This is what gets called when your exploit is used.
  - `generator` is where your input is coming from, and `output` is how your exploit outputs data. You may want to whitelist/blacklist certain generators and output formats.
  - Your `run` method will typically end with `output.output(exploit_results)`, where `exploit_results` is a list of your output.

Beyond the above requirements, your exploit can be written however you'd like.

Contributing Input Generators
-----------------------------

TODO.

Contributing Output Generators
------------------------------

TODO.