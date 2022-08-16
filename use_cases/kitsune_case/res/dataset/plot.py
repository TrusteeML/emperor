import dpkt
import collections

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

from matplotlib import rcParams


FT_NAME = "Roboto"
FT_WEIGHT = "light"

rcParams["font.family"] = "serif"
rcParams["font.serif"] = [FT_NAME]
rcParams["font.weight"] = FT_WEIGHT

PCAP_PATH = "mirai.pcap"
PCAP_PATH_50_90 = "mirai_tampered_50-90.pcap"
PCAP_PATH_30_70 = "mirai_tampered_30-70.pcap"
PCAP_PATH_10_50 = "mirai_tampered_10-50.pcap"
# PCAP_PATH = "mirai_tampered_no_arp.pcap"


def parse_pkts_per_second(filename):
    """Parses pcap file, counting packets per second"""

    packets_per_second = {}
    attack_start_sec = 0
    counter, start, end = 0, 0, 0
    with open(filename, "rb") as pcap_file:
        for ts, pkt in dpkt.pcap.Reader(pcap_file):
            if counter == 0:
                start = int(ts)
            end = int(ts)
            counter += 1
            if counter == 121621:
                attack_start_sec = int(ts)

            # timestamp = dt.utcfromtimestamp(ts)
            # key = '{}{}{}'.format(timestamp.hour, timestamp.minute, timestamp.second)
            key = int(ts)
            if key not in packets_per_second:
                packets_per_second[key] = 0
            packets_per_second[key] += 1

    # print('start, end, diff, counter', start, end, end - start, counter, len(packets_per_second.items()))
    # cover seconds with no packets (if any)
    count = 0
    for sec in range(start, end + 1):
        if sec not in packets_per_second:
            count += 1
            packets_per_second[sec] = 0

    # print('count', count, len(packets_per_second.items()))
    ordered = collections.OrderedDict(sorted(packets_per_second.items()))
    time_series = list(ordered.values())
    attack_idx = list(sorted(packets_per_second.keys())).index(attack_start_sec)
    # print(time_series[:attack_start_sec], time_series[attack_start_sec:])
    return (
        np.array(time_series[:attack_idx]),
        np.array(time_series[attack_idx:]),
        attack_idx,
    )


def plot_time_series(time_series, filename=None):
    """
    Plots time series
    """
    colors = [
        "#a7c3cd",
        "#d75d5b",
        "#8a4444",
        "#c8c5c3",
        "#524a47",
        "#f5f0ed",
        "#edeef0",
    ]
    labels = [
        "Original",
        "Tampered 50-90",
        "Tampered 30-70",
        "Tampered 10-50",
    ]
    cmap = ListedColormap(["#a7c3cd", "#d75d5b"])

    plt.figure(figsize=(4, 2.1))
    fig, axs = plt.subplots(
        2,
        2,
    )

    attack_start = time_series[0][2]
    total_length = len(time_series[0][0]) + len(time_series[0][1])
    axs[0, 0].plot(range(0, attack_start), time_series[0][0], color=colors[0])
    axs[0, 0].plot(
        range(attack_start, total_length), time_series[0][1], color=colors[1]
    )
    axs[0, 0].set_title(labels[0], fontsize=12, fontname=FT_NAME, fontweight=FT_WEIGHT)
    axs[0, 0].set_ylim(0, 320)

    attack_start = time_series[2][2]
    total_length = len(time_series[1][0]) + len(time_series[1][1])
    axs[0, 1].plot(range(0, attack_start), time_series[1][0], color=colors[0])
    axs[0, 1].plot(
        range(attack_start, total_length), time_series[1][1], color=colors[1]
    )
    axs[0, 1].set_title(labels[1], fontsize=12, fontname=FT_NAME, fontweight=FT_WEIGHT)
    axs[0, 1].set_ylim(0, 320)

    attack_start = time_series[2][2]
    total_length = len(time_series[2][0]) + len(time_series[2][1])
    axs[1, 0].plot(range(0, attack_start), time_series[2][0], color=colors[0])
    axs[1, 0].plot(
        range(attack_start, total_length), time_series[2][1], color=colors[1]
    )
    axs[1, 0].set_title(labels[2], fontsize=12, fontname=FT_NAME, fontweight=FT_WEIGHT)
    axs[1, 0].set_ylim(0, 320)

    attack_start = time_series[3][2]
    total_length = len(time_series[3][0]) + len(time_series[3][1])
    axs[1, 1].plot(range(0, attack_start), time_series[3][0], color=colors[0])
    axs[1, 1].plot(
        range(attack_start, total_length), time_series[3][1], color=colors[1]
    )
    axs[1, 1].set_title(labels[3], fontsize=12, fontname=FT_NAME, fontweight=FT_WEIGHT)
    axs[1, 1].set_ylim(0, 320)

    # for idx, series in enumerate(time_series):
    # plt.plot(series, color=colors[idx], label=labels[idx])

    fig.supylabel("# of Packets", fontsize=12, fontname=FT_NAME, fontweight=FT_WEIGHT)
    fig.supxlabel(
        "Seconds elapsed", fontsize=12, fontname=FT_NAME, fontweight=FT_WEIGHT
    )

    # fig.legend(ncol=4)
    plt.tight_layout()

    if filename:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()


def plot_pcap(paths):
    """Analyses periodicity in signal broke down by packet per second"""
    time_series = []
    for path in paths:
        time_series.append(parse_pkts_per_second(path))

    plot_time_series(time_series, filename="./mirai_traces_pps.pdf")


if __name__ == "__main__":
    plot_pcap(
        [
            PCAP_PATH,
            PCAP_PATH_50_90,
            PCAP_PATH_30_70,
            PCAP_PATH_10_50,
        ]
    )
