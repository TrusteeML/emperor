# Copy and pasted from IDS case
import csv
import pyshark
import nest_asyncio

from os import listdir
from os.path import isfile, join

PCAPS_FOLDER = "pcaps/"
LABELS_INPUT = "labels-os.txt"
LABELS_OUTPUT = "labels.txt"

nest_asyncio.apply()

print("Reading ip_addresses from pcaps...")
ip_addresses = []
for pcap_file in listdir(PCAPS_FOLDER):
    print(pcap_file)
    if isfile(join(PCAPS_FOLDER, pcap_file)) and not pcap_file.startswith("."):
        print(pcap_file)
        capture = pyshark.FileCapture(join(PCAPS_FOLDER, pcap_file))
        packet = capture[0]

        try:
            src_address = packet.ip.src
            dst_address = packet.ip.dst

            ip_addresses.append((src_address, dst_address, pcap_file))
            print(src_address, dst_address, pcap_file)
        except Exception as e:
            print("ERROR", e)
            pass
        finally:
            capture.close()


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
                    print([pcap_file, label])
                    labels_writer.writerow([PCAPS_FOLDER, label])
