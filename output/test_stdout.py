import os
import sys
from mock import patch
from stdout import Stdout


def test_defaults():
    with patch.object(sys, 'stdout') as mock_stdout:
        s = Stdout()
        s.output([7, 'hello', 'c', [1, 2, 3]])
        mock_stdout.write.assert_called_once_with('7\nhello\nc\n[1, 2, 3]' + os.linesep)


def test_separator():
    with patch.object(sys, 'stdout') as mock_stdout:
        s = Stdout()
        s.options.set_value('separator', 'comma')
        s.output([7, 'hello', 'c', [1, 2, 3]])
        mock_stdout.write.assert_called_once_with('7,hello,c,[1, 2, 3]' + os.linesep)


def test_ints_decimal():
    with patch.object(sys, 'stdout') as mock_stdout:
        s = Stdout()
        s.options.set_value('number_format', 'decimal')
        s.output([7, 8, 15, 20])
        mock_stdout.write.assert_called_once_with('7\n8\n15\n20' + os.linesep)


def test_ints_hexadecimal():
    with patch.object(sys, 'stdout') as mock_stdout:
        s = Stdout()
        s.options.set_value('number_format', 'hexadecimal')
        s.output([7, 8, 15, 20])
        mock_stdout.write.assert_called_once_with('0x7\n0x8\n0xf\n0x14' + os.linesep)


def test_ints_octal():
    with patch.object(sys, 'stdout') as mock_stdout:
        s = Stdout()
        s.options.set_value('number_format', 'octal')
        s.output([7, 8, 15, 20])
        mock_stdout.write.assert_called_once_with('07\n010\n017\n024' + os.linesep)
