import os
import requests
import multiprocessing.pool

from acsploit.options import Options
from . import output_common


class Http:
    """Http class."""

    OUTPUT_NAME = 'http'  # exploits can use this internally to whitelist/blacklist supported output formats

    _SEPARATORS = {
        'newline': '\n',
        'comma': ',',
        'space': ' ',
        'tab': '\t',
        'os_newline': os.linesep,
        'CRLF': '\r\n',
        'none': ''
    }

    def __init__(self):
        """Initialize the Http class."""
        self.options = Options()
        self.options.add_option('url', 'http://127.0.0.1:80/', 'Host to connect to')
        self.options.add_option('separator', 'newline', 'Separator between elements',
                                list(self._SEPARATORS.keys()), True)
        self.options.add_option('final_separator', False, 'Whether to end output with an instance of the separator')
        self.options.add_option('number_format', 'decimal', 'Format for numbers', ['decimal', 'hexadecimal', 'octal'])

        # TODO - eventually support PUT, DELETE, HEAD, and OPTIONS, since requests easily handles those
        self.options.add_option('http_method', 'GET', 'Type of HTTP request to make', ['POST', 'GET'])
        self.options.add_option('content_type', '', 'Content-Type header for the HTTP request')
        self.options.add_option('url_param_name', 'param', 'Name of URL arg(s) to use')
        self.options.add_option('spread_params', True, 'Put each output in its own URL arg, as opposed to all in one')
        self.options.add_option('use_body', False, 'Put exploit output in body, not URL args')

        self.options.add_option('print_request', False, 'Print HTTP request')
        self.options.add_option('send_request', True, 'Send HTTP request')

        self.options.add_option('n_requests', 1, 'Total number of times to send the request')
        self.options.add_option('n_parallel', 1, 'Number of requests to send simultaneously')

    # TODO - eventually allow printing out http response?
    def output(self, output_list):
        """Create an HTTP request and send the payload."""
        url_payload = {}
        data_payload = ''
        separator = output_common.get_separator(self.options['separator'], self._SEPARATORS)

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
        if self.options['content_type'] != '':
            standard_headers['Content-Type'] = self.options['content_type']

        # Must use HTTP or HTTPS; default to http if user has not specified
        url = self.options['url']
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url

        req = requests.Request(self.options['http_method'], url, params=url_payload, headers=standard_headers,
                               data=data_payload)
        prepared = req.prepare()

        if self.options['print_request']:
            self.pretty_print_http(prepared)

        if self.options['send_request'] and self.options['n_requests'] > 0:
            request = self.get_request(prepared)

            if self.options['n_requests'] == 1:
                print('Sending HTTP request (est. {} bytes)'.format(len(request)))
                self.send_request(prepared)

            else:
                pool = multiprocessing.pool.ThreadPool(self.options['n_parallel'])
                print('Sending {} HTTP requests (est. {} bytes each)'.format(self.options['n_requests'], len(request)))

                # This will send n_parallel requests at once; each thread blocks until receiving a response
                # Each thread continues sending requests until n_requests have been sent in total across all threads
                pool.map(self.send_request, [prepared]*self.options['n_requests'])
                pool.close()
                pool.join()

            print('All HTTP requests sent')

    def send_request(self, prepared_req):
        s = requests.Session()
        s.send(prepared_req)
        s.close()

    # NOTE: This is only an approximation of the request that will actually be sent
    #       The requests API does not expose the actual bytes of a request that will be sent over the wire
    #       If using HTTPS, will return the unencrypted HTTP payload, not the TLS payloads
    def get_request(self, prepared_req):
        _, full_url = prepared_req.url.split('://', maxsplit=1)  # Strip http:// or https://
        url, _, path = full_url.partition('/')  # Requests formats the url so there should always be a '/'
        headers = ''.join('{}: {}\r\n'.format(k, v) for k, v in prepared_req.headers.items())
        body = '' if prepared_req.body is None else prepared_req.body
        request = '{} /{} HTTP/1.1\r\nHost: {}\r\n{}\r\n{}'.format(prepared_req.method, path, url, headers, body)
        return request

    def pretty_print_http(self, prepared_req):
        """Print readable http output."""
        print('-----------START-----------')
        print(self.get_request(prepared_req))
        print('------------END------------')

    def convert_item(self, item):
        """Convert output to a str type."""
        # NB: this doesn't recurse onto lists
        if type(item) is int:
            if self.options['number_format'] == 'hexadecimal':
                item = hex(item)
            elif self.options['number_format'] == 'octal':
                item = oct(item)

        return str(item)
