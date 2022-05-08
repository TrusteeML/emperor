# Main code

from dtextract.util import persist
from dtextract.data.data import CAT, NUM, ID, CAT_RES
from dtextract.examples.runCompare import runCompare


# dtextract params
CIC_IDS_2017_PATH = "../../../../use_cases/heartbleed_case/res/dataset/CIC-IDS-2017_OverSampled_min.csv.zip"
CIC_IDS_2017_HAS_HEADER = True
CIC_IDS_2017_HEADERS = [
    "Destination Port",
    "Flow Duration",
    "Total Fwd Packets",
    "Total Backward Packets",
    "Total Length of Fwd Packets",
    "Total Length of Bwd Packets",
    "Fwd Packet Length Max",
    "Fwd Packet Length Min",
    "Fwd Packet Length Mean",
    "Fwd Packet Length Std",
    "Bwd Packet Length Max",
    "Bwd Packet Length Min",
    "Bwd Packet Length Mean",
    "Bwd Packet Length Std",
    "Flow Bytes/s",
    "Flow Packets/s",
    "Flow IAT Mean",
    "Flow IAT Std",
    "Flow IAT Max",
    "Flow IAT Min",
    "Fwd IAT Total",
    "Fwd IAT Mean",
    "Fwd IAT Std",
    "Fwd IAT Max",
    "Fwd IAT Min",
    "Bwd IAT Total",
    "Bwd IAT Mean",
    "Bwd IAT Std",
    "Bwd IAT Max",
    "Bwd IAT Min",
    "Fwd PSH Flags",
    "Bwd PSH Flags",
    "Fwd URG Flags",
    "Bwd URG Flags",
    "Fwd Header Length 2",
    "Bwd Header Length",
    "Fwd Packets/s",
    "Bwd Packets/s",
    "Min Packet Length",
    "Max Packet Length",
    "Packet Length Mean",
    "Packet Length Std",
    "Packet Length Variance",
    "FIN Flag Count",
    "SYN Flag Count",
    "RST Flag Count",
    "PSH Flag Count",
    "ACK Flag Count",
    "URG Flag Count",
    "CWE Flag Count",
    "ECE Flag Count",
    "Down/Up Ratio",
    "Average Packet Size",
    "Avg Fwd Segment Size",
    "Avg Bwd Segment Size",
    "Fwd Header Length",
    "Fwd Avg Bytes/Bulk",
    "Fwd Avg Packets/Bulk",
    "Fwd Avg Bulk Rate",
    "Bwd Avg Bytes/Bulk",
    "Bwd Avg Packets/Bulk",
    "Bwd Avg Bulk Rate",
    "Subflow Fwd Packets",
    "Subflow Fwd Bytes",
    "Subflow Bwd Packets",
    "Subflow Bwd Bytes",
    "Init_Win_bytes_forward",
    "Init_Win_bytes_backward",
    "act_data_pkt_fwd",
    "min_seg_size_forward",
    "Active Mean",
    "Active Std",
    "Active Max",
    "Active Min",
    "Idle Mean",
    "Idle Std",
    "Idle Max",
    "Idle Min",
    "Label",
]

CIC_IDS_2017_DATA_TYPES = [NUM for _ in range(30)] + [CAT, ID, CAT, ID, ID] + [NUM for _ in range(43)] + [CAT_RES]
CIC_IDS_2017_IS_CLASSIFY = True
CIC_IDS_2017_N_DATA_MATRIX_COLS = 79

CIC_IDS_2017_OUTPUT = "./output.log"


if __name__ == "__main__":
    runCompare(
        CIC_IDS_2017_PATH,
        CIC_IDS_2017_HAS_HEADER,
        CIC_IDS_2017_DATA_TYPES,
        CIC_IDS_2017_IS_CLASSIFY,
        CIC_IDS_2017_N_DATA_MATRIX_COLS,
        CIC_IDS_2017_OUTPUT,
        headers=CIC_IDS_2017_HEADERS,
    )
