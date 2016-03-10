This directory contains the modified monitor and shooter scripts that were
used for the BroCon 2015 demo.

monitor
-------
No real changes other than switching back to old OptionParser module for Python 2.6 support.

``stdbuf --output=0 tcpdump -nn -i eth0 "host jsonip.com and port 80 and tcp[tcpflags]=(tcp-syn|tcp-ack)" | python monitor.py -s 10.0.0.3``

``stdbuf --output=0 tcpdump -nn -i eth0 "host bro.org and port 80 and tcp[tcpflags]=(tcp-syn|tcp-ack)" | python monitor.py -s 10.0.0.3``

shooter
-------
The modifications allow for sending multiple QI packets to account for MTU.
Also supports compressing the HTML page and injecting a javascript file.

``python shooter.py --response index.html --inject inject.js``

index.html
----------
The `index.html` is a mirror of the `bro.org` main page using `wget -k` to fix relative links to absolute.

inject.js
---------
This file is the javascript that is injected after the `<body>` tag of the content. It's a modified javascript file that performs the Harlem Shake.
