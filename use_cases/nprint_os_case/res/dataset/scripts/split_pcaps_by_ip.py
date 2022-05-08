from os import listdir
from os.path import isfile, join

from pcap_splitter.splitter import PcapSplitter

PCAPS_FOLDER = None  # "../../CIC-IDS-2017/pcaps/"
PCAP_FILE = '../os_100_packet_hard.pcap'
SPLITS_FOLDER = "../pcaps-ip/"

# PCAPS_FOLDER = "pcaps/"
# SPLITS_FOLDER = "pcaps-100k/"

if PCAPS_FOLDER:
    for file in listdir(PCAPS_FOLDER):
        if ".pcap" in file and isfile(join(PCAPS_FOLDER, file)):
            print(file)
            ps = PcapSplitter(join(PCAPS_FOLDER, file))
            print(ps.split_by_client_ip(SPLITS_FOLDER))
            # print(ps.split_by_count(100000, SPLITS_FOLDER))
elif PCAP_FILE:
    ps = PcapSplitter(PCAP_FILE)
    print(ps.split_by_client_ip(SPLITS_FOLDER))