ACsploit: a tool for generating worst-case inputs for algorithms
=======================================================================

ACsploit is an interactive command-line utility to generate worst-case inputs to commonly used algorithms. These
worst-case inputs are designed to result in the target program utilizing a large amount of resources (e.g. time or memory).

ACsploit is designed to be easy to contribute to. Future features will include adding arbitrary constraints to inputs,
creating an API, and hooking into running programs to feed worst-case input directly to functions of interest.

Join us on the ACsploit Slack [here](https://join.slack.com/t/acsploit/shared_invite/enQtNjE2MTc3MDQ0NTQ2LTllYjViMjc5NTM1YzM0OWUwMTBiMmM3M2MxNGEwNWNmNjkyNDFiMTgyMjRiMzExZWU4Y2NhNTVlZTA4MThiZjg)!

![Screenshot](acsploit.png)


Usage
-----

Start ACsploit with `python3 acsploit.py`. From there, you can use the `help` command to see what commands are available.
You can call `help` on any of them to learn more about how to use that command, such as `help set`.

To see the available exploits, use the `show` command. To stage one for use, use `use [exploit_name]`. To see a
description of the exploit, run `info`. At any point, you can run `options` to see the current input, output, and
exploit options, and then use `set [option_name] [value]` to set an option. To see detailed descriptions of the options,
 use `options describe`.

Tab completion is enabled for exploit and option names.

Finally, use `run` to generate output from the exploit.

ACsploit supports abbreviated commands, bash commands using `!`, `CTRL+R` history search, and more.

#### Command-line Options

`--load-file SCRIPT` runs the commands in `SCRIPT` as if they had been entered in an interactive ACsploit session and then exits. `#` can be used for comments as in Python.

`--debug` enables debug mode, in which ACsploit prints stack-traces when errors occur.

Documentation
------------------------

Documents are generated using pdoc3 and can be found in the `docs` directory.

#### Generating Documents
Run `pip3 install pdoc3` to install the documentation dependencies and then run `python generate_docs.py`


Warning
------------------------

Caution should be used in generating and accessing ACsploit exploits. Using unreasonable exploit parameters may cause denial of service on generation. Additionally, the canned exploits (e.g. compression bombs) may cause denial of service if accessed by relevant applications.

Tests
------------------------
Tests for ACsploit can be invoked by running `python -m pytest test`. Alternatively, individual tests can be invoked by running `python -m pytest test/path/to/test.py`.

To run the tests and obtain an HTML coverage report run the following:

```
python -m pytest --cov=. --cov-report html:cov test/
```

Finally to run the tests in parellel the `-n` flag can be used followed by the number of tests to run in parallel.  On Linux and Mac the following works:

```
python -m pytest -n`nproc` --cov=. --cov-report html:cov test/
```

Contributing to ACsploit
------------------------

We welcome community contributions to all aspects of ACsploit! For guidelines on contributing, please see [Contributing](CONTRIBUTING.md)
