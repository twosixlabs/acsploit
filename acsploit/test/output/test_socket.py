import socket
from unittest.mock import MagicMock, patch
from output import Socket


def test_output_defaults():
    mock_socket = MagicMock()
    with patch.object(socket, 'socket', MagicMock(return_value=mock_socket)) as mock_socket_constructor:
        n = Socket()
        n.output([7, 'hello', 'c', [1, 2, 3]])
        mock_socket_constructor.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
        mock_socket.connect.assert_called_once_with(('127.0.0.1', 80))
        mock_socket.sendall.assert_called_once_with(b'7\nhello\nc\n[1, 2, 3]')
        mock_socket.close.assert_called_once_with()


def test_output_separator():
    mock_socket = MagicMock()
    with patch.object(socket, 'socket', MagicMock(return_value=mock_socket)) as mock_socket_constructor:
        n = Socket()
        n.options.set_value('separator', 'CRLF')
        n.output([7, 'hello', 'c', [1, 2, 3]])
        mock_socket_constructor.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
        mock_socket.connect.assert_called_once_with(('127.0.0.1', 80))
        mock_socket.sendall.assert_called_once_with(b'7\r\nhello\r\nc\r\n[1, 2, 3]')
        mock_socket.close.assert_called_once_with()


def test_final_separator():
    mock_socket = MagicMock()
    with patch.object(socket, 'socket', MagicMock(return_value=mock_socket)) as mock_socket_constructor:
        n = Socket()
        n.options.set_value('final_separator', True)
        n.output([7, 'hello', 'c', [1, 2, 3]])
        mock_socket_constructor.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
        mock_socket.connect.assert_called_once_with(('127.0.0.1', 80))
        mock_socket.sendall.assert_called_once_with(b'7\nhello\nc\n[1, 2, 3]\n')
        mock_socket.close.assert_called_once_with()


def test_await_banner():
    mock_socket = MagicMock()
    with patch.object(socket, 'socket', MagicMock(return_value=mock_socket)) as mock_socket_constructor:
        n = Socket()
        n.options.set_value('await_banner', True)
        n.output([7, 'hello', 'c', [1, 2, 3]])
        mock_socket_constructor.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
        mock_socket.connect.assert_called_once_with(('127.0.0.1', 80))
        mock_socket.recv.assert_called_once_with(1024)
        mock_socket.sendall.assert_called_once_with(b'7\nhello\nc\n[1, 2, 3]')
        mock_socket.close.assert_called_once_with()


def test_host():
    mock_socket = MagicMock()
    with patch.object(socket, 'socket', MagicMock(return_value=mock_socket)) as mock_socket_constructor:
        n = Socket()
        n.options.set_value('host', '192.168.100.100')
        n.output([7, 'hello', 'c', [1, 2, 3]])
        mock_socket_constructor.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
        mock_socket.connect.assert_called_once_with(('192.168.100.100', 80))
        mock_socket.sendall.assert_called_once_with(b'7\nhello\nc\n[1, 2, 3]')
        mock_socket.close.assert_called_once_with()


def test_port():
    mock_socket = MagicMock()
    with patch.object(socket, 'socket', MagicMock(return_value=mock_socket)) as mock_socket_constructor:
        n = Socket()
        n.options.set_value('port', 13337)
        n.output([7, 'hello', 'c', [1, 2, 3]])
        mock_socket_constructor.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
        mock_socket.connect.assert_called_once_with(('127.0.0.1', 13337))
        mock_socket.sendall.assert_called_once_with(b'7\nhello\nc\n[1, 2, 3]')
        mock_socket.close.assert_called_once_with()


def test_ip_version_host():
    mock_socket = MagicMock()
    with patch.object(socket, 'socket', MagicMock(return_value=mock_socket)) as mock_socket_constructor:
        n = Socket()
        n.options.set_value('ip_version', 'IPv6')
        n.options.set_value('host', '::1')
        n.output([7, 'hello', 'c', [1, 2, 3]])
        mock_socket_constructor.assert_called_once_with(socket.AF_INET6, socket.SOCK_STREAM)
        mock_socket.connect.assert_called_once_with(('::1', 80))
        mock_socket.sendall.assert_called_once_with(b'7\nhello\nc\n[1, 2, 3]')
        mock_socket.close.assert_called_once_with()


def test_many_options():
    mock_socket = MagicMock()
    with patch.object(socket, 'socket', MagicMock(return_value=mock_socket)) as mock_socket_constructor:
        n = Socket()
        n.options.set_value('separator', 'comma')
        n.options.set_value('number_format', 'octal')
        n.options.set_value('final_separator', True)
        n.options.set_value('port', 500)
        n.output([15, 'hello', 'c', [1, 2, 3]])
        mock_socket_constructor.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
        mock_socket.connect.assert_called_once_with(('127.0.0.1', 500))
        mock_socket.sendall.assert_called_once_with(b'0o17,hello,c,[1, 2, 3],')
        mock_socket.close.assert_called_once_with()


def test_convert_item_ints_decimal():
    n = Socket()
    n.options.set_value('number_format', 'decimal')
    for item in [7, 8, 15, 20]:
        assert n.convert_item(item) == str(item).encode()


def test_convert_item_ints_hexadecimal():
    n = Socket()
    n.options.set_value('number_format', 'hexadecimal')
    for item in [7, 8, 15, 20]:
        assert n.convert_item(item) == hex(item).encode()


def test_convert_item_ints_octal():
    n = Socket()
    n.options.set_value('number_format', 'octal')
    for item in [7, 8, 15, 20]:
        assert n.convert_item(item) == oct(item).encode()


def test_convert_item_non_int():
    n = Socket()
    for item in ['a', [1, 2, 3]]:
        assert n.convert_item(item) == str(item).encode()
