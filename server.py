import socketserver
from struct import pack, unpack
import time
import datetime

BUFFER_SIZE = 1214
# to do 
# 1. make server to listen at the port 80
#   - receive package and store delays to the db;
#   - unpack it and get timestam date = datetime.datetime.fromtimestamp(your_timestamp)
#   - first of all have to know which requesti is which unpack('c',package[:1])
class TCPHandler(socketserver.StreamRequestHandler):

    def handle(self):

        print("Connected address: {}".format(self.client_address[0]))
        data = self.request.recv(BUFFER_SIZE)
        if(data[:1]==b'd'):
            self.handle_delay_request(data)

    def finish(self):
        print('Done')
        return socketserver.BaseRequestHandler.finish(self)
    def handle_delay_request(self, data):
        char, date = unpack('c26s', data)
        time0 = datetime.datetime.strptime(date.decode(),"%Y-%m-%d %H:%M:%S.%f")
        time0 = time.mktime(time0.timetuple())
        time1 = time.time()
        delay = time1-time0
        print('delay----->', delay)

def run_tcp_server(HOST, PORT):

    server = socketserver.TCPServer((HOST, PORT), TCPHandler)
    server.serve_forever()



if __name__ == "__main__":

    HOST, PORT = "localhost", 9999

    run_tcp_server(HOST, PORT)
