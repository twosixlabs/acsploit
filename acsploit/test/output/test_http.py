from unittest.mock import MagicMock, call, patch

from output import Http

STANDARD_HEADERS = {
    'User-Agent': 'python-requests',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive', 'Accept': '*/*',
}


def test_output():
    h = Http()
    with patch('output.Http.send_request', MagicMock()) as mock_send:
        with patch('output.Http.get_request', MagicMock(return_value='test')):
            with patch('requests.Request', MagicMock(return_values=MagicMock(prepare=MagicMock(return_value='test')))) as mock_request:
                h.output(['a', 'b', 'c'])
                mock_send.assert_called_once_with(mock_request.return_value.prepare.return_value)
                mock_request.assert_called_once_with('GET', 'http://127.0.0.1:80/', params={'param': ['a', 'b', 'c']},
                                                     headers=STANDARD_HEADERS, data='')


def test_output_url():
    h = Http()
    with patch('output.Http.send_request', MagicMock()) as mock_send:
        with patch('output.Http.get_request', MagicMock(return_value='test')):
            with patch('requests.Request', MagicMock(return_values=MagicMock(prepare=MagicMock(return_value='test')))) as mock_request:
                h.options['url'] = 'https://twosixlabs.com:8080'
                h.output(['a', 'b', 'c'])
                mock_send.assert_called_once_with(mock_request.return_value.prepare.return_value)
                mock_request.assert_called_once_with('GET', 'https://twosixlabs.com:8080',
                                                     params={'param': ['a', 'b', 'c']},
                                                     headers=STANDARD_HEADERS, data='')


def test_output_no_spread_params_separator():
    h = Http()
    with patch('output.Http.send_request', MagicMock()) as mock_send:
        with patch('output.Http.get_request', MagicMock(return_value='test')):
            with patch('requests.Request', MagicMock(return_values=MagicMock(prepare=MagicMock(return_value='test')))) as mock_request:
                h.options['spread_params'] = False
                h.options['separator'] = 'space'
                h.output(['a', 'b', 'c'])
                mock_send.assert_called_once_with(mock_request.return_value.prepare.return_value)
                mock_request.assert_called_once_with('GET', 'http://127.0.0.1:80/', params={'param': 'a b c'},
                                                     headers=STANDARD_HEADERS, data='')


def test_output_no_spread_params_final_separator():
    h = Http()
    with patch('output.Http.send_request', MagicMock()) as mock_send:
        with patch('output.Http.get_request', MagicMock(return_value='test')):
            with patch('requests.Request', MagicMock(return_values=MagicMock(prepare=MagicMock(return_value='test')))) as mock_request:
                h.options['spread_params'] = False
                h.options['final_separator'] = True
                h.output(['a', 'b', 'c'])
                mock_send.assert_called_once_with(mock_request.return_value.prepare.return_value)
                mock_request.assert_called_once_with('GET', 'http://127.0.0.1:80/', params={'param': 'a\nb\nc\n'},
                                                     headers=STANDARD_HEADERS, data='')


def test_output_number_format():
    h = Http()
    with patch('output.Http.send_request', MagicMock()) as mock_send:
        with patch('output.Http.get_request', MagicMock(return_value='test')):
            with patch('requests.Request',
                       MagicMock(return_values=MagicMock(prepare=MagicMock(return_value='test')))) as mock_request:
                h.options['number_format'] = 'hexadecimal'
                h.output([1, 2])
                mock_send.assert_called_once_with(mock_request.return_value.prepare.return_value)
                mock_request.assert_called_once_with('GET', 'http://127.0.0.1:80/', params={'param': ['0x1', '0x2']},
                                                     headers=STANDARD_HEADERS, data='')


def test_output_http_method():
    h = Http()
    with patch('output.Http.send_request', MagicMock()) as mock_send:
        with patch('output.Http.get_request', MagicMock(return_value='test')):
            with patch('requests.Request',
                       MagicMock(return_values=MagicMock(prepare=MagicMock(return_value='test')))) as mock_request:
                h.options['http_method'] = 'POST'
                h.output(['a', 'b', 'c'])
                mock_send.assert_called_once_with(mock_request.return_value.prepare.return_value)
                mock_request.assert_called_once_with('POST', 'http://127.0.0.1:80/', params={'param': ['a', 'b', 'c']},
                                                     headers=STANDARD_HEADERS, data='')


def test_output_url_param_name():
    h = Http()
    with patch('output.Http.send_request', MagicMock()) as mock_send:
        with patch('output.Http.get_request', MagicMock(return_value='test')):
            with patch('requests.Request', MagicMock(return_values=MagicMock(prepare=MagicMock(return_value='test')))) as mock_request:
                h.options['url_param_name'] = 'e'
                h.output(['a', 'b', 'c'])
                mock_send.assert_called_once_with(mock_request.return_value.prepare.return_value)
                mock_request.assert_called_once_with('GET', 'http://127.0.0.1:80/', params={'e': ['a', 'b', 'c']},
                                                     headers=STANDARD_HEADERS, data='')


def test_output_no_spread_params():
    h = Http()
    with patch('output.Http.send_request', MagicMock()) as mock_send:
        with patch('output.Http.get_request', MagicMock(return_value='test')):
            with patch('requests.Request', MagicMock(return_values=MagicMock(prepare=MagicMock(return_value='test')))) as mock_request:
                h.options['spread_params'] = False
                h.output(['a', 'b', 'c'])
                mock_send.assert_called_once_with(mock_request.return_value.prepare.return_value)
                mock_request.assert_called_once_with('GET', 'http://127.0.0.1:80/', params={'param': 'a\nb\nc'},
                                                     headers=STANDARD_HEADERS, data='')


def test_output_use_body():
    h = Http()
    with patch('output.Http.send_request', MagicMock()) as mock_send:
        with patch('output.Http.get_request', MagicMock(return_value='test')):
            with patch('requests.Request', MagicMock(return_values=MagicMock(prepare=MagicMock(return_value='test')))) as mock_request:
                h.options['use_body'] = True
                h.output(['a', 'b', 'c'])
                mock_send.assert_called_once_with(mock_request.return_value.prepare.return_value)
                mock_request.assert_called_once_with('GET', 'http://127.0.0.1:80/', params={}, headers=STANDARD_HEADERS,
                                                     data='a\nb\nc')


def test_output_use_body_final_separator():
    h = Http()
    with patch('output.Http.send_request', MagicMock()) as mock_send:
        with patch('output.Http.get_request', MagicMock(return_value='test')):
            with patch('requests.Request', MagicMock(return_values=MagicMock(prepare=MagicMock(return_value='test')))) as mock_request:
                h.options['use_body'] = True
                h.options['final_separator'] = True
                h.output(['a', 'b', 'c'])
                mock_send.assert_called_once_with(mock_request.return_value.prepare.return_value)
                mock_request.assert_called_once_with('GET', 'http://127.0.0.1:80/', params={}, headers=STANDARD_HEADERS,
                                                     data='a\nb\nc\n')


def test_output_content_type():
    h = Http()
    with patch('output.Http.send_request', MagicMock()) as mock_send:
        with patch('output.Http.get_request', MagicMock(return_value='test')):
            with patch('requests.Request', MagicMock(return_values=MagicMock(prepare=MagicMock(return_value='test')))) as mock_request:
                h.options['content_type'] = 'text/xml'
                h.output(['a', 'b', 'c'])
                headers = dict(STANDARD_HEADERS)
                headers['Content-Type'] = 'text/xml'
                mock_send.assert_called_once_with(mock_request.return_value.prepare.return_value)
                mock_request.assert_called_once_with('GET', 'http://127.0.0.1:80/', params={'param': ['a', 'b', 'c']},
                                                     headers=headers, data='')


def test_output_print_request():
    h = Http()
    with patch('output.Http.send_request', MagicMock()) as mock_send:
        with patch('output.Http.get_request', MagicMock(return_value='test')):
            with patch('output.Http.pretty_print_http') as mock_print_request:
                with patch('requests.Request', MagicMock(return_values=MagicMock(prepare=MagicMock(return_value='test')))) as mock_request:
                    h.options['print_request'] = True
                    h.output(['a', 'b', 'c'])
                    mock_send.assert_called_once_with(mock_request.return_value.prepare.return_value)
                    mock_request.assert_called_once_with('GET', 'http://127.0.0.1:80/',
                                                         params={'param': ['a', 'b', 'c']},
                                                         headers=STANDARD_HEADERS, data='')
                    mock_print_request.assert_called_once_with(mock_request.return_value.prepare.return_value)


def test_output_send_request():
    h = Http()
    with patch('output.Http.send_request', MagicMock()) as mock_send:
        with patch('output.Http.get_request', MagicMock(return_value='test')):
            with patch('requests.Request', MagicMock(return_values=MagicMock(prepare=MagicMock(return_value='test')))) as mock_request:
                h.options['send_request'] = False
                h.output(['a', 'b', 'c'])
                mock_send.assert_not_called()
                mock_request.assert_called_once_with('GET', 'http://127.0.0.1:80/', params={'param': ['a', 'b', 'c']},
                                                     headers=STANDARD_HEADERS, data='')


def test_output_n_requests():
    h = Http()
    with patch('output.Http.get_request', MagicMock(return_value='test')):
        with patch('multiprocessing.pool.ThreadPool') as mock_pool:
            with patch('requests.Request', MagicMock(return_values=MagicMock(prepare=MagicMock(return_value='test')))) as mock_request:
                h.options['n_requests'] = 5
                h.output(['a', 'b', 'c'])
                mock_pool.assert_called_once_with(1)
                mock_pool.return_value.map.assert_called_once_with(h.send_request, [mock_request.return_value.prepare.return_value] * 5)
                mock_pool.return_value.close.assert_called_once_with()
                mock_pool.return_value.join.assert_called_once_with()
                mock_request.assert_called_once_with('GET', 'http://127.0.0.1:80/',
                                                     params={'param': ['a', 'b', 'c']},
                                                     headers=STANDARD_HEADERS, data='')


def test_output_n_requests_n_parallel():
    h = Http()
    with patch('output.Http.get_request', MagicMock(return_value='test')):
        with patch('multiprocessing.pool.ThreadPool') as mock_pool:
            with patch('requests.Request', MagicMock(return_values=MagicMock(prepare=MagicMock(return_value='test')))) as mock_request:
                h.options['n_requests'] = 5
                h.options['n_parallel'] = 2
                h.output(['a', 'b', 'c'])
                mock_pool.assert_called_once_with(2)
                mock_pool.return_value.map.assert_called_once_with(h.send_request, [mock_request.return_value.prepare.return_value] * 5)
                mock_pool.return_value.close.assert_called_once_with()
                mock_pool.return_value.join.assert_called_once_with()
                mock_request.assert_called_once_with('GET', 'http://127.0.0.1:80/',
                                                     params={'param': ['a', 'b', 'c']},
                                                     headers=STANDARD_HEADERS, data='')


def test_send_request():
    h = Http()
    with patch('requests.Session', MagicMock()) as mock_session:
        h.send_request('p')
        mock_session.return_value.send.assert_called_once_with('p')
        mock_session.return_value.close.assert_called_once_with()


def test_get_request():
    h = Http()
    p = MagicMock(method='GET', url='http://twosixlabs.com/hello.xml', headers={'a': 'b', 'c': 'd'}, body='test test')
    ret = h.get_request(p)
    assert(ret == 'GET /hello.xml HTTP/1.1\r\nHost: twosixlabs.com\r\na: b\r\nc: d\r\n\r\ntest test')


def test_get_request_no_body():
    h = Http()
    p = MagicMock(method='GET', url='http://twosixlabs.com/hello.xml', headers={'a': 'b', 'c': 'd'}, body=None)
    ret = h.get_request(p)
    assert(ret == 'GET /hello.xml HTTP/1.1\r\nHost: twosixlabs.com\r\na: b\r\nc: d\r\n\r\n')


def test_pretty_print_http():
    h = Http()
    with patch('builtins.print', MagicMock()) as mock_print:
        with patch('output.Http.get_request', MagicMock(return_value='x')) as mock_get_request:
            h.pretty_print_http('p')
            mock_get_request.assert_called_once_with('p')
            mock_print.assert_has_calls([call(mock_get_request.return_value)])


def test_convert_item_ints_decimal():
    h = Http()
    h.options.set_value('number_format', 'decimal')
    for item in [7, 8, 15, 20]:
        assert h.convert_item(item) == str(item)


def test_convert_item_ints_hexadecimal():
    h = Http()
    h.options.set_value('number_format', 'hexadecimal')
    for item in [7, 8, 15, 20]:
        assert h.convert_item(item) == hex(item)


def test_convert_item_ints_octal():
    h = Http()
    h.options.set_value('number_format', 'octal')
    for item in [7, 8, 15, 20]:
        assert h.convert_item(item) == oct(item)


def test_convert_item_non_int():
    h = Http()
    for item in ['a', [1, 2, 3]]:
        assert h.convert_item(item) == str(item)
