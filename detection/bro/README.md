Quantum Insert detection for Bro-IDS
===================================

Fox-IT made a proof of concept policy for Bro-IDS to detect `QUANTUMINSERT` attacks.

The Bro policy is released into the public domain.

Install
-------

Add the `qi.bro` policy to your `local.bro` file, eg:

	@load qi.bro

Testing
-------

You can also run the policy directly on a pcap file:

	bro --no-checksums -r ../pcaps/qi_putty_dl.pcap qi.bro

The policy will print hits to stdout and log to `notice.log`, example:

	POSSIBLE QI: sequence 1: 10.0.1.4:51358/tcp <- 46.43.34.31:80/tcp --
	[HTTP/1.1 302 Found^M^JDate: Tue, 21 Apr 2015 00:41:55 GMT^M^JServer: Apache^M^JLocation: http://the.earth.li/~sgtatham/putty/0.64/x86/putty.exe^M^JContent-Length: 300^M^JKeep-Alive: timeout=15, max=100^M^JConnection: Keep-Alive^M^JContent-Type: text/html; charset=iso-8859-1^M^J^M^J<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">^J<html><head>^J<title>302 Found</title>^J</head><body>^J<h1>Found</h1>^J<p>The document has moved <a href="http://the.earth.li/~sgtatham/putty/0.64/x86/putty.exe">here</a>.</p>^J<hr>^J<address>Apache Server at the.earth.li Port 80</address>^J</body></html>^J]	
	differs from	
	[HTTP/1.1 302 Found^M^JLocation: http://www.7-zip.org/a/7z938.exe^M^JContent-Length: 0^M^J^M^J]

Technical details of the policy
-------------------------------
We initially thought we could trigger `weird.log` events using Bro on our pcaps containing a Quantum Insert like attack.
Especially as Bro has an event called `rexmit_inconsistency`. However this event seems not capable of detecting Quantum Insert as it does not keep a history of TCP segments.

Our Bro policy does not make use of this event, but rather tracks the first content carrying TCP packet. If another TCP packet claims to be the first content it will be compared.
If they are different it will trigger an event.

Currently the policy uses a less ineffecient `tcp_packet` event.
It should be feasible to make improvements to internals of Bro, to (optionally) keep track of a sliding window of (ACKed and/or unACKed) TCP segments.
This way the `rexmit_inconsistency` event could make use of it and fire the event based on the sliding window.


References
----------

 * https://bro-tracker.atlassian.net/browse/BIT-1314
 * http://mailman.icsi.berkeley.edu/pipermail/bro/2014-July/007141.html
