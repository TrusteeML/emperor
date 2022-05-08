import numpy as np

from enum import Enum


class FeatureType(Enum):
    """Types of features in training/testing datasets"""

    CATEGORICAL = 0
    NUMERICAL = 1
    IDENTIFIER = 2


def cic_ids_2017_label_converter(label):
    value = -1
    labels = {
        "BENIGN": 0,
        "Bot": 1,
        "DDoS": 2,
        "DoS GoldenEye": 3,
        "DoS Hulk": 4,
        "DoS Slowhttptest": 5,
        "DoS slowloris": 6,
        "FTP-Patator": 7,
        "Heartbleed": 8,
        "Infiltration": 9,
        "PortScan": 10,
        "SSH-Patator": 11,
        "Web Attack Brute Force": 12,
        "Web Attack Sql Injection": 13,
        "Web Attack XSS": 14,
    }

    try:
        value = labels[label.strip()]
    except Exception as err:
        print("Exception", err, label)

    return np.uint8(value)


CIC_IDS_2017_DATASET_META = {
    "name": "cic_ids_2017",
    "has_header": True,
    "fields": [
        ("Destination Port", FeatureType.NUMERICAL, "uint32", False),
        ("Flow Duration", FeatureType.NUMERICAL, "uint32", False),
        ("Total Fwd Packets", FeatureType.NUMERICAL, "uint32", False),
        ("Total Backward Packets", FeatureType.NUMERICAL, "uint32", False),
        ("Total Length of Fwd Packets", FeatureType.NUMERICAL, "uint32", False),
        ("Total Length of Bwd Packets", FeatureType.NUMERICAL, "uint32", False),
        ("Fwd Packet Length Max", FeatureType.NUMERICAL, "uint16", False),
        ("Fwd Packet Length Min", FeatureType.NUMERICAL, "uint16", False),
        ("Fwd Packet Length Mean", FeatureType.NUMERICAL, "float16", False),
        ("Fwd Packet Length Std", FeatureType.NUMERICAL, "float16", False),
        ("Bwd Packet Length Max", FeatureType.NUMERICAL, "uint16", False),
        ("Bwd Packet Length Min", FeatureType.NUMERICAL, "uint16", False),
        ("Bwd Packet Length Mean", FeatureType.NUMERICAL, "float16", False),
        ("Bwd Packet Length Std", FeatureType.NUMERICAL, "float16", False),
        ("Flow Bytes/s", FeatureType.NUMERICAL, "float32", False),
        ("Flow Packets/s", FeatureType.NUMERICAL, "float32", False),
        ("Flow IAT Mean", FeatureType.NUMERICAL, "float32", False),
        ("Flow IAT Std", FeatureType.NUMERICAL, "float32", False),
        ("Flow IAT Max", FeatureType.NUMERICAL, "uint32", False),
        ("Flow IAT Min", FeatureType.NUMERICAL, "uint32", False),
        ("Fwd IAT Total", FeatureType.NUMERICAL, "uint32", False),
        ("Fwd IAT Mean", FeatureType.NUMERICAL, "float32", False),
        ("Fwd IAT Std", FeatureType.NUMERICAL, "float32", False),
        ("Fwd IAT Max", FeatureType.NUMERICAL, "uint32", False),
        ("Fwd IAT Min", FeatureType.NUMERICAL, "uint32", False),
        ("Bwd IAT Total", FeatureType.NUMERICAL, "uint32", False),
        ("Bwd IAT Mean", FeatureType.NUMERICAL, "float32", False),
        ("Bwd IAT Std", FeatureType.NUMERICAL, "float32", False),
        ("Bwd IAT Max", FeatureType.NUMERICAL, "uint32", False),
        ("Bwd IAT Min", FeatureType.NUMERICAL, "uint32", False),
        ("Fwd PSH Flags", FeatureType.CATEGORICAL, "uint8", False),
        ("Bwd PSH Flags", FeatureType.IDENTIFIER, "uint8", False),
        ("Fwd URG Flags", FeatureType.CATEGORICAL, "uint8", False),
        ("Bwd URG Flags", FeatureType.IDENTIFIER, "uint8", False),
        (
            "Fwd Header Length 2",
            FeatureType.IDENTIFIER,
            "uint32",
            False,
        ),  # duplicate column, so ignore it
        ("Bwd Header Length", FeatureType.NUMERICAL, "uint32", False),
        ("Fwd Packets/s", FeatureType.NUMERICAL, "float16", False),
        ("Bwd Packets/s", FeatureType.NUMERICAL, "float16", False),
        ("Min Packet Length", FeatureType.NUMERICAL, "float16", False),
        ("Max Packet Length", FeatureType.NUMERICAL, "float16", False),
        ("Packet Length Mean", FeatureType.NUMERICAL, "float16", False),
        ("Packet Length Std", FeatureType.NUMERICAL, "float16", False),
        ("Packet Length Variance", FeatureType.NUMERICAL, "float32", False),
        ("FIN Flag Count", FeatureType.NUMERICAL, "uint8", False),
        ("SYN Flag Count", FeatureType.NUMERICAL, "uint8", False),
        ("RST Flag Count", FeatureType.NUMERICAL, "uint8", False),
        ("PSH Flag Count", FeatureType.NUMERICAL, "uint8", False),
        ("ACK Flag Count", FeatureType.NUMERICAL, "uint8", False),
        ("URG Flag Count", FeatureType.NUMERICAL, "uint8", False),
        ("CWE Flag Count", FeatureType.NUMERICAL, "uint8", False),
        ("ECE Flag Count", FeatureType.NUMERICAL, "uint8", False),
        ("Down/Up Ratio", FeatureType.NUMERICAL, "float16", False),
        ("Average Packet Size", FeatureType.NUMERICAL, "float16", False),
        ("Avg Fwd Segment Size", FeatureType.NUMERICAL, "float16", False),
        ("Avg Bwd Segment Size", FeatureType.NUMERICAL, "float16", False),
        ("Fwd Header Length", FeatureType.NUMERICAL, "uint32", False),
        ("Fwd Avg Bytes/Bulk", FeatureType.NUMERICAL, "uint8", False),
        ("Fwd Avg Packets/Bulk", FeatureType.NUMERICAL, "uint8", False),
        ("Fwd Avg Bulk Rate", FeatureType.NUMERICAL, "uint8", False),
        ("Bwd Avg Bytes/Bulk", FeatureType.NUMERICAL, "uint8", False),
        ("Bwd Avg Packets/Bulk", FeatureType.NUMERICAL, "uint8", False),
        ("Bwd Avg Bulk Rate", FeatureType.NUMERICAL, "uint8", False),
        ("Subflow Fwd Packets", FeatureType.NUMERICAL, "uint32", False),
        ("Subflow Fwd Bytes", FeatureType.NUMERICAL, "uint32", False),
        ("Subflow Bwd Packets", FeatureType.NUMERICAL, "uint32", False),
        ("Subflow Bwd Bytes", FeatureType.NUMERICAL, "uint32", False),
        ("Init_Win_bytes_forward", FeatureType.NUMERICAL, "uint32", False),
        ("Init_Win_bytes_backward", FeatureType.NUMERICAL, "uint32", False),
        ("act_data_pkt_fwd", FeatureType.NUMERICAL, "uint16", False),
        ("min_seg_size_forward", FeatureType.NUMERICAL, "uint16", False),
        ("Active Mean", FeatureType.NUMERICAL, "float32", False),
        ("Active Std", FeatureType.NUMERICAL, "float32", False),
        ("Active Max", FeatureType.NUMERICAL, "uint32", False),
        ("Active Min", FeatureType.NUMERICAL, "uint32", False),
        ("Idle Mean", FeatureType.NUMERICAL, "float32", False),
        ("Idle Std", FeatureType.NUMERICAL, "float32", False),
        ("Idle Max", FeatureType.NUMERICAL, "uint32", False),
        ("Idle Min", FeatureType.NUMERICAL, "uint32", False),
        ("Label", FeatureType.CATEGORICAL, "uint8", True),
    ],
    "categories": {
        "Fwd PSH Flags": [np.uint8(0), np.uint8(1)],
        # "Bwd PSH Flags": [np.uint8(0)],
        "Fwd URG Flags": [np.uint8(0), np.uint8(1)],
        # "Bwd URG Flags": [np.uint8(0)],
    },
    "classes": [
        "BENIGN",
        "Bot",
        "DDoS",
        "DoS GoldenEye",
        "DoS Hulk",
        "DoS Slowhttptest",
        "DoS slowloris",
        "FTP-Patator",
        "Heartbleed",
        "Infiltration",
        "PortScan",
        "SSH-Patator",
        "Web Attack Brute Force",
        "Web Attack Sql Injection",
        "Web Attack XSS",
    ],
    "converters": {"Label": lambda x: cic_ids_2017_label_converter(x)},
    "type": "classification",
    "url": "https://www.unb.ca/cic/datasets/ids-2017.html",
}
