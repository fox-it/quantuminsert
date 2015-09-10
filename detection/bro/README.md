Quantum Insert detection for Bro-IDS
===================================

Fox-IT made a proof of concept policy for Bro-IDS to detect `QUANTUMINSERT` attacks. This policy using the `tcp_packet` event has now been deprecated in favour for a patch that improves the `rexmit_inconsistency` event.

The README and the old policy utilizing the `tcp_packet` event can still be found [here](./old).

Patches are available for following stable Bro versions:

 * `bro-2.4.1`: [rexmit_inconsistency-bro-2.4.1.patch](./rexmit_inconsistency-bro-2.4.1.patch)
 * `bro-2.3.2`: [rexmit_inconsistency-bro-2.3.2.patch](./rexmit_inconsistency-bro-2.3.2.patch)

~~We hope it will be patched upstream as well.~~

The patch has been merged in https://github.com/bro/bro/commit/c1f060be63ad72d37b37e5649887d4c047c116e1 on 28 June 2015.

Patch for `rexmit_inconsistency`
--------------------------------

This patch fixes the `rexmit_inconsistency` event for Quantum Insert attacks. See also the Bro ticket ([BIT-1314](https://bro-tracker.atlassian.net/browse/BIT-1314)) regarding detection of `QUANTUM INSERT`.

The patch improves the TCP_Reassembler class so that it can keep a history of old TCP segments. How many segments it will track can be configured using the
`tcp_max_old_segments` option. A value of zero will disable it. We recommend setting it to a low number, such as 10:

```bro
const tcp_max_old_segments = 10 &redef;
```

This will mean that every TCP session will keep a maximum of 10 extra TCP segments in memory which is still reasonable.

An overlapping segment with different data can indicate a possible TCP injection attack. 

### Applying the patch

Unpack the Bro 2.3.2 source:

```shell
tar -zxvf bro-2.3.2.tar.gz
```
	
Apply the patch

```shell
git apply < rexmit_inconsistency-bro-2.3.2.patch
```
	
Configure and make as normal.

### Testing the patch

You can use the following example policy for testing:

```bro
const tcp_max_old_segments = 10 &redef;
event rexmit_inconsistency(c: connection, t1: string, t2: string)
	{
    print(fmt("POSSIBLE QUANTUM INSERT: %s: %s <> %s\n", c$id, t1, t2));
	}
```

Save it as `test-qi-patch.bro` and test it against one of our QI pcaps:

```shell
bro --no-checksums -r qi_internet_SYNACK_curl_jsonip.pcap test-qi-patch.bro
```

You should see the following on stdout:

	POSSIBLE QUANTUM INSERT: [orig_h=178.200.100.200, orig_p=39976/tcp, resp_h=96.126.98.124, resp_p=80/tcp]: HTTP/1.1 200 OK^M^JContent-Length: 5^M^J^M^JBANG! <> HTTP/1.1 200 OK^M^JServer: nginx/1.4.4^M^JDate:^J


### Remarks
The default `weirds.bro` already logs the `rexmit_inconsistency` event as `Conn::Retransmission_Inconsistency`.
Just ensure that you define the `tcp_max_old_segments` variable in your Bro config, e.g. in `init-bare.bro`.


References
----------

 * https://bro-tracker.atlassian.net/browse/BIT-1314
 * http://mailman.icsi.berkeley.edu/pipermail/bro/2014-July/007141.html
 * https://github.com/bro/bro/commit/c1f060be63ad72d37b37e5649887d4c047c116e1
