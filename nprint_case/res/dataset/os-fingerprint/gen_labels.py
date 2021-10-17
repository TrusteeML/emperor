# Copy and pasted from IDS case
import csv
import pyshark
import nest_asyncio

from os import listdir
from os.path import isfile, join

PCAPS_FOLDER = "pcaps/"
LABELS_FOLDER = "../CIC-IDS-2017/TrafficLabelling/"
LABELS_FILE = "labels.txt"

nest_asyncio.apply()

print("Reading flows from pcaps...")
flows = []  # [("6", "192.168.10.12", "35158", "50.63.243.230", "80", "Friday-WorkingHours", "Friday-WorkingHours.pcap")]
for pcap_file in listdir(PCAPS_FOLDER):
    print(pcap_file)
    if isfile(join(PCAPS_FOLDER, pcap_file)) and not pcap_file.startswith("."):
        print(pcap_file)
        pcap_day_arr = pcap_file.split("-")
        pcap_day_arr.pop()
        pcap_day = "-".join(pcap_day_arr)

        capture = pyshark.FileCapture(join(PCAPS_FOLDER, pcap_file))
        packet = capture[0]

        try:
            protocol = packet.transport_layer
            protocol_number = packet.ip.proto
            src_address = packet.ip.src
            src_port = packet[protocol].srcport
            dst_address = packet.ip.dst
            dst_port = packet[protocol].dstport

            flows.append((protocol_number, src_address, src_port, dst_address, dst_port, pcap_day, pcap_file))
            print(protocol, protocol_number, src_address, src_port, dst_address, dst_port, pcap_day, pcap_file)
        except Exception as e:
            print("ERROR", e)
            pass
        finally:
            capture.close()


print("Looking for flow labels...")
with open(LABELS_FILE, "w") as labels_result:
    labels_writer = csv.writer(labels_result, delimiter=",")
    labels_writer.writerow(["item", "label"])

    for (protocol_number, src_address, src_port, dst_address, dst_port, pcap_day, pcap_file) in flows:
        for labels_file in listdir(LABELS_FOLDER):
            if pcap_day in labels_file:
                with open(join(LABELS_FOLDER, labels_file), "r") as csvfile:
                    label_reader = csv.reader(csvfile, delimiter=",")
                    for row in label_reader:
                        label = row[-1]
                        label_src_address = row[1]
                        label_src_port = row[2]
                        label_dst_address = row[3]
                        label_dst_port = row[4]
                        label_protocol = row[5]

                        if protocol_number == label_protocol and (
                            (
                                src_address == label_src_address
                                and src_port == label_src_port
                                and dst_address == label_dst_address
                                and dst_port == label_dst_port
                            )
                            or (
                                dst_address == label_src_address
                                and dst_port == label_src_port
                                and src_address == label_dst_address
                                and src_port == label_dst_port
                            )
                        ):
                            print([join(PCAPS_FOLDER, pcap_file), label])
                            labels_writer.writerow([join(PCAPS_FOLDER, pcap_file), label])
