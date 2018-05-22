import socketserver
from struct import pack, unpack
import time
import socket

import datetime
import argparse
import os
from utils import store_metric_to_db
print()

BUFFER_SIZE = 1214
MY_IP = socket.gethostbyname(socket.gethostname())
if MY_IP.startswith('127.'):
    MY_IP = os.environ['MY_IP']

parser = argparse.ArgumentParser()

parser.add_argument("server_type", type=str,
                    help="please provide server type  final/proxy")
parser.add_argument("-listen_port", type=str,
                    help="please provide server listen port (default is 80)")

parser.add_argument("-proxy_pass",
                    help="please input the target hostname if server is proxy")
parser.add_argument("-proxy_port",
                    help="please input the target port if server proxy")

args = parser.parse_args()
print(args)


# to do
# 1. make server to listen at the port 80
#   - receive package and store delays to the db;
#   - unpack it and get timestam date = datetime.datetime.fromtimestamp(your_timestamp)
#   - first of all have to know which requesti is which unpack('c',package[:1])
class TCPHandler(socketserver.StreamRequestHandler):

    def handle(self):

        # print("Connected address: {}".format(self.client_address[0]))
        data = self.request.recv(BUFFER_SIZE)
        if (data[:1] == b'd'):
            self.handle_delay_request(data)
        else:
            self.handle_rtt_request(data)

    def finish(self):
        print('Done')
        return socketserver.BaseRequestHandler.finish(self)

    def handle_delay_request(self, data):
        time1 = datetime.datetime.now()
        char, t0 = unpack('c26s', data)
        # print(t0)
        time0 = datetime.datetime.strptime(t0.decode(), "%Y-%m-%d %H:%M:%S.%f")
        diff = time1 - time0
        # print(time0)
        # print(time1)
        print(diff.days, diff.seconds, diff.microseconds)
        delay_ms = (diff.days * 86400000) + (diff.seconds * 1000) + (diff.microseconds / 1000)
        # store client_ip, my_ip, delay_ms
        store_metric_to_db('delay', self.client_address[0], MY_IP, delay_ms)
        print(args.server_type)
        if args.server_type == 'final':
            pass
        else:
            # to do: 
            # forward request
            
            print('forward the request to ', args.proxy_pass)
            do_proxy_delay_metric(args.proxy_pass, int(args.proxy_port))
            pass

    def handle_rtt_request(self, data):
        pass

def do_proxy_delay_metric(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, 32)
    now = time.time()
    date = datetime.datetime.fromtimestamp(now).strftime("%Y-%m-%d %H:%M:%S.%f")
    package = pack('c26s',b'd',date.encode())
    print(package)
    try:
        sock.connect((host, port))
        sock.send(package)
    finally:
        print('close socket')
        sock.close()


def run_tcp_server(HOST, PORT):
    server = socketserver.TCPServer((HOST, PORT), TCPHandler)
    server.serve_forever()


if __name__ == "__main__":

    port = 80
    print(args)
    if args.listen_port is not None:
        port = int(args.listen_port)
    print(port)
    HOST, PORT = "0.0.0.0", port

    run_tcp_server(HOST, PORT)
