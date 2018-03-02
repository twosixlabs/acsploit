ACsploit: a tool for generating worst-case inputs for algorithms
=======================================================================

ACsploit is an interactive command-line utility to generate worst-case inputs to commonly used algorithms. These
worst-case inputs are designed to result in the target program utilizing a large amount of resources (e.g. time or memory).

ACsploit is designed to be easy to contribute to. Future features will include adding arbitrary constraints to inputs, 
creating an API, and hooking into running programs to feed worst-case input directly to functions of interest.

[![Screenshot](acsploit.png)](gitlab.labs/stac/acsploit/awesomebranch/acsploit.png)

Usage
-----

Start ACsploit with `python acsploit.py`. From there, you can use the `help` command to see what commands are available.
You can call `help` on any of them to learn more about how to use that command, such as `help set`.

To see the available exploits, use the `show` command. To stage one for use, use `use [exploit_name]`. At any point, you
can run `options` to see the current input, output, and exploit options, and then use `set [option_name] [value]` to set
an options. To see detailed descriptions of the options, use `options describe`.

Finally, just use `run` to obtain the output from the exploit.

ACsploit supports abbreviated commands, bash commands using `!`, CTRL+R history search, and more.

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