ACsploit: a tool for generating worst-case inputs for algorithms
=======================================================================

TODO: write description.

Usage
-----

TODO: write usage.

Contributing Exploits
---------------------

Requirements for exploit contribution:

- Create a python class titled [yourExploitType]Exploit. Name this file something appropriate and place it in the "exploits" directory.
- The class must include an attribute titled "options", which is a dictionary of all the options specific to your exploit. 
- The class must include a function "run(self, generator)" that takes an ACsploit input generator as an argument.
- Add the approptiate line to `exploits/__init__.py`

Beyond the above requirements, your exploit can be written however you'd like.

Contributing Input Generators
-----------------------------

TODO.
