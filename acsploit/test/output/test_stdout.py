import os
import sys
from unittest.mock import patch
from output import Stdout


def test_output_defaults():
    with patch.object(sys, 'stdout') as mock_stdout:
        s = Stdout()
        s.output([7, 'hello', 'c', [1, 2, 3]])
        mock_stdout.write.assert_called_once_with('7\nhello\nc\n[1, 2, 3]' + os.linesep)


def test_output_separator():
    with patch.object(sys, 'stdout') as mock_stdout:
        s = Stdout()
        s.options.set_value('separator', 'comma')
        s.output([7, 'hello', 'c', [1, 2, 3]])
        mock_stdout.write.assert_called_once_with('7,hello,c,[1, 2, 3]' + os.linesep)


def test_output_separator_number_format():
    with patch.object(sys, 'stdout') as mock_stdout:
        s = Stdout()
        s.options.set_value('separator', 'comma')
        s.options.set_value('number_format', 'octal')
        s.output([15, 'hello', 'c', [1, 2, 3]])
        mock_stdout.write.assert_called_once_with('0o17,hello,c,[1, 2, 3]' + os.linesep)


def test_convert_item_ints_decimal():
    s = Stdout()
    s.options.set_value('number_format', 'decimal')
    for item in [7, 8, 15, 20]:
        assert s.convert_item(item) == str(item)


def test_convert_item_ints_hexadecimal():
    s = Stdout()
    s.options.set_value('number_format', 'hexadecimal')
    for item in [7, 8, 15, 20]:
        assert s.convert_item(item) == hex(item)


def test_convert_item_ints_octal():
    s = Stdout()
    s.options.set_value('number_format', 'octal')
    for item in [7, 8, 15, 20]:
        assert s.convert_item(item) == oct(item)


def test_convert_item_non_int():
    s = Stdout()
    for item in ['a', [1, 2, 3]]:
        assert s.convert_item(item) == str(item)
