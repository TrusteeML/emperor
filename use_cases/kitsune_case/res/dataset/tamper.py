import scapy.all as scapy
from scapy.utils import rdpcap, wrpcap

from random import randrange


PCAP_PATH = "mirai.pcap"
OUTPUT_PATH = ""


def tamper_no_arp(limit_start, limit_end):
    packets_per_second = {}
    limits_per_second = {}
    count = 0

    pkts = rdpcap(PCAP_PATH)
    arp_resps = set({})
    cooked = []
    last_key_ok = 0
    skipped_packets = 0
    print("READING PCAP", PCAP_PATH)
    for idx, p in enumerate(pkts):
        next_p = None
        count += 1
        if count % 1000 == 0:
            print(count)

        if (
            p.haslayer(scapy.ARP)
            and p[scapy.Ether].dst == "3c:33:00:98:ee:fd"
            and p[scapy.ARP].op == 2
            and str(p.time) in arp_resps
        ):
            print("SKIPPING PACKET")
            skipped_packets += 1
            continue

        key = int(p.time)
        if key not in packets_per_second:
            packets_per_second[key] = 0
            limits_per_second[key] = randrange(limit_start, limit_end)

        num_pkts_to_inc = 1
        if count > 120000:  # to make sure we only affect attack traffic
            if (
                p.haslayer(scapy.ARP)
                and p[scapy.Ether].src == "3c:33:00:98:ee:fd"
                and not p[scapy.ARP].op == 2
            ):
                last_arp_time_inc = 0
                # print(packets_per_second[key], limits_per_second[key])
                while packets_per_second[key] > limits_per_second[key]:
                    # print("Over the limit", packets_per_second[key], limit)
                    inc = max(last_key_ok - int(p.time), 0)
                    last_arp_time_inc = int(p.time)
                    p.time += inc
                    key = int(p.time)
                    if key not in packets_per_second:
                        packets_per_second[key] = 0
                        limits_per_second[key] = randrange(limit_start, limit_end)

                    if packets_per_second[key] > limits_per_second[key]:
                        p.time += 1

                if idx + 1 < len(pkts):  # if pcap is not over
                    next_p = pkts[idx + 1]
                    # if the next packet is an ARP response from the previous ARP request
                    if (
                        next_p.haslayer(scapy.ARP)
                        and next_p[scapy.Ether].dst == "3c:33:00:98:ee:fd"
                        and next_p[scapy.ARP].op == 2
                        and next_p[scapy.ARP].pdst == p[scapy.ARP].psrc
                    ):
                        # print(next_p[scapy.ARP].pdst, p[scapy.ARP].psrc)
                        # print("LAST ARP INC", last_arp_time_inc)
                        arp_resps.add(str(next_p.time))
                        next_p.time += last_arp_time_inc  # if an ARP response from
                        num_pkts_to_inc += 1

        last_key_ok = key
        packets_per_second[key] += num_pkts_to_inc
        cooked.append(p)
        if num_pkts_to_inc > 1 and next_p:
            print("added ARP response")
            cooked.append(next_p)
    print("SKIPPED PACKETS", skipped_packets)
    print("NEW PCAP LEN", len(cooked), len(pkts))
    print("WRITING PCAP", limit_start, limit_end)
    wrpcap(f"mirai_tampered_{limit_start}-{limit_end}.pcap", cooked)
    print("DONE")


def tamper(limit_start, limit_end):
    packets_per_second = {}
    limits_per_second = {}
    count = 0

    print("READING PCAP", PCAP_PATH)
    pkts = rdpcap(PCAP_PATH)
    cooked = []
    last_key_ok = 0
    for p in pkts:  # scapy.PcapReader(PCAP_PATH):
        count += 1
        if count % 1000 == 0:
            print(count)

        key = int(p.time)
        if key not in packets_per_second:
            packets_per_second[key] = 0
            limits_per_second[key] = randrange(limit_start, limit_end)
            # print("Current limit", limit)

        if count > 120000:  # to make sure we only affect attack traffic
            if p.haslayer(scapy.ARP) and p[scapy.Ether].src == "3c:33:00:98:ee:fd":
                # print(packets_per_second[key], limits_per_second[key])
                while packets_per_second[key] > limits_per_second[key]:
                    # print("Over the limit", packets_per_second[key], limit)
                    inc = max(last_key_ok - int(p.time), 0)
                    p.time += inc  # while the number of packet per second is larger than the limit, increment packet time
                    key = int(p.time)
                    if key not in packets_per_second:
                        packets_per_second[key] = 0
                        limits_per_second[key] = randrange(limit_start, limit_end)

                    if packets_per_second[key] > limits_per_second[key]:
                        p.time += 1

        last_key_ok = key
        packets_per_second[key] += 1
        cooked.append(p)

    print("NEW PCAP LEN", len(cooked), count)
    print("WRITING PCAP", limit_start, limit_end)
    wrpcap(f"mirai_tampered_{limit_start}-{limit_end}.pcap", cooked)
    print("DONE")


if __name__ == "__main__":
    tamper(10, 50)
    tamper(30, 70)
    tamper(50, 90)
