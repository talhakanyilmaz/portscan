#!/usr/bin/python

import time
import random
import struct
import select
import socket
import sys
import dpkt
class ICMP(dpkt.Packet):
    __hdr__ = (
        ('type', 'B', 8),
        ('code', 'B', 0),
        ('sum', 'H', 0)
        )
    class Echo(dpkt.Packet):
        __hdr__ = (('id', 'H', 0), ('seq', 'H', 0))
def paket_olustur(boyut):
    echo = dpkt.icmp.ICMP.Echo()
    echo.id = random.randint(0, 0xffff)
    echo.seq = random.randint(0, 0xffff)
    echo.data = '1'
    for i in range(boyut-9):
    	echo.data = echo.data + '1'
    icmp = dpkt.icmp.ICMP()
    icmp.type = dpkt.icmp.ICMP_ECHO
    icmp.data = echo
    return icmp
def ping(addr,boyut):
        protokol=socket.getprotobyname('icmp')
    	baglanti = socket.socket(socket.AF_INET, socket.SOCK_RAW, protokol)
        payload = paket_olustur(boyut)
        try:
            ip=socket.gethostbyname(addr)
        except socket.gaierror:
            return False
        baglanti.connect((ip, 80))
        gonderilen=baglanti.send(str(payload))
        start = time.time()
        print ip
        alinan=False
        while select.select([baglanti], [], [], max(0, start + 1 - time.time()))[0]:
            alinan = baglanti.recv(65536)
            if len(alinan) < boyut+1 or len(alinan) < struct.unpack_from('!xxH', alinan)[0]:
                continue
        if alinan:
            return True
        else:
            return False
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(ping(sys.argv[1],56))
    else:
        print(ping(sys.argv[1],int(sys.argv[2])))
