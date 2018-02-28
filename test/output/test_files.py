import os
from mock import MagicMock, call, mock_open, patch
from output import File

OPEN = '%s.open' % __name__
TEST_OUTPUT_LINES = [17, 'hello', 'c', [1, 20, 3]]
TEST_OUTPUT_LINES_STR = ['17', 'hello', 'c', '[1, 20, 3]']


def test_output_defaults():
    with patch('__builtin__.open', mock_open()) as mock_open_f:
        f = File()
        f.output(TEST_OUTPUT_LINES)
        mock_open_f.assert_called_once_with('acsploit_output.dat', 'w')
        mock_open_f().write.assert_has_calls([call(os.linesep.join(TEST_OUTPUT_LINES_STR)), call(os.linesep)])


def test_output_no_trailing_newline():
    with patch('__builtin__.open', mock_open()) as mock_open_f:
        f = File()
        f.options.set_value('final_newline', 'No')
        f.output(TEST_OUTPUT_LINES)
        mock_open_f.assert_called_once_with('acsploit_output.dat', 'w')
        mock_open_f().write.assert_called_once_with(os.linesep.join(TEST_OUTPUT_LINES_STR))


def test_output_custom_filename():
    with patch('__builtin__.open', mock_open()) as mock_open_f:
        f = File()
        f.options.set_value('filename', 'very_suspicious_file.exe')
        f.output(TEST_OUTPUT_LINES)
        mock_open_f.assert_called_once_with('very_suspicious_file.exe', 'w')
        mock_open_f().write.assert_has_calls([call(os.linesep.join(TEST_OUTPUT_LINES_STR)), call(os.linesep)])


def test_output_number_format():
    with patch('__builtin__.open', mock_open()) as mock_open_f:
        f = File()
        f.options.set_value('number_format', 'octal')
        f.output(TEST_OUTPUT_LINES)
        mock_open_f.assert_called_once_with('acsploit_output.dat', 'w')
        mock_open_f().write.assert_has_calls([call(os.linesep.join(['021', 'hello', 'c', '[1, 20, 3]'])),
                                              call(os.linesep)])


def test_write_plaintext_file():
    mock_output = MagicMock()
    f = File()
    f.write_plaintext_file(TEST_OUTPUT_LINES, mock_output)
    mock_output.write.assert_called_once_with(os.linesep.join(TEST_OUTPUT_LINES_STR))


def test_write_sv_file():
    mock_output = MagicMock()
    f = File()
    f.write_sv_file(TEST_OUTPUT_LINES, mock_output, ' ')
    mock_output.write.assert_called_once_with(' '.join(TEST_OUTPUT_LINES_STR))


def test_write_sv_file_list_of_lists():
    mock_output = MagicMock()
    f = File()
    f.write_sv_file([[1, 2, 3], [4, 5], [6]], mock_output, ' ')
    mock_output.write.assert_called_once_with(os.linesep.join(['1 2 3', '4 5', '6']))


def test_write_sv_file_list_of_lists_number_format():
    mock_output = MagicMock()
    f = File()
    f.options.set_value('number_format', 'hexadecimal')
    f.write_sv_file([[10, 20, 3], [4, 5], [6]], mock_output, ' ')
    mock_output.write.assert_called_once_with(os.linesep.join(['0xa 0x14 0x3', '0x4 0x5', '0x6']))


def test_convert_item_ints_decimal():
    f = File()
    f.options.set_value('number_format', 'decimal')
    for item in [7, 8, 15, 20]:
        assert f.convert_item(item) == str(item)


def test_convert_item_ints_hexadecimal():
    f = File()
    f.options.set_value('number_format', 'hexadecimal')
    for item in [7, 8, 15, 20]:
        assert f.convert_item(item) == hex(item)


def test_convert_item_ints_octal():
    f = File()
    f.options.set_value('number_format', 'octal')
    for item in [7, 8, 15, 20]:
        assert f.convert_item(item) == oct(item)


def test_convert_item_non_int():
    f = File()
    for item in ['a', [1, 2, 3]]:
        assert f.convert_item(item) == str(item)
