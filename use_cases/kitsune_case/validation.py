import os
import time
import pickle
import zipfile
import numpy as np
import pandas as pd

from matplotlib import pyplot as plt
from scipy.stats import norm


from Kitsune import Kitsune

##############################################################################
# Kitsune a lightweight online network intrusion detection system based on an ensemble of autoencoders (kitNET).
# For more information and citation, please see our NDSS'18 paper: Kitsune: An Ensemble of Autoencoders for Online Network Intrusion Detection

# This script demonstrates Kitsune's ability to incrementally learn, and detect anomalies in recorded a pcap of the Mirai Malware.
# The demo involves an m-by-n dataset with n=115 dimensions (features), and m=100,000 observations.
# Each observation is a snapshot of the network's state in terms of incremental damped statistics (see the NDSS paper for more details)

# The runtimes presented in the paper, are based on the C++ implimentation (roughly 100x faster than the python implimentation)
###################  Last Tested with Anaconda 3.6.3   #######################

# KITSUNE_PATH = "res/output/kitsune.paaath.pkl"
OUTPUT_PATH = "res/output"

# File location
ORIGINAL_PCAP = "res/dataset/mirai.pcap"  # the pcap, pcapng, or tsv file to process.
VALIDATION_PCAP_10_50 = "res/dataset/mirai_tampered_10-50.pcap"
VALIDATION_PCAP_30_70 = "res/dataset/mirai_tampered_30-70.pcap"
VALIDATION_PCAP_50_90 = "res/dataset/mirai_tampered_50-90.pcap"

packet_limit = 300000  # the number of packets to process

# KitNET params:
maxAE = 10  # maximum size for any autoencoder in the ensemble layer
FMgrace = 5000  # the number of instances taken to learn the feature mapping (the ensemble's architecture)
ADgrace = 100000  # the number of instances used to train the anomaly detector (ensemble itself)

TRAINING_SAMPLES = FMgrace + ADgrace + 1


def run(pcap):
    """Main body of code"""
    ###############################################################
    ######################## ORIGINAL PCAP ########################
    ###############################################################
    kitsune = Kitsune(pcap, packet_limit, maxAE, FMgrace, ADgrace)

    # if the dataset hasn't been extracted yet, run Kitsune on mirai.pcap
    feature_names = kitsune.FE.nstat.getNetStatHeaders()
    print("Feature names", feature_names)

    print("Running Kitsune with original PCAP:")
    X, y = [], []
    i = 0
    start = time.time()
    # Here we process (train/execute) each individual packet.
    while True:
        i += 1
        if i % 1000 == 0:
            print(i)

        x = kitsune.get_next_vector()
        if len(x) == 0:  # if pcap is over
            break

        rmse = kitsune.predict(x)

        X.append(x)
        y.append(rmse)

    df = pd.DataFrame(X, columns=feature_names)
    df["rmse"] = y
    df.to_csv(
        f"{OUTPUT_PATH}/{pcap.rsplit('/', maxsplit=1)[-1].replace('.pcap', '')}.csv",
        index=False,
    )
    stop = time.time()
    print("Complete. Time elapsed: " + str(stop - start))

    benign_sample = np.log(y[TRAINING_SAMPLES:100000])
    log_probs = norm.logsf(np.log(y), np.mean(benign_sample), np.std(benign_sample))

    # plot the RMSE anomaly scores
    print("Plotting results")
    plt.figure(figsize=(10, 5))
    plt.scatter(
        range(TRAINING_SAMPLES, len(y)),
        y[TRAINING_SAMPLES:],
        s=0.1,
        c=log_probs[TRAINING_SAMPLES:],
        cmap="RdYlGn",
    )
    plt.yscale("log")
    plt.title("Anomaly Scores from Kitsune's Execution Phase")
    plt.ylabel("RMSE (log scaled)")
    plt.xlabel("Time elapsed [min]")
    figbar = plt.colorbar()
    figbar.ax.set_ylabel("Log Probability\n ", rotation=270)
    plt.savefig(
        f"{OUTPUT_PATH}/{pcap.rsplit('/', maxsplit=1)[-1].replace('.pcap', '')}_plot_kitsune.png"
    )
    plt.close()


if __name__ == "__main__":
    if not os.path.exists(ORIGINAL_PCAP):
        with zipfile.ZipFile(f"{ORIGINAL_PCAP}.zip", "r") as zip_ref:
            zip_ref.extractall(path="res/dataset/")

    if not os.path.exists(VALIDATION_PCAP_10_50):
        with zipfile.ZipFile(f"{VALIDATION_PCAP_10_50}.zip", "r") as zip_ref:
            zip_ref.extractall(path="res/dataset/")

    if not os.path.exists(VALIDATION_PCAP_30_70):
        with zipfile.ZipFile(f"{VALIDATION_PCAP_30_70}.zip", "r") as zip_ref:
            zip_ref.extractall(path="res/dataset/")

    if not os.path.exists(VALIDATION_PCAP_50_90):
        with zipfile.ZipFile(f"{VALIDATION_PCAP_50_90}.zip", "r") as zip_ref:
            zip_ref.extractall(path="res/dataset/")

    run(ORIGINAL_PCAP)
    run(VALIDATION_PCAP_10_50)
    run(VALIDATION_PCAP_30_70)
    run(VALIDATION_PCAP_50_90)
