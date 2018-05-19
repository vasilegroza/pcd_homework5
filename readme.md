# Delay traffic analyzer
### Spawn 4 vms: 
    1. S1, S2, S3 proxy pass tcp
    2. S4 80 receive request and log the data in sql database
    3. Topology: S1 -> S2 -> S3 -> S4 one of following two
        - Toate serverele sunt in aceeasi retea
        - Cel putin 2 servere sa fie in retele diferite
### S1 generate TCP package p

    S1 ----p----> S2 ----p----> S3 ----p----> S4

De pe S1 se genereaza pachete TCP, care vor trece prin S2, S3 cu destinatia S4.

### S4 receptioneaza pachetele TCP pe portul 80.
### S1 reprezinta momentul T0 si in fiecare hop trebuie inregistrat delay-ul pachetelor
pana la destinatia S4.
f. In S4 se instaleaza o baza de date sql (la alegere) in care vor fi inregistrate
rezultatele: ip sursa, ip destinatie, delay la fiecare hop, RTT intre fiecare server (de la S(i)
la S(i+1), 1<=i<=4),
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

    consul.