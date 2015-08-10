##! Detect Quantum Insert
#
# qi.bro
#
# Fox-IT Security Research Team <srt@fox-it.com>
# 

@load base/frameworks/notice

module QuantumInsert;

export {
    redef enum Notice::Type += {
        ## Indicates that a host performed a possible Quantum Insert
        PayloadDiffers,
    };
}

export {
    redef record connection += {
        last_seq: count &optional;
        last_payload: string &optional;
    };
}

event tcp_packet (c: connection, is_orig: bool, flags: string, seq: count, ack: count, len: count, payload: string)
{
    # only process first server response and responses with data and only if the connection is established
    if (c$resp$state != TCP_ESTABLISHED || is_orig || len == 0) {
        return;
    }

    # check if we receive a packet with duplicate sequence numbers (only track the last seq)
    if (c?$last_payload && seq == c$last_seq) {
        local last_payload = c$last_payload;
        local last_len = |last_payload|;

        # if payloads are of equal length then this is a false positive more than likely so exit
        if (last_len == len) {
            return;
        } else {
            local other_payload = payload;
        }

        # one side of the payload can be smaller, so only compare the smallest.
        if (last_len < len) {
            other_payload = sub_bytes(payload, 0, last_len);
        } else if (last_len > len) {
            last_payload = sub_bytes(last_payload, 0, len);
        }

        # if payload differs it's a possible QI
        if (last_payload != other_payload) {
            print(fmt("POSSIBLE QI: sequence %s: %s:%s <- %s:%s -- [%s] differs from [%s]", 
                    seq, c$id$orig_h, c$id$orig_p, c$id$resp_h, c$id$resp_p,
                    payload, other_payload));
            NOTICE([$note=QuantumInsert::PayloadDiffers,
                $msg=fmt("Possible QuantumInsert detected. Payload differs (%s, %s): [%s], [%s]",
                        last_len, len, last_payload, other_payload),
                $conn=c,
                $identifier=c$uid
            ]);
        }
    }
    
    # keep track of payload and seq from server
    c$last_payload = payload;
    c$last_seq = seq;
}
