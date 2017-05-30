import sys
from scapy.all import *

dest_ip=sys.argv[1]
min_port=int(sys.argv[2])
max_port=int(sys.argv[3])
src_port=sys.argv[4]


def scan_port(port):
    pkt=IP(dst=str(dest_ip))/TCP(sport=int(src_port), dport=port,flags="S")
    conf.verb=0
    sapack=sr1(pkt)
    flag=sapack.getlayer(TCP).flags
    if flag==0x12:
        return True
    else:
        return False
    rst=IP(dst=str(dest_ip))/TCP(sport=int(src_port), dport=port,flags="R")
    send(rst)

print "[*] Port Taramasi Basladi"
for i in range(min_port,max_port+1):
    if scan_port(i):
        print "[+] Port ",i," acik"

