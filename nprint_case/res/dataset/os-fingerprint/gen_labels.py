# Copy and pasted from IDS case
import csv

# import time
import pyshark

# import nest_asyncio

from os import listdir
from os.path import isfile, join

from multiprocessing import Pool


PCAPS_FOLDER = "pcaps/"
LABELS_INPUT = "labels-os.txt"
LABELS_OUTPUT = "labels.txt"

POOL_SIZE = 8

# nest_asyncio.apply()


def process_pcap(pcap_file):
    # start_time = time.time()
    ip_addresses = (None, None, None)
    if isfile(join(PCAPS_FOLDER, pcap_file)) and ".pcap" in pcap_file:
        capture = pyshark.FileCapture(join(PCAPS_FOLDER, pcap_file))
        packet = capture[0]

        try:
            src_address = packet.ip.src
            dst_address = packet.ip.dst

            ip_addresses = (src_address, dst_address, pcap_file)
            # print("--- %s seconds ---" % (time.time() - start_time))
            # print(src_address, dst_address, pcap_file)
        except Exception as e:
            print("ERROR", e)
            pass
        finally:
            capture.close()

    return ip_addresses


if __name__ == "__main__":
    print("Reading ip_addresses from pcaps...")
    eta = len(listdir(PCAPS_FOLDER)) * 0.30
    print("Proceesing {} pcaps (eta: {} minutes)...".format(len(listdir(PCAPS_FOLDER)), eta / 60 / POOL_SIZE))

    ip_addresses = []
    with Pool(POOL_SIZE) as pool:
        ip_addresses = pool.map(process_pcap, listdir(PCAPS_FOLDER))

    print("Looking for flow labels...")
    with open(LABELS_OUTPUT, "w") as labels_output:
        labels_writer = csv.writer(labels_output, delimiter=",")
        labels_writer.writerow(["item", "label"])

        for (src_address, dst_address, pcap_file) in ip_addresses:
            with open(LABELS_INPUT, "r") as csvfile:
                label_reader = csv.reader(csvfile, delimiter=",")
                for row in label_reader:
                    label_src_address = row[0]
                    label = row[1]

                    if src_address == label_src_address or dst_address == label_src_address:
                        # print([pcap_file, label])
                        labels_writer.writerow([pcap_file, label])
