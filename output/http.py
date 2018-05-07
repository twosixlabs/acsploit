import os
import requests
from options import Options


class Http:

    OUTPUT_NAME = 'http'  # exploits can use this internally to whitelist/blacklist supported output formats

    _SEPARATORS = {  # as bytes because
        'newline': b'\n',
        'comma': b',',
        'space': b' ',
        'tab': b'\t',
        'os_newline': bytes(os.linesep.encode()),
        'CRLF': b'\r\n',
        'none': b''
    }

    def __init__(self):
        self.options = Options()
        self.options.add_option('url', 'http://127.0.0.1:80/', 'Host to connect to')
        self.options.add_option('separator', 'newline', 'Separator between elements', ['newline', 'comma', 'space',
                                                                                       'tab', 'os_newline', 'CRLF',
                                                                                       'none'])
        self.options.add_option('custom_separator', '', 'Custom separator to override "separator"')
        self.options.add_option('final_separator', False, 'Whether to end output with an instance of the separator')
        self.options.add_option('number_format', 'decimal', 'Format for numbers', ['decimal', 'hexadecimal', 'octal'])

        # TODO - eventually support PUT, DELETE, HEAD, and OPTIONS, since requests easily handles those
        self.options.add_option('http_method', 'GET', 'Type of HTTP request to make', ['POST', 'GET'])
        self.options.add_option('url_param_name', 'param', 'Name of URL arg(s) to use')
        self.options.add_option('spread_params', True, 'Put each output in its own URL arg, as opposed to all in one')
        self.options.add_option('use_body', False, 'Put exploit output in body, not URL args')

        self.options.add_option('print_request', False, 'Print HTTP request')
        self.options.add_option('send_request', True, 'Send HTTP request')

    # TODO - eventually allow printing out http response?
    def output(self, output_list):
        url_payload = {}
        data_payload = ''
        if self.options['custom_separator'] != '':
            separator = self.options['custom_separator'].encode()
        else:
            separator = Http._SEPARATORS[self.options['separator']]

        if self.options['use_body']:
            data_payload = separator.join([self.convert_item(item) for item in output_list])
            if self.options['final_separator']:
                data_payload += separator
        else:
            if self.options['spread_params']:
                url_payload[self.options['url_param_name']] = [self.convert_item(item) for item in output_list]
            else:
                line = separator.join([self.convert_item(item) for item in output_list])
                if self.options['final_separator']:
                    line += separator
                url_payload = {self.options['url_param_name']: line}

        standard_headers = {'User-Agent': 'python-requests', 'Accept-Encoding': 'gzip, deflate',
                            'Connection': 'keep-alive', 'Accept': '*/*'}
        req = requests.Request(self.options['http_method'], self.options['url'], params=url_payload,
                               headers=standard_headers, data=data_payload)
        prepared = req.prepare()

        if self.options['print_request']:
            self.pretty_print_http(prepared)

        if self.options['send_request']:
            s = requests.Session()
            print('Sending HTTP request...')
            s.send(prepared)    # TODO - eventually wrap this in try/except for ConnectionError?
            print('HTTP request sent.')
            s.close()

    def pretty_print_http(self, prepared_req):
        print(str('{}'+os.linesep+'{}'+os.linesep+'{}').format(
            '-----------START-----------',
            prepared_req.method + ' ' + prepared_req.url,
            os.linesep.join('{}: {}'.format(k, v) for k, v in prepared_req.headers.items())
        ))

        if self.options['use_body']:
            print(str(os.linesep + '{}').format(prepared_req.body.decode()))
            print('{}'.format('------------END------------'))
        else:
            print(str(os.linesep + '{}').format('------------END------------'))

    def convert_item(self, item):
        # NB: this doesn't recurse onto lists
        if type(item) is int:
            if self.options['number_format'] == 'hexadecimal':
                item = hex(item)
            elif self.options['number_format'] == 'octal':
                item = oct(item)
        if type(item) is not bytes:
            item = str(item).encode()  # TODO: this is a bit of a hack, to put it mildly

        return item
