# Reproducibility of DeepTraffic shortcut learning
import os
import numpy as np
import input_data
import pandas as pd

from sklearn.metrics import classification_report

from dtextract.data.data import NUM, CAT_RES
from dtextract.examples.runCompare import runCompare

from deeptraffic import DeepTraffic

DATA_DIR = "../../../../use_cases/vpn_case/res/dataset/train_test/2class/SessionAllLayers"
MODEL_DIR = os.path.split(DATA_DIR)[1]

CLASS_NUM = 2
dict_2class = {0: "Novpn", 1: "Vpn"}

# dtextract params
VPN_NONVPN_PATH = None
VPN_NONVPN_HAS_HEADER = False
VPN_NONVPN_DATA_TYPES = [NUM for i in range(784)] + [CAT_RES]
VPN_NONVPN_IS_CLASSIFY = True
VPN_NONVPN_N_DATA_MATRIX_COLS = 784
VPN_NONVPN_OUTPUT = "./output.log"


def main():
    dataset = input_data.read_data_sets(DATA_DIR, one_hot=True, num_classes=CLASS_NUM)
    class_names = dict_2class.values()
    print("Initializing DeepTraffic")
    deep_traffic = DeepTraffic()
    deep_traffic.fit(dataset.train, model_dir=MODEL_DIR)
    X_train = dataset.train.images
    y_train = np.array([np.argmax(i) for i in dataset.train.labels])
    X_test = dataset.test.images
    y_test = np.array([np.argmax(i) for i in dataset.test.labels])

    print("Testing DeepTraffic")
    y_pred = deep_traffic.predict(X_test)
    print(classification_report(y_test, y_pred, digits=3, target_names=class_names))

    train_df = pd.DataFrame(X_train)
    train_df["label"] = y_train
    test_df = pd.DataFrame(X_test)
    test_df["label"] = y_test

    runCompare(
        VPN_NONVPN_PATH,
        VPN_NONVPN_HAS_HEADER,
        VPN_NONVPN_DATA_TYPES,
        VPN_NONVPN_IS_CLASSIFY,
        VPN_NONVPN_N_DATA_MATRIX_COLS,
        VPN_NONVPN_OUTPUT,
        model=deep_traffic,
        trainDf=train_df,
        testDf=test_df,
        res="label",
        catFeats=[],
    )


if __name__ == "__main__":
    main()
