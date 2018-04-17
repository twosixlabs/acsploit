# Installing ACsploit

## TL;DR

```
$ python --version
Python 3.6
$ git clone TKTK-URL-GOES-HERE-TKTK
$ cd acsploit
$ python -m venv acvenv
$ source acvenv/bin/activate
$ pip install -r requirements.txt
$ ./acsploit.py
```

## The long version, with explanations

#### Python 3

ACsploit requires Python 3.5 or above. To check the version of Python installed on your system, run  `python --version`. (If you have multiple versions of Python installed, try `python3 --version`.)

If you do not have `python3` installed on your system see [here](https://www.python.org/downloads/) for information on how to install it.

#### Downloading ACsploit

Run `git clone TKTK-URL-GOES-HERE-TKTK` to check out the newest version of ACsploit into the current folder, then `cd acsploit`.

#### Creating and activating a `virtualenv`

Unless you want to install the dependencies for ACsploit system-wide, you should create a virtual environment for ACsploit.

Run `pyvenv acvenv` to create a virtual environment called `acvenv` in the current folder.

(If you have Python 3.6 or higher you should run `python -m venv acvenv` instead.)

Activate the virtual environment with `source acvenv/bin/activate`

#### Installing dependencies

Run `pip install -r requirements.txt` to install the dependencies for ACsploit. This may take several minutes, as `pip` may need to compile `z3` as part of the installation process.

#### Running ACsploit

If using a virtual environment, activate it as above.

Run `./acsploit.py`.
