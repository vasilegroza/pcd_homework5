#  Delay traffic analyzer
###  Spawn 4 vms: 
    1. S1, S2, S3 proxy pass tcp
    2. S4 80 receive request and log the data in sql database
    3. Topology: S1 -> S2 -> S3 -> S4 one of following two
        - All the servers are in the same network
### S1 generate TCP package p

    S1 ----p----> S2 ----p----> S3 ----p----> S4

S1 generates TCP package and sends it to the S4 via S2 and S3


### S4 is waiting for the TCP packages on port 80.
### S1 has the time T0 and on each forward node we log the delay of the package until we reach S4 node

### On S4 node install sql database were we will store metrics (delays and RTT)
    For each S{i} --> S{i+1} where 1<=i<=4
        1. source_ip, destination_ip, delay (let's name it delay_table)
        2. source_ip, destination_ip, rtt (let's name it rtt table)

### Setup NTP server
- Overview

           S4 - NTP Controller
          / | \
         /  |  \
        S1  S2  S3
    
- install ntp daemon and ntpdate tool
    - don't forget to change /etc/ntp.conf for s1,s2,s3 to  point to s4 for time sync.
- manual sync with 

```sh
root@s1:~# date; systemctl stop ntp; ntpdate -q s4; systemctl start ntp; date;
```
### Health check all the servers in real-time
    1. Start-up a daemon which will ping those machines and write result to local log.
    2. install and start Consul on each S{i} node and have the status check buildin. ^_^
    checkout ./start_consul.sh

