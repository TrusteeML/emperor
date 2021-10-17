from os import listdir
from os.path import isfile, join

from pcap_splitter.splitter import PcapSplitter

PCAPS_FOLDER = "../CIC-IDS-2017/pcaps/"
SPLITS_FOLDER = "pcaps/"

for file in listdir(PCAPS_FOLDER):
    if isfile(join(PCAPS_FOLDER, file)):
        print(file)
        ps = PcapSplitter(join(PCAPS_FOLDER, file))
        print(ps.split_by_session(SPLITS_FOLDER))
