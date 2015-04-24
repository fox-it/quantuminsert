Quantum Insert PCAPS
====================

Example pcaps containing `QUANTUMINSERT` attacks created in a controlled environment. 

> PCAPS or it didn't happen!

We have shared the annotated pcapng files with [CloudShark](https://appliance.cloudshark.org/blog/quantuminsert-analysis-capture/).

curl jsonip.com
-----------------------
We shot on our client making a request to `jsonip.com` using curl. The payload is a simple textual payload containing `BANG!`. We shot on the SYN+ACK of the server.

 * [qi_local_SYNACK_curl_jsonip.pcap](qi_local_SYNACK_curl_jsonip.pcap) (view [annotated version](https://www.cloudshark.org/captures/ea5002f082f9) on CloudShark)
 
The following pcap is the same but over the real internet:

 * [qi_internet_SYNACK_curl_jsonip.pcap](qi_internet_SYNACK_curl_jsonip.pcap) (view [annotated version](https://www.cloudshark.org/captures/918b07d06902) on CloudShark)
 
putty.exe download
------------------
We shot on a client downloading `putty.exe` from the official PuTTY website.
The inserted payload contains a redirect to a different url and executable, namely that of 7zip. Browser sucessfully downloaded the `7z938.exe` instead of `putty.exe`. The shot was performed on the SYN+ACK of the PuTTY download server (the.earth.li).
 
 * [qi_local_SYNACK_putty_dl.pcap](qi_local_SYNACK_putty_dl.pcap) (view [annotated version](https://www.cloudshark.org/captures/54394cac6297) on CloudShark)

The `Content-Length: 0` header ensures that the original response is ignored after our inserted content.


302 HTTP Redirects
-------------------
The following pcaps contains a HTTP 302 redirect to `http://www.fox-it.com`, which we shot on the SYN+ACK of `slashdot.org` and `www.linkedin.com`. The browser was succesfully redirected as can be seen in the pcaps.

 * [qi_local_SYNACK_linkedin_redirect.pcap](qi_local_SYNACK_linkedin_redirect.pcap) (view [annotated version](https://www.cloudshark.org/captures/ceec4d3636c0) on CloudShark)
 * [qi_local_SYNACK_slashdot_redirect.pcap](qi_local_SYNACK_slashdot_redirect.pcap) (view [annotated version](https://www.cloudshark.org/captures/fc259c97fab9) on CloudShark)
 
The following pcap is also a redirect, but shot on the client's actual HTTP GET request after checking the unique identifier in the `Cookie` header:

 * [qi_local_GET_slashdot_redirect.pcap](qi_local_GET_slashdot_redirect.pcap) (view [annotated version](https://www.cloudshark.org/captures/b5524b5950ab) on CloudShark)

The `Content-Length: 0` header ensures that the original response is ignored after our inserted content.

Malicious Javascript
--------------------
The following pcap contains a malicious javascript response that is inserted when the browser visits `imgur.com`.
The shot is done on the SYN+ACK of the following url `http://platform.twitter.com/widgets.js`, which is loaded by imgur.com.

 * [qi_local_SYNACK_imgur_qdp.pcap](qi_local_SYNACK_imgur_qdp.pcap) (view [annotated version](https://www.cloudshark.org/captures/334234f85e96) on CloudShark)

The `Content-Length: 108` header ensures that the original response is ignored after our inserted javascript payload.

