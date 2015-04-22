Quantum Insert detection for Suricata
=====================================

Suricata can already detect `QUANTUMINSERT` like attacks out of the box, using the `stream-event` called `reassembly_overlap_different_data`.

Combining the `stream-event` with a signature detecing a `HTTP 302` redirect one could easily detect malicious HTTP redirects.

Ofcourse the payload could also contain other content, such as malicious javascript.

Signatures
----------
Victor Julien shared the following signatures for detecting `QUANTUMINSERT`:

	alert tcp any any -> any any (msg:"SURICATA STREAM reassembly overlap with different data"; stream-event:reassembly_overlap_different_data; classtype:protocol-command-decode; sid:2210050; rev:2;)
	alert tcp any any -> any any (msg:"LOCAL QI 302 and possible inject"; stream-event:reassembly_overlap_different_data; content:"302"; http_stat_code; classtype:protocol-command-decode; sid:12345; rev:2;)

References
----------

 * http://blog.inliniac.net/2013/04/19/suricata-handling-of-multiple-different-synacks/
 * https://redmine.openinfosecfoundation.org/issues/603
 * https://github.com/inliniac/suricata/commit/6f76ac176d70d85fa2a5719dacdc8fef0ef074dc