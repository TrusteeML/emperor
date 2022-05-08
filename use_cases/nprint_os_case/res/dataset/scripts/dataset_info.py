import csv

# import time
import pyshark
import traceback

from os import listdir
from os.path import isfile, join


from multiprocessing import Pool

TCP_FLAGS = [
    "flags_ack",
    "flags_cwr",
    "flags_ecn",
    "flags_fin",
    "flags_ns",
    "flags_push",
    "flags_res",
    "flags_reset",
    "flags_syn",
    "flags_urg",
]

TCP_OPTIONS = [
    "window_size",
    "window_size_value",
    "window_scale_factor",
    "option_len",
    "options_mss",
    "options_mss_val",
    "options_nop",
    "options_sack_perm",
    "options_timestamp",
    "options_timestamp_tsecr",
    "options_timestamp_tsval",
    "options_wscale",
    "options_wscale_multiplier",
    "options_wscale_shift",
]

PACKET_HEADERS = ["protocol", "src_ip", "dst_ip", "ttl"] + TCP_FLAGS + TCP_OPTIONS
LABELS_OUTPUT = "../dataset_info.csv"
PCAPS_FOLDER = "../pcaps/"
POOL_SIZE = 8


def process_pcap(pcap_file):
    # start_time = time.time()
    packet_info = []
    if isfile(join(PCAPS_FOLDER, pcap_file)) and ".pcap" in pcap_file:
        # print(pcap_file)
        try:
            capture = pyshark.FileCapture(join(PCAPS_FOLDER, pcap_file))
            packet = capture[0]
            # for packet in capture:
            protocol = packet.transport_layer
            packet_info.append(protocol)
            packet_info.append(packet.ip.src)
            packet_info.append(packet.ip.dst)
            packet_info.append(packet.ip.ttl)

            if protocol == "TCP":
                for flag in TCP_FLAGS:
                    if flag in dir(packet.tcp):
                        packet_info.append(getattr(packet.tcp, flag))
                    else:
                        packet_info.append(-1)

                for option in TCP_OPTIONS:
                    if option in dir(packet.tcp):
                        packet_info.append(getattr(packet.tcp, option))
                    else:
                        packet_info.append(-1)
            else:
                packet_info += [-1] * 24

                # print(packet_info)
                # print("--- %s seconds ---" % (time.time() - start_time))
        except Exception:
            print("ERROR")
            traceback.print_exc()
            # pass
        finally:
            capture.close()

    return packet_info


def read_pcaps():
    print("Reading packets_info from pcaps...")
    eta = len(listdir(PCAPS_FOLDER)) * 0.30
    print("Proceesing {} pcaps (eta: {} minutes)...".format(len(listdir(PCAPS_FOLDER)), eta / 60 / POOL_SIZE))

    packets_info = []
    with Pool(POOL_SIZE) as pool:
        packets_info = pool.map(process_pcap, listdir(PCAPS_FOLDER))

    with open(LABELS_OUTPUT, "w") as labels_output:
        labels_writer = csv.writer(labels_output, delimiter=",")
        labels_writer.writerow(PACKET_HEADERS)
        for row in packets_info:
            labels_writer.writerow(row)


if __name__ == "__main__":
    read_pcaps()
    # plot_ttl()
