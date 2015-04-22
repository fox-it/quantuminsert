Quantum Insert PCAPS
====================

Example pcaps containing `QUANTUMINSERT` attacks created in a controlled environment. 

> PCAPS or it didn't happen!

curl jsonip.com
-----------------------
We shot on our client making a request to `jsonip.com` using curl. The payload is a simple textual payload containing `BANG!`. We shot on the SYN+ACK of the server.

 * [qi_local_SYNACK_curl_jsonip.pcap](qi_local_SYNACK_curl_jsonip.pcap)
 
The following pcap is the same but over the real internet:

 * [qi_internet_SYNACK_curl_jsonip.pcap](qi_internet_SYNACK_curl_jsonip.pcap)
 
putty.exe download
------------------
We shot on a client downloading `putty.exe` from the official PuTTY website.
The inserted payload contains a redirect to a different url and executable, namely that of 7zip. Browser sucessfully downloaded the `7z938.exe` instead of `putty.exe`. The shot was performed on the SYN+ACK of the PuTTY download server (the.earth.li).
 
 * [qi_local_SYNACK_putty_dl.pcap](qi_local_SYNACK_putty_dl.pcap)

The `Content-Length: 0` header ensures that the original response is ignored after our inserted content.


302 HTTP Redirects
-------------------
The following pcaps contains a HTTP 302 redirect to `http://www.fox-it.com`, which we shot on the SYN+ACK of `slashdot.org` and `www.linkedin.com`. The browser was succesfully redirected as can be seen in the pcaps.

 * [qi_local_SYNACK_linkedin_redirect.pcap](qi_local_SYNACK_linkedin_redirect.pcap)
 * [qi_local_SYNACK_slashdot_redirect.pcap](qi_local_SYNACK_slashdot_redirect.pcap)
 
The following pcap is also a redirect, but shot on the client's actual HTTP GET request after checking the unique identifier in the `Cookie` header:

 * [qi_local_GET_slashdot_redirect.pcap](qi_local_GET_slashdot_redirect.pcap)

The `Content-Length: 0` header ensures that the original response is ignored after our inserted content.

Malicious Javascript
--------------------
The following pcap contains a malicious javascript response that is inserted when the browser visits `imgur.com`.
The shot is done on the SYN+ACK of the following url `http://platform.twitter.com/widgets.js`, which is loaded by imgur.com.

 * [qi_local_SYNACK_imgur_qdp.pcap](qi_local_SYNACK_imgur_qdp.pcap)

The `Content-Length: 108` header ensures that the original response is ignored after our inserted javascript payload.

