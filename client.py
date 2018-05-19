import socket
from random import choice
from string import ascii_uppercase
import time 

HOST, PORT = "localhost", 9999

BUFFER_SIZE = 1214
# to do 
# 1. make client to start with args 
#   - client_type ex proxy --> (s2, s3)[have to listhen to the tcp connection too], normal s1.
#   - endpoint (aka hostname to the next pont for tcp package to get)
#   - analysed_metric one of [delay, rtt]
# 2. calculate delay and rtt
#   - find a elegant way to calculate rtt and store it in sql
#   - can get timestamp store it in package and forward the pachage for delay
#   - time_send: C -->S: time_receive S---> C time_ack  rtt = time_ack-time_send; store it to the sql 
def client_tcp():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, 32)

    try:

        sock.connect((HOST, PORT))
        print(sock.send(str.encode(''.join(choice(ascii_uppercase) for i in range(1214)))))

    finally:
        sock.close()

client_tcp()