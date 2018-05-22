import socket
import random 
from struct import pack, unpack
import time
import datetime
import argparse




HOST, PORT = 's2', 80

BUFFER_SIZE = 1214
# to do
# 1. make client to start with args
#   + client_type ex proxy --> (s2, s3)[have to listhen to the tcp connection too], normal s1.
#   + endpoint (aka hostname to the next pont for tcp package to get)
# 2. calculate delay and rtt
#   - find a elegant way to calculate rtt and store it in sql
#   - can get timestamp store it in package and forward the pachage for delay
#   - time_send: C -->S: time_receive S---> C time_ack  rtt = time_ack-time_send; store it to the sql

# package format  
def do_delay_metric():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, 32)
    now = time.time()
    date = datetime.datetime.fromtimestamp(now).strftime("%Y-%m-%d %H:%M:%S.%f")
    package = pack('c26s',b'd',date.encode())
    print(package)
    try:
        sock.connect((HOST, PORT))
        sock.send(package)
    finally:
        print('close socket')
        sock.close()

def do_rtt_metric():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, 32)
    try:
        sock.connect((HOST, PORT))
        # print(sock.send(str.encode(''.join(random.choice(ascii_uppercase)
                                        #    for i in range(1214)))))
    finally:
        sock.close()

def do_metrics():
    """
    This function will call two functions one for delay metric
    and other for rtt metric.
    """
    do_delay_metric()
    # do_rtt_metric()
    

def main():
    while 1:
        do_metrics()
        sleep_time = random.randint(5,10)
        print('sleep', sleep_time)
        time.sleep(sleep_time)

    pass
if __name__=="__main__":
    """
    This is the entrypoint of the current script
    """
    main()
