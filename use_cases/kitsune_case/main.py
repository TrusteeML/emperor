import os
import time
import zipfile
import pickle
import graphviz
import numpy as np
import pandas as pd

from sklearn import tree

from trustee.utils import log
from trustee.report.trust import TrustReport
from Kitsune import Kitsune

##############################################################################
# Kitsune a lightweight online network intrusion detection system based on an ensemble of autoencoders (kitNET).
# For more information and citation, please see our NDSS'18 paper: Kitsune: An Ensemble of Autoencoders for Online Network Intrusion Detection

# This script demonstrates Kitsune's ability to incrementally learn, and detect anomalies in recorded a pcap of the Mirai Malware.
# The demo involves an m-by-n dataset with n=115 dimensions (features), and m=100,000 observations.
# Each observation is a snapshot of the network's state in terms of incremental damped statistics (see the NDSS paper for more details)

# The runtimes presented in the paper, are based on the C++ implimentation (roughly 100x faster than the python implimentation)
###################  Last Tested with Anaconda 3.6.3   #######################

KITSUNE_PATH = "res/output/kitsune.pkl"
MIRAI_PATH = "res/dataset/mirai.csv"
OUTPUT_PATH = "res/output/"
REPORT_PATH = f"{OUTPUT_PATH}/report/trust_report.obj"

# File location
path = "res/dataset/mirai.pcap"  # the pcap, pcapng, or tsv file to process.
packet_limit = 300000  # np.Inf  # the number of packets to process

# KitNET params:
maxAE = 10  # maximum size for any autoencoder in the ensemble layer
FMgrace = 5000  # the number of instances taken to learn the feature mapping (the ensemble's architecture)
ADgrace = 50000  # the number of instances used to train the anomaly detector (ensemble itself)


def main():
    """Main body of code"""
    logger = log.Logger(f"{OUTPUT_PATH}/output.log")

    if not os.path.exists(path):
        # Load Mirai pcap (a recording of the Mirai botnet malware being activated)
        # The first 70,000 observations are clean...
        logger.log("Unzipping Sample Capture...")

        with zipfile.ZipFile("res/dataset/mirai.pcap.zip", "r") as zip_ref:
            zip_ref.extractall(path="res/dataset/")

    # Build Kitsune
    if os.path.exists(MIRAI_PATH):
        kitsune = None
        with open(KITSUNE_PATH, "rb") as file:
            kitsune = pickle.load(file)
    else:
        kitsune = Kitsune(path, packet_limit, maxAE, FMgrace, ADgrace)

    feature_names = kitsune.FE.nstat.getNetStatHeaders()
    logger.log("Feature names", feature_names)

    if not os.path.exists(MIRAI_PATH):
        # if the dataset hasn't been extracted yet, run Kitsune on mirai.pcap
        logger.log("Running Kitsune:")
        X, y = [], []
        i = 0
        start = time.time()
        # Here we process (train/execute) each individual packet.
        while True:
            i += 1
            if i % 1000 == 0:
                logger.log(i)

            x = kitsune.get_next_vector()
            if len(x) == 0:  # if pcap is over
                break

            rmse = kitsune.predict(x)

            X.append(x)
            y.append(rmse)
        stop = time.time()
        logger.log("Complete. Time elapsed: " + str(stop - start))

        df = pd.DataFrame(X, columns=feature_names)
        df["rmse"] = y
        df.to_csv(MIRAI_PATH, index=False)

        # save trained Kitsune
        with open(KITSUNE_PATH, "wb") as file:
            pickle.dump(kitsune, file)
    else:
        df = pd.read_csv(MIRAI_PATH, header=0)
        y = df["rmse"]
        X = df.drop(labels=["rmse"], axis=1)

    if os.path.exists(REPORT_PATH):
        logger.log("Loading trust report from {}...".format(REPORT_PATH))
        trust_report = TrustReport.load(REPORT_PATH)
        logger.log("Done!")
    else:
        trust_report = TrustReport(
            kitsune,
            X=X,
            y=y,
            top_k=10,
            max_iter=50,
            trustee_num_iter=10,
            num_pruning_iter=0,
            skip_retrain=True,
            analyze_stability=True,
            trustee_sample_size=0.3,
            feature_names=feature_names,
            verbose=True,
            is_classify=False,
        )

    logger.log(trust_report)
    trust_report.save(OUTPUT_PATH)


if __name__ == "__main__":
    main()
