from ..__main__ import ACsploit
import os
import pytest

def test_acsploit_init():
    cmdlineobj = ACsploit(None)

# Cmd2 has a transcript that is in the master branch but is not yet released.
# This feature is the most natural way to test ACsploit but cannot be installed
# via pip yet.  When the next version of Cmd2 is released tests via transcript
# should be added.
