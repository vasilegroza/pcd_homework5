import socketserver
BUFFER_SIZE = 1214
# to do 
# 1. make server to listen at the port 80
#   - receive package and store delays to the db;
class TCPHandler(socketserver.StreamRequestHandler):

    def handle(self):

        print("Connected address: {}".format(self.client_address[0]))
        data = self.request.recv(BUFFER_SIZE)
        print('received from client', data)

    def finish(self):
        print('Done')
        return socketserver.BaseRequestHandler.finish(self)

def run_tcp_server(HOST, PORT):

    server = socketserver.TCPServer((HOST, PORT), TCPHandler)
    server.serve_forever()



if __name__ == "__main__":

    HOST, PORT = "localhost", 9999

    run_tcp_server(HOST, PORT)
